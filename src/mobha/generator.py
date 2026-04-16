"""Generators for simple movement models."""

from __future__ import annotations

import numpy as np


def square_distribution(size: int | tuple[int, ...]) -> np.ndarray:
    """Sample on [0, 1] from the normalized density p(x) = 3 x^2."""
    uniform_samples = np.random.uniform(0.0, 1.0, size)
    return uniform_samples ** (1.0 / 3.0)


def square_symmetric_distribution(size: int | tuple[int, ...]) -> np.ndarray:
    """Sample on [-1, 1] from the normalized density p(x) = 3 x^2 / 2."""
    magnitudes = square_distribution(size)
    signs = np.where(np.random.uniform(0.0, 1.0, size) < 0.5, -1.0, 1.0)
    return signs * magnitudes


def _random_steps(standard_deviation: float, distribution: str, size: int | tuple[int, ...]) -> np.ndarray:
    """Draw random steps with the requested standard deviation."""
    # same standard deviation for all distributions
    if distribution == "gaussian":
        return standard_deviation * np.random.standard_normal(size)
    if distribution == "constant":
        return standard_deviation * np.where(np.random.uniform(0.0, 1.0, size) < 0.5, -1.0, 1.0)
    if distribution == "square":
        mean = 3.0 / 4.0
        std = np.sqrt(3.0 / 80.0)
        return standard_deviation * (square_distribution(size) - mean) / std
    if distribution == "square_symmetric":
        std = np.sqrt(3.0 / 5.0)
        return standard_deviation * square_symmetric_distribution(size) / std

    half_width = np.sqrt(3.0) * standard_deviation
    return np.random.uniform(-half_width, half_width, size)


class RandomWalk1D:
    """Generate a one-dimensional random walk."""

    def __init__(self, standard_deviation: float, distribution: str = "gaussian") -> None:
        if distribution not in {"gaussian", "uniform", "constant", "square", "square_symmetric"}:
            raise ValueError(
                "distribution must be 'gaussian', 'uniform', 'constant', 'square', or "
                "'square_symmetric'."
            )

        self.standard_deviation = standard_deviation
        self.distribution = distribution
        self.path = np.array([0.0])

    def walk(self, timesteps: int) -> np.ndarray:
        """Generate a path for the requested number of timesteps."""
        if timesteps < 0:
            raise ValueError("timesteps must be non-negative.")

        start = self.path[-1]
        steps = _random_steps(self.standard_deviation, self.distribution, timesteps)
        steps[0] += start
        self.path = np.concatenate((self.path, np.cumsum(steps)))
        return self.path


class RandomWalk2D:
    """Generate a two-dimensional random walk."""

    def __init__(self, standard_deviation: float, distribution: str = "gaussian") -> None:
        if distribution not in {"gaussian", "uniform", "constant", "square", "square_symmetric"}:
            raise ValueError(
                "distribution must be 'gaussian', 'uniform', 'constant', 'square', or "
                "'square_symmetric'."
            )

        self.standard_deviation = standard_deviation
        self.distribution = distribution
        self.path = np.array([[0.0, 0.0]])

    def walk(self, timesteps: int) -> np.ndarray:
        """Generate a 2D path for the requested number of timesteps."""
        if timesteps < 0:
            raise ValueError("timesteps must be non-negative.")

        start = self.path[-1]
        steps = _random_steps(self.standard_deviation, self.distribution, (timesteps, 2))
        steps[0] += start
        self.path = np.vstack((self.path, np.cumsum(steps, axis=0)))
        return self.path

    def set_distribution(self, distribution: str) -> None:
        """Set the distribution for future walks."""
        if distribution not in {"gaussian", "uniform", "constant", "square", "square_symmetric"}:
            raise ValueError(
                "distribution must be 'gaussian', 'uniform', 'constant', 'square', or "
                "'square_symmetric'."
            )
        self.distribution = distribution


class CorrelatedRandomWalk2D:
    """Generate a two-dimensional correlated random walk with constant step size."""

    def __init__(
        self,
        step_size: float,
        turning_angle_standard_deviation: float,
        initial_angle: float = 0.0,
    ) -> None:
        self.step_size = step_size
        self.turning_angle_standard_deviation = turning_angle_standard_deviation
        self.initial_angle = initial_angle
        self.path = np.array([[0.0, 0.0]])
        self.angles = np.array([initial_angle])

    def walk(self, timesteps: int) -> np.ndarray:
        """Generate a correlated 2D path for the requested number of timesteps."""
        if timesteps < 0:
            raise ValueError("timesteps must be non-negative.")

        turning_angles = self.turning_angle_standard_deviation * np.random.standard_normal(timesteps)
        start_angle = self.angles[-1]
        angles = start_angle + np.cumsum(turning_angles)
        steps = self.step_size * np.column_stack((np.cos(angles), np.sin(angles)))
        start = self.path[-1]
        steps[0] += start
        self.path = np.vstack((self.path, np.cumsum(steps, axis=0)))
        self.angles = np.concatenate((self.angles, angles))
        return self.path
