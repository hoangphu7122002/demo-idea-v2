from typing import Literal

from pydantic import BaseModel


class CheckIn(BaseModel):
    release_url: str | None = None
    release_text: str | None = None


class FlagOut(BaseModel):
    paragraph_id: str  # "p-<db id>"
    reason: str
    source_quote: str
    proposed_fix: str


class CheckOut(BaseModel):
    check_id: int
    source: Literal["live", "cache"] | None = None  # null when read back via GET
    release_url: str | None
    flags: list[FlagOut]
