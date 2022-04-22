"""Prometheus exporter of metrics collected from aggregated Anchor protocol data"""

import logging

from prometheus_client import start_http_server

from bot import MakerBot
from bot.config import EXPORTER_PORT

log = logging.getLogger(__name__)


if __name__ == "__main__":
    log.info("Starting prometheus exporter server on port %s", EXPORTER_PORT)
    start_http_server(EXPORTER_PORT)
    bot = MakerBot()
    bot.run()
