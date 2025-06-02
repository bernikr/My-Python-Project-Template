from typing import Any, Callable

VERSION = "0.1.0"

type JobDef = dict[Callable, str | dict[str, Any]]
