from __future__ import annotations

from typing import Dict

import numpy as np
from scipy import stats


def random_variable_examples(seed: int = 42, n: int = 5000) -> Dict[str, np.ndarray]:
    """Generate discrete and continuous random variables."""
    rng = np.random.default_rng(seed)
    discrete_rv = rng.binomial(n=10, p=0.2, size=n)
    continuous_rv = rng.normal(loc=0.0, scale=1.0, size=n)
    return {"discrete": discrete_rv, "continuous": continuous_rv}


def expectation_variance(samples: np.ndarray) -> Dict[str, float]:
    return {
        "expectation": float(np.mean(samples)),
        "variance": float(np.var(samples, ddof=1)),
    }


def distribution_probabilities() -> Dict[str, float]:
    """Compute representative probabilities from named distributions."""
    return {
        "binomial_P(X<=3)": float(stats.binom.cdf(3, n=15, p=0.2)),
        "poisson_P(X=5)": float(stats.poisson.pmf(5, mu=4.0)),
        "negative_binomial_P(X=7)": float(stats.nbinom.pmf(7, n=4, p=0.45)),
        "normal_P(X<1.2)": float(stats.norm.cdf(1.2, loc=0.0, scale=1.0)),
        "gamma_P(X<3)": float(stats.gamma.cdf(3, a=2.0, scale=1.5)),
        "chi_square_P(X<8)": float(stats.chi2.cdf(8, df=5)),
    }


def sampling_distribution_clt(seed: int = 42, n_pop: int = 20000) -> Dict[str, float]:
    """Simulate sampling distribution of sample mean and show CLT behavior."""
    rng = np.random.default_rng(seed)
    population = rng.gamma(shape=2.5, scale=3.0, size=n_pop)

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
