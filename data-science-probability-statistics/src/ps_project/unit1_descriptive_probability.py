from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


def descriptive_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Measure central tendency and variation for numeric columns."""
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
    """Demonstrate additive, multiplicative, conditional probability and Bayes theorem."""
    p_a = 0.40
    p_b = 0.30
    p_a_and_b = 0.12

    p_a_or_b = p_a + p_b - p_a_and_b
    p_a_given_b = p_a_and_b / p_b
    p_b_given_a = p_a_and_b / p_a

    # Bayes: P(B|A) = P(A|B)P(B) / P(A)
    bayes_p_b_given_a = p_a_given_b * p_b / p_a

    return {
        "P(A)": p_a,
        "P(B)": p_b,
        "P(A and B)": p_a_and_b,
        "P(A or B)": p_a_or_b,
        "P(A|B)": p_a_given_b,
        "P(B|A)": p_b_given_a,
        "Bayes_P(B|A)": bayes_p_b_given_a,
    }


def categorical_probabilities(df: pd.DataFrame) -> pd.Series:
    """Empirical probabilities for process status classes."""
    return df["status"].value_counts(normalize=True)
