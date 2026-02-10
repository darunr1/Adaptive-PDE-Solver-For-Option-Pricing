"""
Benchmarking utilities for comparing different pricing methods.

This module provides functions to benchmark the fixed-grid and adaptive
PDE solvers against the analytical Black-Scholes solution.
"""

import numpy as np
from typing import Dict, Tuple, List
import pandas as pd
from .config import PDEConfig
from . import bs_analytic
from . import pde_fixed_grid


def benchmark_solver(
    solver_func,
    params: Dict[str, float],
    test_cases: List[Dict[str, float]],
    name: str = "Solver"
) -> pd.DataFrame:
    """
    Benchmark a pricing solver against multiple test cases.
    
    Parameters
    ----------
    solver_func : callable
        Pricing function to benchmark
    params : dict
        Configuration parameters
    test_cases : list
        List of parameter dictionaries for test cases
    name : str
        Name of the solver
    
    Returns
    -------
    pd.DataFrame
        Results dataframe with prices and errors
    """
    results = []
    for tc in test_cases:
        try:
            price = solver_func(**tc, **params)
            bs_price = bs_analytic.call_price(**tc) if tc.get('option_type', 'call') == 'call' else \
                       bs_analytic.put_price(**tc)
            error = abs(price - bs_price)
            rel_error = error / bs_price if bs_price != 0 else 0
            
            results.append({
                'spot': tc.get('spot'),
                'strike': tc.get('strike'),
                'solver_price': price,
                'bs_price': bs_price,
                'abs_error': error,
                'rel_error': rel_error
            })
        except Exception as e:
            print(f"Error in test case {tc}: {e}")
    
    df = pd.DataFrame(results)
    return df


def compare_solvers(
    test_cases: List[Dict[str, float]],
    params: Dict[str, float]
) -> Dict[str, pd.DataFrame]:
    """
    Compare fixed-grid and adaptive solvers on the same test cases.
    
    Parameters
    ----------
    test_cases : list
        List of parameter dictionaries
    params : dict
        Configuration parameters
    
    Returns
    -------
    dict
        Dictionary with results for each solver
    """
    results = {}
    
    # Benchmark fixed-grid solver
    results['fixed_grid'] = benchmark_solver(
        pde_fixed_grid.price_option_fixed_grid,
        params,
        test_cases,
        name='Fixed Grid'
    )
    
    return results
