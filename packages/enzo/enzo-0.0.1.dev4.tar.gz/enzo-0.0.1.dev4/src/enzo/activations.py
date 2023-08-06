"""Activation functions"""

import numpy as np


@np.vectorize
def _relu(n):
    """Return max(0, n)."""
    return n if n > 0 else 0


def relu(matrix):
    """Apply max(0, n) to each n in ``matrix``.

    Parameters
    ----------
    matrix : `list` of `list`
    """
    return _relu(matrix)


@np.vectorize
def _sigmoid(n):
    """Return 1 / (1 + e ^ -n)."""
    return 1 / (1 + np.exp(-n))


def sigmoid(matrix):
    """Apply 1 / (1 + e ^ -n) to each n in ``matrix``.

    Parameters
    ----------
    matrix : `list` of `list`
    """
    return _sigmoid(matrix)


def noactivation(matrix):
    """Do nothing, return ``matrix``."""
    return matrix


def softmax():
    """TODO"""
