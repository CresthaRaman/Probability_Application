# Probability and Statistics Data Science Project

This project covers all topics listed in `prob_and_stat.pdf` using Python-based data science workflows.

## Topics Coverage (from PDF)

### Unit 1: Descriptive Statistics and Basic Probability
- Introduction to statistics in engineering context
- Central tendency and variation
- Graphical representation: histogram, box plot, scatter plot
- Additive and multiplicative probability laws
- Conditional probability and Bayes theorem

### Unit 2: Probability Distributions and Sampling Distribution
- Discrete and continuous random variables
- Expectation and variance
- Discrete distributions: Binomial, Poisson, Negative Binomial
- Continuous distributions: Normal, Gamma, Chi-Square
- Population and sample concepts
- Sampling distribution of means/proportions
- Central Limit Theorem

### Unit 3: Estimation and Hypothesis Testing
- Point estimators and their use
- Confidence intervals for mean and proportion
- Parametric tests (single/two-sample/paired t-test)
- Non-parametric testing (Kruskal-Wallis)
- Goodness-of-fit and independence (Chi-square)
- Normality checks

### Unit 4: Correlation and Regression
- Correlation analysis and significance test
- Simple linear regression
- Multiple regression
- Explained and unexplained variation

### Unit 5: Quality Control and Six Sigma
- Quality control concepts
- X-bar and R chart limits
- P-chart limits
- Six Sigma metric (DPMO, approximate sigma level)

## Project Structure

- `data/`: generated sample engineering dataset
- `notebooks/`: notebook guide files for topic-by-topic study
- `reports/`: generated figures and result workbook
- `src/ps_project/`: reusable modules grouped by unit
- `run_all.py`: executes end-to-end analysis for all units

## Setup

```powershell
cd d:\prob\data-science-probability-statistics
d:/prob/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

## Run

```powershell
d:/prob/.venv/Scripts/python.exe run_all.py
```

Outputs produced:
- `data/engineering_process.csv`
- `reports/analysis_outputs.xlsx`
- `reports/hist_quality_score.png`
- `reports/box_variables.png`
- `reports/scatter_temp_quality.png`

## Notebook Plan

Create one notebook per unit and import from `src/ps_project`:
- `notebooks/01_unit1_descriptive_probability.ipynb`
- `notebooks/02_unit2_distributions_sampling.ipynb`
- `notebooks/03_unit3_estimation_testing.ipynb`
- `notebooks/04_unit4_regression_correlation.ipynb`
- `notebooks/05_unit5_quality_control.ipynb`

You can run everything from script first, then convert sections into notebook exercises.
