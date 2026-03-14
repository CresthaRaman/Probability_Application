from src.ps_project.data_factory import make_engineering_dataset
from src.ps_project.unit1_descriptive_probability import (
    categorical_probabilities,
    descriptive_summary,
    probability_laws_demo,
)


df = make_engineering_dataset(seed=42, n=300)

print("=== Descriptive Summary ===")
print(descriptive_summary(df))

print("\n=== Empirical Class Probabilities ===")
print(categorical_probabilities(df))

print("\n=== Probability Laws Demo ===")
print(probability_laws_demo())
