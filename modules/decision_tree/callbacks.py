"""Decision Tree Callbacks with integrated calculations"""
from dash import Input, Output
import numpy as np
from typing import Dict, List, Any

# ============================================================================
# INTEGRATED DECISION TREE CALCULATIONS
# ============================================================================

def calculate_decision_tree(
    tree_structure: Dict[str, Any],
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate expected values for a decision tree - recursive evaluation"""
    
    def calculate_node(node: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively calculate expected values for a node"""
        node_type = node.get('type', 'chance')
        
        if node_type == 'terminal':
            return {
                'cost': node.get('cost', 0),
                'utility': node.get('utility', 0),
                'qaly': node.get('qaly', node.get('utility', 0))
            }
        
        elif node_type == 'chance':
            branches = node.get('branches', [])
            expected_cost = 0
            expected_utility = 0
            expected_qaly = 0
            
            for branch in branches:
                probability = branch.get('probability', 0)
                branch_values = calculate_node(branch.get('node', {}))
                
                expected_cost += probability * branch_values['cost']
                expected_utility += probability * branch_values['utility']
                expected_qaly += probability * branch_values['qaly']
            
            node_cost = node.get('cost', 0)
            
            return {
                'cost': expected_cost + node_cost,
                'utility': expected_utility,
                'qaly': expected_qaly
            }
        
        elif node_type == 'decision':
            options = node.get('options', [])
            option_results = []
            
            for option in options:
                option_name = option.get('name', 'Option')
                option_values = calculate_node(option.get('node', {}))
                option_results.append({
                    'name': option_name,
                    **option_values
                })
            
            return {'options': option_results}
        
        return {}
    
    results = calculate_node(tree_structure)
    
    if 'options' in results:
        options = results['options']
        sorted_options = sorted(options, key=lambda x: x.get('cost', 0))
        
        for i in range(1, len(sorted_options)):
            prev = sorted_options[i-1]
            curr = sorted_options[i]
            
            inc_cost = curr['cost'] - prev['cost']
            inc_qaly = curr['qaly'] - prev['qaly']
            
            if inc_qaly > 0:
                icer = inc_cost / inc_qaly
            else:
                icer = float('inf') if inc_cost > 0 else float('-inf')
            
            curr['icer'] = icer
            curr['incremental_cost'] = inc_cost
            curr['incremental_qaly'] = inc_qaly
        
        results['optimal_strategy'] = max(sorted_options, key=lambda x: x.get('qaly', 0))
    
    return results

# ============================================================================
# DASH CALLBACKS
# ============================================================================

def register_callbacks(app):
    """Register decision tree callbacks"""
    pass
