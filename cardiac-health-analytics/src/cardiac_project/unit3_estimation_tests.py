from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd
from scipy import stats


def point_estimates(df: pd.DataFrame) -> Dict[str, float]:
    bp_sample = df["resting_bp"].to_numpy()
    return {
        "mean_resting_bp": float(np.mean(bp_sample)),
        "variance_resting_bp": float(np.var(bp_sample, ddof=1)),
        "proportion_disease": float(np.mean(df["heart_disease"] == 1)),
    }


def confidence_intervals(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, float]:
    x = df["resting_bp"].to_numpy()
    n = x.size
    mean = float(np.mean(x))
    s = float(np.std(x, ddof=1))

    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin = t_crit * s / np.sqrt(n)

    p_hat = float(np.mean(df["heart_disease"] == 1))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_margin = z_crit * np.sqrt((p_hat * (1 - p_hat)) / n)

    return {
        "bp_mean_ci_low": mean - margin,
        "bp_mean_ci_high": mean + margin,
        "prop_disease_ci_low": max(0.0, p_hat - p_margin),
        "prop_disease_ci_high": min(1.0, p_hat + p_margin),
    }


def hypothesis_tests(df: pd.DataFrame) -> Dict[str, float]:
    """Run parametric and non-parametric hypothesis tests on cardiac data."""
    bp = df["resting_bp"].to_numpy()

    # One-sample t-test: is population mean resting BP = 130?
    t_single = stats.ttest_1samp(bp, popmean=130.0)

    # Two-sample t-test: disease vs healthy resting BP
    group_d = df.loc[df["heart_disease"] == 1, "resting_bp"].to_numpy()
    group_h = df.loc[df["heart_disease"] == 0, "resting_bp"].to_numpy()
    t_two = stats.ttest_ind(group_d, group_h, equal_var=False)

    # Paired t-test: resting_bp vs estimated systolic from max_heart_rate
    est1 = df["resting_bp"].to_numpy()
    est2 = (220 - df["max_heart_rate"] + 60).to_numpy()  # rough proxy
    t_paired = stats.ttest_rel(est1, est2)

    # Kruskal-Wallis: cholesterol across smoking status groups
    groups_kw = [
        g["cholesterol"].to_numpy()
        for _, g in df.groupby("smoking_status", observed=True)
    ]
    h_stat, h_p = stats.kruskal(*groups_kw)

    # Chi-square test: label vs exercise_angina
    chi = pd.crosstab(df["exercise_angina"], df["label"])
    chi2_stat, chi2_p, _, _ = stats.chi2_contingency(chi)

    # Normality test on resting BP
    norm_test = stats.shapiro(bp[:500])  # shapiro limit

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
