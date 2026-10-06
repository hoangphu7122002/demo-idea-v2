from typing import Literal

from pydantic import BaseModel, Field


class CheckIn(BaseModel):
    """Body of a check request: a resource URL from the offline index, or pasted text.

    `release_url` / `release_text` are the deprecated names of `resource_url` / `resource_text`.
    They are still accepted; the `resource_*` field wins when both are sent.
    """

    resource_url: str | None = None
    resource_text: str | None = None
    release_url: str | None = Field(
        default=None, deprecated=True, description="Deprecated: use `resource_url`."
    )
    release_text: str | None = Field(
        default=None, deprecated=True, description="Deprecated: use `resource_text`."
    )

    @property
    def url(self) -> str | None:
        """The resource URL, preferring the new field over the deprecated one."""
        return self.resource_url or self.__dict__["release_url"]  # no DeprecationWarning

    @property
    def text(self) -> str | None:
        """The pasted resource text, preferring the new field over the deprecated one."""
        return self.resource_text or self.__dict__["release_text"]  # no DeprecationWarning


class FlagOut(BaseModel):
    paragraph_id: str  # "p-<db id>"
    reason: str
    source_quote: str
    proposed_fix: str


class CheckOut(BaseModel):
    check_id: int
    source: Literal["live", "cache"] | None = None  # null when read back via GET
    resource_url: str | None
    release_url: str | None = Field(
        default=None, deprecated=True, description="Deprecated: same value as `resource_url`."
    )
    flags: list[FlagOut]
