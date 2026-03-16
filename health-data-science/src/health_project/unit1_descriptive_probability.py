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
    in a clinical screening context.

    Scenario
    --------
    * P(Malignant) = 0.37  (base rate in dataset ≈ 212/569)
    * P(PositiveTest) = 0.42
    * P(Positive AND Malignant) = 0.34
    """
    p_m = 0.37
    p_pos = 0.42
    p_m_and_pos = 0.34

    p_m_or_pos = p_m + p_pos - p_m_and_pos          # Additive law
    p_m_given_pos = p_m_and_pos / p_pos              # Conditional
    p_pos_given_m = p_m_and_pos / p_m                # Conditional

    # Bayes: P(M|Pos) = P(Pos|M) * P(M) / P(Pos)
    bayes_p_m_given_pos = p_pos_given_m * p_m / p_pos

    return {
        "P(Malignant)": p_m,
        "P(Positive)": p_pos,
        "P(M and Pos)": p_m_and_pos,
        "P(M or Pos)": p_m_or_pos,
        "P(M|Pos)": p_m_given_pos,
        "P(Pos|M)": p_pos_given_m,
        "Bayes_P(M|Pos)": bayes_p_m_given_pos,
    }


def categorical_probabilities(df: pd.DataFrame) -> pd.Series:
    """Empirical probabilities for diagnosis labels."""
    return df["label"].value_counts(normalize=True)
