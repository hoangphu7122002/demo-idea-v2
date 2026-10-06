from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import text

from app.core.db import sync_engine
from app.models import Base

OLD_HEAD = "7862eab74dc3"
ALEMBIC_INI = Path(__file__).parent.parent / "alembic.ini"


def _reset() -> None:
    """Leave the test DB empty (also if a failed run left the old table name behind)."""
    with sync_engine.begin() as c:
        c.execute(text("DROP TABLE IF EXISTS release_checks, alembic_version CASCADE"))
    Base.metadata.drop_all(sync_engine)


def test_rename_keeps_rows_and_downgrade_restores() -> None:
    cfg = Config(str(ALEMBIC_INI))
    _reset()
    try:
        command.upgrade(cfg, OLD_HEAD)
        with sync_engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO posts (id, slug, title, created_at, updated_at)"
                    " VALUES (1, 's', 'T', now(), now())"
                )
            )
            c.execute(
                text(
                    "INSERT INTO post_paragraphs (id, post_id, position, md) VALUES (1, 1, 0, 'a')"
                )
            )
            c.execute(
                text(
                    "INSERT INTO release_checks"
                    " (id, post_id, source_url, release_hash, model, created_at)"
                    " VALUES (1, 1, 'u', 'abc', 'm', now())"
                )
            )
            c.execute(
                text(
                    "INSERT INTO paragraph_flags"
                    " (id, check_id, paragraph_id, reason, source_quote, proposed_fix)"
                    " VALUES (1, 1, 1, 'r', 'q', 'f')"
                )
            )

        command.upgrade(cfg, "head")
        with sync_engine.connect() as c:
            row = c.execute(text("SELECT id, resource_hash, source_url FROM resource_checks")).one()
            assert tuple(row) == (1, "abc", "u")
            joined = c.execute(
                text(
                    "SELECT count(*) FROM paragraph_flags f"
                    " JOIN resource_checks r ON r.id = f.check_id"
                )
            ).scalar()
            assert joined == 1
            assert c.execute(text("SELECT to_regclass('release_checks')")).scalar() is None

        command.downgrade(cfg, OLD_HEAD)
        with sync_engine.connect() as c:
            row = c.execute(text("SELECT id, release_hash FROM release_checks")).one()
            assert tuple(row) == (1, "abc")
            assert c.execute(text("SELECT to_regclass('resource_checks')")).scalar() is None
    finally:
        _reset()
