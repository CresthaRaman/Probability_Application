from src.health_project.data_factory import make_health_dataset
from src.health_project.unit5_quality_control import (
    p_chart_limits,
    six_sigma_metrics,
    xbar_r_chart_limits,
)


df = make_health_dataset()

# For quality control, use 'malignant' as the binary flag (1 = malignant, 0 = benign)
malignant_flag = (df["diagnosis"] == 0).astype(int)

print("=== X-bar and R chart limits (Mean Radius) ===")
for k, v in xbar_r_chart_limits(df["mean radius"], subgroup_size=5).items():
    print(f"  {k}: {v:.6f}")

print("\n=== P-chart limits (Malignant rate) ===")
for k, v in p_chart_limits(malignant_flag, subgroup_size=10).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Six Sigma Metrics ===")
for k, v in six_sigma_metrics(df).items():
    print(f"  {k}: {v:.4f}")
