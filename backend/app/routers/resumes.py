from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import tempfile, os
import docx2txt
import PyPDF2
from app.services import nlp, embeddings, storage

router = APIRouter()

class ParsedResume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    skills: list[str] = []

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    if file.content_type == "application/pdf":
        text = ""
        with open(tmp_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    else:
        text = docx2txt.process(tmp_path)

    os.unlink(tmp_path)

    parsed = nlp.parse_resume_text(text)
    emb = await embeddings.embed_text(text)
    storage_path = await storage.save_original(file)

    return {"parsed": parsed, "embedding_dim": len(emb), "storage_path": storage_path}
