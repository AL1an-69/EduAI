import os
from dotenv import load_dotenv
from client.core import client
from client.core import SYSTEM_PROMPT

from client.token_utils import count_tokens
from client.token_utils import MAX_TOKENS

load_dotenv()


history={}

"""Созадние небольшого саммари для длинных диалогов, чтобы не терять контекст, но при этом не превышать лимит токенов"""
async def make_summary(messages: list) -> str:
    try:
        response = await client.chat.completions.create(
            model=os.getenv('AI_MODEL'),
            temperature=0.2,  # почти без креатива
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Сожми диалог в 1-2 коротких предложения. "
                        "Сохрани только ключевой смысл: тему задачи, прогресс ученика и ошибки. "
                        "Без лишних слов."
                    )
                },
                {
                    "role": "user",
                    "content": str(messages)
                }
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Ошибка summary: {e}")
        return "Контекст предыдущего диалога был сокращён."



"""Нарезка истории(чтоб не привышать лимитй токенов)"""
async def trim_history(user_id: int):
    while count_tokens(history[user_id]) > MAX_TOKENS:
        if len(history[user_id]) <= 4:
            break

        # берём старые сообщения
        old_messages = history[user_id][1:6]

        # делаем summary через LLM
        summary = await make_summary(old_messages)

        # собираем новую историю
        history[user_id] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Контекст диалога: {summary}"},
        ] + history[user_id][6:]




