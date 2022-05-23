"""Exporter metrics definitions"""

from prometheus_client import Gauge

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
