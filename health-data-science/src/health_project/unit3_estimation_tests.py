from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd
from scipy import stats


def point_estimates(df: pd.DataFrame) -> Dict[str, float]:
    sample = df["mean radius"].to_numpy()
    return {
        "mean_radius": float(np.mean(sample)),
        "variance_radius": float(np.var(sample, ddof=1)),
        "proportion_malignant": float(np.mean(df["diagnosis"] == 0)),
    }


def confidence_intervals(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, float]:
    x = df["mean radius"].to_numpy()
    n = x.size
    mean = float(np.mean(x))
    s = float(np.std(x, ddof=1))

    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin = t_crit * s / np.sqrt(n)

    p_hat = float(np.mean(df["diagnosis"] == 0))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_margin = z_crit * np.sqrt((p_hat * (1 - p_hat)) / n)

    return {
        "mean_ci_low": mean - margin,
        "mean_ci_high": mean + margin,
        "prop_malignant_ci_low": max(0.0, p_hat - p_margin),
        "prop_malignant_ci_high": min(1.0, p_hat + p_margin),
    }


def hypothesis_tests(df: pd.DataFrame) -> Dict[str, float]:
    """Run parametric and non-parametric hypothesis tests on tumor data."""
    radius = df["mean radius"].to_numpy()

    # One-sample t-test: is population mean radius = 14?
    t_single = stats.ttest_1samp(radius, popmean=14.0)

    # Two-sample t-test: malignant vs benign mean radius
    group_m = df.loc[df["diagnosis"] == 0, "mean radius"].to_numpy()
    group_b = df.loc[df["diagnosis"] == 1, "mean radius"].to_numpy()
    t_two = stats.ttest_ind(group_m, group_b, equal_var=False)

    # Paired t-test: mean radius vs mean perimeter / pi  (two estimates of diameter)
    est1 = df["mean radius"].to_numpy()
    est2 = (df["mean perimeter"] / np.pi).to_numpy()
    t_paired = stats.ttest_rel(est1, est2)

    # Kruskal-Wallis across texture quartile groups
    texture_q = pd.qcut(df["mean texture"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    groups_kw = [g["mean radius"].to_numpy() for _, g in df.groupby(texture_q, observed=True)]
    h_stat, h_p = stats.kruskal(*groups_kw)

    # Chi-square test: label vs smoothness category
    smooth_cat = pd.qcut(df["mean smoothness"], q=3, labels=["Low", "Med", "High"])
    chi = pd.crosstab(smooth_cat, df["label"])
    chi2_stat, chi2_p, _, _ = stats.chi2_contingency(chi)

    # Normality test on mean radius
    norm_test = stats.shapiro(radius)

    return {
        "t_single_stat": float(t_single.statistic),
        "t_single_p": float(t_single.pvalue),
        "t_two_stat": float(t_two.statistic),
        "t_two_p": float(t_two.pvalue),
        "paired_t_stat": float(t_paired.statistic),
        "paired_t_p": float(t_paired.pvalue),
        "kruskal_h_stat": float(h_stat),
        "kruskal_h_p": float(h_p),
        "chi_square_stat": float(chi2_stat),
        "chi_square_p": float(chi2_p),
        "shapiro_stat": float(norm_test.statistic),
        "shapiro_p": float(norm_test.pvalue),
    }
