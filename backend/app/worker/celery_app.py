from celery import Celery

from app.core.settings import get_settings

_s = get_settings()

celery_app = Celery("app", broker=_s.redis_url, backend=_s.redis_url, include=["app.worker.tasks"])
celery_app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_queue="default",
    task_routes={"app.worker.tasks.llm_*": {"queue": "llm"}},
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
)
