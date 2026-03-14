from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd
from scipy import stats


def point_estimates(df: pd.DataFrame) -> Dict[str, float]:
    sample = df["quality_score"].to_numpy()
    return {
        "mean": float(np.mean(sample)),
        "variance": float(np.var(sample, ddof=1)),
        "proportion_defect": float(np.mean(df["defect"])),
    }


def confidence_intervals(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, float]:
    x = df["quality_score"].to_numpy()
    n = x.size
    mean = float(np.mean(x))
    s = float(np.std(x, ddof=1))

    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    margin = t_crit * s / np.sqrt(n)

    p_hat = float(np.mean(df["defect"]))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_margin = z_crit * np.sqrt((p_hat * (1 - p_hat)) / n)

    return {
        "mean_ci_low": mean - margin,
        "mean_ci_high": mean + margin,
        "prop_ci_low": max(0.0, p_hat - p_margin),
        "prop_ci_high": min(1.0, p_hat + p_margin),
    }


def hypothesis_tests(df: pd.DataFrame) -> Dict[str, float]:
    """Run parametric and non-parametric hypothesis tests."""
    x = df["quality_score"].to_numpy()

    t_single = stats.ttest_1samp(x, popmean=80.0)

    group_a = df.loc[df["shift"] == "A", "quality_score"].to_numpy()
    group_b = df.loc[df["shift"] == "B", "quality_score"].to_numpy()
    t_two = stats.ttest_ind(group_a, group_b, equal_var=False)

    # Paired t-test using pre/post synthetic adjustment.
    pre = x[:120]
    post = pre + np.random.default_rng(42).normal(0.6, 1.2, size=pre.shape[0])
    t_paired = stats.ttest_rel(post, pre)

    h_stat, h_p = stats.kruskal(
        df.loc[df["shift"] == "A", "quality_score"],
        df.loc[df["shift"] == "B", "quality_score"],
        df.loc[df["shift"] == "C", "quality_score"],
    )

    chi = pd.crosstab(df["shift"], df["status"])
    chi2_stat, chi2_p, _, _ = stats.chi2_contingency(chi)

    norm_test = stats.shapiro(x[:500] if len(x) > 500 else x)

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
