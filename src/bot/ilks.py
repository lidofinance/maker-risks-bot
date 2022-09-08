"""Maker assets"""

# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod
from dataclasses import dataclass

from unsync import unsync
from web3.types import BlockIdentifier

from .eth import CDP_MANAGER, CDP_REGISTRY, CROPPER


@dataclass
class MakerIlk(ABC):
    """Maker collateral type abstraction"""

    ilk: str
    join: str
    key: str
    symbol: str
    created: int
    decimals: int

    @abstractmethod
    def get_urn_by_cdp(self, cdp: int, block: BlockIdentifier) -> str:
        """Retrieve urn by the given cdp"""


@dataclass
class GemJoinIlk(MakerIlk):
    """Collateral based on GemJoin contract"""

    @unsync
    def get_urn_by_cdp(self, cdp: int, block: BlockIdentifier) -> str:
        return CDP_MANAGER.functions.urns(cdp).call(block_identifier=block)


@dataclass
class CropJoinIlk(MakerIlk):
    """Collateral based on CropJoin contract"""

    @unsync
    def get_urn_by_cdp(self, cdp: int, block: BlockIdentifier) -> str:
        owner = CDP_REGISTRY.functions.owns(cdp).call(block_identifier=block)
        return CROPPER.functions.proxy(owner).call(block_identifier=block)


# Check via https://etherscan.io/address/0x5a464C28D19848f44199D003BeF5ecc87d090F87#readContract#F8
# List of keys at https://tracker-vaults.makerdao.network

WSTETH_A = GemJoinIlk(
    "0x5753544554482d41000000000000000000000000000000000000000000000000",
    "0x10CD5fbe1b404B7E19Ef964B63939907bdaf42E2",
    "WSTETH-A",
    "wstETH_A",
    13426395,
    18,
)
WSTETH_B = GemJoinIlk(
    "0x5753544554482d42000000000000000000000000000000000000000000000000",
    "0x248cCBf4864221fC0E840F29BB042ad5bFC89B5c",
    "WSTETH-B",
    "wstETH_B",
    14673262,
    18,
)
STECRV_A = CropJoinIlk(
    "0x435256563145544853544554482d410000000000000000000000000000000000",
    "0x82D8bfDB61404C796385f251654F6d7e92092b5D",
    "CRVV1ETHSTETH-A",
    "steCRV_A",
    14352592,
    18,
)
