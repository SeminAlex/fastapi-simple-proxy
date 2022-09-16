import aioredis

from app.routers import photos
from app.utils.settings import Settings
from app.utils.aiohttpsingleton import SingletonAiohttp

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


app = FastAPI()
app.include_router(photos.router)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{Settings.CACHE_URL}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    SingletonAiohttp.get_aiohttp_client()


@app.on_event("shutdown")
def shutdown():
    SingletonAiohttp.close_aiohttp_client()
