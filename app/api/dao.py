from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.api.models import User, Service, Master, Application


class UserDAO(BaseDAO):
    model = User


class ServiceDAO(BaseDAO):
    model = Service


class MasterDAO(BaseDAO):
    model = Master


class ApplicationDAO(BaseDAO):
    model = Application

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            results = await session.scalars(
                select(cls.model)
                .options(joinedload(cls.model.master), joinedload(cls.model.service), joinedload(cls.model.user))
                .filter_by(**filter_by)
            )
            application = results.all()
            return application

