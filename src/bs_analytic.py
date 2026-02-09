from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, Tuple

from scipy.stats import norm


OptionType = Literal["call", "put"]


def _validate_inputs(S0: float, K: float, T: float, r: float, sigma: float) -> None:
    """Basic input checks to avoid silent bugs."""
    if S0 <= 0:
        raise ValueError("S0 (spot price) must be > 0")
    if K <= 0:
        raise ValueError("K (strike) must be > 0")
    if T <= 0:
        raise ValueError("T (time to maturity, years) must be > 0")
    if sigma <= 0:
        raise ValueError("sigma (volatility) must be > 0")

def _d1_d2(S0: float, K: float, T: float, r: float, sigma: float) -> Tuple[float, float]:
    """
    Compute Black–Scholes d1 and d2.
    """
    _validate_inputs(S0, K, T, r, sigma)

    denom = sigma * math.sqrt(T)
    d1 = (math.log(S0 / K) + (r + 0.5 * sigma * sigma) * T) / denom
    d2 = d1 - denom
    return d1, d2


def bs_price(S0: float, K: float, T: float, r: float, sigma: float, option_type: OptionType) -> float:

    d1, d2 = _d1_d2(S0, K, T, r, sigma)
    disc = math.exp(-r * T)

    if option_type == "call":
        return S0 * norm.cdf(d1) - K * disc * norm.cdf(d2)
    elif option_type == "put":
        return K * disc * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")


def bs_call_price(S0: float, K: float, T: float, r: float, sigma: float) -> float:
    return bs_price(S0, K, T, r, sigma, "call")


def bs_put_price(S0: float, K: float, T: float, r: float, sigma: float) -> float:
    return bs_price(S0, K, T, r, sigma, "put")


@dataclass(frozen=True)
class Greeks:
    delta: float
    gamma: float
    vega: float


def bs_greeks(S0: float, K: float, T: float, r: float, sigma: float, option_type: OptionType) -> Greeks:
    d1, d2 = _d1_d2(S0, K, T, r, sigma)

    pdf_d1 = norm.pdf(d1) 
    sqrtT = math.sqrt(T)

    gamma = pdf_d1 / (S0 * sigma * sqrtT)

    vega = S0 * pdf_d1 * sqrtT

    if option_type == "call":
        delta = norm.cdf(d1)
    elif option_type == "put":
        delta = norm.cdf(d1) - 1.0
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return Greeks(delta=delta, gamma=gamma, vega=vega)


def call_put_parity_error(S0: float, K: float, T: float, r: float, sigma: float) -> float:
    C = bs_call_price(S0, K, T, r, sigma)
    P = bs_put_price(S0, K, T, r, sigma)
    parity_rhs = S0 - K * math.exp(-r * T)
    return abs((C - P) - parity_rhs)


if __name__ == "__main__":
    S0, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    call = bs_call_price(S0, K, T, r, sigma)
    put = bs_put_price(S0, K, T, r, sigma)
    greeks_call = bs_greeks(S0, K, T, r, sigma, "call")
    parity_err = call_put_parity_error(S0, K, T, r, sigma)

    print(f"Call price: {call:.6f}")
    print(f"Put price : {put:.6f}")
    print(f"Call Greeks: delta={greeks_call.delta:.6f}, gamma={greeks_call.gamma:.6f}, vega={greeks_call.vega:.6f}")
    print(f"Call-put parity abs error: {parity_err:.12f}")
