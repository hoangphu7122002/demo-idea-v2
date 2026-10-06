from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.posts import service
from app.posts.schemas import PostOut, PostSummary

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("")
async def list_posts(session: SessionDep) -> list[PostSummary]:
    return await service.list_posts(session)


@router.get("/{slug}", responses={404: {"description": "Post not found"}})
async def get_post(slug: str, session: SessionDep) -> PostOut:
    post = await service.get_post(session, slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
