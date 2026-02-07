"""Configuration values for the Adaptive PDE Option Pricer"""

# Default grid sizes
DEFAULT_PRICE_STEPS = 200     # number of stock price steps (M)
DEFAULT_TIME_STEPS = 200      # number of time steps (N)

# Stock price grid
S_MAX_MULTIPLIER = 3.0        # S_max = multiplier * strike price

# Numerical tolerances
ERROR_TOLERANCE = 1e-4        # acceptable pricing error

# Benchmark settings
BENCHMARK_RUNS = 5            # how many times to time each method
