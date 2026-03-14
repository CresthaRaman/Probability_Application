from src.ps_project.data_factory import make_engineering_dataset
from src.ps_project.unit5_quality_control import (
    p_chart_limits,
    six_sigma_metrics,
    xbar_r_chart_limits,
)


df = make_engineering_dataset(seed=42, n=300)

print("=== X-bar and R chart limits ===")
print(xbar_r_chart_limits(df["quality_score"], subgroup_size=5))

print("\n=== P-chart limits ===")
print(p_chart_limits(df["defect"], subgroup_size=10))

print("\n=== Six Sigma Metrics ===")
print(six_sigma_metrics(df))
