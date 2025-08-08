import os
from celery import Celery
import httpx

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

@celery.task(name="rezumy.apply_to_job")
def apply_to_job(apply_url: str, payload: dict, actually_submit: bool = False):
    bot_url = os.getenv("BOT_URL", "http://playwright-bot:4000")
    try:
        with httpx.Client(timeout=120) as client:
            r = client.post(f"{bot_url}/apply", json={
                "applyUrl": apply_url,
                "payload": payload,
                "actuallySubmit": bool(actually_submit),
            })
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Run a worker if executed directly
    celery.worker_main(argv=["worker", "-l", "INFO"])
