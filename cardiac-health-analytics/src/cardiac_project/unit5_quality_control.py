from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


def subgroup_stats(values: pd.Series, subgroup_size: int = 5) -> pd.DataFrame:
    trimmed = values.iloc[: len(values) - (len(values) % subgroup_size)]
    groups = trimmed.to_numpy().reshape(-1, subgroup_size)

    means = groups.mean(axis=1)
    ranges = groups.max(axis=1) - groups.min(axis=1)

    return pd.DataFrame({"xbar": means, "range": ranges})


def xbar_r_chart_limits(values: pd.Series, subgroup_size: int = 5) -> Dict[str, float]:
    """X-bar and R chart control limits for a continuous measurement."""
    # Constants for n=5 subgroup size
    a2 = 0.577
    d3 = 0.0
    d4 = 2.115

    sg = subgroup_stats(values, subgroup_size=subgroup_size)
    xbar_bar = float(sg["xbar"].mean())
    r_bar = float(sg["range"].mean())

    return {
        "xbar_center": xbar_bar,
        "xbar_ucl": xbar_bar + a2 * r_bar,
        "xbar_lcl": xbar_bar - a2 * r_bar,
        "r_center": r_bar,
        "r_ucl": d4 * r_bar,
        "r_lcl": d3 * r_bar,
    }


def p_chart_limits(defect_series: pd.Series, subgroup_size: int = 10) -> Dict[str, float]:
    """P-chart limits treating heart disease diagnosis as the 'defect' event."""
    trimmed = defect_series.iloc[: len(defect_series) - (len(defect_series) % subgroup_size)]
    groups = trimmed.to_numpy().reshape(-1, subgroup_size)

    p_i = groups.mean(axis=1)
    p_bar = float(p_i.mean())
    se = np.sqrt((p_bar * (1 - p_bar)) / subgroup_size)

    return {
        "p_center": p_bar,
        "p_ucl": min(1.0, p_bar + 3 * se),
        "p_lcl": max(0.0, p_bar - 3 * se),
    }


def six_sigma_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """Six Sigma metrics treating heart disease as the non-conforming event."""
    disease_count = int((df["heart_disease"] == 1).sum())
    opportunities = int(len(df))
    dpmo = (disease_count / opportunities) * 1_000_000

    return {
        "disease_count": disease_count,
        "total_patients": opportunities,
        "DPMO": float(dpmo),
        "sigma_level_approx": float(6.0 - np.log10(max(dpmo, 1.0))),
    }
