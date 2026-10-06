from sqlalchemy import select

from app.core.db import SyncSessionLocal
from app.models import Note
from app.seed import reseed


def _notes() -> list[tuple[int, str, str]]:
    with SyncSessionLocal() as s:
        return [(n.id, n.title, n.body) for n in s.scalars(select(Note).order_by(Note.id))]


def test_reseed_is_idempotent() -> None:
    with SyncSessionLocal() as s:
        reseed(s)
    first = _notes()
    with SyncSessionLocal() as s:
        reseed(s)
    assert first and _notes() == first


def test_reseed_restores_after_mutation() -> None:
    with SyncSessionLocal() as s:
        reseed(s)
    expected = _notes()
    with SyncSessionLocal() as s:
        s.add(Note(title="extra", body="x"))
        s.query(Note).filter(Note.id == 1).update({"title": "changed"})
        s.commit()
    assert _notes() != expected
    with SyncSessionLocal() as s:
        reseed(s)
    assert _notes() == expected
