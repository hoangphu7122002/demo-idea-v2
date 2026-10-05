"""Write the FastAPI OpenAPI schema to backend/openapi.json (input for openapi-typescript)."""

import json
from pathlib import Path

from app.api.main import app

OUT = Path(__file__).resolve().parent.parent / "openapi.json"


def main() -> None:
    OUT.write_text(json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
