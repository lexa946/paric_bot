from aiogram.types import Update
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import logging

from starlette.staticfiles import StaticFiles

from app.config import settings
from app.bot.create_bot import bot, dp, start_bot, stop_bot
from app.bot.routers.user import router as user_router
from app.bot.routers.admin import router as admin_router
from app.pages.router import router as page_router
from app.api.routers import router as api_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await start_bot()
    response = await bot.set_webhook(url=settings.WEBHOOK_URL, allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)

    logging.info(f"{response=}")
    logging.info(f"Webhook set to {settings.WEBHOOK_URL}")
    yield
    logging.info("Shutting down bot...")
    await stop_bot()
    await bot.delete_webhook()
    logging.info(f"Webhook deleted")

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(page_router)
app.include_router(api_router)


@app.post("/webhook")
async def webhook(request: Request)->None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot":bot})
    await dp.feed_update(bot=bot, update=update)
    logging.info("Update processed")

