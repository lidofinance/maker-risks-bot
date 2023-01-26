"""ETH Web3 connection"""

import json
import logging
import os
from functools import cache
from pathlib import Path

from web3 import HTTPProvider, Web3
from web3.contract import Contract

from .config import FALLBACK_NODE_ENDPOINT, NODE_ENDPOINT
from .middleware import chain_id_mock, construct_fallback_provider_middleware, metrics_collector, retryable

log = logging.getLogger(__name__)

ABI_HOME = Path(os.path.dirname(__file__), "abi")

# The list of deployed contracts is here:
# https://chainlog.makerdao.com/api/mainnet/active.json
CDP_REGISTRY_ADDRESS = "0xBe0274664Ca7A68d6b5dF826FB3CcB7c620bADF3"
CDP_MANAGER_ADDRESS = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
CROPPER_ADDRESS = "0x8377CD01a5834a6EaD3b7efb482f678f2092b77e"
VAT_ADDRESS = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B"


w3 = Web3(HTTPProvider(NODE_ENDPOINT))
w3.middleware_onion.add(metrics_collector)
w3.middleware_onion.add(retryable)
if FALLBACK_NODE_ENDPOINT:
    w3.middleware_onion.add(construct_fallback_provider_middleware(w3, FALLBACK_NODE_ENDPOINT))
w3.middleware_onion.add(chain_id_mock)


@cache
def _contract(address: str, abi_file: os.PathLike) -> Contract:
    """Get Contract instance by the given address"""

    address = w3.toChecksumAddress(address)
    with open(abi_file, mode="r", encoding="utf-8") as file:
        abi = json.load(file)
        return w3.eth.contract(address=address, abi=abi)


CDP_REGISTRY = _contract(CDP_REGISTRY_ADDRESS, ABI_HOME / "cdp-registry-abi.json")
CDP_MANAGER = _contract(CDP_MANAGER_ADDRESS, ABI_HOME / "cdp-manager-abi.json")
CROPPER = _contract(CROPPER_ADDRESS, ABI_HOME / "cropper-abi.json")
VAT = _contract(VAT_ADDRESS, ABI_HOME / "vat-abi.json")
