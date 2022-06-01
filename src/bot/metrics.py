"""Exporter metrics definitions"""

from prometheus_client import Counter, Gauge, Histogram

PREFIX = "maker_risks"

COLLATERALS_ZONES_PERCENT = Gauge(
    f"{PREFIX}_collateral_percentage",
    "Maker collaterals percentage distribution",
    ("ilk", "zone"),
)
PARSER_LAST_FETCHED = Gauge(
    f"{PREFIX}_parser_last_fetched",
    "Last one successful parsing cycle completion timestamp",
    ("ilk",),
)
PARSER_LAST_BLOCK = Gauge(
    f"{PREFIX}_parser_last_block",
    "Last block available to fetch from Maker database",
    ("ilk",),
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
