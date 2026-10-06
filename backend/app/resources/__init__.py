"""Offline resource resolver. URLs are looked up in a local index; never fetched."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

FIXTURES = Path(__file__).parent / "fixtures"


@dataclass(frozen=True)
class ResourceSource:
    url: str | None
    text: str
    hash: str


def _normalize(url: str) -> str:
    parts = urlsplit(url.strip())
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}{parts.path.rstrip('/')}"


def _index() -> dict[str, str]:
    raw: dict[str, str] = json.loads((FIXTURES / "index.json").read_text(encoding="utf-8"))
    return {_normalize(u): f for u, f in raw.items()}


def resolve(url: str | None, text: str | None) -> ResourceSource:
    """Pasted text wins (url is kept as the source link); else the url must be in the index."""
    url = (url or "").strip() or None
    text = (text or "").strip() or None
    if text is None:
        if url is None:
            raise ValueError("Provide a resource URL or paste the resource text")
        name = _index().get(_normalize(url))
        if name is None:
            raise ValueError(f"Unknown resource URL (not in offline index): {url}")
        text = (FIXTURES / name).read_text(encoding="utf-8").strip()
    return ResourceSource(url=url, text=text, hash=hashlib.sha256(text.encode()).hexdigest())
