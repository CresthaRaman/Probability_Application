# Cardiac Health Analytics – Probability & Statistics

A complete statistical analysis of a **synthetic cardiac-health dataset** covering
five units of probability and statistics:

| Unit | Topic |
|------|-------|
| 1 | Descriptive Statistics & Probability |
| 2 | Distributions & Sampling |
| 3 | Estimation & Hypothesis Testing |
| 4 | Regression & Correlation |
| 5 | Quality Control |

## Dataset

A synthetic cardiac-health dataset (600 patients, 11 features) generated using
clinically motivated distributions. Features include age, sex, resting blood
pressure, cholesterol, fasting blood sugar, max heart rate, exercise-induced
angina, ST depression (oldpeak), BMI, and smoking status. The binary target
indicates **heart disease** (0 = healthy, 1 = disease).

## Quick Start

```bash
pip install -r requirements.txt
python run_all.py
```

Results (Excel workbook + PNG charts) are saved in the `reports/` folder.

## Project Structure

```
cardiac-health-analytics/
├── data/                     # Generated CSV
├── notebooks/                # Per-unit scripts
├── reports/                  # Auto-generated outputs
├── src/cardiac_project/      # Reusable analysis modules
├── run_all.py
├── requirements.txt
└── README.md
```
