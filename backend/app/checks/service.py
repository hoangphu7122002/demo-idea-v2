from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.release_check import CheckUnavailable, check
from app.checks.errors import CheckServiceUnavailable, InvalidRelease, PostNotFound
from app.checks.schemas import CheckOut, FlagOut
from app.core.settings import get_settings
from app.models import ParagraphFlag, Post, ReleaseCheck
from app.models.post import paragraph_ref
from app.releases import resolve


def _to_out(rc: ReleaseCheck, source: str | None = None) -> CheckOut:
    """Convert a persisted check into its API shape.

    Args:
        rc: the check, with its `flags` relationship already loaded.
        source: "live" or "cache" when the check was just run; None when read back later,
            because the origin of a stored check is not persisted.

    Returns:
        The check with flags in insertion order and paragraph ids as "p-<db id>".
    """
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
    """Load a post and its paragraphs in one round trip.

    Args:
        session: the request's async DB session.
        slug: the post slug.

    Returns:
        The post with `paragraphs` loaded, or None if no post has that slug.
    """
    return await session.scalar(
        select(Post).where(Post.slug == slug).options(selectinload(Post.paragraphs))
    )


async def run_check(
    session: AsyncSession, slug: str, release_url: str | None, release_text: str | None
) -> CheckOut:
    """Check a post against a release note and persist the result.

    Resolves the release offline (pasted text wins; a URL must be in the local index), runs
    the release-check agent (live, or the cache as fallback) over the post's paragraphs, then
    stores one `ReleaseCheck` with one `ParagraphFlag` per flag.

    Args:
        session: the request's async DB session; committed on success.
        slug: slug of the post to check.
        release_url: release note URL, looked up in the offline index; kept as the source link.
        release_text: pasted release note text; takes precedence over the URL.

    Returns:
        The stored check, with `source` set to "live" or "cache".

    Raises:
        PostNotFound: no post has this slug.
        InvalidRelease: unknown release URL, or neither URL nor text was given.
        CheckServiceUnavailable: the live check failed and no cached result exists.
    """
    post = await _post_with_paragraphs(session, slug)
    if post is None:
        raise PostNotFound
    try:
        release = resolve(release_url, release_text)
    except ValueError as exc:
        raise InvalidRelease(str(exc)) from exc
    paragraphs = [(paragraph_ref(p.id), p.md) for p in post.paragraphs]
    try:
        result = await check(paragraphs, release)
    except CheckUnavailable as exc:
        raise CheckServiceUnavailable(str(exc)) from exc
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


async def latest_check(session: AsyncSession, slug: str) -> CheckOut | None:
    """Read back the most recent check of a post.

    Args:
        session: the request's async DB session.
        slug: slug of the post.

    Returns:
        The latest check (with `source` None), or None if the post was never checked.

    Raises:
        PostNotFound: no post has this slug.
    """
    post = await session.scalar(select(Post).where(Post.slug == slug))
    if post is None:
        raise PostNotFound
    rc = await session.scalar(
        select(ReleaseCheck)
        .where(ReleaseCheck.post_id == post.id)
        .order_by(ReleaseCheck.id.desc())
        .limit(1)
        .options(selectinload(ReleaseCheck.flags))
    )
    return _to_out(rc) if rc else None
