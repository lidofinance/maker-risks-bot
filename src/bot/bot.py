"""Maker protocol collaterals monitoring bot"""

import logging
import time
from pprint import PrettyPrinter

import pandas as pd
from unsync import unsync

from .analytics import calculate_values
from .ilks import STECRV, WSTETH, MakerCollateral
from .makerparser import MakerParser, make_parser
from .metrics import COLLATERALS_ZONES_PERCENT, PARSER_LAST_FETCHED

S15MIN = 15 * 60


class MakerBot:  # pylint: disable=too-few-public-methods
    """The main class of the Aave bot"""

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.pprint = PrettyPrinter(indent=4)

    def _fetch_block(self) -> None:
        self.log.info("Fetching has been started")

    def _compute_metrics(self, data: pd.DataFrame, ilk: MakerCollateral, parser: MakerParser) -> None:
        values = calculate_values(data, ilk, parser)
        for zone, percent in values.items():
            COLLATERALS_ZONES_PERCENT.labels(ilk.symbol, zone).set(percent)
        self.log.debug("Metrics has been updated\n%s", self.pprint.pformat(values))

    @unsync
    def _parse(self, ilk: MakerCollateral) -> None:
        parser = make_parser(ilk)
        data = parser.parse()
        self._compute_metrics(data, ilk, parser)
        PARSER_LAST_FETCHED.labels(ilk.symbol).set_to_current_time()

    @staticmethod
    def _settle() -> None:
        time.sleep(S15MIN)

    def run(self) -> None:
        """Main loop of bot"""

        while True:

            try:
                tasks = [
                    (ilk, self._parse(ilk))
                    for ilk in (
                        WSTETH,
                        STECRV,
                    )
                ]
            except Exception as ex:  # pylint: disable=broad-except
                self.log.error("Tasks collecting has been failed", exc_info=ex)
            else:
                for ilk, task in tasks:
                    try:
                        task.result()  # type: ignore
                    except Exception as ex:  # pylint: disable=broad-except
                        self.log.error("Fetching %s collateral has been failed", ilk.symbol, exc_info=ex)

            self._settle()
