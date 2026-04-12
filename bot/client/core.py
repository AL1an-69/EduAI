import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

from pathlib import Path

with open(Path("bot/prompt/system_prompt_v2.txt"), "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

client = AsyncOpenAI(
    api_key=os.getenv("CHATGPT_TOKEN"),
)

ai_model = 'gpt-5.4-mini'
temp = 0.2