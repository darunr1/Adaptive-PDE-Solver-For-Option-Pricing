"""
Plotting utilities for visualization of option prices and errors.

This module provides functions to create plots for:
- Option prices across different spot prices
- Convergence analysis
- Error comparison between solvers
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List
import pandas as pd


def plot_price_profile(
    spot_range: np.ndarray,
    prices_dict: Dict[str, np.ndarray],
    strike: float,
    time_to_expiry: float,
    title: str = "Option Price Profile",
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Plot option prices across different spot prices.
    
    Parameters
    ----------
    spot_range : np.ndarray
        Array of spot prices
    prices_dict : dict
        Dictionary of {name: prices_array}
    strike : float
        Strike price
    time_to_expiry : float
        Time to expiration
    title : str
        Plot title
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for name, prices in prices_dict.items():
        ax.plot(spot_range, prices, label=name, linewidth=2)
    
    ax.axvline(strike, color='k', linestyle='--', alpha=0.5, label='Strike')
    ax.set_xlabel('Spot Price')
    ax.set_ylabel('Option Price')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_error_comparison(
    results: Dict[str, pd.DataFrame],
    title: str = "Absolute Error Comparison",
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Plot error comparison between different solvers.
    
    Parameters
    ----------
    results : dict
        Dictionary of {solver_name: results_dataframe}
    title : str
        Plot title
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for name, df in results.items():
        ax.semilogy(df.index, df['abs_error'], marker='o', label=name, linewidth=2)
    
    ax.set_xlabel('Test Case')
    ax.set_ylabel('Absolute Error')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    
    return fig


def plot_convergence(
    grid_sizes: List[int],
    errors: List[float],
    title: str = "Convergence Analysis",
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Plot convergence behavior as grid is refined.
    
    Parameters
    ----------
    grid_sizes : list
        List of grid sizes
    errors : list
        List of corresponding errors
    title : str
        Plot title
    figsize : tuple
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.loglog(grid_sizes, errors, marker='o', linewidth=2, markersize=8, label='Actual')
    
    # Add reference lines for different convergence rates
    x0, y0 = grid_sizes[0], errors[0]
    ax.loglog(grid_sizes, y0 * (np.array(grid_sizes) / x0)**(-1), '--', alpha=0.5, label='O(h)')
    ax.loglog(grid_sizes, y0 * (np.array(grid_sizes) / x0)**(-2), ':', alpha=0.5, label='O(h²)')
    
    ax.set_xlabel('Grid Size (number of points)')
    ax.set_ylabel('Error')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')
    
    return fig
