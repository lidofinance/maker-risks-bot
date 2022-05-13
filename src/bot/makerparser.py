"""Module for parsing data from Anchor protocol contracts"""

from abc import ABC, abstractmethod
from typing import Iterable

import pandas as pd
import requests
from unsync import unsync

from .config import FLIPSIDE_ENDPOINT_STECRV, FLIPSIDE_ENDPOINT_WSTETH
from .eth import CDP_MANAGER, CDP_REGISTRY, CROPPER, VAT
from .ilks import STECRV, WSTETH, MakerCollateral

RAY_DECIMALS = 27
RAD_DECIMALS = 45
WAD_DECIMALS = 18


class MakerParser(ABC):
    """Maker protocol parser"""

    ILK: str
    FLIPSIDE_ENDPOINT: str

    def get_cdps(self) -> Iterable:
        """Get the list of CDP:VAULT_ADDRESS.
        NB! It's subject to change!"""

        response = requests.get(self.FLIPSIDE_ENDPOINT, timeout=15)
        response.raise_for_status()
        return response.json()

    def get_vat_stats(self) -> tuple:
        """
        Get statistic about collateral type from Vault Engine.
        https://docs.makerdao.com/smart-contract-modules/core-module/vat-detailed-documentation#glossary-vat-vault-engine
        """

        return VAT.functions.ilks(self.ILK).call()

    @abstractmethod
    @unsync
    def get_vault(self, cdp: int) -> str:
        """Get UrnHandler, i.e. vault by CDP"""

    @unsync
    def get_vault_stat(self, vault: str) -> tuple[int, int]:
        """Get collateral and debt for the given vault"""

        return VAT.functions.urns(self.ILK, vault).call()

    def parse(self) -> pd.DataFrame:
        """Parse required data"""

        df = pd.DataFrame(self.get_cdps())
        df.rename(columns={"ADDRESS": "address", "CDP": "cdp"}, inplace=True)
        df["cdp"] = pd.to_numeric(df["cdp"])  # contracts accept uint256 as and argument
        df.drop_duplicates(inplace=True)

        vaults, stats = [], []

        tasks = [(cdp, self.get_vault(cdp)) for cdp in df["cdp"]]
        for cdp, task in tasks:
            vat = task.result()  # type: ignore
            vaults.append(
                {
                    "cdp": cdp,
                    "vault": vat,
                }
            )

        tasks = [(item["cdp"], self.get_vault_stat(item["vault"])) for item in vaults]
        for cdp, task in tasks:
            ink, art = task.result()  # type: ignore
            stats.append(
                {
                    "cdp": cdp,
                    "ink": ink,
                    "art": art,
                }
            )

        for part in (vaults, stats):
            df = df.merge(pd.DataFrame(part), on="cdp", how="left")

        return df


class WSTETHParser(MakerParser):
    """WSTETH collateral Maker parser"""

    ILK = WSTETH.ilk
    FLIPSIDE_ENDPOINT = FLIPSIDE_ENDPOINT_WSTETH

    @staticmethod
    def _get_urn(cdp: int) -> str:
        return CDP_MANAGER.functions.urns(cdp).call()

    @unsync
    def get_vault(self, cdp: int) -> str:
        return self._get_urn(cdp)


class STECRVParser(MakerParser):
    """STECRV collateral Maker parser"""

    ILK = STECRV.ilk
    FLIPSIDE_ENDPOINT = FLIPSIDE_ENDPOINT_STECRV

    @staticmethod
    def _get_owner(cdp: int) -> str:
        return CDP_REGISTRY.functions.owns(cdp).call()

    @staticmethod
    def _get_proxy(owner: str) -> str:
        return CROPPER.functions.proxy(owner).call()

    @unsync
    def get_vault(self, cdp: int) -> str:
        return self._get_proxy(self._get_owner(cdp))


def make_parser(ilk_type: MakerCollateral) -> MakerParser:
    """Parsers dispatch helper function"""

    if ilk_type is WSTETH:
        return WSTETHParser()

    if ilk_type is STECRV:
        return STECRVParser()

    raise ValueError("Unknows type of Maker collateral")
