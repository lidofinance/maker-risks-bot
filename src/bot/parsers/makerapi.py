"""MakerDAO Data API based parser"""

import logging
from threading import Lock
from time import monotonic_ns
from typing import Iterable, Optional

import pandas as pd

from ..http import requests_get, requests_post
from ..ilks import MakerCollateral
from .base import BaseParser

API_BASE = "https://data-api.makerdao.network/v1"
API_QUERY_LIMIT = 100
TOKEN_REFRESH_INTERVAL = 45 * 60  # seconds

log = logging.getLogger(__name__)


class MakerAPIProvider:
    """Maker Data API provider"""

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

        self._lock = Lock()
        self._token: Optional[str] = None
        self._token_updated_at: Optional[int] = None

    def _auth(self) -> None:
        resp = requests_post(
            url=f"{API_BASE}/login/access-token",
            data={
                "username": self.username,
                "password": self.password,
            },
        )
        resp.raise_for_status()

        self._token = resp.json()["access_token"]
        self._token_updated_at = monotonic_ns()

        log.info("API token refreshed")

    @property
    def token(self) -> str:
        """Authorization token to Maker Data API"""

        with self._lock:
            # first time request for token
            if not self._token_updated_at:
                self._auth()
            else:
                # check for refresh requirements
                refresh_timestamp = self._token_updated_at + TOKEN_REFRESH_INTERVAL * 10**9
                if monotonic_ns() > refresh_timestamp:
                    log.info("API token expired, refreshing")
                    self._auth()

            # just to make sure
            if not self._token:
                raise RuntimeError("No token available")

        return self._token

    def get(self, url: str, **kwargs):
        """Make GET requests to Maker Data API"""

        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests_get(url=f"{API_BASE}{url}", headers=headers, **kwargs)
        resp.raise_for_status()
        return resp.json()


class MakerAPIParser(BaseParser):
    """Maker protocol parser based on Maker Data API"""

    def __init__(self, asset: MakerCollateral, api: MakerAPIProvider) -> None:
        super().__init__(asset)
        self._api = api

    def fetch_block(self) -> int:
        """Retrieve the id of the latest synchronised block"""

        req = self._api.get("/state/last_block")
        return req["last_block"]

    def get_urns(self) -> Iterable:
        """Get data from Maker Data API"""

        params = {
            "ilk": self.asset.key,
            "limit": API_QUERY_LIMIT,
            "skip": 0,
        }

        def _map_func(item: dict) -> dict:
            obj = {}
            for key in ("vault", "owner", "urn"):
                obj[key] = item[key]
            return obj

        out = []
        while req := self._api.get("/vaults/current_state", params=params):
            out.extend(_map_func(item) for item in req)
            params["skip"] += params["limit"]

        return out

    def parse(self) -> pd.DataFrame:
        self.block = self.fetch_block()
        log.info("fetching data for %s ilk from block %d", self.asset.symbol, self.block)

        df = pd.DataFrame(self.get_urns())
        df.drop_duplicates(inplace=True)

        stats = []
        tasks = [(item["urn"], self.get_vault_stat(item["urn"])) for _, item in df.iterrows()]
        for urn, task in tasks:
            ink, art = task.result()  # type: ignore
            stats.append(
                {
                    "urn": urn,
                    "ink": ink,
                    "art": art,
                }
            )

        df = df.merge(pd.DataFrame(stats), on="urn", how="left")
        return df
