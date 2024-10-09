from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards import app_keyboard
from app.bot.utils import greet_user, get_about_us_text
from app.api.dao import UserDAO

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)

    if not user:
        await UserDAO.add(telegram_id=message.from_user.id,
                          first_name=message.from_user.first_name,
                          username=message.from_user.username
                          )

    await greet_user(message, is_new_user=not user)

@router.message(F.text == "🔙 Назад")
async def cmd_back_home(message: Message) -> None:
    await greet_user(message, is_new_user=False)

@router.message(F.text == "user")
async def cmd_user(message: Message):
    print(message.from_user.url)
    await message.answer(str(message.from_user))

@router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(get_about_us_text(), reply_markup=kb)
