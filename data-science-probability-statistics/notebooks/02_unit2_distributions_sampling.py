from src.ps_project.unit2_distributions_sampling import (
    distribution_probabilities,
    expectation_variance,
    random_variable_examples,
    sampling_distribution_clt,
)

rv = random_variable_examples(seed=42)

print("=== Expectation and Variance: Discrete ===")
print(expectation_variance(rv["discrete"]))

print("\n=== Expectation and Variance: Continuous ===")
print(expectation_variance(rv["continuous"]))

print("\n=== Distribution Probabilities ===")
print(distribution_probabilities())

print("\n=== Sampling Distribution / CLT ===")
print(sampling_distribution_clt())
