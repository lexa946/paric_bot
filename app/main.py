from aiogram.types import Update
from fastapi import FastAPI, Request

import logging

from starlette.staticfiles import StaticFiles


from app.pages.router import router as page_router
from app.api.routers import router as api_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(page_router)
app.include_router(api_router)


@app.post("/webhook")
async def webhook(request: Request)->None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot":bot})
    await dp.feed_update(bot=bot, update=update)
    logging.info("Update processed")

