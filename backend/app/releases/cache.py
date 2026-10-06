"""JSON cache of check results, keyed by the exact inputs (paragraphs + release text)."""

import hashlib
import json
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "fixtures" / "cache"


def cache_key(paragraphs: list[tuple[str, str]], release_text: str) -> str:
    """sha256 over the paragraphs ([id, md] pairs, in order) and the release text."""
    payload = json.dumps(
        {"paragraphs": [[pid, md] for pid, md in paragraphs], "release": release_text},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def load(key: str) -> list[dict[str, str]] | None:
    path = CACHE_DIR / f"{key}.json"
    if not path.is_file():
        return None
    data: dict[str, list[dict[str, str]]] = json.loads(path.read_text(encoding="utf-8"))
    return data["flags"]


def save(key: str, flags: list[dict[str, str]]) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{key}.json"
    path.write_text(
        json.dumps({"flags": flags}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path
