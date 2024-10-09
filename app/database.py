from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

async_engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)


class Base(DeclarativeBase):
    crated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())