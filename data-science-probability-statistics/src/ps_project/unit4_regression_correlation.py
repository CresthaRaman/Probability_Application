from __future__ import annotations

from typing import Dict

import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm


def correlation_analysis(df: pd.DataFrame) -> Dict[str, float]:
    corr, p = stats.pearsonr(df["temperature"], df["quality_score"])
    return {"pearson_r": float(corr), "pearson_p": float(p)}


def simple_regression(df: pd.DataFrame) -> Dict[str, float]:
    x = sm.add_constant(df[["temperature"]])
    model = sm.OLS(df["quality_score"], x).fit()
    return {
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "coef_const": float(model.params["const"]),
        "coef_temperature": float(model.params["temperature"]),
    }


def multiple_regression(df: pd.DataFrame) -> Dict[str, float]:
    x = sm.add_constant(df[["temperature", "pressure", "humidity", "operator_skill"]])
    model = sm.OLS(df["quality_score"], x).fit()

    # Explained and unexplained variations for interpretation.
    sst = float(((df["quality_score"] - df["quality_score"].mean()) ** 2).sum())
    sse = float((model.resid**2).sum())
    ssr = sst - sse

    return {
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_stat": float(model.fvalue),
        "f_pvalue": float(model.f_pvalue),
        "SST": sst,
        "SSR_explained": ssr,
        "SSE_unexplained": sse,
    }
