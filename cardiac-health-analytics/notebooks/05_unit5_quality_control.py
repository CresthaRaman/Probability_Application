from src.cardiac_project.data_factory import make_cardiac_dataset
from src.cardiac_project.unit5_quality_control import (
    p_chart_limits,
    six_sigma_metrics,
    xbar_r_chart_limits,
)


df = make_cardiac_dataset()

# Binary disease flag for p-chart
disease_flag = df["heart_disease"].astype(int)

print("=== X-bar and R chart limits (Resting Blood Pressure) ===")
for k, v in xbar_r_chart_limits(df["resting_bp"], subgroup_size=5).items():
    print(f"  {k}: {v:.6f}")

print("\n=== P-chart limits (Heart disease rate) ===")
for k, v in p_chart_limits(disease_flag, subgroup_size=10).items():
    print(f"  {k}: {v:.6f}")

print("\n=== Six Sigma Metrics ===")
for k, v in six_sigma_metrics(df).items():
    print(f"  {k}: {v:.4f}")
