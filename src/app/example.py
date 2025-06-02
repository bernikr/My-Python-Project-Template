import logging

from init import api, scheduler

logger = logging.getLogger(__name__)


@api.get("/")
def index() -> str:
    return "Hello World"


@scheduler.scheduled_job("interval", seconds=5)
def test() -> None:
    logger.info("test")
