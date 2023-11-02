"""Maker protocol collaterals monitoring bot"""

import logging
import time
from pprint import PrettyPrinter
from typing import Iterable

import pandas as pd

from .analytics import calculate_values
from .config import MAIN_ERROR_COOLDOWN, PARSE_INTERVAL
from .eth import w3
from .ilks import STECRV_A, WSTETH_A, WSTETH_B, MakerIlk
from .metrics import (
    APP_ERRORS,
    BOT_LAST_BLOCK,
    COLLATERALS_ZONES_PERCENT,
    COLLATERALS_ZONES_VALUE,
    COLLATERALS_ZONES_CURRENCY,
    ETH_LATEST_BLOCK,
    FETCH_DURATION,
    PROCESSING_COMPLETED,
)
from .parsers import OnChainParser
from .middleware import wstethLastPrice, ethLastPrice, stETHLastPrice

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
        self.prices = {
            "wstETH_A": 0,
            "wstETH_B": 0,
            "steCRV_A": 0
        }

        self.parser = OnChainParser(assets=self.assets)  # type: ignore

    def run(self) -> None:
        """Main loop of bot"""

        while True:
            try:
                # The approximate price of the coin on this block
                self.prices["wstETH_A"] = wstethLastPrice()
                self.prices["wstETH_B"] = self.prices["wstETH_A"]
                self.prices["steCRV_A"] = ethLastPrice() * 0.5 + stETHLastPrice() * 0.5
            except Exception as ex:  # pylint: disable=broad-except
                APP_ERRORS.labels("fetchingPrice").inc()
                self._on_error("Fetching price data has been failed", ex)
                continue

            try:
                results = self._run()
                # set block number metric for status test
                ETH_LATEST_BLOCK.set(w3.eth.block_number)
                BOT_LAST_BLOCK.set(0 if self.parser.block == "latest" else self.parser.block)
            except Exception as ex:  # pylint: disable=broad-except
                APP_ERRORS.labels("fetching").inc()
                self._on_error("Fetching data has been failed", ex)
                continue

            errors: list[tuple[MakerIlk, Exception]] = []
            for asset, df in results:
                try:  # try to compute metrics for each asset
                    self._compute_metrics(df, asset)
                    PROCESSING_COMPLETED.labels(asset.symbol).set_to_current_time()

                    self.log.info("%s ilk processed", asset.symbol)
                except Exception as ex:  # pylint: disable=broad-except
                    errors.append((asset, ex))
            if errors:
                for asset, ex in errors:
                    self.log.error("Processing %s has been failed", asset.symbol, exc_info=ex)
                    APP_ERRORS.labels("calculations").inc()
                self._on_error("Processing has been failed", Exception("See logs for details"))
                continue

            self._on_success()

    def _fetch_block(self) -> None:
        self.log.info("Fetching has been started")

    def _run(self) -> Iterable[tuple[MakerIlk, pd.DataFrame]]:
        with FETCH_DURATION.time():
            with APP_ERRORS.labels("fetching").count_exceptions():
                return self.parser.fetch()

    def _compute_metrics(self, df: pd.DataFrame, asset: MakerIlk) -> None:
        with APP_ERRORS.labels("calculations").count_exceptions():
            values = calculate_values(df, asset, self.parser)

        for zone, stat in values.items():
            COLLATERALS_ZONES_CURRENCY.labels(
                asset.symbol,
                zone,
            ).set(self.prices[asset.symbol] * stat["ilk"])
            COLLATERALS_ZONES_VALUE.labels(
                asset.symbol,
                zone,
            ).set(stat["ilk"])
            COLLATERALS_ZONES_PERCENT.labels(
                asset.symbol,
                zone,
            ).set(stat["percent"])

        self.log.debug("Metrics has been updated\n%s", self.pprint.pformat(values))

    def _on_success(self) -> None:
        self.log.info("Wait for %d seconds for the next fetch", PARSE_INTERVAL)
        time.sleep(PARSE_INTERVAL)

    def _on_error(self, msg: str, ex: Exception) -> None:
        self.log.error(msg, exc_info=ex)
        self.log.info("Wait for %d seconds before the next try", MAIN_ERROR_COOLDOWN)
        time.sleep(MAIN_ERROR_COOLDOWN)
