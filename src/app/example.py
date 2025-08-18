import logging

from apscheduler.triggers.interval import IntervalTrigger

from init import api, schedule

logger = logging.getLogger(__name__)


@api.get("/")
def index() -> str:
    return "Hello World"


@schedule(IntervalTrigger(seconds=5))
def test() -> None:
    logger.info("test")
