from src.cardiac_project.data_factory import make_cardiac_dataset
from src.cardiac_project.unit1_descriptive_probability import (
    categorical_probabilities,
    descriptive_summary,
    probability_laws_demo,
)


df = make_cardiac_dataset()

print("=== Descriptive Summary ===")
print(descriptive_summary(df))

print("\n=== Empirical Heart Disease Probabilities ===")
print(categorical_probabilities(df))

print("\n=== Probability Laws Demo (Cardiac Screening) ===")
for k, v in probability_laws_demo().items():
    print(f"  {k}: {v:.4f}")
