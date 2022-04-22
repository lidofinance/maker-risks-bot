"""Module for parsing data from Anchor protocol contracts"""

from typing import Iterable

import pandas as pd
import requests
from unsync import unsync

from .config import FLIPSIDE_ENDPOINT
from .eth import CDP_MANAGER, VAT

# Check via https://etherscan.io/address/0x5a464C28D19848f44199D003BeF5ecc87d090F87
ILK_WSTETH = "0x5753544554482d41000000000000000000000000000000000000000000000000"

RAY_DECIMALS = 27
RAD_DECIMALS = 45
WAD_DECIMALS = 18


def get_cdps() -> Iterable[dict]:
    """Get the list of CDP:VAULT_ADDRESS.
    NB! It's subject to change!"""

    response = requests.get(FLIPSIDE_ENDPOINT, timeout=15)
    response.raise_for_status()
    return response.json()


def get_vat_stats() -> tuple[int, int, int, int, int]:
    """
    Get statistic about collateral type from Vault Engine.
    https://docs.makerdao.com/smart-contract-modules/core-module/vat-detailed-documentation#glossary-vat-vault-engine
    """

    return VAT.functions.ilks(ILK_WSTETH).call()


@unsync
def get_vault(cdp: int) -> str:
    """Get UrnHandler, i.e. vault by CDP"""

    return CDP_MANAGER.functions.urns(cdp).call()


@unsync
def get_vault_stat(vault: str) -> tuple[int, int]:
    """Get collateral and debt for the given vault"""

    return VAT.functions.urns(ILK_WSTETH, vault).call()


def parse() -> pd.DataFrame:
    """Parse required data"""

    df = pd.DataFrame(get_cdps())
    df.rename(columns={"ADDRESS": "address", "CDP": "cdp"}, inplace=True)
    df["cdp"] = pd.to_numeric(df["cdp"])  # contracts accept uint256 as and argument
    df.drop_duplicates(inplace=True)

    vaults, stats = [], []

    tasks = [(cdp, get_vault(cdp)) for cdp in df["cdp"]]
    for cdp, task in tasks:
        vat = task.result()  # type: ignore
        vaults.append(
            {
                "cdp": cdp,
                "vault": vat,
            }
        )

    tasks = [(item["cdp"], get_vault_stat(item["vault"])) for item in vaults]
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
