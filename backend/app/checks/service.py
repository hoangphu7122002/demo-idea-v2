from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.resource_check import CheckUnavailable, check
from app.checks.errors import CheckServiceUnavailable, InvalidResource, PostNotFound
from app.checks.schemas import CheckOut, FlagOut
from app.core.settings import get_settings
from app.models import ParagraphFlag, Post, ResourceCheck
from app.models.post import paragraph_ref
from app.resources import resolve


def _to_out(rc: ResourceCheck, source: str | None = None) -> CheckOut:
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
            "resource_url": rc.source_url,
            "release_url": rc.source_url,  # deprecated alias, removed in the cleanup PR
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
    session: AsyncSession, slug: str, resource_url: str | None, resource_text: str | None
) -> CheckOut:
    """Check a post against a resource and persist the result.

    Resolves the resource offline (pasted text wins; a URL must be in the local index), runs
    the resource-check agent (live, or the cache as fallback) over the post's paragraphs, then
    stores one `ResourceCheck` with one `ParagraphFlag` per flag.

    Args:
        session: the request's async DB session; committed on success.
        slug: slug of the post to check.
        resource_url: resource URL, looked up in the offline index; kept as the source link.
        resource_text: pasted resource text; takes precedence over the URL.

    Returns:
        The stored check, with `source` set to "live" or "cache".

    Raises:
        PostNotFound: no post has this slug.
        InvalidResource: unknown resource URL, or neither URL nor text was given.
        CheckServiceUnavailable: the live check failed and no cached result exists.
    """
    post = await _post_with_paragraphs(session, slug)
    if post is None:
        raise PostNotFound
    try:
        resource = resolve(resource_url, resource_text)
    except ValueError as exc:
        raise InvalidResource(str(exc)) from exc
    paragraphs = [(paragraph_ref(p.id), p.md) for p in post.paragraphs]
    try:
        result = await check(paragraphs, resource)
    except CheckUnavailable as exc:
        raise CheckServiceUnavailable(str(exc)) from exc
    rc = ResourceCheck(
        post_id=post.id,
        source_url=resource.url,
        resource_hash=resource.hash,
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
        select(ResourceCheck)
        .where(ResourceCheck.post_id == post.id)
        .order_by(ResourceCheck.id.desc())
        .limit(1)
        .options(selectinload(ResourceCheck.flags))
    )
    return _to_out(rc) if rc else None
