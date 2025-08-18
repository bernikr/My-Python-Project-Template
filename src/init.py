from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from apscheduler import AsyncScheduler
from apscheduler.abc import Trigger
from fastapi import FastAPI

VERSION = "0.1.0"

scheduler = AsyncScheduler()

Job = Callable[[], Awaitable[None] | None]

_scheduled_jobs: list[tuple[Job, Trigger]] = []


def schedule[T: Job](trigger: Trigger) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        _scheduled_jobs.append((func, trigger))
        return func

    return decorator


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa: ARG001
    async with scheduler:
        for func, trigger in _scheduled_jobs:
            await scheduler.add_schedule(func, trigger)
        await scheduler.start_in_background()
        yield


api = FastAPI(lifespan=_lifespan)
