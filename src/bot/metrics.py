"""Exporter metrics definitions"""

from prometheus_client import Gauge

PREFIX = "maker_risks"

COLLATERALS_ZONES_PERCENT_NAME = f"{PREFIX}_collateral_percentage"
COLLATERALS_ZONES_PERCENT_HELP = "Maker collaterals percentage distribution"
COLLATERALS_ZONES_PERCENT = Gauge(COLLATERALS_ZONES_PERCENT_NAME, COLLATERALS_ZONES_PERCENT_HELP, ("ilk", "zone"))
PARSER_LAST_FETCHED_NAME = f"{PREFIX}_parser_last_fetched"
PARSER_LAST_FETCHED_HELP = "Last one successful parsing cycle completion timestamp"
PARSER_LAST_FETCHED = Gauge(PARSER_LAST_FETCHED_NAME, PARSER_LAST_FETCHED_HELP, ("ilk",))
