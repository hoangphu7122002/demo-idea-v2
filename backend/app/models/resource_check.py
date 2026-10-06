from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.job import _now


class ResourceCheck(Base):
    __tablename__ = "resource_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    source_url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    resource_hash: Mapped[str] = mapped_column(String(64))
    model: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    flags: Mapped[list["ParagraphFlag"]] = relationship(
        back_populates="check",
        order_by="ParagraphFlag.id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ParagraphFlag(Base):
    __tablename__ = "paragraph_flags"

    id: Mapped[int] = mapped_column(primary_key=True)
    check_id: Mapped[int] = mapped_column(
        ForeignKey("resource_checks.id", ondelete="CASCADE"), index=True
    )
    paragraph_id: Mapped[int] = mapped_column(
        ForeignKey("post_paragraphs.id", ondelete="CASCADE"), index=True
    )
    reason: Mapped[str] = mapped_column(Text)
    source_quote: Mapped[str] = mapped_column(Text)
    proposed_fix: Mapped[str] = mapped_column(Text)
    check: Mapped[ResourceCheck] = relationship(back_populates="flags")
