from fastapi import APIRouter, Query, HTTPException
import httpx, os

router = APIRouter()

@router.get("/search")
async def search_jobs(q: str, location: str | None = None, remote: bool | None = None, num: int = 20):
    serp_key = os.getenv("SERPAPI_KEY")
    if not serp_key:
        raise HTTPException(status_code=500, detail="SERPAPI_KEY not configured")
    params = {
        "engine": "google_jobs",
        "q": q,
        "hl": "en",
        "api_key": serp_key,
        "num": num,
    }
    if location:
        params["location"] = location
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get("https://serpapi.com/search", params=params)
        r.raise_for_status()
        data = r.json()
    jobs = []
    for j in data.get("jobs_results", []):
        jobs.append({
            "title": j.get("title"),
            "company": j.get("company_name"),
            "location": j.get("location"),
            "via": j.get("via"),
            "desc": j.get("description"),
            "link": j.get("apply_link") or j.get("job_id")
        })
    return {"results": jobs}
