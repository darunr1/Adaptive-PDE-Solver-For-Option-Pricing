from __future__ import annotations

import math
from typing import Literal, Dict, Any, Tuple

import numpy as np

from .config import DEFAULT_PRICE_STEPS, DEFAULT_TIME_STEPS, S_MAX_MULTIPLIER
from .utils import validate_option_inputs

OptionType = Literal["call", "put"]


def _thomas_solve(lower: np.ndarray, diag: np.ndarray, upper: np.ndarray, rhs: np.ndarray) -> np.ndarray:

    n = diag.size
    if rhs.size != n:
        raise ValueError("rhs length must match diag length")

    c = upper.astype(float).copy()
    d = diag.astype(float).copy()
    b = lower.astype(float).copy()
    y = rhs.astype(float).copy()

    for i in range(1, n):
        w = b[i - 1] / d[i - 1]
        d[i] -= w * c[i - 1]
        y[i] -= w * y[i - 1]

    x = np.empty(n, dtype=float)
    x[-1] = y[-1] / d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (y[i] - c[i] * x[i + 1]) / d[i]

    return x


def price_european_fixed_grid(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: OptionType = "call",
    M: int | None = None,
    N: int | None = None,
    Smax: float | None = None,
    return_grid: bool = False,
) -> float | Tuple[float, Dict[str, Any]]:
   
    validate_option_inputs(S0, K, T, sigma)
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")

    M = int(M if M is not None else DEFAULT_PRICE_STEPS)
    N = int(N if N is not None else DEFAULT_TIME_STEPS)
    if M < 3 or N < 1:
        raise ValueError("Need M >= 3 and N >= 1 for a meaningful grid")

    Smax = float(Smax if Smax is not None else (S_MAX_MULTIPLIER * K))
    if Smax <= S0:
        Smax = max(Smax, 1.5 * S0)

    dS = Smax / M
    dt = T / N 

    S = np.linspace(0.0, Smax, M + 1)

    if option_type == "call":
        V = np.maximum(S - K, 0.0)
    else:
        V = np.maximum(K - S, 0.0)

    i = np.arange(1, M)  
    S_i = S[i]

    alpha = 0.5 * sigma * sigma * S_i * S_i
    beta = r * S_i

    A = alpha / (dS * dS) - beta / (2.0 * dS)
    B = -2.0 * alpha / (dS * dS) - r
    C = alpha / (dS * dS) + beta / (2.0 * dS)

   
    lower_L = -0.5 * dt * A[1:]              
    diag_L = 1.0 - 0.5 * dt * B              
    upper_L = -0.5 * dt * C[:-1]             

    lower_R = 0.5 * dt * A[1:]               
    diag_R = 1.0 + 0.5 * dt * B              
    upper_R = 0.5 * dt * C[:-1]              

    surface = None
    if return_grid:
        surface = np.empty((N + 1, M + 1), dtype=float)
        surface[0, :] = V  

    for n in range(N):
        tau_n = n * dt
        tau_np1 = (n + 1) * dt

        if option_type == "call":
            V0_n = 0.0
            VM_n = Smax - K * math.exp(-r * tau_n)
            V0_np1 = 0.0
            VM_np1 = Smax - K * math.exp(-r * tau_np1)
        else:
            V0_n = K * math.exp(-r * tau_n)
            VM_n = 0.0
            V0_np1 = K * math.exp(-r * tau_np1)
            VM_np1 = 0.0

        V[0] = V0_n
        V[M] = VM_n

        V_in = V[1:M]  
        rhs = diag_R * V_in
        rhs[1:] += lower_R * V_in[:-1]
        rhs[:-1] += upper_R * V_in[1:]

        rhs[0] += 0.5 * dt * A[0] * (V0_n + V0_np1)
        rhs[-1] += 0.5 * dt * C[-1] * (VM_n + VM_np1)

        V_new_in = _thomas_solve(lower_L, diag_L, upper_L, rhs)

        V[0] = V0_np1
        V[1:M] = V_new_in
        V[M] = VM_np1

        if return_grid:
            surface[n + 1, :] = V

    price = float(np.interp(S0, S, V))

    if not return_grid:
        return price

    info: Dict[str, Any] = {
        "S_grid": S,
        "V_tau_T": V.copy(),       
        "dS": dS,
        "dt": dt,
        "M": M,
        "N": N,
        "Smax": Smax,
        "surface": surface,        
    }
    return price, info