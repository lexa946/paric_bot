from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.config import settings


def main_keyboard(user_id: int, first_name: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🌐 Мои заявки", web_app=WebAppInfo(
        url=f"{settings.BASE_SITE}/applications?user_id={user_id}"
    ))
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(
        url=f"{settings.BASE_SITE}/form?user_id={user_id}&first_name={first_name}"
    ))
    kb.button(text="ℹ️ О нас")
    if user_id == settings.ADMIN_ID:
        kb.button(text="🔑 Админ панель")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🔙 Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def admin_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 На главную", callback_data="back_home")
    kb.button(text="📝 Смотреть заявки", web_app=WebAppInfo(
        url=f"{settings.BASE_SITE}/admin?admin_id={user_id}"
    ))
    kb.adjust(1)
    return kb.as_markup()


def app_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(
        url=f"{settings.BASE_SITE}/form?user_id={user_id}&first_name={first_name}"
    ))
    kb.adjust(1)
    return kb.as_markup()