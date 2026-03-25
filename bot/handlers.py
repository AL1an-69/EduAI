from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv
import os

from client.ai import ai_generate,ai_generate_image

load_dotenv()


router = Router()


class Gen(StatesGroup):
    wait = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, я бот который помогает в подготовке к Егэ по математике!')

@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('Подождите, я еще не ответил на предыдущий вопрос')

@router.message(F.photo)
async def get_photo(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    await message.answer('Генерирую ответ...')
    
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_TOKEN')}/{file.file_path}"
    
    caption = message.caption or "Объясни задачу на фото"

    
    response = await ai_generate_image(file_url, message.from_user.id)
    try:
        await message.answer(response, parse_mode='Markdown')
    except Exception as e:
        await message.answer(response)
    await state.clear()

@router.message()
async def get_message(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    await message.answer('Генерирую ответ...')
    response = await ai_generate(message.text, message.from_user.id)  
    try:
        await message.answer(response, parse_mode='Markdown')
    except Exception as e:
        await message.answer(response)
    await state.clear()


