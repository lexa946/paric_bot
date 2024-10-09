

from pydantic import BaseModel, Field
from datetime import date, time


class SAppointment(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя клиента")
    gender: str = Field(..., min_length=2, max_length=50, description="Пол клиента")
    service: str = Field(..., min_length=2, max_length=50, description="Услуга клиента")
    stylist: str = Field(..., min_length=2, max_length=50, description="Имя мастера")
    appointment_date: date = Field(..., description="Дата назначения")
    appointment_time: time = Field(..., description="Время назначения")
    user_id: int = Field(..., description="ID пользователя Telegram")
    phone:str = Field(..., description="Номер телефона клиента")

    class Config:
        from_attributes = True


class SService(BaseModel):
    id: int
    name: str

class SMaster(BaseModel):
    id: int
    name:str


class SApplication(BaseModel):
    id: int
    service: SService
    master: SMaster
    appointment_date: date
    appointment_time: time
    gender: str
    phone: str


    class Config:
        from_attributes = True