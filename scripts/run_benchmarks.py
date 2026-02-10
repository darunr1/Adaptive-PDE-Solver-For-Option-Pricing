"""
Script to run benchmarks comparing different solvers.

Usage:
    python scripts/run_benchmarks.py --output results/benchmark_summary.csv
"""

import argparse
import sys
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from benchmarks import compare_solvers
from config import PDEConfig


def main():
    """Main entry point for benchmarks."""
    parser = argparse.ArgumentParser(description='Run option pricing benchmarks')
    parser.add_argument('--output', type=str, default='results/benchmark_summary.csv',
                       help='Output file for benchmark results')
    parser.add_argument('--num-tests', type=int, default=5,
                       help='Number of test cases')
    
    args = parser.parse_args()
    
    # Default parameters
    base_params = {
        'rate': 0.05,
        'volatility': 0.2,
        'time_to_expiry': 1.0,
        'num_space_points': 201
    }
    
    # Create diverse test cases (ATM, ITM, OTM at different spots)
    test_cases = []
    strikes = [80, 90, 100, 110, 120]
    for strike in strikes:
        test_cases.append({
            'spot': 100.0,
            'strike': strike,
            'option_type': 'call'
        })
    
    print(f"\n{'='*60}")
    print(f"Running Benchmarks")
    print(f"{'='*60}")
    print(f"Number of test cases: {len(test_cases)}")
    print(f"Parameters: {base_params}")
    print(f"{'='*60}\n")
    
    try:
        results = compare_solvers(test_cases, base_params)
        
        # Save results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Combine all results into one dataframe
        combined = pd.concat(results, keys=results.keys())
        combined.to_csv(output_path)
        
        print(f"Results saved to {output_path}")
        print(f"\n{'='*60}")
        print("Summary Statistics:")
        print(f"{'='*60}")
        
        for solver_name, df in results.items():
            print(f"\n{solver_name.upper()}")
            print(f"  Mean Absolute Error: ${df['abs_error'].mean():.6e}")
            print(f"  Max Absolute Error:  ${df['abs_error'].max():.6e}")
            print(f"  Mean Relative Error: {df['rel_error'].mean():.4e}")
        
        print(f"\n{'='*60}\n")
        
    except Exception as e:
        print(f"Error running benchmarks: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
