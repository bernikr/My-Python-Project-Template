import logging

from fastapi import APIRouter

from config import JobDef

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def index() -> str:
    return "Hello World"


def test() -> None:
    logger.info("test")


JOBS: JobDef = {
    test: {"second": "*/5"},
}
