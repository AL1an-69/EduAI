from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

history={}

with open("bot/prompt/system_prompt_v1.3.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('DEEPSEEK_TOKEN'),
)

async def ai_generate(text: str, user_id: int):
    if user_id not in history:
        history[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    history[user_id].append({"role": "user", "content": text})
    
    response = await client.chat.completions.create(
        model="deepseek/deepseek-v3.2",
        messages=history[user_id],
    )
    
    answer = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": answer})
    
    return answer



async def ai_generate_image(image_url: str, user_id: int, caption: str = "Объясни задачу на фото"):
    if user_id not in history:
        history[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    history[user_id].append({
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": caption + "\n\nВАЖНО: используй Unicode символы — x², sin²x, √D, π. Никаких ^ и *."}
        ]
    })
    
    response = await client.chat.completions.create(
        model="anthropic/claude-3-haiku",
        messages=history[user_id],
    )
    
    answer = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": answer})
    return answer