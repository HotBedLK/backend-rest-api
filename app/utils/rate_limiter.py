from functools import lru_cache

from decouple import config
from fastapi import HTTPException, Request, status
from redis import Redis


@lru_cache(maxsize=1)
def get_redis_client() -> Redis:
    return Redis(
        host=config("REDIS_HOST", default="redis_database"),
        port=config("REDIS_PORT", default=6379, cast=int),
        password=config("REDIS_PASSWORD", default=None),
        db=config("REDIS_DB", default=0, cast=int),
        decode_responses=True,
    )


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int, key_prefix: str = "rl"):
        self.limit = limit
        self.window_seconds = window_seconds
        self.key_prefix = key_prefix

    def _build_key(self, request: Request) -> str:
        client_ip = request.client.host if request.client else "unknown"
        return f"{self.key_prefix}:{client_ip}:{request.url.path}"

    def __call__(self, request: Request) -> None:
        client = get_redis_client()
        key = self._build_key(request)

        count = client.incr(key)
        if count == 1:
            client.expire(key, self.window_seconds)

        if count > self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={"Retry-After": str(self.window_seconds)},
            )
