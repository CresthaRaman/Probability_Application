from src.ps_project.data_factory import make_engineering_dataset
from src.ps_project.unit3_estimation_tests import (
    confidence_intervals,
    hypothesis_tests,
    point_estimates,
)


df = make_engineering_dataset(seed=42, n=300)

print("=== Point Estimates ===")
print(point_estimates(df))

print("\n=== Confidence Intervals ===")
print(confidence_intervals(df))

print("\n=== Hypothesis Tests ===")
print(hypothesis_tests(df))
