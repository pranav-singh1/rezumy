import re
from typing import Dict, Any

EMAIL_RE = re.compile(r"[\w\.\-]+@[\w\-]+\.[\w\-\.]+")
PHONE_RE = re.compile(r"(\+?\d[\d\s\-\(\)]{7,}\d)")

TECH_SKILLS = [
    "python","java","javascript","typescript","react","node","sql","pandas","numpy",
    "machine learning","deep learning","tensorflow","pytorch","aws","gcp","docker","kubernetes",
]

def parse_resume_text(text: str) -> Dict[str, Any]:
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name = lines[0] if lines else None
    skills_found = []
    lower = text.lower()
    for s in TECH_SKILLS:
        if s in lower:
            skills_found.append(s)
    return {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": sorted(set(skills_found)),
    }
