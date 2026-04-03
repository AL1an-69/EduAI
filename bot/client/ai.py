import asyncio

import os
from dotenv import load_dotenv

from client.core import client
from client.core import SYSTEM_PROMPT

from client.history import trim_history
from client.history import history 

from RAG.Methods.retriever import get_relevant_method

load_dotenv()


async def detect_topic(image_url: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": "Определи тему этой математической задачи одним предложением"}
                ]
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[detect_topic] ошибка: {e}")
        return ""


"""Безопасный запрос к API"""
async def safe_request(func):
    for _ in range(3):
        try:
            return await func()
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(1)
    raise Exception("Ошибка подключения к API")




async def ai_generate(text: str, user_id: int):
    
    method = await asyncio.to_thread(get_relevant_method, text)
    PROMPT = SYSTEM_PROMPT + "\n\n" + method if method else SYSTEM_PROMPT

    if user_id not in history:
        history[user_id] = [{"role": "system", "content": PROMPT}]
    else:
        history[user_id][0] = {"role": "system", "content": PROMPT}
    
    history[user_id].append({"role": "user", "content": text})
    
    try:
        await trim_history(user_id)
    except Exception as e:
        print(f"Ошибка при обрезке истории: {e}")

    
    response = await safe_request(lambda: client.chat.completions.create(
        model=os.getenv('AI_MODEL'),
        # temperature=0.4,
        messages=history[user_id],
    ))
    
    answer = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": answer})
    
    return answer




async def ai_generate_image(image_url: str, user_id: int, caption: str = "Объясни задачу на фото"):
    
    topic = await detect_topic(image_url)
    method = await asyncio.to_thread(get_relevant_method, topic)
    PROMPT = SYSTEM_PROMPT + "\n\n" + method if method else SYSTEM_PROMPT
    
    if user_id not in history:
        history[user_id] = [{"role": "system", "content": PROMPT}]
    else:
        history[user_id][0] = {"role": "system", "content": PROMPT}
   
    message_content = {
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": caption + "\n\nВАЖНО: используй Unicode символы — x², sin²x, √D, π. Никаких ^ и *."}
        ]
    }
    
    history[user_id].append(message_content)
    


    try:
        await trim_history(user_id) 

        response = await safe_request(lambda: client.chat.completions.create(
            model=os.getenv('AI_MODEL'),
            # temperature=0.4,
            messages=history[user_id],
        ))  
        
        answer = response.choices[0].message.content
        
        history[user_id].append({"role": "assistant", "content": answer})
        return answer



    except Exception as e:
        if history[user_id] and history[user_id][-1] == message_content: 
            history[user_id].pop()
        print("изображение не обработалось, удаляю из истории")
        return "Не удалось обработать изображение. Попробуйте отправить его еще раз или опишите задачу текстом."


    
