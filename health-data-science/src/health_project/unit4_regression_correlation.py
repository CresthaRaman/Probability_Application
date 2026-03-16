from __future__ import annotations

from typing import Dict

import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm


def correlation_analysis(df: pd.DataFrame) -> Dict[str, float]:
    """Pearson correlation between mean radius and mean texture."""
    corr, p = stats.pearsonr(df["mean radius"], df["mean texture"])
    return {"pearson_r": float(corr), "pearson_p": float(p)}


def simple_regression(df: pd.DataFrame) -> Dict[str, float]:
    """OLS: mean area predicted by mean radius."""
    x = sm.add_constant(df[["mean radius"]])
    model = sm.OLS(df["mean area"], x).fit()
    return {
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "coef_const": float(model.params["const"]),
        "coef_mean_radius": float(model.params["mean radius"]),
    }


def multiple_regression(df: pd.DataFrame) -> Dict[str, float]:
    """OLS: mean area predicted by radius, texture, smoothness, compactness."""
    predictors = ["mean radius", "mean texture", "mean smoothness", "mean compactness"]
    x = sm.add_constant(df[predictors])
    model = sm.OLS(df["mean area"], x).fit()

    sst = float(((df["mean area"] - df["mean area"].mean()) ** 2).sum())
    sse = float((model.resid ** 2).sum())
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
