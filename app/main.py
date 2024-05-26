from fastapi import FastAPI
from app.database.database import engine, Base
from app.database.models import models

from app.routes.routes import router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
