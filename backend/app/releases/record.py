"""Record a live check into the cache: `python -m app.releases.record --slug S --url U`."""

import argparse
import asyncio

from sqlalchemy import select

from app.ai.release_check import check
from app.core.db import SyncSessionLocal
from app.core.settings import get_settings
from app.models import Post
from app.models.post import paragraph_ref
from app.releases import resolve


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--url")
    ap.add_argument("--text")
    args = ap.parse_args()
    model = get_settings().llm_model
    if model == "test":
        raise SystemExit("Set LLM_MODEL (e.g. anthropic:claude-sonnet-5-5) and the API key first")
    release = resolve(args.url, args.text)
    with SyncSessionLocal() as session:
        post = session.scalars(select(Post).where(Post.slug == args.slug)).one_or_none()
        if post is None:
            raise SystemExit(f"Unknown post slug: {args.slug}")
        paragraphs = [(paragraph_ref(p.id), p.md) for p in post.paragraphs]
    result = asyncio.run(check(paragraphs, release, timeout=120))
    if result.source != "live":
        raise SystemExit("Live run failed; cache not updated")
    print(f"recorded {len(result.flags)} flags:", ", ".join(f.paragraph_id for f in result.flags))


if __name__ == "__main__":
    main()
