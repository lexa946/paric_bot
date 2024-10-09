from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.bot.routers.user import router as user_router
from app.bot.routers.admin import router as admin_router


bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_router(user_router)
dp.include_router(admin_router)


async def start_bot():
    await bot.send_message(settings.ADMIN_ID, f'Я запущен🥳.')
    await dp.start_polling(bot)


