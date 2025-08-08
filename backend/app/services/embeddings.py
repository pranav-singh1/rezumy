import os
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def embed_text(text: str) -> list[float]:
    # Truncate to a reasonable size to avoid token limits
    resp = await client.embeddings.create(model="text-embedding-3-small", input=text[:8000])
    return resp.data[0].embedding
