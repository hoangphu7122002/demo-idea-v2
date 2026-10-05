import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.db import SyncSessionLocal
from app.models import Job
from app.worker.tasks import word_stats


def test_word_stats_enqueues_and_task_is_idempotent(client: TestClient) -> None:
    with patch.object(word_stats, "apply_async") as enqueue:
        r = client.post("/api/jobs/word-stats", json={"text": "a b a"})
    assert r.status_code == 202
    job_id = r.json()["job_id"]
    enqueue.assert_called_once()

    word_stats.run(job_id, "a b a")  # run the task body inline (no broker)
    word_stats.run(job_id, "ignored")  # second delivery is a no-op
    with SyncSessionLocal() as s:
        job = s.get(Job, uuid.UUID(job_id))
        assert job is not None and job.status == "done"
        assert job.result is not None and job.result["words"] == 3

    body = client.get(f"/api/jobs/{job_id}").json()
    assert body["status"] == "done"
