"""Maker ILKs"""

from dataclasses import dataclass


@dataclass
class MakerCollateral:
    """Maker collateral type abstraction"""

    ilk: str
    symbol: str
    decimals: int


# Check via https://etherscan.io/address/0x5a464C28D19848f44199D003BeF5ecc87d090F87
WSTETH = MakerCollateral("0x5753544554482d41000000000000000000000000000000000000000000000000", "wstETH", 18)
STECRV = MakerCollateral("0x435256563145544853544554482d410000000000000000000000000000000000", "steCRV", 18)
