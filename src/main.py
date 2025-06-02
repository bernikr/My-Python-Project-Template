from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import TYPE_CHECKING, Any

from init import VERSION, api

if TYPE_CHECKING:
    from types import ModuleType

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} | {levelname} | {name} | {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@api.get("/version")
def index() -> dict[str, Any]:
    return {"version": VERSION}


def import_submodules(package: str | ModuleType) -> dict[str, ModuleType]:
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if is_pkg:
            results.update(import_submodules(full_name))
    return results


modules = import_submodules("app")
logger.info("Loaded %i modules: %s", len(modules), ", ".join(modules.keys()))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:api", host="0.0.0.0", port=5000, log_level="info", reload=True)  # noqa: S104
