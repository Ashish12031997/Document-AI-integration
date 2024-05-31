import os

import aioredis
from fastapi import FastAPI

from app.database.database import Base, engine
from app.database.models import models

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis_url = f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:6379"
    try:
        app.state.redis = await aioredis.from_url(redis_url, decode_responses=True)
    except aioredis.exceptions.ConnectionError as e:
        logging.error(f"Failed to connect to Redis: {e}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
