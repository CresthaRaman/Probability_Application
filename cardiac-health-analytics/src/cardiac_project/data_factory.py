from __future__ import annotations

import numpy as np
import pandas as pd


def make_cardiac_dataset(n: int = 600, seed: int = 42) -> pd.DataFrame:

    rng = np.random.default_rng(seed)

    age = rng.integers(29, 78, size=n).astype(float)
    sex = rng.choice([0, 1], size=n, p=[0.35, 0.65]).astype(int)

    # Resting blood pressure (mmHg) – influenced by age
    resting_bp = rng.normal(loc=125 + 0.3 * (age - 50), scale=15, size=n)
    resting_bp = np.clip(resting_bp, 90, 200).round(1)

    # Cholesterol (mg/dL)
    cholesterol = rng.normal(loc=220 + 0.5 * (age - 50), scale=40, size=n)
    cholesterol = np.clip(cholesterol, 120, 400).round(1)

    # Fasting blood sugar (mg/dL)
    fasting_blood_sugar = rng.normal(loc=100 + 0.2 * (age - 50), scale=20, size=n)
    fasting_blood_sugar = np.clip(fasting_blood_sugar, 60, 250).round(1)

    # Max heart rate (bpm) – inversely related to age
    max_heart_rate = rng.normal(loc=180 - 0.8 * age, scale=15, size=n)
    max_heart_rate = np.clip(max_heart_rate, 70, 210).round(1)

    # Exercise-induced angina (binary)
    angina_prob = 0.15 + 0.005 * (age - 40)
    exercise_angina = rng.binomial(1, np.clip(angina_prob, 0.05, 0.60), size=n)

    # ST depression (oldpeak)
    oldpeak = rng.exponential(scale=1.0, size=n)
    oldpeak = np.clip(oldpeak, 0, 6.0).round(2)

    # BMI
    bmi = rng.normal(loc=27.5, scale=5.0, size=n)
    bmi = np.clip(bmi, 16, 50).round(1)

    # Smoking status: 0=never, 1=former, 2=current
    smoking_status = rng.choice([0, 1, 2], size=n, p=[0.45, 0.30, 0.25])

    # --- Target: heart_disease (logistic model) ---
    logit = (
        -6.0
        + 0.05 * age
        + 0.4 * sex
        + 0.02 * (resting_bp - 120)
        + 0.008 * (cholesterol - 200)
        + 0.5 * exercise_angina
        + 0.3 * oldpeak
        + 0.03 * (bmi - 25)
        + 0.25 * (smoking_status == 2).astype(float)
    )
    prob_disease = 1.0 / (1.0 + np.exp(-logit))
    heart_disease = rng.binomial(1, prob_disease)

    df = pd.DataFrame(
        {
            "age": age,
            "sex": sex,
            "resting_bp": resting_bp,
            "cholesterol": cholesterol,
            "fasting_blood_sugar": fasting_blood_sugar,
            "max_heart_rate": max_heart_rate,
            "exercise_angina": exercise_angina,
            "oldpeak": oldpeak,
            "bmi": bmi,
            "smoking_status": smoking_status,
            "heart_disease": heart_disease,
        }
    )
    df["label"] = df["heart_disease"].map({0: "Healthy", 1: "Disease"})
    return df


def save_dataset(df: pd.DataFrame, out_csv: str) -> None:
    df.to_csv(out_csv, index=False)
