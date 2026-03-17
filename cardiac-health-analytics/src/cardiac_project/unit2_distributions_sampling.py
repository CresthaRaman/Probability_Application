from __future__ import annotations

from typing import Dict

import numpy as np
from scipy import stats


def random_variable_examples(seed: int = 42, n: int = 5000) -> Dict[str, np.ndarray]:
    """Generate discrete and continuous random variables modelling cardiac events."""
    rng = np.random.default_rng(seed)
    # Discrete: number of cardiac events in 12 monitored patients (p ≈ 0.40)
    discrete_rv = rng.binomial(n=12, p=0.40, size=n)
    # Continuous: simulated resting blood pressure (mmHg)
    continuous_rv = rng.normal(loc=130.0, scale=18.0, size=n)
    return {"discrete": discrete_rv, "continuous": continuous_rv}


def expectation_variance(samples: np.ndarray) -> Dict[str, float]:
    return {
        "expectation": float(np.mean(samples)),
        "variance": float(np.var(samples, ddof=1)),
    }


def distribution_probabilities() -> Dict[str, float]:
    """Compute representative probabilities from named distributions
    parameterised with clinically meaningful cardiac values."""
    return {
        "binomial_P(X<=4)": float(stats.binom.cdf(4, n=12, p=0.40)),
        "poisson_P(X=3)": float(stats.poisson.pmf(3, mu=4.0)),
        "negative_binomial_P(X=6)": float(stats.nbinom.pmf(6, n=3, p=0.40)),
        "normal_P(BP<140)": float(stats.norm.cdf(140, loc=130, scale=18)),
        "gamma_P(X<4)": float(stats.gamma.cdf(4, a=2.5, scale=1.2)),
        "chi_square_P(X<10)": float(stats.chi2.cdf(10, df=6)),
    }


def sampling_distribution_clt(seed: int = 42, n_pop: int = 20000) -> Dict[str, float]:
    """Simulate sampling distribution of sample mean (resting BP) and show CLT."""
    rng = np.random.default_rng(seed)
    population = rng.gamma(shape=5.0, scale=26.0, size=n_pop)  # skewed BP-like

    sample_size = 40
    reps = 2000
    means = np.array(
        [rng.choice(population, size=sample_size, replace=True).mean() for _ in range(reps)]
    )

    return {
        "population_mean": float(np.mean(population)),
        "population_std": float(np.std(population, ddof=1)),
        "sampling_mean": float(np.mean(means)),
        "sampling_std": float(np.std(means, ddof=1)),
        "theoretical_std_error": float(np.std(population, ddof=1) / np.sqrt(sample_size)),
    }
