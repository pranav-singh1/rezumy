import os, uuid, shutil
from fastapi import UploadFile

STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage"))
os.makedirs(STORAGE_DIR, exist_ok=True)

async def save_original(file: UploadFile) -> str:
    ext = ".pdf" if file.filename.lower().endswith(".pdf") else ".docx"
    name = f"{uuid.uuid4()}{ext}"
    dest = os.path.join(STORAGE_DIR, name)
    with open(dest, "wb") as out:
        content = await file.read()
        out.write(content)
    return dest
