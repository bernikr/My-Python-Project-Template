from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

VERSION = "0.1.0"

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa: ARG001, RUF029
    scheduler.start()
    yield


api = FastAPI(lifespan=_lifespan)
