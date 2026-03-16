from src.health_project.unit2_distributions_sampling import (
    distribution_probabilities,
    expectation_variance,
    random_variable_examples,
    sampling_distribution_clt,
)

rv = random_variable_examples(seed=42)

print("=== Expectation and Variance: Discrete (Malignant counts in biopsies) ===")
print(expectation_variance(rv["discrete"]))

print("\n=== Expectation and Variance: Continuous (Tumor radius) ===")
print(expectation_variance(rv["continuous"]))

print("\n=== Distribution Probabilities ===")
for k, v in distribution_probabilities().items():
    print(f"  {k}: {v:.6f}")

print("\n=== Sampling Distribution / CLT ===")
for k, v in sampling_distribution_clt().items():
    print(f"  {k}: {v:.6f}")
