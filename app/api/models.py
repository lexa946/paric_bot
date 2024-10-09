import enum
from datetime import time, date


from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False  )
    username: Mapped[str] = mapped_column(nullable=True)

    applications: Mapped[list["Application"]] = relationship(back_populates="user")




class Master(Base):
    __tablename__ = 'masters'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    applications: Mapped[list["Application"]] = relationship(back_populates="master")

    def __repr__(self):
        return f"Master {self.id}_{self.name}"


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    applications: Mapped[list["Application"]] = relationship(back_populates="service")

    def __repr__(self):
        return f"Service {self.id}_{self.name}"

class Application(Base):
    __tablename__ = 'applications'

    class GenderEnum(enum.Enum):
        male = "Мужской"
        female = "Женский"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    master_id: Mapped[int] = mapped_column(ForeignKey('masters.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))

    appointment_date: Mapped[date] = mapped_column(nullable=False) # Дата заявки
    appointment_time: Mapped[time] = mapped_column(nullable=False) # Время заявки

    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=False)

    client_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)

    user: Mapped[list[User]] = relationship(back_populates="applications")
    service: Mapped[list[Service]] = relationship(back_populates="applications")
    master: Mapped[list[Master]] = relationship(back_populates="applications")
