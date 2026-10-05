import time
import uuid
from collections import Counter

from app.ai.summary import summarise
from app.core.db import SyncSessionLocal
from app.models import Job, Note
from app.worker.celery_app import celery_app


@celery_app.task(name="app.worker.tasks.ping")
def ping() -> str:
    return "pong"


@celery_app.task(name="app.worker.tasks.word_stats", bind=True)
def word_stats(self: object, job_id: str, text: str) -> None:
    """Demo job: count words. Idempotent: a finished job is never recomputed."""
    with SyncSessionLocal() as s:
        job = s.get(Job, uuid.UUID(job_id))
        if job is None or job.status == "done":
            return
        job.status = "running"
        s.commit()
        time.sleep(1)  # pretend this is slow
        words = text.lower().split()
        job.result = {
            "words": len(words),
            "top": Counter(words).most_common(3),
            "worker": celery_app.current_worker_task.request.hostname
            if celery_app.current_worker_task
            else None,
        }
        job.status = "done"
        s.commit()


@celery_app.task(name="app.worker.tasks.llm_summarize_note")
def llm_summarize_note(job_id: str, note_id: int) -> None:
    """Runs on the `llm` queue. Idempotent: a finished job is skipped; re-runs overwrite."""
    with SyncSessionLocal() as s:
        job = s.get(Job, uuid.UUID(job_id))
        if job is None or job.status == "done":
            return
        note = s.get(Note, note_id)
        if note is None:
            job.status, job.error = "failed", "note not found"
            s.commit()
            return
        job.status = "running"
        s.commit()
        try:
            out = summarise(note.body)
        except Exception as exc:  # noqa: BLE001
            job.status, job.error = "failed", f"{type(exc).__name__}: {exc}"
            s.commit()
            return
        note.summary, note.tags, note.sentiment = out.summary, out.tags, out.sentiment
        job.result = {"note_id": note_id, **out.model_dump()}
        job.status = "done"
        s.commit()
