from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

from token_utils import count_tokens
from token_utils import MAX_TOKENS

load_dotenv()

history={}

with open("bot/prompt/system_prompt_v1.3.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

client = AsyncOpenAI(
#   base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('CHATGPT_TOKEN'),
)

async def ai_generate(text: str, user_id: int):
    
    if user_id not in history:
        history[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    history[user_id].append({"role": "user", "content": text})
    
    
    """Подсчет токенов"""
    while count_tokens(history[user_id]) > MAX_TOKENS:
        if len(history[user_id]) <= 2:  
            break
        history[user_id].pop(1)  


    
    response = await client.chat.completions.create(
        model=os.getenv('AI_MODEL'),
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
    
    """Подсчет токенов"""
    while count_tokens(history[user_id]) > MAX_TOKENS:
        if len(history[user_id]) <= 2:  
            break
        history[user_id].pop(1)   



    response = await client.chat.completions.create(
        model=os.getenv('AI_MODEL'),
        messages=history[user_id],
    )
    
    answer = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": answer})
    return answer