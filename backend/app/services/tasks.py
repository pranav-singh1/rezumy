import os
from celery import Celery

_celery = Celery(
    "rezumy-backend",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)


def enqueue_apply(apply_url: str, payload: dict, actually_submit: bool) -> str:
    result = _celery.send_task(
        "rezumy.apply_to_job",
        args=[apply_url, payload, actually_submit],
    )
    return result.id 