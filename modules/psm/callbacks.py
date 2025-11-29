"""PSM Callbacks with integrated calculations"""
from dash import Input, Output
import numpy as np
from scipy.stats import lognorm
from typing import Dict, List, Any

# ============================================================================
# INTEGRATED PSM CALCULATIONS
# ============================================================================

def weibull_survival(t: float, shape: float, scale: float) -> float:
    """Weibull survival function"""
    return np.exp(-((t / scale) ** shape))

def exponential_survival(t: float, rate: float) -> float:
    """Exponential survival function"""
    return np.exp(-rate * t)

def lognormal_survival(t: float, mu: float, sigma: float) -> float:
    """Log-normal survival function"""
    return float(1 - lognorm.cdf(t, s=sigma, scale=np.exp(mu)))

def gompertz_survival(t: float, shape: float, rate: float) -> float:
    """Gompertz survival function"""
    return np.exp((rate / shape) * (1 - np.exp(shape * t)))

def calculate_survival_curve(
    distribution: str,
    params: Dict[str, float],
    time_points: List[float]
) -> List[float]:
    """Calculate survival probabilities at time points"""
    survival_probs = []
    
    for t in time_points:
        if distribution == 'weibull':
            prob = weibull_survival(t, params.get('shape', 1), params.get('scale', 1))
        elif distribution == 'exponential':
            prob = exponential_survival(t, params.get('rate', 0.1))
        elif distribution == 'lognormal':
            prob = lognormal_survival(t, params.get('mu', 0), params.get('sigma', 1))
        elif distribution == 'gompertz':
            prob = gompertz_survival(t, params.get('shape', 0.1), params.get('rate', 0.1))
        else:
            prob = 1.0
        
        survival_probs.append(float(prob))
    
    return survival_probs

def calculate_psm_model(
    survival_curves: Dict[str, Any],
    treatment_costs: Dict[str, float],
    utilities: Dict[str, float],
    time_horizon: int = 20,
    discount_rate_cost: float = 0.03,
    discount_rate_outcome: float = 0.03,
    time_step: float = 1/12
) -> Dict[str, Any]:
    """Calculate Partitioned Survival Model - Area under survival curves"""
    # Time points
    time_points = list(np.arange(0, time_horizon + time_step, time_step))
    
    # PFS and OS curves
    pfs_curve = survival_curves.get('pfs', {})
    os_curve = survival_curves.get('os', {})
    
    pfs_probs = calculate_survival_curve(
        pfs_curve.get('distribution', 'weibull'),
        pfs_curve.get('params', {}),
        time_points
    )
    
    os_probs = calculate_survival_curve(
        os_curve.get('distribution', 'weibull'),
        os_curve.get('params', {}),
        time_points
    )
    
    # State membership (PF, PD, Dead)
    pf_state = np.array(pfs_probs)
    pd_state = np.array(os_probs) - np.array(pfs_probs)
    
    # Calculate QALYs and costs
    total_cost = 0
    total_qalys = 0
    
    for i in range(len(time_points) - 1):
        time = time_points[i]
        
        # State membership at this cycle
        pf_prop = float(pf_state[i])
        pd_prop = float(pd_state[i])
        
        # Costs and utilities
        cycle_cost = (
            pf_prop * treatment_costs.get('PF', 0) +
            pd_prop * treatment_costs.get('PD', 0)
        ) * time_step
        
        cycle_qaly = (
            pf_prop * utilities.get('PF', 0) +
            pd_prop * utilities.get('PD', 0)
        ) * time_step
        
        # Apply discounting
        discount_factor_cost = 1 / ((1 + discount_rate_cost) ** time)
        discount_factor_outcome = 1 / ((1 + discount_rate_outcome) ** time)
        
        total_cost += cycle_cost * discount_factor_cost
        total_qalys += cycle_qaly * discount_factor_outcome
    
    return {
        'total_cost': total_cost,
        'total_qalys': total_qalys,
        'pfs_curve': pfs_probs,
        'os_curve': os_probs,
        'time_points': time_points
    }

# ============================================================================
# DASH CALLBACKS
# ============================================================================

def register_callbacks(app):
    """Register PSM callbacks"""
    pass
