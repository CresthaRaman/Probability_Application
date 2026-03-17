# Cardiac Health Analytics – Probability & Statistics

> **Live Dashboard:** [website-liart-theta-53.vercel.app](https://website-liart-theta-53.vercel.app)

A complete statistical analysis of a **synthetic cardiac-health dataset** covering
five units of probability and statistics with **25 visualizations** and an
**interactive web dashboard**.

| Unit | Topic | Key Techniques |
|------|-------|----------------|
| 1 | Descriptive Statistics & Probability | Central tendency, variability, additive/conditional/Bayes probability |
| 2 | Distributions & Sampling | Binomial, Poisson, Normal, Gamma, Chi-Square; CLT demonstration |
| 3 | Estimation & Hypothesis Testing | Point estimates, confidence intervals, t-tests, Kruskal-Wallis, Chi-Square, Shapiro |
| 4 | Regression & Correlation | Pearson correlation, simple & multiple OLS regression, ANOVA decomposition |
| 5 | Quality Control | X-bar/R charts, P-charts, Six Sigma metrics (DPMO, sigma level) |

## Dataset

A synthetic cardiac-health dataset (**600 patients, 11 features**) generated using
clinically motivated probability distributions.

| Feature | Description |
|---------|-------------|
| `age` | Patient age (29–78 years) |
| `sex` | 0 = Female, 1 = Male |
| `resting_bp` | Resting blood pressure (mmHg) |
| `cholesterol` | Serum cholesterol (mg/dL) |
| `fasting_blood_sugar` | Fasting blood sugar (mg/dL) |
| `max_heart_rate` | Maximum heart rate during exercise (bpm) |
| `exercise_angina` | Exercise-induced angina (0/1) |
| `oldpeak` | ST depression value |
| `bmi` | Body Mass Index |
| `smoking_status` | 0 = Never, 1 = Former, 2 = Current |
| `heart_disease` | **Target** — 0 = Healthy, 1 = Disease |

## Quick Start

```bash
pip install -r requirements.txt
python run_all.py
```

Results (Excel workbook + 25 PNG charts) are saved in the `reports/` folder.

## Visualizations (25 Charts)

| # | Chart | Purpose |
|---|-------|---------|
| 1 | Diagnosis distribution (count + pie) | Class balance overview |
| 2 | Histograms by diagnosis | Feature distributions per group |
| 3 | Violin plots | Distribution shape + quartiles |
| 4 | Box plots by diagnosis | Outlier detection per group |
| 5 | Pair plot | Multi-feature relationships |
| 6 | Correlation heatmap (lower-triangle) | Collinearity check |
| 7 | Age analysis (dist + disease rate) | Age as risk factor |
| 8 | Smoking analysis | Smoking impact on disease |
| 9 | Sex comparison | Gender-based risk |
| 10 | BP vs cholesterol (regression) | Correlation with stats |
| 11 | Age vs max heart rate | Age-heart rate relationship |
| 12 | Age vs cholesterol by sex | Multi-factor scatter |
| 13 | BMI vs oldpeak (bubble) | Three-variable visualization |
| 14 | Exercise angina impact | Angina as predictor |
| 15 | KDE overlays | Smooth density comparison |
| 16 | Q-Q plots | Normality assessment |
| 17 | CLT illustration | Population vs sampling distribution |
| 18 | Confidence interval bars | CI for mean & proportion |
| 19 | Hypothesis test summary | All test p-values at a glance |
| 20 | Regression diagnostics | Model validation (residuals, Q-Q) |
| 21 | Regression coefficients | Predictor importance with CIs |
| 22 | X-bar & R control charts | Process stability |
| 23 | P-chart | Disease rate monitoring |
| 24 | Six Sigma dashboard | DPMO & sigma level |
| 25 | Feature importance | Correlation with target |

## Web Dashboard

An interactive website deployed on **Vercel** featuring:

- Dark / light theme toggle
- 10 interactive Chart.js charts (doughnut, radar, bar, line, gauge)
- 25 matplotlib chart images with lightbox zoom
- Animated counters and scroll-triggered animations
- Fully responsive (mobile / tablet / desktop)

## Project Structure

```
cardiac-health-analytics/
├── data/                     # Generated CSV
├── notebooks/                # Per-unit analysis scripts
├── reports/                  # Auto-generated Excel + 25 PNG charts
├── src/cardiac_project/      # Reusable analysis modules
│   ├── data_factory.py
│   ├── unit1_descriptive_probability.py
│   ├── unit2_distributions_sampling.py
│   ├── unit3_estimation_tests.py
│   ├── unit4_regression_correlation.py
│   └── unit5_quality_control.py
├── website/                  # Interactive web dashboard
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── charts/               # Chart images for web
├── run_all.py
├── requirements.txt
└── README.md
```

## Tech Stack

- **Python** — NumPy, Pandas, SciPy, Statsmodels, Matplotlib, Seaborn
- **Web** — HTML5, CSS3, JavaScript, Chart.js
- **Deployment** — Vercel
