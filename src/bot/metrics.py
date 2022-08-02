"""Exporter metrics definitions"""

import platform as pf

from prometheus_client import Counter, Gauge, Histogram

PREFIX = "maker_risks"

COLLATERALS_ZONES_PERCENT = Gauge(
    f"{PREFIX}_collateral_percentage",
    "Maker collaterals percentage distribution",
    ("ilk", "zone"),
)
PROCESSING_COMPLETED = Gauge(
    f"{PREFIX}_processing_finished_seconds",
    "Last one successful parsing cycle completion timestamp",
    ("ilk",),
)
API_LAST_BLOCK = Gauge(
    f"{PREFIX}_api_last_block_num",
    "Last block number available to fetch from Maker database",
)
ETH_LATEST_BLOCK = Gauge(
    f"{PREFIX}_eth_latest_block_num",
    "Latest block block number fetched by bot",
)
FETCH_DURATION = Gauge(
    f"{PREFIX}_fetch_duration",
    "Collateral type parsing duration",
    ("ilk",),
)
ETH_RPC_REQUESTS = Counter(
    f"{PREFIX}_eth_rpc_requests",
    "Total count of requests to ETH1 RPC",
    ("method", "code"),
)
ETH_RPC_REQUESTS_DURATION = Histogram(
    f"{PREFIX}_eth_rpc_requests_duration",
    "Duration of requests to ETH1 RPC",
)
APP_ERRORS = Counter(
    f"{PREFIX}_app_errors",
    "Errors count raised during app lifecycle",
    ("module",),
)
HTTP_REQUESTS_DURATION = Histogram(
    f"{PREFIX}_http_requests_duration",
    "Duration of HTTP requests",
    ("domain", "path", "method"),
)
HTTP_REQUESTS = Counter(
    f"{PREFIX}_http_requests",
    "Total count of HTTP requests",
    ("domain", "path", "method", "http_code"),
)

BUILD_INFO = Gauge(
    f"{PREFIX}_build_info",
    "Bot build info",
    ("pyversion",),
)


def report_build_info() -> None:
    """Report _build_info metric"""

    pyversion = ".".join(pf.python_version_tuple())
    BUILD_INFO.labels(
        pyversion=pyversion,
    ).set(1)
