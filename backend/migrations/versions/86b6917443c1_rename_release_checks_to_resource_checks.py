"""rename release_checks to resource_checks

Revision ID: 86b6917443c1
Revises: 7862eab74dc3
Create Date: 2026-10-06 11:57:09.976678

Pure renames: rows are kept. The primary-key constraint, id sequence and post_id index are
renamed too so the names match what the models generate (`alembic check` stays clean).
paragraph_flags.check_id keeps pointing at the table: Postgres tracks foreign keys by OID.
"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "86b6917443c1"
down_revision: str | Sequence[str] | None = "7862eab74dc3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _rename(old: str, new: str, old_hash: str, new_hash: str) -> None:
    """Rename table `old` to `new` and its hash column `old_hash` to `new_hash`.

    Also renames the primary key, the id sequence and the post_id index to follow the table.
    """
    op.rename_table(old, new)
    op.alter_column(new, old_hash, new_column_name=new_hash)
    op.execute(f"ALTER TABLE {new} RENAME CONSTRAINT {old}_pkey TO {new}_pkey")
    op.execute(f"ALTER SEQUENCE {old}_id_seq RENAME TO {new}_id_seq")
    op.execute(f"ALTER INDEX ix_{old}_post_id RENAME TO ix_{new}_post_id")


def upgrade() -> None:
    """Rename release_checks → resource_checks and release_hash → resource_hash."""
    _rename("release_checks", "resource_checks", "release_hash", "resource_hash")


def downgrade() -> None:
    """Reverse the rename."""
    _rename("resource_checks", "release_checks", "resource_hash", "release_hash")
