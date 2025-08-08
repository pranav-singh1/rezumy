import os
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

template = (
    "You are an expert career writer. Using the JSON resume and the job JSON, "
    "write a concise, tailored cover letter under 220 words. Keep it specific, professional, and human. "
    "Avoid repeating the resume."
)

async def generate(resume_json: dict, job: dict) -> str:
    content = {"resume": resume_json, "job": job}
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": str(content)},
        ],
        temperature=0.6,
    )
    return resp.choices[0].message.content.strip()
