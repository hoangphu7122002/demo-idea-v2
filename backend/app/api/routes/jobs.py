import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import SessionDep
from app.models import Job
from app.worker.tasks import word_stats

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


class JobOut(BaseModel):
    id: uuid.UUID
    kind: str
    status: str
    result: dict[str, Any] | None
    error: str | None
    created_at: datetime
    updated_at: datetime


@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: uuid.UUID, session: SessionDep) -> Job:
    job = await session.get(Job, job_id)
    if job is None:
        raise HTTPException(404, "job not found")
    return job


class WordStatsIn(BaseModel):
    text: str = Field(min_length=1)


class JobAccepted(BaseModel):
    job_id: uuid.UUID
    status: str


@router.post("/word-stats", response_model=JobAccepted, status_code=202)
async def start_word_stats(data: WordStatsIn, session: SessionDep) -> JobAccepted:
    job = Job(kind="word_stats")
    session.add(job)
    await session.commit()
    word_stats.apply_async(args=[str(job.id), data.text], task_id=str(job.id))
    return JobAccepted(job_id=job.id, status=job.status)
