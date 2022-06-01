"""Maker protocol collaterals monitoring bot"""

import logging
import time
from pprint import PrettyPrinter

import pandas as pd
from unsync import unsync

from .analytics import calculate_values
from .config import MAKER_DATAAPI_PASSWORD, MAKER_DATAAPI_USERNAME, PARSE_INTERVAL
from .ilks import STECRV_A, WSTETH_A, WSTETH_B
from .metrics import APP_ERRORS, COLLATERALS_ZONES_PERCENT, FETCH_DURATION, PARSER_LAST_BLOCK, PARSER_LAST_FETCHED
from .parsers import BaseParser, MakerAPIParser, MakerAPIProvider


class MakerBot:  # pylint: disable=too-few-public-methods
    """The main class of the Maker bot"""

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.pprint = PrettyPrinter(indent=4)
        self.api = MakerAPIProvider(MAKER_DATAAPI_USERNAME, MAKER_DATAAPI_PASSWORD)

    def _fetch_block(self) -> None:
        self.log.info("Fetching has been started")

    def _compute_metrics(self, data: pd.DataFrame, parser: BaseParser) -> None:
        with APP_ERRORS.labels("calculations").count_exceptions():
            values = calculate_values(data, parser)
        for zone, percent in values.items():
            COLLATERALS_ZONES_PERCENT.labels(parser.asset.symbol, zone).set(percent)
        self.log.debug("Metrics has been updated\n%s", self.pprint.pformat(values))

    @unsync
    def _run(self, parser: BaseParser) -> None:
        with FETCH_DURATION.labels(parser.asset.symbol).time():
            with APP_ERRORS.labels("fetching").count_exceptions():
                data = parser.parse()

        self._compute_metrics(data, parser)
        PARSER_LAST_FETCHED.labels(parser.asset.symbol).set_to_current_time()
        PARSER_LAST_BLOCK.labels(parser.asset.symbol).set(parser.block)

        self.log.info("%s ilk fetch completed", parser.asset.symbol)

    @staticmethod
    def _settle() -> None:
        time.sleep(PARSE_INTERVAL)

    def run(self) -> None:
        """Main loop of bot"""

        while True:

            try:
                tasks = [
                    (
                        asset.symbol,
                        self._run(MakerAPIParser(asset, self.api)),
                    )
                    for asset in (
                        WSTETH_A,
                        WSTETH_B,
                        STECRV_A,
                    )
                ]
            except Exception as ex:  # pylint: disable=broad-except
                self.log.error("Tasks collecting has been failed", exc_info=ex)
                APP_ERRORS.labels("scheduling").inc()
            else:
                for symbol, task in tasks:
                    try:
                        task.result()  # type: ignore
                    except Exception as ex:  # pylint: disable=broad-except
                        self.log.error("Fetching %s collateral has been failed", symbol, exc_info=ex)

            self._settle()
