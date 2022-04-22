"""Analytics methods"""

from contextlib import suppress
from typing import List

import pandas as pd

from .makerparser import RAY_DECIMALS, get_vat_stats

RISK_LABELS = ["A", "B+", "B", "B-", "C", "D", "liquidation"]
RISK_VALUES = [2.50, 1.75, 1.50, 1.25, 1.10, 1.00]

DECIMALS_WSTETH = 18


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw data received"""

    df = df.copy()

    df["ink"] = df["ink"] / pow(10, DECIMALS_WSTETH)
    df["art"] = df["art"] / pow(10, DECIMALS_WSTETH)
    df.rename(columns={"art": "debt", "ink": "collateral"}, inplace=True)

    df.fillna(0, inplace=True)
    # df = pd.DataFrame(data=df.query("collateral > 0 and debt > 0"))

    # rate => stablecoin debt multiplier (e.g. 1.015)
    # spot => maximum stablecoin allowed per unit of collateral (e.g. 1889.2)
    (_, rate, spot, _, _) = get_vat_stats()
    rate = rate / pow(10, RAY_DECIMALS)
    spot = spot / pow(10, RAY_DECIMALS)

    df["healthf"] = df["collateral"] * spot / (df["debt"] * rate)

    return df


def get_risks(df: pd.DataFrame, ratio_list: List[float]) -> pd.DataFrame:
    """
    This function calculates the risk level for each position
    and returns the positions sorted by risk
    """

    df = df.copy()

    df["risk_rating"] = [
        (x > ratio_list[0] and "A")
        or (ratio_list[1] < x <= ratio_list[0] and "B+")
        or (ratio_list[2] < x <= ratio_list[1] and "B")
        or (ratio_list[3] < x <= ratio_list[2] and "B-")
        or (ratio_list[4] < x <= ratio_list[3] and "C")
        or (ratio_list[5] < x <= ratio_list[4] and "D")
        or (ratio_list[5] <= x and "liquidation")
        for x in df["healthf"]
    ]

    df.sort_values(by="healthf", ascending=False, inplace=True)

    return df


def get_distr(data) -> pd.DataFrame:
    """This function calculates and returns a pivot table by risk levels"""

    risk_distr = data.pivot_table(index="risk_rating", values=["collateral"], aggfunc=["sum", "count"])
    risk_distr.columns = ["wstETH", "cnt"]
    risk_distr["percent"] = (risk_distr["wstETH"] / risk_distr["wstETH"].sum()) * 100

    return risk_distr


def calculate_values(data: pd.DataFrame) -> dict[str, float]:
    """Calculate risk distribution.
    Almost as is from related jupyter notebook."""

    df = prepare_data(data)

    df = get_risks(df, RISK_VALUES)
    risk_distr = get_distr(df)

    values = {}
    for label in RISK_LABELS:
        value: float = 0
        with suppress(KeyError):
            value = risk_distr.at[label, "percent"]
        values[label] = value

    return values
