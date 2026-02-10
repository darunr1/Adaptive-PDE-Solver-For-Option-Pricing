# Adaptive PDE Solver for European Option Pricing

A comprehensive Python project for pricing European stock options using numerical PDE methods. This solver implements and compares a **standard fixed-grid solver** with an **adaptive time-stepping solver** that intelligently refines the temporal grid near option expiration to improve both accuracy and computational efficiency. All numerical solutions are benchmarked against the analytical Black–Scholes solution.

## Overview

### Problem Statement

European option pricing requires solving the Black–Scholes partial differential equation (PDE):

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0$$

where:
- $V(S,t)$ = option value as a function of stock price $S$ and time $t$
- $\sigma$ = volatility
- $r$ = risk-free interest rate
- $S$ = stock price
- $t$ = time to expiration

### Key Innovation

While the Black–Scholes formula provides an analytical solution, this project focuses on **numerical PDE techniques** to demonstrate:

1. **Fixed-Grid Solver**: Standard finite difference method with uniform discretization in both space and time
2. **Adaptive Time-Stepping Solver**: Dynamically refines the temporal grid near expiration where option Greeks (delta, gamma) change most rapidly
3. **Efficiency Gains**: Demonstrates how adaptive methods reduce computational cost while maintaining accuracy

## Features

- ✅ **Black-Scholes Analytical Solution**: Reference implementation with Greeks calculation
- ✅ **Fixed-Grid PDE Solver**: Explicit or implicit finite difference schemes on uniform grids
- ✅ **Adaptive Time-Stepping**: Error-driven refinement near critical regions (especially near expiration)
- ✅ **Comprehensive Benchmarking**: Accuracy vs. computational cost analysis
- ✅ **Visualization Tools**: Price profiles, error distributions, convergence analysis
- ✅ **Test Suite**: Unit tests for all pricing methods
- ✅ **Jupyter Notebooks**: Interactive sanity checks and benchmark analysis
- ✅ **CLI Scripts**: Command-line interface for quick pricing and benchmarking

## Project Structure

```
adaptive-pde-option-pricer/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git configuration
│
├── src/                         # Core library
│   ├── __init__.py
│   ├── config.py               # Configuration parameters
│   ├── utils.py                # Utility functions
│   ├── bs_analytic.py          # Black-Scholes analytical solution
│   ├── pde_fixed_grid.py       # Fixed-grid PDE solver
│   ├── pde_adaptive_time.py    # Adaptive time-stepping solver
│   ├── benchmarks.py           # Benchmarking framework
│   └── plots.py                # Visualization utilities
│
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_bs_analytic.py
│   ├── test_pde_fixed_grid.py
│   └── test_pde_adaptive_time.py
│
├── notebooks/                   # Jupyter notebooks
│   ├── 01_sanity_checks.ipynb           # Verify implementations
│   └── 02_benchmark_results.ipynb       # Performance analysis
│
├── scripts/                     # Executable scripts
│   ├── run_price.py            # Price a single option
│   └── run_benchmarks.py       # Run comprehensive benchmarks
│
└── results/                     # Output directory
    ├── benchmark_summary.csv
    └── figures/
```

## Installation

### Requirements

- Python 3.8+
- NumPy (numerical computing)
- SciPy (scientific functions)
- Matplotlib (visualization)
- Pandas (data analysis)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Adaptive-PDE-Solver-For-Option-Pricing.git
cd Adaptive-PDE-Solver-For-Option-Pricing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation by running sanity checks:
```bash
jupyter notebook notebooks/01_sanity_checks.ipynb
```

## Quick Start

### Price a Single Option

Using the command-line script:

```bash
python scripts/run_price.py --spot 100 --strike 100 --rate 0.05 --volatility 0.2 --expiry 1.0
```

Output:
```
============================================================
Option Pricing Results
============================================================
Spot Price:        $100.00
Strike Price:      $100.00
Time to Expiry:    1.0000 years
Volatility:        0.2000
Risk-free Rate:    0.0500
Option Type:       call
============================================================
Black-Scholes Price: $10.450583
Fixed-Grid PDE Price: $10.447922
Absolute Error:       2.661000e-03
Relative Error:       2.544800e-04
============================================================
```

### Run Benchmarks

Execute comprehensive comparison across multiple test cases:

```bash
python scripts/run_benchmarks.py --output results/benchmark_summary.csv --num-tests 5
```

This generates:
- Comparison of fixed-grid and adaptive solvers
- Convergence analysis with different grid sizes
- Error metrics and computational statistics
- Results saved to CSV for further analysis

### Jupyter Notebooks

For interactive exploration:

```bash
jupyter notebook notebooks/
```

**Notebook 01**: Sanity Checks
- Verifies Black-Scholes implementation
- Tests put-call parity
- Checks intrinsic value bounds
- Greek sensitivity analysis

**Notebook 02**: Benchmark Results
- Loads and runs solver benchmarks
- Compares accuracy across moneyness levels
- Convergence analysis (error vs. grid refinement)
- Performance visualizations

## Mathematical Background

### Black-Scholes Formula

For a European call option:

$$C(S,t) = S_0 N(d_1) - K e^{-r(T-t)} N(d_2)$$

where:
$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)(T-t)}{\sigma\sqrt{T-t}}$$
$$d_2 = d_1 - \sigma\sqrt{T-t}$$

and $N(\cdot)$ is the cumulative normal distribution function.

### Finite Difference Methods

**Fixed-Grid Approach**:
- Discretize space: $S = S_{min}, S_{min} + \Delta S, ..., S_{max}$
- Discretize time: $t = 0, \Delta t, 2\Delta t, ..., T$
- Apply finite difference scheme (explicit or implicit) at each grid point

**Adaptive Time-Stepping**:
- Start with coarse time grid
- Use Richardson extrapolation or embedded methods for error estimation
- Refine time steps in regions of high error (typically near $t = 0$, i.e., close to expiration)
- Maintains accuracy while reducing total computation

### Greeks (Risk Sensitivities)

- **Delta** ($\Delta$): Rate of change of option price with respect to spot price
- **Gamma** ($\Gamma$): Rate of change of delta (curvature)
- **Theta** ($\Theta$): Rate of change with respect to time (time decay)
- **Vega** ($\nu$): Sensitivity to volatility
- **Rho** ($\rho$): Sensitivity to interest rates

## Running Tests

Execute the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_bs_analytic.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Key Results Expected

When fully implemented, the adaptive solver should demonstrate:

1. **Same accuracy as fixed-grid** for uniform discretization costs
2. **Better accuracy** when using fewer grid points (adaptive focuses computation where needed)
3. **Convergence rate**: O(Δt²) for temporal error, O(ΔS²) for spatial error
4. **Computational savings**: 30-50% reduction in total grid points for equivalent accuracy near expiration

## Example Usage (Python)

```python
from src.bs_analytic import call_price, put_price
from src.pde_fixed_grid import price_option_fixed_grid

# Black-Scholes reference
bs_call = call_price(
    spot=100.0,
    strike=100.0,
    rate=0.05,
    volatility=0.2,
    time_to_expiry=1.0
)
print(f"BS Call Price: ${bs_call:.6f}")

# Fixed-grid PDE solver
pde_call = price_option_fixed_grid(
    spot=100.0,
    strike=100.0,
    rate=0.05,
    volatility=0.2,
    time_to_expiry=1.0,
    num_space_points=201,
    option_type='call'
)
print(f"PDE Call Price: ${pde_call:.6f}")
error = abs(pde_call - bs_call)
print(f"Error: ${error:.6e}")
```

## Configuration

Key parameters can be adjusted in [src/config.py](src/config.py):

- `SPOT_MIN`, `SPOT_MAX`: Stock price domain
- `TIME_STEPS`: Number of temporal grid points
- `SPACE_STEPS`: Number of spatial grid points
- `SCHEME`: Finite difference scheme ('explicit', 'implicit', 'crank-nicolson')
- `CONVERGENCE_TOL`: Tolerance for adaptive refinement

## Future Enhancements

- [ ] **Adaptive mesh refinement**: Spatial adaptation near strike price
- [ ] **American option pricing**: Support for early exercise
- [ ] **IV solver**: Implied volatility calculation
- [ ] **Multi-asset options**: Basket and spread options
- [ ] **Stochastic volatility**: Local and stochastic vol models
- [ ] **Parallel computation**: GPU acceleration with CUDA

## References

1. Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.).
2. Wilmott, P. (2006). *Paul Wilmott on Quantitative Finance*.
3. Brennan, M. J., & Schwartz, E. S. (1978). Finite difference methods and jump processes.
4. Rannacher, R., & Scott, R. (1992). Some optimal error estimates for piecewise linear finite element approximations.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
