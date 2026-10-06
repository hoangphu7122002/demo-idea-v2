from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Post
from app.models.post import paragraph_ref
from app.posts.schemas import ParagraphOut, PostOut, PostSummary


async def list_posts(session: AsyncSession) -> list[PostSummary]:
    rows = await session.scalars(select(Post).order_by(Post.id))
    return [PostSummary(slug=p.slug, title=p.title) for p in rows]


async def get_post(session: AsyncSession, slug: str) -> PostOut | None:
    post = await session.scalar(
        select(Post).where(Post.slug == slug).options(selectinload(Post.paragraphs))
    )
    if post is None:
        return None
    return PostOut(
        slug=post.slug,
        title=post.title,
        paragraphs=[ParagraphOut(id=paragraph_ref(p.id), md=p.md) for p in post.paragraphs],
    )
