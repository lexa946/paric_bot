import asyncio
import json
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert


from app.main import app as fastapi_application
from app.config import settings
from app.database import Base, async_session_maker, async_engine
from app.api.models import Master, Service


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # assert settings.MODE == "TEST"

    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(suffix: str):
        with open(f"app/tests/mock_{suffix}.json", encoding="UTF-8") as file:
            return json.load(file)

    masters = open_mock_json("masters")
    services = open_mock_json("services")

    async with async_session_maker() as session:
        add_threads = insert(Master).values(masters)
        add_services = insert(Service).values(services)

        await session.execute(add_threads)
        await session.execute(add_services)


        await session.commit()



@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()




@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=fastapi_application)) as aclient:
        yield aclient

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session






