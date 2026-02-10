"""
Unit tests for fixed-grid PDE solver.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pde_fixed_grid import price_option_fixed_grid
from bs_analytic import call_price, put_price


class TestPDEFixedGrid(unittest.TestCase):
    """Test fixed-grid PDE option pricing."""
    
    def setUp(self):
        """Set up test parameters."""
        self.spot = 100.0
        self.strike = 100.0
        self.rate = 0.05
        self.volatility = 0.2
        self.time_to_expiry = 1.0
        self.num_space_points = 201
    
    def test_call_price_reasonable(self):
        """Test that solver produces reasonable option prices."""
        try:
            price = price_option_fixed_grid(
                spot=self.spot,
                strike=self.strike,
                rate=self.rate,
                volatility=self.volatility,
                time_to_expiry=self.time_to_expiry,
                num_space_points=self.num_space_points,
                option_type='call'
            )
            # Price should be positive and less than spot
            self.assertGreater(price, 0)
            self.assertLess(price, self.spot)
        except NotImplementedError:
            self.skipTest("PDE fixed grid solver not yet implemented")
    
    def test_convergence_with_grid_refinement(self):
        """Test that error decreases with grid refinement."""
        try:
            bs_price = call_price(
                spot=self.spot,
                strike=self.strike,
                rate=self.rate,
                volatility=self.volatility,
                time_to_expiry=self.time_to_expiry
            )
            
            errors = []
            for num_points in [51, 101, 201]:
                price = price_option_fixed_grid(
                    spot=self.spot,
                    strike=self.strike,
                    rate=self.rate,
                    volatility=self.volatility,
                    time_to_expiry=self.time_to_expiry,
                    num_space_points=num_points,
                    option_type='call'
                )
                error = abs(price - bs_price)
                errors.append(error)
            
            # Errors should generally decrease
            self.assertGreater(errors[0], errors[-1])
        except NotImplementedError:
            self.skipTest("PDE fixed grid solver not yet implemented")


if __name__ == '__main__':
    unittest.main()
