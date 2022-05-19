"""Maker assets"""

from dataclasses import dataclass


@dataclass
class MakerCollateral:
    """Maker collateral type abstraction"""

    ilk: str
    key: str
    symbol: str
    decimals: int


# Check via https://etherscan.io/address/0x5a464C28D19848f44199D003BeF5ecc87d090F87
# List of keys at https://tracker-vaults.makerdao.network

WSTETH_A = MakerCollateral(
    "0x5753544554482d41000000000000000000000000000000000000000000000000",
    "WSTETH-A",
    "wstETH_A",
    18,
)
WSTETH_B = MakerCollateral(
    "0x5753544554482d42000000000000000000000000000000000000000000000000",
    "WSTETH-B",
    "wstETH_B",
    18,
)
STECRV_A = MakerCollateral(
    "0x435256563145544853544554482d410000000000000000000000000000000000",
    "CRVV1ETHSTETH-A",
    "steCRV_A",
    18,
)
