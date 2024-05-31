import json

from app.main import app


async def get_cached_data(key):
    data_str = await app.state.redis.get(key)
    if data_str is not None:
        data = json.loads(data_str)
    else:
        data = None
    return data


async def set_cached_data(key, value, expiry=3600 * 24):
    data_str = json.dumps(value)
    await app.state.redis.set(key, data_str)
    await app.state.redis.expire(key, expiry)  # Set TTL to 1 day
