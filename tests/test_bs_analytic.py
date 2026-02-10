"""
Unit tests for Black-Scholes analytical solution.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bs_analytic import call_price, put_price, option_delta, option_gamma


class TestBlackScholesAnalytic(unittest.TestCase):
    """Test Black-Scholes analytical option pricing."""
    
    def setUp(self):
        """Set up test parameters."""
        self.spot = 100.0
        self.strike = 100.0
        self.rate = 0.05
        self.volatility = 0.2
        self.time_to_expiry = 1.0
    
    def test_call_price_atm(self):
        """Test call price at-the-money."""
        price = call_price(
            spot=self.spot,
            strike=self.strike,
            rate=self.rate,
            volatility=self.volatility,
            time_to_expiry=self.time_to_expiry
        )
        # ATM call should be positive
        self.assertGreater(price, 0)
        # ATM call should be less than spot - strike * exp(-r*T)
        self.assertLess(price, self.spot)
    
    def test_put_call_parity(self):
        """Test put-call parity: C - P = S - K*exp(-rT)."""
        call = call_price(
            spot=self.spot,
            strike=self.strike,
            rate=self.rate,
            volatility=self.volatility,
            time_to_expiry=self.time_to_expiry
        )
        put = put_price(
            spot=self.spot,
            strike=self.strike,
            rate=self.rate,
            volatility=self.volatility,
            time_to_expiry=self.time_to_expiry
        )
        
        lhs = call - put
        rhs = self.spot - self.strike * np.exp(-self.rate * self.time_to_expiry)
        
        np.testing.assert_almost_equal(lhs, rhs, decimal=5)
    
    def test_call_intrinsic_value(self):
        """Test that call price >= intrinsic value."""
        price = call_price(
            spot=self.spot,
            strike=self.strike,
            rate=self.rate,
            volatility=self.volatility,
            time_to_expiry=self.time_to_expiry
        )
        intrinsic = max(self.spot - self.strike, 0)
        self.assertGreaterEqual(price, intrinsic)
    
    def test_delta_range(self):
        """Test that delta is between 0 and 1 for call."""
        delta = option_delta(
            spot=self.spot,
            strike=self.strike,
            rate=self.rate,
            volatility=self.volatility,
            time_to_expiry=self.time_to_expiry,
            option_type='call'
        )
        self.assertGreater(delta, 0)
        self.assertLess(delta, 1)
    
    def test_gamma_positive(self):
        """Test that gamma is always positive."""
        gamma = option_gamma(
            spot=self.spot,
            strike=self.strike,
            volatility=self.volatility,
            time_to_expiry=self.time_to_expiry
        )
        self.assertGreater(gamma, 0)


if __name__ == '__main__':
    unittest.main()
