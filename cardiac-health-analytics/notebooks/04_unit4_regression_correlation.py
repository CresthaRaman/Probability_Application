from src.cardiac_project.data_factory import make_cardiac_dataset
from src.cardiac_project.unit4_regression_correlation import (
    correlation_analysis,
    multiple_regression,
    simple_regression,
)


df = make_cardiac_dataset()

print("=== Correlation Analysis (Resting BP vs Cholesterol) ===")
for k, v in correlation_analysis(df).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Simple Regression (Cholesterol ~ Age) ===")
for k, v in simple_regression(df).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Multiple Regression (Cholesterol ~ Age + BP + BMI + Smoking) ===")
for k, v in multiple_regression(df).items():
    print(f"  {k}: {v:.6f}")
