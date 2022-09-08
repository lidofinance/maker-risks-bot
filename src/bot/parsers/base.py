"""Base parser"""

from abc import ABC, abstractmethod
from typing import Iterable

import pandas as pd
from unsync import unsync
from web3.types import BlockIdentifier

from ..eth import VAT, w3
from ..ilks import MakerIlk


class BaseParser(ABC):
    """Maker protocol parser"""

    def __init__(self, assets: Iterable[MakerIlk]) -> None:
        self.block: BlockIdentifier
        self.assets = assets

    def get_vat_stats(self, asset: MakerIlk) -> tuple:
        """
        Get statistic about collateral type from Vault Engine.
        https://docs.makerdao.com/smart-contract-modules/core-module/vat-detailed-documentation#glossary-vat-vault-engine
        """

        return VAT.functions.ilks(asset.ilk).call(block_identifier=self.block)  # type: ignore

    @unsync
    def get_vault_stat(self, asset: MakerIlk, vault: str) -> tuple[int, int]:
        """Get collateral and debt for the given vault"""

        vault = w3.toChecksumAddress(vault)
        return VAT.functions.urns(asset.ilk, vault).call(block_identifier=self.block)

    @abstractmethod
    def fetch(self) -> Iterable[tuple[MakerIlk, pd.DataFrame]]:
        """Fetch required data"""
