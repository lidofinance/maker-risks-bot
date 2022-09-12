"""Configurable constants here"""

import logging
import os
from typing import Any, Type, TypeAlias

logging_handler = logging.StreamHandler()

if os.getenv("LOG_FORMAT", "simple") == "json":
    from pythonjsonlogger import jsonlogger

    formatter = jsonlogger.JsonFormatter("%(asctime)%(levelname)%(name)%(message)")
    logging_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=(logging_handler,))
log = logging.getLogger(__name__)


T: TypeAlias = Any
D = object()  # sentinel


def getenv(name: str, astype: Type[T] = str, default: T = D, required: bool = False) -> T:
    """Get environment variable in failsafe manner"""

    if required and default is not D:
        raise ValueError("Unable to parse environment variable with both required and default")

    if required and name not in os.environ:
        raise RuntimeError(f"{name} environment variable is required")

    if name in os.environ:
        try:
            return astype(os.getenv(name))
        except (TypeError, ValueError) as ex:
            log.warning("Failed to parse %s environment variable, fallback to default=%s", name, default, exc_info=ex)

    return default


# === Required ===

NODE_ENDPOINT = getenv("NODE_ENDPOINT", required=True)
if "wss://" in NODE_ENDPOINT:
    # WSS provider seems to be broken in python 3.10 and
    # doesn't work in the current flow. Magic asyncio fails happen.
    raise RuntimeError("Only http[s] Web3 provider endpoint supported")

# === Optional ===

PARSE_INTERVAL = getenv("PARSE_INTERVAL", int, 15 * 60)  # 15 min
EXPORTER_PORT = getenv("EXPORTER_PORT", int, default=8080)
