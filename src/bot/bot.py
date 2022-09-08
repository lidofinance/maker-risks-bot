"""Maker protocol collaterals monitoring bot"""

import logging
import time
from functools import partial
from pprint import PrettyPrinter
from typing import Iterable

import pandas as pd

from .analytics import calculate_values
from .config import MAKER_DATAAPI_PASSWORD, MAKER_DATAAPI_USERNAME, PARSE_INTERVAL, PARSE_METHOD
from .eth import w3
from .ilks import STECRV_A, WSTETH_A, WSTETH_B, MakerIlk
from .metrics import (
    API_LAST_BLOCK,
    APP_ERRORS,
    COLLATERALS_ZONES_PERCENT,
    ETH_LATEST_BLOCK,
    FETCH_DURATION,
    PROCESSING_COMPLETED,
)
from .parsers import MakerAPIParser, MakerAPIProvider, OnChainParser


class MakerBot:  # pylint: disable=too-few-public-methods
    """The main class of the Maker bot"""

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.pprint = PrettyPrinter(indent=4)

        self.assets = (
            WSTETH_A,
            WSTETH_B,
            STECRV_A,
        )

        self.api = MakerAPIProvider(MAKER_DATAAPI_USERNAME, MAKER_DATAAPI_PASSWORD)
        method = OnChainParser if PARSE_METHOD == "ONCHAIN" else partial(MakerAPIParser, api=self.api)
        self.parser = method(assets=self.assets)  # type: ignore

    def _fetch_block(self) -> None:
        self.log.info("Fetching has been started")

    def _run(self) -> Iterable[tuple[MakerIlk, pd.DataFrame]]:
        with FETCH_DURATION.time():
            with APP_ERRORS.labels("fetching").count_exceptions():
                return self.parser.fetch()

    def _compute_metrics(self, df: pd.DataFrame, asset: MakerIlk) -> None:
        with APP_ERRORS.labels("calculations").count_exceptions():
            values = calculate_values(df, asset, self.parser)
        for zone, percent in values.items():
            COLLATERALS_ZONES_PERCENT.labels(asset.symbol, zone).set(percent)
        self.log.debug("Metrics has been updated\n%s", self.pprint.pformat(values))

    @staticmethod
    def _settle() -> None:
        time.sleep(PARSE_INTERVAL)

    def run(self) -> None:
        """Main loop of bot"""

        while True:

            try:
                # set block number metric for status test
                ETH_LATEST_BLOCK.set(w3.eth.block_number)
                API_LAST_BLOCK.set(self.api.last_block())

                results = self._run()
            except Exception as ex:  # pylint: disable=broad-except
                self.log.error("Fetching data has been failed", exc_info=ex)
                APP_ERRORS.labels("fetching").inc()
            else:
                for asset, df in results:
                    try:
                        self._compute_metrics(df, asset)
                        PROCESSING_COMPLETED.labels(asset.symbol).set_to_current_time()

                        self.log.info("%s ilk processed", asset.symbol)
                    except Exception as ex:  # pylint: disable=broad-except
                        self.log.error(
                            "Processing %s collateral has been failed",
                            asset.symbol,
                            exc_info=ex,
                        )

            self._settle()
