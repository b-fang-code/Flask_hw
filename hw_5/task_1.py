# Создать API для добавления, обновления, удаления нового пользователя. Приложение
# должно иметь возможность принимать POST, Put и Delete запросы с данными нового
# пользователя и сохранять их.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Создайте маршрут для обновления информации о пользователе (метод PUT).
# Создайте маршрут для удаления пользователя (метод DELETE).
# Реализуйте валидацию данных запроса и ответа.
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []


@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    for i in range(len(users)):
        if users[i].id == user_id:
            users[i] = user
            return user
    return "User not found"


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for i in range(len(users)):
        if users[i].id == user_id:
            users.pop(i)
            return "User deleted"
    return "User not found"


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request, users=users):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
