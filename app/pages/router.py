from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.dao import MasterDAO, ServiceDAO, ApplicationDAO, UserDAO
from app.config import settings

router = APIRouter(prefix="", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "title": "Элегантная парикмахерская"})


@router.get("/form")
async def form(request: Request, user_id: int = None, first_name: str = None) -> HTMLResponse:
    masters = await MasterDAO.find_all()
    services = await ServiceDAO.find_all()
    return templates.TemplateResponse("form.html", {"request": request,
                                                    "masters": masters,
                                                    "services": services,
                                                    "user_id": user_id,
                                                    "first_name": first_name,
                                                    "title": "Запись на услуги - Элегантная парикмахерская",
                                                    })


@router.get("/admin")
async def admin(request: Request, admin_id: int = None) -> HTMLResponse:
    data_page = {"request": request, 'title_h1': "Панель Администратора"}
    if admin_id is None or admin_id != settings.ADMIN_ID:
        data_page['message'] = "У вас нет прав для получения информации о заявках!"
        data_page["access"] = False
    else:
        data_page["access"] = True
        data_page['applications'] = await ApplicationDAO.find_all()
    return templates.TemplateResponse("applications.html", data_page)


@router.get("/applications")
async def applications(request: Request, user_id: int = None) -> HTMLResponse:
    data_page = {"request": request, "title_h1": "Мои записи"}
    user_check = await UserDAO.find_one_or_none(telegram_id=user_id)

    if user_id is None or user_check is None:
        data_page['message'] = 'Пользователь, по которому нужно отобразить заявки, не указан или не найден в базе данных'
        data_page['access'] = False
    else:
        applications = await ApplicationDAO.find_all(user_id=user_id)
        data_page['access'] = True
        if applications:
            data_page['applications'] = applications
        else:
            data_page['message'] = 'У вас нет заявок!'
    return templates.TemplateResponse('applications.html', data_page)
