"""The approximate price of the coin on last block"""

# pylint: disable=unused-argument,invalid-name,unused-import

from dataclasses import asdict, dataclass
import requests


@dataclass
class CoinGeckoPriceRequestParams:
    """Payload for request to /simple/price
    @see https://www.coingecko.com/en/api/documentation for details."""

    ids: str
    vs_currencies: str = "usd"
    include_market_cap: str = "false"
    include_24hr_vol: str = "false"
    include_24hr_change: str = "false"
    include_last_updated_at: str = "false"


def _crypto_to_usd(currency: str) -> float:
    payload = CoinGeckoPriceRequestParams(ids=currency)
    r = requests.get("https://api.coingecko.com/api/v3/simple/price", params=asdict(payload), timeout=5)
    r.raise_for_status()
    return r.json()[currency]["usd"]


def Wsteth_Last_Price() -> float:
    """Current price of wstETH"""

    return _crypto_to_usd("wrapped-steth")


def Eth_Last_Price() -> float:
    """Current price of ETH"""

    return _crypto_to_usd("ethereum")


def StETH_Last_Price() -> float:
    """Current price of stETH"""
    return _crypto_to_usd("staked-ether")
