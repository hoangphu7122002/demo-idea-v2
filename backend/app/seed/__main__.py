from app.core.db import SyncSessionLocal
from app.seed import reseed


def main() -> None:
    with SyncSessionLocal() as session:
        counts = reseed(session)
    print("seeded:", ", ".join(f"{t}={n}" for t, n in counts.items()))


main()
