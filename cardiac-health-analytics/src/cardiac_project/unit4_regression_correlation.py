from __future__ import annotations

from typing import Dict

import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm


def correlation_analysis(df: pd.DataFrame) -> Dict[str, float]:
    """Pearson correlation between resting BP and cholesterol."""
    corr, p = stats.pearsonr(df["resting_bp"], df["cholesterol"])
    return {"pearson_r": float(corr), "pearson_p": float(p)}


def simple_regression(df: pd.DataFrame) -> Dict[str, float]:
    """OLS: cholesterol predicted by age."""
    x = sm.add_constant(df[["age"]])
    model = sm.OLS(df["cholesterol"], x).fit()
    return {
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "coef_const": float(model.params["const"]),
        "coef_age": float(model.params["age"]),
    }


def multiple_regression(df: pd.DataFrame) -> Dict[str, float]:
    """OLS: cholesterol predicted by age, resting_bp, bmi, smoking_status."""
    predictors = ["age", "resting_bp", "bmi", "smoking_status"]
    x = sm.add_constant(df[predictors])
    model = sm.OLS(df["cholesterol"], x).fit()

    sst = float(((df["cholesterol"] - df["cholesterol"].mean()) ** 2).sum())
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
