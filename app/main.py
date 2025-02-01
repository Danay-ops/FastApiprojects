from fastapi import FastAPI, HTTPException
from app.db import database, User
from pydantic import BaseModel

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # создаем тестовую запись
    await User.objects.get_or_create(email="test@test.com")

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

@app.get("/")
def read_root():
    return {"hello": "world"}

# Маршрут для получения всех пользователей
@app.get("/users")
async def get_users():
    users = await User.objects.all()  # Получаем всех пользователей
    return users
