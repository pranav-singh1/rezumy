from fastapi import APIRouter
from pydantic import BaseModel
from app.services import ranker, letters
from app.services.tasks import enqueue_apply

router = APIRouter()

class MatchRequest(BaseModel):
    resume_text: str
    jobs: list[dict]

@router.post("/match")
async def match_jobs(payload: MatchRequest):
    ranked = await ranker.rank(payload.resume_text, payload.jobs)
    return {"ranked": ranked}

class CoverLetterRequest(BaseModel):
    resume_json: dict
    job: dict

@router.post("/cover-letter")
async def cover_letter(req: CoverLetterRequest):
    text = await letters.generate(req.resume_json, req.job)
    return {"cover_letter": text}

class ApplyRequest(BaseModel):
    apply_url: str
    resume_json: dict
    storage_path: str
    job: dict
    actually_submit: bool = False
    cover_letter: str | None = None

@router.post("/apply")
async def apply(req: ApplyRequest):
    cover_letter_text = req.cover_letter
    if not cover_letter_text:
        cover_letter_text = await letters.generate(req.resume_json, req.job)

    payload = {
        "fullName": req.resume_json.get("name"),
        "email": req.resume_json.get("email"),
        "phone": req.resume_json.get("phone"),
        "resumePath": req.storage_path,
        "coverLetter": cover_letter_text,
    }
    task_id = enqueue_apply(req.apply_url, payload, req.actually_submit)
    return {"enqueued": True, "task_id": task_id}
