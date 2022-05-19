"""Base parser"""

from abc import ABC, abstractmethod

import pandas as pd
from unsync import unsync

from ..eth import VAT, w3
from ..ilks import MakerCollateral


class BaseParser(ABC):
    """Maker protocol parser"""

    def __init__(self, asset: MakerCollateral) -> None:
        self.asset = asset
        self.block: str | int = "latest"

    def get_vat_stats(self) -> tuple:
        """
        Get statistic about collateral type from Vault Engine.
        https://docs.makerdao.com/smart-contract-modules/core-module/vat-detailed-documentation#glossary-vat-vault-engine
        """

        return VAT.functions.ilks(self.asset.ilk).call(block_identifier=self.block)  # type: ignore

    @unsync
    def get_vault_stat(self, vault: str) -> tuple[int, int]:
        """Get collateral and debt for the given vault"""

        vault = w3.toChecksumAddress(vault)
        return VAT.functions.urns(self.asset.ilk, vault).call(block_identifier=self.block)  # type: ignore

    @abstractmethod
    def parse(self) -> pd.DataFrame:
        """Parse required data"""
