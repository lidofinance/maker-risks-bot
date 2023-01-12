"""Ethereum blockchain parser"""

import logging
from typing import Iterable, Mapping, Set

import pandas as pd
from unsync import Unfuture, unsync
from web3.types import EventData

from ..eth import CDP_MANAGER, w3
from ..ilks import MakerIlk
from .base import BaseParser

log = logging.getLogger(__name__)

CdpsMap = Mapping[str, Set[int]]


class OnChainParser(BaseParser):
    """Maker protocol parser based on the requests to Ethereum blockchain"""

    def __init__(self, assets: Iterable[MakerIlk]) -> None:
        super().__init__(assets)

        self.cdps_map: CdpsMap = {join: set() for join in (asset.join for asset in self.assets)}
        self.cdps_map_updated_at: int | None = None

    @unsync
    def _cdps_batch(self, l_block: int, r_block: int) -> CdpsMap:
        results: CdpsMap = {join: set() for join in (asset.join for asset in self.assets)}

        new_cdp_filter = CDP_MANAGER.events["NewCdp"].createFilter(
            fromBlock=l_block,
            toBlock=r_block,
        )

        event: EventData
        for event in new_cdp_filter.get_all_entries():

            receipt = w3.eth.get_transaction_receipt(event["transactionHash"])
            for entry in receipt["logs"]:
                join = entry["address"]

                if not any(join == asset.join for asset in self.assets):
                    continue  # not that cdp we are looking for

                if "args" not in event:
                    log.warning("args not found at %s", event)
                    continue

                if cdp := event["args"].get("cdp"):
                    results[join].add(cdp)

        return results

    def update_cdps_map(self) -> None:
        """Get cdps from GemJoin contract logs"""

        if not isinstance(self.block, int):
            raise ValueError("Ethereum block value is not fetched")

        block = self.cdps_map_updated_at or min(asset.created for asset in self.assets)
        batch_size = 100_000

        # schedule tasks
        batches = []
        while block <= self.block:
            batches.append(self._cdps_batch(block, block + batch_size))
            block += batch_size

        # unpack values
        batch: Unfuture
        for batch in batches:
            map: Mapping[str, Iterable[int]]  # pylint: disable=redefined-builtin
            map = batch.result()
            for join, cdps in map.items():
                self.cdps_map[join].update(cdps)
        # store milestone block
        self.cdps_map_updated_at = block

    def fetch(self) -> Iterable[tuple[MakerIlk, pd.DataFrame]]:
        self.block = w3.eth.block_number
        log.info("fetching data for block %d", self.block)

        self.update_cdps_map()

        dfs = []

        for asset in self.assets:
            cdps = self.cdps_map[asset.join]
            urns = []

            tasks = [asset.get_urn_by_cdp(cdp, self.block) for cdp in cdps]
            for task in tasks:
                urn = task.result()  # type:ignore
                urns.append(urn)

            stats = []
            tasks = [(urn, self.get_vault_stat(asset, urn)) for urn in urns]
            for urn, task in tasks:
                ink, art = task.result()  # type: ignore
                stats.append(
                    {
                        "urn": urn,
                        "ink": ink,
                        "art": art,
                    }
                )

            df = pd.DataFrame(stats)
            dfs.append((asset, df))

        return dfs
