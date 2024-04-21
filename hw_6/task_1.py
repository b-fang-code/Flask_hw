# Напишите API для управления списком задач. Для этого создайте модель Task
# со следующими полями:
# id: int (первичный ключ),
# title: str (название задачи),
# description: str (описание задачи),
# done: bool (статус выполнения задачи),
# API должно поддерживать следующие операции:
# Получение списка всех задач: GET /tasks,
# Получение информации о конкретной задаче: GET /tasks/{task_id}/,
# Создание новой задачи: POST /tasks/,
# Обновление информации о задаче: PUT /tasks/{task_id}/,
# Удаление задачи: DELETE /tasks/{task_id}/,
# Для валидации данных используйте параметры Field модели Task.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.


from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases
from typing import List
import sqlalchemy

app = FastAPI()

DATABASE_URL = "sqlite:///tasks.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.String(500)),
    sqlalchemy.Column("done", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


class TaskIn(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    done: bool


class Task(TaskIn):
    id: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskIn):
    query = tasks.insert().values(**task.dict())
    last_record_id = await database.execute(query)
    return {**task.dict(), "id": last_record_id}


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    query = tasks.update().where(tasks.c.id == task_id).values(**task.dict())
    await database.execute(query)
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return 'Task deleted'
