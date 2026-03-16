from src.health_project.data_factory import make_health_dataset
from src.health_project.unit1_descriptive_probability import (
    categorical_probabilities,
    descriptive_summary,
    probability_laws_demo,
)


df = make_health_dataset()

print("=== Descriptive Summary ===")
print(descriptive_summary(df))

print("\n=== Empirical Diagnosis Probabilities ===")
print(categorical_probabilities(df))

print("\n=== Probability Laws Demo (Clinical Screening) ===")
for k, v in probability_laws_demo().items():
    print(f"  {k}: {v:.4f}")
