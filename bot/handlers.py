from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction



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

@router.message(Command('reset'))
async def cmd_reset(message: Message):
    from client.history import history
    if message.from_user.id in history:
        del history[message.from_user.id]
    await message.answer("История очищена, начинаем заново!")

@router.message(F.document | F.video | F.audio | F.voice | F.sticker | F.video_note)
async def unsupported_content(message: Message):
    await message.answer("Я принимаю только текст и фотографии. Попробуй описать задачу текстом или отправь фото.")



@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('Подождите, я еще не ответил на предыдущий вопрос')

@router.message(F.photo)
async def get_photo(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    await message.chat.do(ChatAction.TYPING)
    await message.answer('Генерирую ответ...')

    
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_TOKEN')}/{file.file_path}"
    
    caption = message.caption or "Объясни задачу на фото"

    try:
        response = await ai_generate_image(file_url, message.from_user.id,caption)
        
        await message.answer(response)
    
    except Exception as e:
        await message.answer(" Произошла ошибка при обработке фото. Попробуйте отправить его еще раз или опишите задачу текстом.")
        print(f"Ошибка при обработке фото: {e}")
    
    finally:
        await state.clear()



@router.message()
async def get_message(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    await message.chat.do(ChatAction.TYPING)
    await message.answer('Генерирую ответ...')
    
    
    try:
        response = await ai_generate(message.text, message.from_user.id)  
        try:
            await message.answer(response)
        except Exception as e:
            await message.answer(response)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса, попрбуйте еще раз.")
        print(f"Ошибка при обработке запроса: {e}")
    finally:
        await state.clear()



