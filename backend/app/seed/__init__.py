"""Seeder registry. Add a module under app/seed/ that calls `register(...)`; it is auto-loaded."""

import importlib
import pkgutil
from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy import Integer, delete, func, inspect, select
from sqlalchemy.orm import DeclarativeBase, Session


@dataclass(frozen=True)
class Seeder:
    name: str
    models: tuple[type[DeclarativeBase], ...]  # tables this seeder owns (cleared on reseed)
    load: Callable[[Session], None]


_REGISTRY: list[Seeder] = []


def register(
    name: str, models: tuple[type[DeclarativeBase], ...]
) -> Callable[[Callable[[Session], None]], Callable[[Session], None]]:
    def deco(fn: Callable[[Session], None]) -> Callable[[Session], None]:
        if any(s.name == name for s in _REGISTRY):
            return fn
        _REGISTRY.append(Seeder(name, models, fn))
        return fn

    return deco


def load_all() -> list[Seeder]:
    """Import every submodule so it registers itself; order = module name."""
    for mod in sorted(m.name for m in pkgutil.iter_modules(__path__) if m.name != "__main__"):
        importlib.import_module(f"{__name__}.{mod}")
    return list(_REGISTRY)


def reseed(session: Session) -> dict[str, int]:
    """Clear seeded tables (reverse order), then load in order. Idempotent."""
    seeders = load_all()
    for s in reversed(seeders):
        for model in reversed(s.models):
            session.execute(delete(model))
    for s in seeders:
        s.load(session)
    session.flush()
    counts: dict[str, int] = {}
    for s in seeders:
        for model in s.models:
            counts[model.__tablename__] = _count_and_sync_sequence(session, model)
    session.commit()
    return counts


def _count_and_sync_sequence(session: Session, model: type[DeclarativeBase]) -> int:
    """Count rows; move an integer-pk sequence past seeded fixed ids so inserts don't collide."""
    mapper = inspect(model)
    table = mapper.local_table
    count = session.scalar(select(func.count()).select_from(model)) or 0
    pk = list(mapper.primary_key)
    if len(pk) == 1 and isinstance(pk[0].type, Integer):
        col = pk[0]
        max_id = session.scalar(select(func.max(col)))
        if max_id is not None:
            seq = func.pg_get_serial_sequence(table.description, col.name)
            session.execute(select(func.setval(seq, max_id)))
    return count
