"""ETH Web3 connection"""

import json
import logging
import os
from functools import cache
from pathlib import Path

from web3 import HTTPProvider, Web3
from web3.contract import Contract
from web3_multi_provider import MultiProvider

from .config import FALLBACK_NODE_ENDPOINT, NODE_ENDPOINT
from .consts import CDP_MANAGER_ADDRESS, CDP_REGISTRY_ADDRESS, CROPPER_ADDRESS, VAT_ADDRESS
from .middleware import chain_id_mock, metered_rpc_request, retryable

log = logging.getLogger(__name__)

ABI_HOME = Path(os.path.dirname(__file__), "abi")

# we cannot use middleware here, because MultiHTTPProvider's make_request is short circuited
# to itself and makes metering from middleware useless: one call produces at up to N calls
# to the underlying providers, where N is the number of fallbacks
HTTPProvider.make_request = metered_rpc_request(HTTPProvider.make_request)

if FALLBACK_NODE_ENDPOINT:
    provider = MultiProvider(
        [
            NODE_ENDPOINT,
            FALLBACK_NODE_ENDPOINT,
        ]
    )
else:
    # use an usual provider instead of MultiProvider to be able to switch seamlessly in case of errors
    provider = HTTPProvider(NODE_ENDPOINT)

w3 = Web3(provider)
w3.middleware_onion.add(retryable)
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
