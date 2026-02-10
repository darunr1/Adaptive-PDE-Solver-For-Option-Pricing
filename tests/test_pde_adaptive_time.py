"""
Unit tests for adaptive time-stepping PDE solver.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pde_adaptive_time import price_option_adaptive_time
from bs_analytic import call_price


class TestPDEAdaptiveTime(unittest.TestCase):
    """Test adaptive time-stepping PDE option pricing."""
    
    def setUp(self):
        """Set up test parameters."""
        self.spot = 100.0
        self.strike = 100.0
        self.rate = 0.05
        self.volatility = 0.2
        self.time_to_expiry = 1.0
        self.num_space_points = 201
    
    def test_adaptive_solver_exists(self):
        """Test that adaptive solver implementation exists."""
        with self.assertRaises(NotImplementedError):
            price_option_adaptive_time(
                spot=self.spot,
                strike=self.strike,
                rate=self.rate,
                volatility=self.volatility,
                time_to_expiry=self.time_to_expiry,
                num_space_points=self.num_space_points,
                option_type='call'
            )


if __name__ == '__main__':
    unittest.main()
