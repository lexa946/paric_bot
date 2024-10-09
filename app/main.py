from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging

from app.pages.router import router as page_router
from app.api.routers import router as api_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(page_router)
app.include_router(api_router)

origins = [
    'http://localhost:8080', 'http://0.0.0.0',
    'http://alex.pozharsite.ru',
    "http://db.pozharsite.ru",
    "http://bots.pozharsite.ru", "https://bots.pozharsite.ru",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
