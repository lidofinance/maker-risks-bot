"""ETH Web3 connection"""

import json
import logging
import os
from functools import cache
from pathlib import Path

from web3 import HTTPProvider, Web3
from web3.contract import Contract

from .config import NODE_ENDPOINT
from .middleware import requests_cache

log = logging.getLogger(__name__)

ABI_HOME = Path(os.path.dirname(__file__), "abi")

# The list of deployed contracts is here:
# https://chainlog.makerdao.com/api/mainnet/active.json
VAT_ADDRESS = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B"


w3 = Web3(HTTPProvider(NODE_ENDPOINT))
w3.middleware_onion.add(requests_cache, "requests_cache")


@cache
def _contract(address: str, abi_file: os.PathLike) -> Contract:
    """Get Contract instance by the given address"""

    address = w3.toChecksumAddress(address)
    with open(abi_file, mode="r", encoding="utf-8") as file:
        abi = json.load(file)
        return w3.eth.contract(address=address, abi=abi)


VAT = _contract(VAT_ADDRESS, ABI_HOME / "vat-abi.json")
