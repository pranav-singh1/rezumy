from fastapi import APIRouter
from pydantic import BaseModel
from app.services import ranker, letters

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
