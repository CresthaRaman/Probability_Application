from src.ps_project.data_factory import make_engineering_dataset
from src.ps_project.unit4_regression_correlation import (
    correlation_analysis,
    multiple_regression,
    simple_regression,
)


df = make_engineering_dataset(seed=42, n=300)

print("=== Correlation Analysis ===")
print(correlation_analysis(df))

print("\n=== Simple Regression ===")
print(simple_regression(df))

print("\n=== Multiple Regression ===")
print(multiple_regression(df))
