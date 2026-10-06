from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.release_check import check
from app.checks.schemas import CheckOut, FlagOut
from app.core.settings import get_settings
from app.models import ParagraphFlag, Post, ReleaseCheck
from app.models.post import paragraph_ref
from app.releases import resolve


def _to_out(rc: ReleaseCheck, source: str | None = None) -> CheckOut:
    return CheckOut.model_validate(
        {
            "check_id": rc.id,
            "source": source,
            "release_url": rc.source_url,
            "flags": [
                FlagOut(
                    paragraph_id=paragraph_ref(f.paragraph_id),
                    reason=f.reason,
                    source_quote=f.source_quote,
                    proposed_fix=f.proposed_fix,
                )
                for f in rc.flags
            ],
        }
    )


async def _post_with_paragraphs(session: AsyncSession, slug: str) -> Post | None:
    return await session.scalar(
        select(Post).where(Post.slug == slug).options(selectinload(Post.paragraphs))
    )


async def run_check(
    session: AsyncSession, slug: str, release_url: str | None, release_text: str | None
) -> CheckOut | None:
    """None if the post is unknown. Raises ValueError (bad release input) or CheckUnavailable."""
    post = await _post_with_paragraphs(session, slug)
    if post is None:
        return None
    release = resolve(release_url, release_text)
    paragraphs = [(paragraph_ref(p.id), p.md) for p in post.paragraphs]
    result = await check(paragraphs, release)
    rc = ReleaseCheck(
        post_id=post.id,
        source_url=release.url,
        release_hash=release.hash,
        model=get_settings().llm_model,
        flags=[
            ParagraphFlag(
                paragraph_id=int(f.paragraph_id.removeprefix("p-")),
                reason=f.reason,
                source_quote=f.source_quote,
                proposed_fix=f.proposed_fix,
            )
            for f in result.flags
        ],
    )
    session.add(rc)
    await session.commit()
    await session.refresh(rc, attribute_names=["flags"])
    return _to_out(rc, result.source)


async def latest_check(session: AsyncSession, slug: str) -> tuple[bool, CheckOut | None]:
    """(post exists, latest check or None)."""
    post = await session.scalar(select(Post).where(Post.slug == slug))
    if post is None:
        return False, None
    rc = await session.scalar(
        select(ReleaseCheck)
        .where(ReleaseCheck.post_id == post.id)
        .order_by(ReleaseCheck.id.desc())
        .limit(1)
        .options(selectinload(ReleaseCheck.flags))
    )
    return True, (_to_out(rc) if rc else None)
