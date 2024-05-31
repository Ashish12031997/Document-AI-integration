import tracemalloc

from dotenv import load_dotenv
from fastapi import FastAPI

from app.app_state import app

tracemalloc.start()
load_dotenv()


from app.routes.routes import router

app.include_router(router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/test_redis")
async def test_redis():
    await app.state.redis.set("my-key", "Hello, World!")
    value = await app.state.redis.get("my-key")
    return {"value": value}
