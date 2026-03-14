from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.ps_project.data_factory import make_engineering_dataset, save_dataset
from src.ps_project.unit1_descriptive_probability import (
    categorical_probabilities,
    descriptive_summary,
    probability_laws_demo,
)
from src.ps_project.unit2_distributions_sampling import (
    distribution_probabilities,
    expectation_variance,
    random_variable_examples,
    sampling_distribution_clt,
)
from src.ps_project.unit3_estimation_tests import (
    confidence_intervals,
    hypothesis_tests,
    point_estimates,
)
from src.ps_project.unit4_regression_correlation import (
    correlation_analysis,
    multiple_regression,
    simple_regression,
)
from src.ps_project.unit5_quality_control import (
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

    df = make_engineering_dataset(seed=42, n=300)
    save_dataset(df, str(data_dir / "engineering_process.csv"))

    rv = random_variable_examples()
    unit_results = {
        "Unit1_Descriptive": descriptive_summary(df),
        "Unit1_Empirical_Probabilities": categorical_probabilities(df).to_frame("probability"),
        "Unit1_Probability_Laws": pd.DataFrame([probability_laws_demo()]),
        "Unit2_Expectation_Discrete": pd.DataFrame([expectation_variance(rv["discrete"])]),
        "Unit2_Expectation_Continuous": pd.DataFrame([expectation_variance(rv["continuous"])]),
        "Unit2_Distribution_Probabilities": pd.DataFrame([distribution_probabilities()]),
        "Unit2_CLT": pd.DataFrame([sampling_distribution_clt()]),
        "Unit3_Point_Estimates": pd.DataFrame([point_estimates(df)]),
        "Unit3_Confidence_Intervals": pd.DataFrame([confidence_intervals(df)]),
        "Unit3_Hypothesis_Tests": pd.DataFrame([hypothesis_tests(df)]),
        "Unit4_Correlation": pd.DataFrame([correlation_analysis(df)]),
        "Unit4_Simple_Regression": pd.DataFrame([simple_regression(df)]),
        "Unit4_Multiple_Regression": pd.DataFrame([multiple_regression(df)]),
        "Unit5_Xbar_R": pd.DataFrame([xbar_r_chart_limits(df["quality_score"])]),
        "Unit5_P_Chart": pd.DataFrame([p_chart_limits(df["defect"])]),
        "Unit5_Six_Sigma": pd.DataFrame([six_sigma_metrics(df)]),
    }

    with pd.ExcelWriter(reports_dir / "analysis_outputs.xlsx", engine="openpyxl") as writer:
        for name, table in unit_results.items():
            table.to_excel(writer, sheet_name=name[:31], index=True)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 5))
    sns.histplot(df["quality_score"], kde=True)
    plt.title("Histogram of Quality Score")
    plt.tight_layout()
    plt.savefig(reports_dir / "hist_quality_score.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df[["temperature", "pressure", "humidity"]])
    plt.title("Box Plots for Process Variables")
    plt.tight_layout()
    plt.savefig(reports_dir / "box_variables.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="temperature", y="quality_score", hue="shift")
    plt.title("Scatter Plot: Temperature vs Quality Score")
    plt.tight_layout()
    plt.savefig(reports_dir / "scatter_temp_quality.png", dpi=150)
    plt.close()

    print(f"Saved dataset: {data_dir / 'engineering_process.csv'}")
    print(f"Saved report workbook: {reports_dir / 'analysis_outputs.xlsx'}")
    print(f"Saved figures in: {reports_dir}")


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    main()
