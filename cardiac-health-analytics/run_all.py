from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from src.cardiac_project.unit5_quality_control import subgroup_stats

from src.cardiac_project.data_factory import make_cardiac_dataset, save_dataset
from src.cardiac_project.unit1_descriptive_probability import (
    categorical_probabilities,
    descriptive_summary,
    probability_laws_demo,
)
from src.cardiac_project.unit2_distributions_sampling import (
    distribution_probabilities,
    expectation_variance,
    random_variable_examples,
    sampling_distribution_clt,
)
from src.cardiac_project.unit3_estimation_tests import (
    confidence_intervals,
    hypothesis_tests,
    point_estimates,
)
from src.cardiac_project.unit4_regression_correlation import (
    correlation_analysis,
    multiple_regression,
    simple_regression,
)
from src.cardiac_project.unit5_quality_control import (
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
    df = make_cardiac_dataset()
    save_dataset(df, str(data_dir / "cardiac_health.csv"))

    # Binary disease flag for p-chart
    disease_flag = df["heart_disease"].astype(int)

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
        "Unit5_Xbar_R": pd.DataFrame([xbar_r_chart_limits(df["resting_bp"])]),
        "Unit5_P_Chart": pd.DataFrame([p_chart_limits(disease_flag)]),
        "Unit5_Six_Sigma": pd.DataFrame([six_sigma_metrics(df)]),
    }

    # --- Write Excel workbook ---
    with pd.ExcelWriter(reports_dir / "analysis_outputs.xlsx", engine="openpyxl") as writer:
        for name, table in unit_results.items():
            table.to_excel(writer, sheet_name=name[:31], index=True)

    # --- Visualisations ---
    sns.set_theme(style="whitegrid")

    # Helper labels
    smoking_map = {0: "Never", 1: "Former", 2: "Current"}
    df["smoking_label"] = df["smoking_status"].map(smoking_map)

    # ── 1. Diagnosis distribution (count + percentage pie) ──
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.countplot(data=df, x="label", hue="label", palette="Set2", legend=False, ax=axes[0])
    axes[0].set_title("Heart Disease Count")
    axes[0].bar_label(axes[0].containers[0])
    counts = df["label"].value_counts()
    axes[1].pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["#66c2a5", "#fc8d62"],
                startangle=90, wedgeprops={"edgecolor": "white"})
    axes[1].set_title("Heart Disease Proportion")
    plt.tight_layout()
    plt.savefig(reports_dir / "01_diagnosis_distribution.png", dpi=150)
    plt.close()

    # ── 2. Histograms of key features split by diagnosis ──
    hist_features = ["resting_bp", "cholesterol", "max_heart_rate", "bmi"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for ax, feat in zip(axes.ravel(), hist_features):
        sns.histplot(data=df, x=feat, hue="label", kde=True, bins=30, ax=ax)
        ax.set_title(f"Distribution of {feat} by Diagnosis")
    plt.tight_layout()
    plt.savefig(reports_dir / "02_histograms_by_diagnosis.png", dpi=150)
    plt.close()

    # ── 3. Violin plots: continuous features by diagnosis ──
    violin_feats = ["resting_bp", "cholesterol", "max_heart_rate", "bmi", "oldpeak"]
    fig, axes = plt.subplots(1, len(violin_feats), figsize=(20, 5))
    for ax, feat in zip(axes, violin_feats):
        sns.violinplot(data=df, x="label", y=feat, hue="label", palette="muted",
                       inner="quart", ax=ax, legend=False)
        ax.set_title(feat)
        ax.set_xlabel("")
    fig.suptitle("Violin Plots – Feature Distributions by Diagnosis", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(reports_dir / "03_violin_plots.png", dpi=150, bbox_inches="tight")
    plt.close()

    # ── 4. Box plots grouped by diagnosis ──
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for ax, feat in zip(axes.ravel(), hist_features):
        sns.boxplot(data=df, x="label", y=feat, hue="label", palette="Set2", ax=ax, legend=False)
        ax.set_title(f"{feat} by Diagnosis")
        ax.set_xlabel("")
    plt.tight_layout()
    plt.savefig(reports_dir / "04_boxplots_by_diagnosis.png", dpi=150)
    plt.close()

    # ── 5. Scatter matrix (pair plot) for top features ──
    pair_feats = ["resting_bp", "cholesterol", "max_heart_rate", "bmi", "label"]
    g = sns.pairplot(df[pair_feats], hue="label", palette="Set1",
                     diag_kind="kde", plot_kws={"alpha": 0.5, "s": 20})
    g.figure.suptitle("Pair Plot – Key Cardiac Features", y=1.02, fontsize=14)
    g.savefig(reports_dir / "05_pairplot.png", dpi=150, bbox_inches="tight")
    plt.close()

    # ── 6. Full correlation heatmap ──
    num_feat = ["age", "resting_bp", "cholesterol", "fasting_blood_sugar",
                "max_heart_rate", "oldpeak", "bmi", "heart_disease"]
    plt.figure(figsize=(10, 8))
    corr_matrix = df[num_feat].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="RdBu_r",
                mask=mask, vmin=-1, vmax=1, linewidths=0.5)
    plt.title("Lower-Triangle Correlation Heatmap – Cardiac Features")
    plt.tight_layout()
    plt.savefig(reports_dir / "06_heatmap_correlations.png", dpi=150)
    plt.close()

    # ── 7. Age distribution & disease rate by age group ──
    df["age_group"] = pd.cut(df["age"], bins=[28, 35, 45, 55, 65, 78],
                             labels=["29-35", "36-45", "46-55", "56-65", "66-78"])
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(data=df, x="age", hue="label", kde=True, bins=25, ax=axes[0])
    axes[0].set_title("Age Distribution by Diagnosis")
    disease_rate = df.groupby("age_group", observed=True)["heart_disease"].mean()
    axes[1].bar(disease_rate.index, disease_rate.values, color="#e74c3c", edgecolor="white")
    axes[1].set_ylabel("Disease Proportion")
    axes[1].set_title("Heart Disease Rate by Age Group")
    for i, v in enumerate(disease_rate.values):
        axes[1].text(i, v + 0.01, f"{v:.2f}", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(reports_dir / "07_age_analysis.png", dpi=150)
    plt.close()

    # ── 8. Smoking status analysis ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    ct = pd.crosstab(df["smoking_label"], df["label"])
    ct.plot(kind="bar", stacked=True, ax=axes[0], color=["#66c2a5", "#fc8d62"], edgecolor="white")
    axes[0].set_title("Diagnosis Count by Smoking Status")
    axes[0].set_xlabel("")
    axes[0].tick_params(axis="x", rotation=0)
    smoke_rate = df.groupby("smoking_label", observed=True)["heart_disease"].mean()
    axes[1].barh(smoke_rate.index, smoke_rate.values, color=["#3498db", "#e67e22", "#e74c3c"])
    axes[1].set_xlabel("Disease Proportion")
    axes[1].set_title("Heart Disease Rate by Smoking Status")
    for i, v in enumerate(smoke_rate.values):
        axes[1].text(v + 0.005, i, f"{v:.2f}", va="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(reports_dir / "08_smoking_analysis.png", dpi=150)
    plt.close()

    # ── 9. Sex-based comparison ──
    df["sex_label"] = df["sex"].map({0: "Female", 1: "Male"})
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sex_rate = df.groupby("sex_label", observed=True)["heart_disease"].mean()
    axes[0].bar(sex_rate.index, sex_rate.values, color=["#e88dbc", "#7db8e0"], edgecolor="white")
    axes[0].set_title("Disease Rate by Sex")
    axes[0].set_ylabel("Proportion")
    for i, v in enumerate(sex_rate.values):
        axes[0].text(i, v + 0.01, f"{v:.2f}", ha="center", fontweight="bold")
    sns.boxplot(data=df, x="sex_label", y="cholesterol", hue="label",
                palette="Set2", ax=axes[1])
    axes[1].set_title("Cholesterol by Sex & Diagnosis")
    axes[1].set_xlabel("")
    sns.boxplot(data=df, x="sex_label", y="resting_bp", hue="label",
                palette="Set2", ax=axes[2])
    axes[2].set_title("Resting BP by Sex & Diagnosis")
    axes[2].set_xlabel("")
    plt.tight_layout()
    plt.savefig(reports_dir / "09_sex_comparison.png", dpi=150)
    plt.close()

    # ── 10. Scatter: resting BP vs cholesterol with regression line ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.regplot(data=df, x="resting_bp", y="cholesterol", scatter_kws={"alpha": 0.4},
                line_kws={"color": "red"}, ax=axes[0])
    r, p = stats.pearsonr(df["resting_bp"], df["cholesterol"])
    axes[0].set_title(f"Resting BP vs Cholesterol (r={r:.3f}, p={p:.3f})")
    sns.scatterplot(data=df, x="resting_bp", y="cholesterol", hue="label",
                    alpha=0.6, ax=axes[1])
    axes[1].set_title("Resting BP vs Cholesterol by Diagnosis")
    plt.tight_layout()
    plt.savefig(reports_dir / "10_scatter_bp_cholesterol.png", dpi=150)
    plt.close()

    # ── 11. Scatter: age vs max heart rate ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.regplot(data=df, x="age", y="max_heart_rate", scatter_kws={"alpha": 0.4},
                line_kws={"color": "red"}, ax=axes[0])
    r2, p2 = stats.pearsonr(df["age"], df["max_heart_rate"])
    axes[0].set_title(f"Age vs Max Heart Rate (r={r2:.3f}, p={p2:.4f})")
    sns.scatterplot(data=df, x="age", y="max_heart_rate", hue="label",
                    alpha=0.6, ax=axes[1])
    axes[1].set_title("Age vs Max Heart Rate by Diagnosis")
    plt.tight_layout()
    plt.savefig(reports_dir / "11_scatter_age_heartrate.png", dpi=150)
    plt.close()

    # ── 12. Scatter: age vs cholesterol ──
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="age", y="cholesterol", hue="label",
                    style="sex_label", alpha=0.7)
    plt.title("Age vs Cholesterol by Diagnosis & Sex")
    plt.tight_layout()
    plt.savefig(reports_dir / "12_scatter_age_cholesterol.png", dpi=150)
    plt.close()

    # ── 13. BMI vs oldpeak by diagnosis ──
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="bmi", y="oldpeak", hue="label", size="age",
                    sizes=(20, 200), alpha=0.6, palette="Set1")
    plt.title("BMI vs ST Depression (Oldpeak) – Size = Age")
    plt.tight_layout()
    plt.savefig(reports_dir / "13_scatter_bmi_oldpeak.png", dpi=150)
    plt.close()

    # ── 14. Exercise angina impact ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    angina_ct = pd.crosstab(df["exercise_angina"].map({0: "No", 1: "Yes"}), df["label"])
    angina_ct.plot(kind="bar", stacked=False, ax=axes[0], color=["#66c2a5", "#fc8d62"],
                   edgecolor="white")
    axes[0].set_title("Diagnosis by Exercise-Induced Angina")
    axes[0].set_xlabel("Exercise Angina")
    axes[0].tick_params(axis="x", rotation=0)
    sns.boxplot(data=df, x=df["exercise_angina"].map({0: "No", 1: "Yes"}),
                y="max_heart_rate", hue="label", palette="Set2", ax=axes[1])
    axes[1].set_title("Max Heart Rate by Angina & Diagnosis")
    axes[1].set_xlabel("Exercise Angina")
    plt.tight_layout()
    plt.savefig(reports_dir / "14_angina_analysis.png", dpi=150)
    plt.close()

    # ── 15. KDE overlays for disease vs healthy ──
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    kde_feats = ["age", "resting_bp", "cholesterol", "max_heart_rate", "bmi", "oldpeak"]
    for ax, feat in zip(axes.ravel(), kde_feats):
        for lbl, color in zip(["Healthy", "Disease"], ["#2ecc71", "#e74c3c"]):
            subset = df.loc[df["label"] == lbl, feat]
            sns.kdeplot(subset, label=lbl, color=color, fill=True, alpha=0.3, ax=ax)
        ax.set_title(f"KDE: {feat}")
        ax.legend()
    fig.suptitle("Kernel Density Estimates – Healthy vs Disease", fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(reports_dir / "15_kde_overlays.png", dpi=150, bbox_inches="tight")
    plt.close()

    # ── 16. QQ-plots for normality assessment ──
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, feat in zip(axes.ravel(), ["resting_bp", "cholesterol", "max_heart_rate", "bmi"]):
        stats.probplot(df[feat], dist="norm", plot=ax)
        ax.set_title(f"Q-Q Plot: {feat}")
    plt.tight_layout()
    plt.savefig(reports_dir / "16_qq_plots.png", dpi=150)
    plt.close()

    # ── 17. Sampling distribution / CLT illustration ──
    rng = np.random.default_rng(42)
    pop = df["resting_bp"].to_numpy()
    sample_means = [rng.choice(pop, size=30, replace=True).mean() for _ in range(2000)]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(pop, bins=30, color="#3498db", edgecolor="white", alpha=0.8)
    axes[0].axvline(pop.mean(), color="red", linestyle="--", label=f"μ = {pop.mean():.1f}")
    axes[0].set_title("Population: Resting BP")
    axes[0].legend()
    axes[1].hist(sample_means, bins=40, color="#2ecc71", edgecolor="white", alpha=0.8)
    axes[1].axvline(np.mean(sample_means), color="red", linestyle="--",
                    label=f"x̄ mean = {np.mean(sample_means):.2f}")
    axes[1].set_title("Sampling Distribution of x̄  (n=30, 2000 reps)")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(reports_dir / "17_clt_illustration.png", dpi=150)
    plt.close()

    # ── 18. Confidence interval visualization ──
    ci = confidence_intervals(df)
    pe = point_estimates(df)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].barh(["Mean Resting BP"], [pe["mean_resting_bp"]], xerr=[[pe["mean_resting_bp"] - ci["bp_mean_ci_low"]]],
                 color="#3498db", capsize=10)
    axes[0].set_xlim(ci["bp_mean_ci_low"] - 2, ci["bp_mean_ci_high"] + 2)
    axes[0].set_title(f"95% CI for Mean Resting BP: [{ci['bp_mean_ci_low']:.2f}, {ci['bp_mean_ci_high']:.2f}]")
    axes[1].barh(["Prop Disease"], [pe["proportion_disease"]], xerr=[[pe["proportion_disease"] - ci["prop_disease_ci_low"]]],
                 color="#e74c3c", capsize=10)
    axes[1].set_xlim(ci["prop_disease_ci_low"] - 0.05, ci["prop_disease_ci_high"] + 0.05)
    axes[1].set_title(f"95% CI for Disease Proportion: [{ci['prop_disease_ci_low']:.3f}, {ci['prop_disease_ci_high']:.3f}]")
    plt.tight_layout()
    plt.savefig(reports_dir / "18_confidence_intervals.png", dpi=150)
    plt.close()

    # ── 19. Hypothesis test results summary ──
    ht = hypothesis_tests(df)
    test_names = ["1-Sample t", "2-Sample t", "Paired t", "Kruskal-Wallis", "Chi-Square", "Shapiro"]
    p_values = [ht["t_single_p"], ht["t_two_p"], ht["paired_t_p"],
                ht["kruskal_h_p"], ht["chi_square_p"], ht["shapiro_p"]]
    colors = ["#2ecc71" if p > 0.05 else "#e74c3c" for p in p_values]
    plt.figure(figsize=(10, 5))
    bars = plt.barh(test_names, p_values, color=colors, edgecolor="white")
    plt.axvline(0.05, color="black", linestyle="--", linewidth=1.5, label="α = 0.05")
    for bar, pv in zip(bars, p_values):
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                 f"p={pv:.4f}", va="center", fontsize=9)
    plt.xlabel("p-value")
    plt.title("Hypothesis Test Results (green = fail to reject H0, red = reject H0)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(reports_dir / "19_hypothesis_tests.png", dpi=150)
    plt.close()

    # ── 20. Simple & Multiple regression diagnostics ──
    import statsmodels.api as sm
    x_simple = sm.add_constant(df[["age"]])
    model_s = sm.OLS(df["cholesterol"], x_simple).fit()
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    axes[0].scatter(df["age"], df["cholesterol"], alpha=0.4, s=15)
    axes[0].plot(df["age"].sort_values(),
                 model_s.predict(sm.add_constant(df[["age"]].sort_values("age"))),
                 color="red", linewidth=2)
    axes[0].set_title(f"Simple Regression: Cholesterol ~ Age (R²={model_s.rsquared:.3f})")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Cholesterol")
    axes[1].scatter(model_s.fittedvalues, model_s.resid, alpha=0.4, s=15, color="#e67e22")
    axes[1].axhline(0, color="red", linestyle="--")
    axes[1].set_title("Residuals vs Fitted")
    axes[1].set_xlabel("Fitted Values")
    axes[1].set_ylabel("Residuals")
    stats.probplot(model_s.resid, dist="norm", plot=axes[2])
    axes[2].set_title("Q-Q Plot of Residuals")
    plt.tight_layout()
    plt.savefig(reports_dir / "20_regression_diagnostics.png", dpi=150)
    plt.close()

    # ── 21. Multiple regression coefficient plot ──
    predictors = ["age", "resting_bp", "bmi", "smoking_status"]
    x_mult = sm.add_constant(df[predictors])
    model_m = sm.OLS(df["cholesterol"], x_mult).fit()
    coefs = model_m.params.drop("const")
    ci_low = model_m.conf_int().drop("const")[0]
    ci_high = model_m.conf_int().drop("const")[1]
    plt.figure(figsize=(8, 5))
    y_pos = range(len(coefs))
    plt.barh(list(y_pos), coefs.values, color="#3498db", edgecolor="white")
    plt.errorbar(coefs.values, list(y_pos),
                 xerr=[coefs.values - ci_low.values, ci_high.values - coefs.values],
                 fmt="none", color="black", capsize=5)
    plt.yticks(list(y_pos), coefs.index)
    plt.axvline(0, color="red", linestyle="--")
    plt.title(f"Multiple Regression Coefficients (Adj R²={model_m.rsquared_adj:.3f})")
    plt.xlabel("Coefficient Value")
    plt.tight_layout()
    plt.savefig(reports_dir / "21_regression_coefficients.png", dpi=150)
    plt.close()

    # ── 22. X-bar & R control charts ──
    sg = subgroup_stats(df["resting_bp"], subgroup_size=5)
    limits = xbar_r_chart_limits(df["resting_bp"])
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    axes[0].plot(sg["xbar"], marker="o", markersize=3, linewidth=0.8)
    axes[0].axhline(limits["xbar_center"], color="green", linestyle="-", label="CL")
    axes[0].axhline(limits["xbar_ucl"], color="red", linestyle="--", label="UCL")
    axes[0].axhline(limits["xbar_lcl"], color="red", linestyle="--", label="LCL")
    ooc_x = sg["xbar"][(sg["xbar"] > limits["xbar_ucl"]) | (sg["xbar"] < limits["xbar_lcl"])]
    axes[0].scatter(ooc_x.index, ooc_x.values, color="red", zorder=5, s=40, label="Out of control")
    axes[0].set_title("X-bar Chart – Resting Blood Pressure")
    axes[0].set_ylabel("Subgroup Mean")
    axes[0].legend(loc="upper right")
    axes[1].plot(sg["range"], marker="o", markersize=3, linewidth=0.8, color="#e67e22")
    axes[1].axhline(limits["r_center"], color="green", linestyle="-", label="CL")
    axes[1].axhline(limits["r_ucl"], color="red", linestyle="--", label="UCL")
    axes[1].axhline(limits["r_lcl"], color="red", linestyle="--", label="LCL")
    ooc_r = sg["range"][(sg["range"] > limits["r_ucl"]) | (sg["range"] < limits["r_lcl"])]
    axes[1].scatter(ooc_r.index, ooc_r.values, color="red", zorder=5, s=40, label="Out of control")
    axes[1].set_title("R Chart – Resting Blood Pressure")
    axes[1].set_xlabel("Subgroup Number")
    axes[1].set_ylabel("Subgroup Range")
    axes[1].legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(reports_dir / "22_xbar_r_charts.png", dpi=150)
    plt.close()

    # ── 23. P-chart ──
    p_limits = p_chart_limits(disease_flag, subgroup_size=10)
    trimmed = disease_flag.iloc[:len(disease_flag) - (len(disease_flag) % 10)]
    p_groups = trimmed.to_numpy().reshape(-1, 10).mean(axis=1)
    plt.figure(figsize=(14, 5))
    plt.plot(p_groups, marker="o", markersize=4, linewidth=0.8)
    plt.axhline(p_limits["p_center"], color="green", linestyle="-", label="CL")
    plt.axhline(p_limits["p_ucl"], color="red", linestyle="--", label="UCL")
    plt.axhline(p_limits["p_lcl"], color="red", linestyle="--", label="LCL")
    ooc_p = np.where((p_groups > p_limits["p_ucl"]) | (p_groups < p_limits["p_lcl"]))[0]
    plt.scatter(ooc_p, p_groups[ooc_p], color="red", zorder=5, s=50, label="Out of control")
    plt.title("P-Chart – Heart Disease Rate per Subgroup")
    plt.xlabel("Subgroup Number")
    plt.ylabel("Proportion Diseased")
    plt.legend()
    plt.tight_layout()
    plt.savefig(reports_dir / "23_p_chart.png", dpi=150)
    plt.close()

    # ── 24. Six Sigma summary dashboard ──
    ss = six_sigma_metrics(df)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].bar(["Disease", "Healthy"], [ss["disease_count"], ss["total_patients"] - ss["disease_count"]],
                color=["#e74c3c", "#2ecc71"], edgecolor="white")
    axes[0].set_title("Disease vs Healthy Count")
    axes[1].bar(["DPMO"], [ss["DPMO"]], color="#e67e22", edgecolor="white", width=0.4)
    axes[1].set_title(f"DPMO = {ss['DPMO']:,.0f}")
    axes[1].set_ylabel("Defects Per Million")
    axes[2].barh(["Sigma Level"], [ss["sigma_level_approx"]], color="#3498db", edgecolor="white")
    axes[2].set_xlim(0, 6)
    axes[2].set_title(f"Approx Sigma Level = {ss['sigma_level_approx']:.2f}")
    plt.tight_layout()
    plt.savefig(reports_dir / "24_six_sigma_dashboard.png", dpi=150)
    plt.close()

    # ── 25. Feature importance (correlation with target) ──
    target_corr = df[num_feat].corr()["heart_disease"].drop("heart_disease").sort_values()
    plt.figure(figsize=(8, 5))
    colors_corr = ["#e74c3c" if v < 0 else "#2ecc71" for v in target_corr.values]
    plt.barh(target_corr.index, target_corr.values, color=colors_corr, edgecolor="white")
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Feature Correlation with Heart Disease")
    plt.xlabel("Pearson Correlation")
    for i, v in enumerate(target_corr.values):
        plt.text(v + 0.005 if v >= 0 else v - 0.04, i, f"{v:.3f}", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(reports_dir / "25_feature_importance.png", dpi=150)
    plt.close()

    # cleanup helper columns
    df.drop(columns=["age_group", "smoking_label", "sex_label"], inplace=True, errors="ignore")

    print(f"Saved dataset  : {data_dir / 'cardiac_health.csv'}")
    print(f"Saved workbook : {reports_dir / 'analysis_outputs.xlsx'}")
    print(f"Saved figures  : {reports_dir}")


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    main()
