from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


def descriptive_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Central tendency & variation for numeric columns."""
    numeric = df.select_dtypes(include=[np.number])
    out = pd.DataFrame(
        {
            "mean": numeric.mean(),
            "median": numeric.median(),
            "mode": numeric.mode().iloc[0],
            "variance": numeric.var(ddof=1),
            "std_dev": numeric.std(ddof=1),
            "min": numeric.min(),
            "max": numeric.max(),
        }
    )
    return out


def probability_laws_demo() -> Dict[str, float]:
    """Demonstrate additive, multiplicative, conditional probability & Bayes theorem
    in a cardiac screening context.

    Scenario
    --------
    * P(HeartDisease) = 0.40  (base rate in synthetic dataset)
    * P(HighBP)      = 0.35
    * P(HighBP AND HeartDisease) = 0.22
    """
    p_hd = 0.40
    p_hbp = 0.35
    p_hd_and_hbp = 0.22

    p_hd_or_hbp = p_hd + p_hbp - p_hd_and_hbp           # Additive law
    p_hd_given_hbp = p_hd_and_hbp / p_hbp                # Conditional
    p_hbp_given_hd = p_hd_and_hbp / p_hd                 # Conditional

    # Bayes: P(HD|HighBP) = P(HighBP|HD) * P(HD) / P(HighBP)
    bayes_p_hd_given_hbp = p_hbp_given_hd * p_hd / p_hbp

    return {
        "P(HeartDisease)": p_hd,
        "P(HighBP)": p_hbp,
        "P(HD and HighBP)": p_hd_and_hbp,
        "P(HD or HighBP)": p_hd_or_hbp,
        "P(HD|HighBP)": p_hd_given_hbp,
        "P(HighBP|HD)": p_hbp_given_hd,
        "Bayes_P(HD|HighBP)": bayes_p_hd_given_hbp,
    }


def categorical_probabilities(df: pd.DataFrame) -> pd.Series:
    """Empirical probabilities for heart disease labels."""
    return df["label"].value_counts(normalize=True)
