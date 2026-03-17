from src.cardiac_project.data_factory import make_cardiac_dataset
from src.cardiac_project.unit3_estimation_tests import (
    confidence_intervals,
    hypothesis_tests,
    point_estimates,
)


df = make_cardiac_dataset()

print("=== Point Estimates ===")
for k, v in point_estimates(df).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Confidence Intervals ===")
for k, v in confidence_intervals(df).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Hypothesis Tests ===")
for k, v in hypothesis_tests(df).items():
    print(f"  {k}: {v:.6f}")
