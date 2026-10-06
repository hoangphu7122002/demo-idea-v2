from typing import Literal

from pydantic import BaseModel


class CheckIn(BaseModel):
    """Body of a check request: a resource URL from the offline index, or pasted text.

    Pasted text wins over the URL; the URL is then kept as the source link. Unknown fields
    (e.g. the removed `release_url` / `release_text`) are ignored.
    """

    resource_url: str | None = None
    resource_text: str | None = None


class FlagOut(BaseModel):
    paragraph_id: str  # "p-<db id>"
    reason: str
    source_quote: str
    proposed_fix: str


class CheckOut(BaseModel):
    check_id: int
    source: Literal["live", "cache"] | None = None  # null when read back via GET
    resource_url: str | None
    flags: list[FlagOut]
