from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.core.db import SyncSessionLocal
from app.models import ParagraphFlag, Post, PostParagraph, ResourceCheck
from app.seed import reseed


def _count(s: Session, model: type) -> int:
    return s.scalar(select(func.count()).select_from(model)) or 0


def _make_check(s: Session) -> tuple[Post, ResourceCheck]:
    post = Post(
        slug="p",
        title="P",
        paragraphs=[PostParagraph(position=0, md="a"), PostParagraph(position=1, md="b")],
    )
    s.add(post)
    s.flush()
    check = ResourceCheck(
        post_id=post.id,
        source_url=None,
        resource_hash="0" * 64,
        model="test",
        flags=[
            ParagraphFlag(paragraph_id=p.id, reason="r", source_quote="q", proposed_fix="f")
            for p in post.paragraphs
        ],
    )
    s.add(check)
    s.commit()
    return post, check


def test_flags_roundtrip_ordered() -> None:
    with SyncSessionLocal() as s:
        _, check = _make_check(s)
        got = s.get(ResourceCheck, check.id)
        assert got is not None
        assert [f.reason for f in got.flags] == ["r", "r"]


def test_delete_check_cascades_flags() -> None:
    with SyncSessionLocal() as s:
        _, check = _make_check(s)
        s.delete(check)
        s.commit()
        assert _count(s, ParagraphFlag) == 0
        assert _count(s, PostParagraph) == 2


def test_delete_post_cascades_checks_and_flags() -> None:
    with SyncSessionLocal() as s:
        post, _ = _make_check(s)
        s.execute(delete(Post).where(Post.id == post.id))  # DB-level cascade
        s.commit()
        assert _count(s, ResourceCheck) == 0
        assert _count(s, ParagraphFlag) == 0


def test_delete_paragraph_cascades_its_flags() -> None:
    with SyncSessionLocal() as s:
        post, _ = _make_check(s)
        s.execute(delete(PostParagraph).where(PostParagraph.id == post.paragraphs[0].id))
        s.commit()
        assert _count(s, ParagraphFlag) == 1
        assert _count(s, ResourceCheck) == 1


def test_reseed_clears_checks_and_flags() -> None:
    with SyncSessionLocal() as s:
        reseed(s)
        post = s.scalars(select(Post)).one()
        para = post.paragraphs[0]
        s.add(
            ResourceCheck(
                post_id=post.id,
                resource_hash="1" * 64,
                model="test",
                flags=[
                    ParagraphFlag(
                        paragraph_id=para.id, reason="r", source_quote="q", proposed_fix="f"
                    )
                ],
            )
        )
        s.commit()
        assert _count(s, ParagraphFlag) == 1
        reseed(s)
        assert _count(s, ResourceCheck) == 0
        assert _count(s, ParagraphFlag) == 0
