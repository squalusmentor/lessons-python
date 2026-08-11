"""Точка входа приложения.

Здесь живёт ровно две вещи:
1) создание объекта FastAPI (`app`) и подключение роутеров;
2) запуск сервера (uvicorn).

Никакой бизнес-логики тут быть не должно — она в хендлерах и сервисах.
"""

import uvicorn
from fastapi import FastAPI

from source.routers.users import router as users_router


app = FastAPI(title="Users API — урок B2")


@app.get("/")
async def root():
    """Корневой эндпоинт — просто подсказка, куда идти за документацией."""
    return {"message": "Users API. Документация: /docs"}


# Подключаем роутер пользователей: все его пути получат префикс /users
app.include_router(users_router, prefix="/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
