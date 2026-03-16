from __future__ import annotations

import pandas as pd
from sklearn.datasets import load_breast_cancer


def make_health_dataset() -> pd.DataFrame:
    """Load Wisconsin Breast Cancer dataset and return a tidy DataFrame.

    Columns include all 30 numeric features plus:
      - ``diagnosis``: 0 = malignant, 1 = benign  (original sklearn target)
      - ``label``: human-readable string ('Malignant' / 'Benign')
    """
    bunch = load_breast_cancer()
    df = pd.DataFrame(bunch.data, columns=bunch.feature_names)
    df["diagnosis"] = bunch.target  # 0 malignant, 1 benign
    df["label"] = df["diagnosis"].map({0: "Malignant", 1: "Benign"})
    return df


def save_dataset(df: pd.DataFrame, out_csv: str) -> None:
    df.to_csv(out_csv, index=False)
