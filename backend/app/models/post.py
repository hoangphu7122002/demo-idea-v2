from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.job import _now


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    title: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )
    paragraphs: Mapped[list["PostParagraph"]] = relationship(
        back_populates="post",
        order_by="PostParagraph.position",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class PostParagraph(Base):
    __tablename__ = "post_paragraphs"
    __table_args__ = (UniqueConstraint("post_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    position: Mapped[int]
    md: Mapped[str] = mapped_column(Text)
    post: Mapped[Post] = relationship(back_populates="paragraphs")

    @property
    def ref(self) -> str:
        """Stable API id, derived from the DB id (never from content)."""
        return paragraph_ref(self.id)


def paragraph_ref(paragraph_id: int) -> str:
    return f"p-{paragraph_id}"
