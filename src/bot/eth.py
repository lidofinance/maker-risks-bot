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
CDP_MANAGER_ADDRESS = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
CDP_REGISTRY_ADDRESS = "0xBe0274664Ca7A68d6b5dF826FB3CcB7c620bADF3"
CROPPER_ADDRESS = "0x8377CD01a5834a6EaD3b7efb482f678f2092b77e"
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


# https://docs.makerdao.com/smart-contract-modules/proxy-module/cdp-manager-detailed-documentation
CDP_MANAGER = _contract(CDP_MANAGER_ADDRESS, ABI_HOME / "cdp-manager-abi.json")
# TODO: find any description
CDP_REGISTRY = _contract(CDP_REGISTRY_ADDRESS, ABI_HOME / "cdp-registry-abi.json")
# TODO: find any description
CROPPER = _contract(CROPPER_ADDRESS, ABI_HOME / "cropper-abi.json")
# https://docs.makerdao.com/smart-contract-modules/core-module/vat-detailed-documentation
VAT = _contract(VAT_ADDRESS, ABI_HOME / "vat-abi.json")
