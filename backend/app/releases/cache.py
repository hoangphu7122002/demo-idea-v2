"""JSON cache of check results, keyed by the exact inputs (paragraphs + release text)."""

import hashlib
import json
import os
import tempfile
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "fixtures" / "cache"
_FIELDS = ("paragraph_id", "reason", "source_quote", "proposed_fix")


def cache_key(paragraphs: list[tuple[str, str]], release_text: str) -> str:
    """sha256 over the paragraphs ([id, md] pairs, in order) and the release text."""
    payload = json.dumps(
        {"paragraphs": [[pid, md] for pid, md in paragraphs], "release": release_text},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def load(key: str) -> list[dict[str, str]] | None:
    """Cached flags, or None on a miss. A corrupt or malformed file counts as a miss."""
    path = CACHE_DIR / f"{key}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        flags = data["flags"]
        if not isinstance(flags, list) or not all(
            isinstance(f, dict) and all(isinstance(f.get(k), str) for k in _FIELDS) for f in flags
        ):
            return None
        return [{k: f[k] for k in _FIELDS} for f in flags]
    except (OSError, ValueError, KeyError, TypeError):
        return None


def save(key: str, flags: list[dict[str, str]]) -> Path:
    """Atomic write: temp file in the same dir + os.replace, so readers never see a partial file."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{key}.json"
    text = json.dumps({"flags": flags}, ensure_ascii=False, indent=2) + "\n"
    tmp = tempfile.NamedTemporaryFile(  # noqa: SIM115 - closed explicitly, replaced below
        "w", encoding="utf-8", dir=CACHE_DIR, suffix=".tmp", delete=False
    )
    try:
        with tmp:
            tmp.write(text)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp.name, path)
    except BaseException:
        Path(tmp.name).unlink(missing_ok=True)
        raise
    return path
