from __future__ import annotations

import numpy as np
import pandas as pd


def make_engineering_dataset(seed: int = 42, n: int = 300) -> pd.DataFrame:
    """Create a synthetic engineering process dataset for all analyses."""
    rng = np.random.default_rng(seed)

    temperature = rng.normal(72.0, 4.5, size=n)
    pressure = rng.normal(30.0, 2.0, size=n)
    humidity = rng.uniform(35.0, 80.0, size=n)
    operator_skill = rng.choice([1, 2, 3], p=[0.2, 0.5, 0.3], size=n)
    shifts = rng.choice(["A", "B", "C"], p=[0.4, 0.35, 0.25], size=n)

    # Process quality score with signal plus noise.
    quality_score = (
        100
        - 0.35 * (temperature - 72.0) ** 2
        - 0.8 * np.abs(pressure - 30.0)
        - 0.05 * humidity
        + 2.5 * operator_skill
        + rng.normal(0.0, 2.5, size=n)
    )

    defect_prob = 1.0 / (1.0 + np.exp((quality_score - 78.0) / 2.8))
    defects = rng.binomial(1, np.clip(defect_prob, 0.02, 0.95))

    category = np.where(defects == 1, "Defect", "OK")

    return pd.DataFrame(
        {
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "operator_skill": operator_skill,
            "shift": shifts,
            "quality_score": quality_score,
            "defect": defects,
            "status": category,
        }
    )


def save_dataset(df: pd.DataFrame, out_csv: str) -> None:
    df.to_csv(out_csv, index=False)
