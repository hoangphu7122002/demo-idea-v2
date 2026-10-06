from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import SessionDep
from app.models import Post
from app.models.post import paragraph_ref

router = APIRouter(prefix="/api/posts", tags=["posts"])


class PostSummary(BaseModel):
    slug: str
    title: str


class ParagraphOut(BaseModel):
    id: str  # stable "p-<db id>"
    md: str


class PostOut(BaseModel):
    slug: str
    title: str
    paragraphs: list[ParagraphOut]


@router.get("")
async def list_posts(session: SessionDep) -> list[PostSummary]:
    rows = await session.scalars(select(Post).order_by(Post.id))
    return [PostSummary(slug=p.slug, title=p.title) for p in rows]


@router.get("/{slug}", responses={404: {"description": "Post not found"}})
async def get_post(slug: str, session: SessionDep) -> PostOut:
    post = await session.scalar(
        select(Post).where(Post.slug == slug).options(selectinload(Post.paragraphs))
    )
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostOut(
        slug=post.slug,
        title=post.title,
        paragraphs=[ParagraphOut(id=paragraph_ref(p.id), md=p.md) for p in post.paragraphs],
    )
