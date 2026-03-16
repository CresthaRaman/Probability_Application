from src.health_project.data_factory import make_health_dataset
from src.health_project.unit4_regression_correlation import (
    correlation_analysis,
    multiple_regression,
    simple_regression,
)


df = make_health_dataset()

print("=== Correlation Analysis (Radius vs Texture) ===")
for k, v in correlation_analysis(df).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Simple Regression (Area ~ Radius) ===")
for k, v in simple_regression(df).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Multiple Regression (Area ~ Radius + Texture + Smoothness + Compactness) ===")
for k, v in multiple_regression(df).items():
    print(f"  {k}: {v:.6f}")
