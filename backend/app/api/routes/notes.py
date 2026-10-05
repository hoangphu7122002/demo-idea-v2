from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select

from app.api.deps import SessionDep
from app.api.routes.jobs import JobAccepted
from app.models import Job, Note
from app.worker.tasks import llm_summarize_note

router = APIRouter(prefix="/api/notes", tags=["notes"])


class NoteIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    created_at: datetime
    summary: str | None = None
    tags: list[str] | None = None
    sentiment: Literal["positive", "neutral", "negative"] | None = None


@router.get("", response_model=list[NoteOut])
async def list_notes(session: SessionDep) -> list[Note]:
    return list((await session.scalars(select(Note).order_by(Note.id))).all())


@router.post("", response_model=NoteOut, status_code=201)
async def create_note(data: NoteIn, session: SessionDep) -> Note:
    note = Note(title=data.title, body=data.body)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


@router.post("/{note_id}/summary", response_model=JobAccepted, status_code=202)
async def summarise_note(note_id: int, session: SessionDep) -> JobAccepted:
    """Queue an AI summary of the note; poll GET /api/jobs/{job_id} for the result."""
    if await session.get(Note, note_id) is None:
        raise HTTPException(404, "note not found")
    job = Job(kind="note_summary")
    session.add(job)
    await session.commit()
    llm_summarize_note.apply_async(args=[str(job.id), note_id], task_id=str(job.id))
    return JobAccepted(job_id=job.id, status=job.status)
