from sqlalchemy import select

from app.core.db import SyncSessionLocal
from app.models import Note, Post, PostParagraph
from app.seed import reseed


def _snapshot() -> tuple[str, str, list[tuple[int, int, str]]]:
    with SyncSessionLocal() as s:
        post = s.scalars(select(Post)).one()
        paras = s.scalars(
            select(PostParagraph)
            .where(PostParagraph.post_id == post.id)
            .order_by(PostParagraph.position)
        ).all()
        return post.slug, post.title, [(p.id, p.position, p.md) for p in paras]


def test_reseed_creates_post_with_rich_blocks() -> None:
    with SyncSessionLocal() as s:
        reseed(s)
    slug, title, paras = _snapshot()
    mds = [md for _, _, md in paras]
    assert slug == "llm-api-post"
    assert title == "Calling the Claude API from Python"
    assert len(paras) >= 8
    assert not any(md.startswith("# ") for md in mds)  # H1 is the title only
    assert any(md.startswith("```python") for md in mds)
    assert any(md.startswith("$$\n") and md.endswith("\n$$") for md in mds)
    assert any("$p_{in}$" in md for md in mds)  # inline math


def test_ids_identical_across_reseeds_and_notes_unaffected() -> None:
    with SyncSessionLocal() as s:
        reseed(s)
    first = _snapshot()
    with SyncSessionLocal() as s:
        reseed(s)
        assert len(s.scalars(select(Note)).all()) == 2
    assert _snapshot() == first
    assert [i for i, _, _ in first[2]] == list(range(1, len(first[2]) + 1))
