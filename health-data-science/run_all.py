from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.health_project.data_factory import make_health_dataset, save_dataset
from src.health_project.unit1_descriptive_probability import (
    categorical_probabilities,
    descriptive_summary,
    probability_laws_demo,
)
from src.health_project.unit2_distributions_sampling import (
    distribution_probabilities,
    expectation_variance,
    random_variable_examples,
    sampling_distribution_clt,
)
from src.health_project.unit3_estimation_tests import (
    confidence_intervals,
    hypothesis_tests,
    point_estimates,
)
from src.health_project.unit4_regression_correlation import (
    correlation_analysis,
    multiple_regression,
    simple_regression,
)
from src.health_project.unit5_quality_control import (
    p_chart_limits,
    six_sigma_metrics,
    xbar_r_chart_limits,
)


def main() -> None:
    root = Path(__file__).resolve().parent
    data_dir = root / "data"
    reports_dir = root / "reports"
    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    # --- Load dataset ---
    df = make_health_dataset()
    save_dataset(df, str(data_dir / "breast_cancer.csv"))

    # Binary malignant flag for p-chart (1 = malignant)
    malignant_flag = (df["diagnosis"] == 0).astype(int)

    # --- Collect all unit results ---
    rv = random_variable_examples()
    unit_results = {
        "Unit1_Descriptive": descriptive_summary(df),
        "Unit1_Empirical_Prob": categorical_probabilities(df).to_frame("probability"),
        "Unit1_Probability_Laws": pd.DataFrame([probability_laws_demo()]),
        "Unit2_Expect_Discrete": pd.DataFrame([expectation_variance(rv["discrete"])]),
        "Unit2_Expect_Continuous": pd.DataFrame([expectation_variance(rv["continuous"])]),
        "Unit2_Dist_Probs": pd.DataFrame([distribution_probabilities()]),
        "Unit2_CLT": pd.DataFrame([sampling_distribution_clt()]),
        "Unit3_Point_Estimates": pd.DataFrame([point_estimates(df)]),
        "Unit3_Confidence_Intervals": pd.DataFrame([confidence_intervals(df)]),
        "Unit3_Hypothesis_Tests": pd.DataFrame([hypothesis_tests(df)]),
        "Unit4_Correlation": pd.DataFrame([correlation_analysis(df)]),
        "Unit4_Simple_Regression": pd.DataFrame([simple_regression(df)]),
        "Unit4_Multiple_Regression": pd.DataFrame([multiple_regression(df)]),
        "Unit5_Xbar_R": pd.DataFrame([xbar_r_chart_limits(df["mean radius"])]),
        "Unit5_P_Chart": pd.DataFrame([p_chart_limits(malignant_flag)]),
        "Unit5_Six_Sigma": pd.DataFrame([six_sigma_metrics(df)]),
    }

    # --- Write Excel workbook ---
    with pd.ExcelWriter(reports_dir / "analysis_outputs.xlsx", engine="openpyxl") as writer:
        for name, table in unit_results.items():
            table.to_excel(writer, sheet_name=name[:31], index=True)

    # --- Visualisations ---
    sns.set_theme(style="whitegrid")

    # 1. Histogram of mean radius by diagnosis
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="mean radius", hue="label", kde=True, bins=30)
    plt.title("Distribution of Mean Radius by Diagnosis")
    plt.tight_layout()
    plt.savefig(reports_dir / "hist_mean_radius.png", dpi=150)
    plt.close()

    # 2. Box plots for key tumor features
    features = ["mean radius", "mean texture", "mean smoothness", "mean compactness"]
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df[features])
    plt.title("Box Plots of Key Tumor Features")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(reports_dir / "box_tumor_features.png", dpi=150)
    plt.close()

    # 3. Scatter: radius vs area coloured by diagnosis
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="mean radius", y="mean area", hue="label", alpha=0.7)
    plt.title("Mean Radius vs Mean Area by Diagnosis")
    plt.tight_layout()
    plt.savefig(reports_dir / "scatter_radius_area.png", dpi=150)
    plt.close()

    # 4. Correlation heatmap (top 10 features)
    top_feat = [
        "mean radius", "mean texture", "mean perimeter", "mean area",
        "mean smoothness", "mean compactness", "mean concavity",
        "mean concave points", "mean symmetry", "mean fractal dimension",
    ]
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[top_feat].corr(), annot=True, fmt=".2f", cmap="RdBu_r")
    plt.title("Correlation Heatmap – Mean Tumor Features")
    plt.tight_layout()
    plt.savefig(reports_dir / "heatmap_correlations.png", dpi=150)
    plt.close()

    # 5. Count plot of diagnosis
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="label", hue="label", palette="Set2", legend=False)
    plt.title("Diagnosis Distribution")
    plt.tight_layout()
    plt.savefig(reports_dir / "countplot_diagnosis.png", dpi=150)
    plt.close()

    print(f"Saved dataset  : {data_dir / 'breast_cancer.csv'}")
    print(f"Saved workbook : {reports_dir / 'analysis_outputs.xlsx'}")
    print(f"Saved figures  : {reports_dir}")


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    main()
