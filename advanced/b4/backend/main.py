import uvicorn
from fastapi import FastAPI

from source.config import settings
from source.db_connect import connect_with_retry, disconnect
from source.routers.auth import router as auth_router
from source.routers.users import router as users_router
from source.routers.articles import router as articles_router


app = FastAPI(
    title="Test Task API"
)


@app.on_event("startup")
async def open_connection():
    await connect_with_retry()


@app.on_event("shutdown")
async def close_connection():
    await disconnect()


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(articles_router, prefix="/articles", tags=["Articles"])


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
