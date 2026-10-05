import os
from collections.abc import Iterator

import pytest

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    f"postgresql+psycopg://app:app@127.0.0.1:{os.environ.get('DB_PORT', '5432')}/app_test",
)
os.environ["DB_NULL_POOL"] = "1"

from fastapi.testclient import TestClient  # noqa: E402

from app.api.main import app  # noqa: E402
from app.core.db import sync_engine  # noqa: E402
from app.models import Base  # noqa: E402


@pytest.fixture(autouse=True)
def _clean_db() -> Iterator[None]:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
