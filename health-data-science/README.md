# Health Data Science – Probability & Statistics

A complete statistical analysis of the **Wisconsin Breast Cancer** dataset covering
five units of probability and statistics:

| Unit | Topic |
|------|-------|
| 1 | Descriptive Statistics & Probability |
| 2 | Distributions & Sampling |
| 3 | Estimation & Hypothesis Testing |
| 4 | Regression & Correlation |
| 5 | Quality Control |

## Dataset

The Wisconsin Breast Cancer dataset (569 samples, 30 numeric features) is loaded
from **scikit-learn** (`sklearn.datasets.load_breast_cancer`). The target indicates
whether a tumor is **malignant** (0) or **benign** (1).

## Quick Start

```bash
pip install -r requirements.txt
python run_all.py
```

Results (Excel workbook + PNG charts) are saved in the `reports/` folder.

## Project Structure

```
health-data-science/
├── data/                 # Generated CSV
├── notebooks/            # Per-unit scripts
├── reports/              # Auto-generated outputs
├── src/health_project/   # Reusable analysis modules
├── run_all.py
├── requirements.txt
└── README.md
```
