"""
Script to price a single option using different methods.

Usage:
    python scripts/run_price.py --spot 100 --strike 100 --rate 0.05 --volatility 0.2 --expiry 1.0
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bs_analytic import call_price, put_price
from pde_fixed_grid import price_option_fixed_grid


def main():
    """Main entry point for pricing."""
    parser = argparse.ArgumentParser(description='Price a European option')
    parser.add_argument('--spot', type=float, default=100.0, help='Spot price')
    parser.add_argument('--strike', type=float, default=100.0, help='Strike price')
    parser.add_argument('--rate', type=float, default=0.05, help='Risk-free rate')
    parser.add_argument('--volatility', type=float, default=0.2, help='Volatility')
    parser.add_argument('--expiry', type=float, default=1.0, help='Time to expiry (years)')
    parser.add_argument('--option-type', type=str, default='call', choices=['call', 'put'],
                       help='Option type')
    parser.add_argument('--grid-points', type=int, default=201, help='Number of grid points')
    
    args = parser.parse_args()
    
    params = {
        'spot': args.spot,
        'strike': args.strike,
        'rate': args.rate,
        'volatility': args.volatility,
        'time_to_expiry': args.expiry
    }
    
    # Calculate Black-Scholes price
    if args.option_type == 'call':
        bs_price = call_price(**params)
    else:
        bs_price = put_price(**params)
    
    print(f"\n{'='*60}")
    print(f"Option Pricing Results")
    print(f"{'='*60}")
    print(f"Spot Price:        ${args.spot:.2f}")
    print(f"Strike Price:      ${args.strike:.2f}")
    print(f"Time to Expiry:    {args.expiry:.4f} years")
    print(f"Volatility:        {args.volatility:.4f}")
    print(f"Risk-free Rate:    {args.rate:.4f}")
    print(f"Option Type:       {args.option_type}")
    print(f"{'='*60}")
    print(f"Black-Scholes Price: ${bs_price:.6f}")
    
    # Try fixed-grid solver
    try:
        pde_price = price_option_fixed_grid(
            **params,
            num_space_points=args.grid_points,
            option_type=args.option_type
        )
        error = abs(pde_price - bs_price)
        rel_error = error / bs_price if bs_price != 0 else 0
        print(f"Fixed-Grid PDE Price: ${pde_price:.6f}")
        print(f"Absolute Error:       ${error:.6e}")
        print(f"Relative Error:       {rel_error:.4e}")
    except NotImplementedError:
        print("Fixed-Grid PDE solver not yet implemented")
    
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
