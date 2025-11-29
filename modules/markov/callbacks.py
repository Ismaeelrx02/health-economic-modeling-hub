"""Markov Model Callbacks with integrated calculations"""
from dash import Input, Output
import numpy as np
from typing import Dict, List, Any, Optional

# ============================================================================
# INTEGRATED MARKOV CALCULATIONS
# ============================================================================

def calculate_markov_model(
    states: List[str],
    transition_matrix: List[List[float]],
    state_costs: Dict[str, float],
    state_utilities: Dict[str, float],
    time_horizon: int,
    cycle_length: float = 1.0,
    discount_rate_cost: float = 0.03,
    discount_rate_outcome: float = 0.03,
    starting_distribution: Optional[List[float]] = None
) -> Dict[str, Any]:
    """Calculate Markov model cohort simulation - Real matrix multiplication"""
    n_states = len(states)
    
    # Convert to numpy array
    P = np.array(transition_matrix)
    
    # Validate
    if P.shape != (n_states, n_states):
        raise ValueError(f"Matrix shape {P.shape} doesn't match {n_states} states")
    
    # Initialize distribution
    if starting_distribution is None:
        state_distribution = np.zeros(n_states)
        state_distribution[0] = 1.0
    else:
        state_distribution = np.array(starting_distribution)
    
    # Initialize trace
    trace = np.zeros((time_horizon + 1, n_states))
    trace[0] = state_distribution
    
    # Simulate cohort
    for t in range(1, time_horizon + 1):
        trace[t] = trace[t-1] @ P
    
    # Calculate costs and QALYs
    discounted_costs = []
    discounted_qalys = []
    
    for t in range(time_horizon):
        # Cycle cost
        cycle_cost = sum(
            trace[t, i] * state_costs.get(states[i], 0)
            for i in range(n_states)
        )
        
        # Cycle QALY
        cycle_qaly = sum(
            trace[t, i] * state_utilities.get(states[i], 0) * cycle_length
            for i in range(n_states)
        )
        
        # Apply discounting
        time_midpoint = (t + 0.5) * cycle_length
        discount_factor_cost = 1 / ((1 + discount_rate_cost) ** time_midpoint)
        discount_factor_outcome = 1 / ((1 + discount_rate_outcome) ** time_midpoint)
        
        discounted_costs.append(cycle_cost * discount_factor_cost)
        discounted_qalys.append(cycle_qaly * discount_factor_outcome)
    
    return {
        'total_cost': sum(discounted_costs),
        'total_qalys': sum(discounted_qalys),
        'trace': trace.tolist(),
        'costs_per_cycle': discounted_costs,
        'qalys_per_cycle': discounted_qalys
    }

# ============================================================================
# DASH CALLBACKS
# ============================================================================

def register_callbacks(app):
    """Register Markov model callbacks"""
    pass
