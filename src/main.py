import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from app import JOBS, router
from config import VERSION

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} | {levelname} | {name} | {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa: ARG001, RUF029
    scheduler = AsyncIOScheduler()
    for job, args in JOBS.items():
        if isinstance(args, str):
            scheduler.add_job(job, CronTrigger.from_crontab(args))
        elif isinstance(args, dict):
            scheduler.add_job(job, args.get("trigger", "cron"), **{k: v for k, v in args.items() if k != "trigger"})
    scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/version")
def index() -> dict[str, Any]:
    return {"version": VERSION}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)  # noqa: S104
