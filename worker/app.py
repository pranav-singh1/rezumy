import os
from celery import Celery

celery = Celery(
    "rezumy",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

@celery.task
def scrape_and_store_jobs(query: str, location: str | None = None):
    return {"ok": True, "query": query, "location": location}

@celery.task
def rank_and_queue_applications(user_id: str, resume_id: str):
    return {"queued_for": user_id, "resume": resume_id}

if __name__ == "__main__":
    # Run a worker if executed directly
    celery.worker_main(argv=["worker", "-l", "INFO"])
