"""
Utility/helper functions used across the project
"""

import time
import numpy as np

def time_function(func, *args, **kwargs):
    """
    Measures how long a function takes to run.

    Returns:
        result: output of the function
        elapsed_time: time in seconds
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    return result, end - start

def linear_interpolate(x, x_grid, y_grid):
    """
    Simple linear interpolation.

    x: target value
    x_grid: array of grid x-values
    y_grid: array of corresponding y-values
    """
    return np.interp(x, x_grid, y_grid)

def validate_option_inputs(S0, K, T, sigma):
    if S0 <= 0 or K <= 0:
        raise ValueError("Stock price and strike must be positive")
    if T <= 0:
        raise ValueError("Time to maturity must be positive")
    if sigma <= 0:
        raise ValueError("Volatility must be positive")

