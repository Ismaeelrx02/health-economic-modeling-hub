"""Analysis Callbacks - DSA, PSA, Compare with integrated calculations"""
from dash import Input, Output
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Any

# ============================================================================
# INTEGRATED CALCULATIONS (No separate calculations folder needed)
# ============================================================================

def calculate_icer(
    cost_intervention: float,
    cost_comparator: float,
    effect_intervention: float,
    effect_comparator: float
) -> Tuple[float, float, float]:
    """Calculate Incremental Cost-Effectiveness Ratio (ICER)"""
    inc_cost = cost_intervention - cost_comparator
    inc_effect = effect_intervention - effect_comparator
    
    if inc_effect == 0:
        icer = float('inf') if inc_cost > 0 else float('-inf')
    else:
        icer = inc_cost / inc_effect
    
    return icer, inc_cost, inc_effect

def calculate_nmb(cost: float, effect: float, wtp_threshold: float = 50000) -> float:
    """Calculate Net Monetary Benefit (NMB)"""
    return (effect * wtp_threshold) - cost

def discount_value(value: float, rate: float, time: float) -> float:
    """Apply discount rate to a value"""
    return value / ((1 + rate) ** time)

def calculate_qalys(
    utilities: List[float],
    durations: List[float],
    discount_rate: float = 0.03
) -> float:
    """Calculate Quality-Adjusted Life Years (QALYs)"""
    total_qalys = 0.0
    cumulative_time = 0.0
    
    for utility, duration in zip(utilities, durations):
        mid_point = cumulative_time + (duration / 2)
        discounted_utility = discount_value(utility * duration, discount_rate, mid_point)
        total_qalys += discounted_utility
        cumulative_time += duration
    
    return total_qalys

def perform_dsa(
    base_params: Dict[str, float],
    param_ranges: Dict[str, Tuple[float, float]],
    n_points: int = 10
) -> Dict[str, List[Dict[str, Any]]]:
    """Perform Deterministic Sensitivity Analysis (DSA)"""
    results = {}
    
    for param_name, (min_val, max_val) in param_ranges.items():
        param_results = []
        values = np.linspace(min_val, max_val, n_points)
        
        for value in values:
            modified_params = base_params.copy()
            modified_params[param_name] = value
            param_results.append({
                'value': float(value),
                'params': modified_params
            })
        
        results[param_name] = param_results
    
    return results

def perform_psa(
    base_params: Dict[str, float],
    param_distributions: Dict[str, Dict[str, Any]],
    n_simulations: int = 1000
) -> Dict[str, Any]:
    """Perform Probabilistic Sensitivity Analysis (PSA)"""
    simulations = []
    
    for i in range(n_simulations):
        sim_params = {}
        
        for param_name, dist_info in param_distributions.items():
            dist_type = dist_info.get('dist', 'normal')
            
            if dist_type == 'normal':
                value = np.random.normal(
                    dist_info.get('mean', base_params.get(param_name, 0)),
                    dist_info.get('sd', 0.1)
                )
            elif dist_type == 'beta':
                value = np.random.beta(
                    dist_info.get('alpha', 2),
                    dist_info.get('beta', 2)
                )
            elif dist_type == 'gamma':
                value = np.random.gamma(
                    dist_info.get('shape', 2),
                    dist_info.get('scale', 1)
                )
            else:
                value = base_params.get(param_name, 0)
            
            sim_params[param_name] = float(value)
        
        simulations.append(sim_params)
    
    return {
        'simulations': simulations,
        'n_simulations': n_simulations
    }

def calculate_ceac(
    costs: List[float],
    effects: List[float],
    wtp_range: Tuple[float, float] = (0, 100000),
    n_points: int = 100
) -> List[Dict[str, float]]:
    """Calculate Cost-Effectiveness Acceptability Curve (CEAC)"""
    wtp_thresholds = np.linspace(wtp_range[0], wtp_range[1], n_points)
    ceac_data = []
    
    costs_array = np.array(costs)
    effects_array = np.array(effects)
    
    for wtp in wtp_thresholds:
        nmbs = (effects_array * wtp) - costs_array
        prob_cost_effective = np.mean(nmbs > 0)
        
        ceac_data.append({
            'wtp': float(wtp),
            'probability': float(prob_cost_effective)
        })
    
    return ceac_data

# ============================================================================
# DASH CALLBACKS
# ============================================================================

def register_callbacks(app):
    """Register analysis callbacks"""
    pass
