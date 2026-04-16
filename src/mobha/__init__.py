"""Top-level package for minimal-template."""

from mobha.generator import (
    CorrelatedRandomWalk2D,
    RandomWalk1D,
    RandomWalk2D,
    square_distribution,
    square_symmetric_distribution,
)

__author__ = "Pascal Peter Klamser"
__email__ = "klamser@physik.hu-berlin.de"
__version__ = "0.1.0"

__all__ = [
    "RandomWalk1D",
    "RandomWalk2D",
    "CorrelatedRandomWalk2D",
    "square_distribution",
    "square_symmetric_distribution",
    "__author__",
    "__email__",
    "__version__",
]
