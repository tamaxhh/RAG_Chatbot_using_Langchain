from langchain_openai import OpenAI
from backend.config import settings

llm = OpenAI(openai_api_key=settings.openai_api_key)

def summarize(text: str) -> str:
    return llm("Summarize this: " + text)[:200]  # Truncate for example