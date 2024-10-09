from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.dao import ApplicationDAO
from app.api.schemas import SAppointment, SApplication
from app.bot.create_bot import bot
from app.bot.keyboards import main_keyboard
from app.config import settings

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/appointment")
async def create_appointment(appointment: SAppointment) -> JSONResponse:
    master_id, master_name = appointment.stylist.split('_')
    service_id, service_name = appointment.service.split('_')
    gender, gender_name = appointment.gender.split('_')

    message = (
        f"🎉 <b>{appointment.name}, ваша заявка успешно принята!</b>\n\n"
        "💬 <b>Информация о вашей записи:</b>\n"
        f"👤 <b>Имя клиента:</b> {appointment.name}\n"
        f"📱 <b>Телефон клиента:</b> {appointment.phone}\n"
        f"🧑‍🦰 <b>Пол клиента:</b> {gender_name}\n"
        f"💇 <b>Услуга:</b> {service_name}\n"
        f"✂️ <b>Мастер:</b> {master_name}\n"
        f"📅 <b>Дата записи:</b> {appointment.appointment_date}\n"
        f"⏰ <b>Время записи:</b> {appointment.appointment_time}\n\n"
        "Спасибо за выбор нашей студии! ✨ Мы ждём вас в назначенное время."
    )

    admin_message = (
        "🔔 <b>Новая запись!</b>\n\n"
        "📄 <b>Детали заявки:</b>\n"
        f"👤 Имя клиента: {appointment.name}\n"
        f"📱 Телефон клиента: {appointment.phone}\n"
        f"💇 Услуга: {service_name}\n"
        f"✂️ Мастер: {master_name}\n"
        f"📅 Дата: {appointment.appointment_date}\n"
        f"⏰ Время: {appointment.appointment_time}\n"
        f"🧑‍🦰 Пол клиента: {gender_name}"
    )

    await ApplicationDAO.add(
        user_id=appointment.user_id,
        master_id=int(master_id),
        service_id=int(service_id),
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        client_name=appointment.name,
        gender=gender,
        phone=appointment.phone,
    )
    kb = main_keyboard(user_id=appointment.user_id, first_name=appointment.name)

    await bot.send_message(chat_id=appointment.user_id, text=message, reply_markup=kb)
    await bot.send_message(chat_id=settings.ADMIN_ID, text=admin_message, reply_markup=kb)

    return {"message": "success!"}


@router.get("/applications")
async def get_applications(user_id: int, all: bool = None) -> list[SApplication]:
    if user_id == settings.ADMIN_ID and all:
        applications = await ApplicationDAO.find_all()
    else:
        applications = await ApplicationDAO.find_all(user_id=user_id)
    return applications
