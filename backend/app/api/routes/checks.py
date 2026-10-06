from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.checks import service
from app.checks.errors import CheckError
from app.checks.schemas import CheckIn, CheckOut

router = APIRouter(prefix="/api/posts", tags=["checks"])


@router.post(
    "/{slug}/check",
    responses={
        404: {"description": "Post not found"},
        422: {"description": "Unknown release URL, or neither URL nor text given"},
        503: {"description": "Live check failed and no cached result exists"},
    },
)
async def check_post(slug: str, body: CheckIn, session: SessionDep) -> CheckOut:
    """Check a post against a release note (URL from the offline index, or pasted text)."""
    try:
        return await service.run_check(session, slug, body.release_url, body.release_text)
    except CheckError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.get("/{slug}/flags", responses={404: {"description": "Post not found"}})
async def latest_flags(slug: str, session: SessionDep) -> CheckOut | None:
    """Flags of the latest check, or null if the post was never checked."""
    try:
        return await service.latest_check(session, slug)
    except CheckError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
