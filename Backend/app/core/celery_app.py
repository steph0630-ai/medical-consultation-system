from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.schedule.jobs.payment_callback"],
)

celery_app.conf.update(
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=3,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
