from .embeddings import embed_text
from typing import List, Dict
import numpy as np

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))

async def rank(resume_text: str, jobs: List[Dict]):
    resume_vec = await embed_text(resume_text)
    ranked = []
    for j in jobs:
        desc = j.get("desc") or j.get("title", "")
        j_vec = await embed_text(desc[:2000])
        score = cosine(resume_vec, j_vec)
        ranked.append({**j, "score": score})
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
