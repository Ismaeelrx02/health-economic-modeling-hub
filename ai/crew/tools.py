"""
Custom Tools for Health Economics Agents
Provides specialized capabilities for agents
"""
from crewai_tools import BaseTool
from typing import Dict, Any, List, Optional
import numpy as np
from scipy import stats
import json


class LiteratureSearchTool(BaseTool):
    """Tool for searching health economics literature"""
    
    name: str = "Literature Search Tool"
    description: str = """Search health economics literature for parameters. 
    Input should be a JSON with: disease_area, intervention, comparator, parameter_type.
    Returns relevant studies with parameter estimates."""
    
    def _run(self, query: str) -> str:
        """
        Search literature databases
        
        Note: In production, this would integrate with:
        - PubMed API
        - Cochrane Library
        - Cost-Effectiveness Analysis Registry
        - NICE Evidence Search
        """
        try:
            query_dict = json.loads(query) if isinstance(query, str) else query
            
            # Mock literature search results
            # In production, replace with actual API calls
            mock_results = {
                'parameters': {
                    'intervention_efficacy_rr': {
                        'value': 0.75,
                        'ci': [0.65, 0.85],
                        'source': 'Smith et al. 2023, NEJM',
                        'quality': 'high'
                    },
                    'utility_healthy': {
                        'value': 0.85,
                        'ci': [0.80, 0.90],
                        'source': 'Jones et al. 2022, Value in Health',
                        'quality': 'moderate'
                    },
                    'utility_diseased': {
                        'value': 0.65,
                        'ci': [0.58, 0.72],
                        'source': 'Brown et al. 2021, Pharmacoeconomics',
                        'quality': 'moderate'
                    },
                    'intervention_cost_annual': {
                        'value': 15000,
                        'ci': [12000, 18000],
                        'source': 'Medicare Fee Schedule 2023',
                        'quality': 'high'
                    },
                    'comparator_cost_annual': {
                        'value': 5000,
                        'ci': [4000, 6000],
                        'source': 'Medicare Fee Schedule 2023',
                        'quality': 'high'
                    }
                },
                'sources': [
                    'Smith et al. 2023, NEJM',
                    'Jones et al. 2022, Value in Health',
                    'Brown et al. 2021, Pharmacoeconomics'
                ],
                'missing_parameters': []
            }
            
            return json.dumps(mock_results)
            
        except Exception as e:
            return json.dumps({'error': str(e), 'parameters': {}})


class ParameterValidationTool(BaseTool):
    """Tool for validating model parameters"""
    
    name: str = "Parameter Validation Tool"
    description: str = """Validate health economics model parameters for consistency 
    and plausibility. Input should be JSON with model_structure and parameters."""
    
    def _run(self, input_data: str) -> str:
        """
        Validate parameters
        """
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            model_structure = data.get('model_structure', {})
            parameters = data.get('parameters', {})
            
            errors = []
            warnings = []
            suggestions = []
            
            # Check probabilities
            for key, value in parameters.items():
                if 'prob' in key.lower() or 'probability' in key.lower():
                    val = value if isinstance(value, (int, float)) else value.get('value', 0)
                    if not 0 <= val <= 1:
                        errors.append(f"Probability {key} = {val} not in [0, 1]")
                
                if 'utility' in key.lower():
                    val = value if isinstance(value, (int, float)) else value.get('value', 0)
                    if not 0 <= val <= 1:
                        errors.append(f"Utility {key} = {val} not in [0, 1]")
                    if val > 0.95:
                        warnings.append(f"Utility {key} = {val} seems very high")
                
                if 'cost' in key.lower():
                    val = value if isinstance(value, (int, float)) else value.get('value', 0)
                    if val < 0:
                        errors.append(f"Cost {key} = {val} is negative")
            
            # Check for missing critical parameters
            required_params = ['intervention_cost', 'comparator_cost', 'utility']
            for param in required_params:
                if not any(param in key.lower() for key in parameters.keys()):
                    warnings.append(f"Missing {param} parameter")
            
            # Suggestions
            if not errors and not warnings:
                suggestions.append("Model parameters look good")
            
            result = {
                'errors': errors,
                'warnings': warnings,
                'suggestions': suggestions,
                'is_valid': len(errors) == 0
            }
            
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({
                'errors': [str(e)],
                'warnings': [],
                'suggestions': [],
                'is_valid': False
            })


class CalculationTool(BaseTool):
    """Tool for health economics calculations"""
    
    name: str = "Health Economics Calculation Tool"
    description: str = """Perform health economics calculations including ICER, NMB, 
    discounting, QALY calculations. Input should be JSON with calculation type and parameters."""
    
    def _run(self, input_data: str) -> str:
        """
        Perform calculations
        """
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            calc_type = data.get('type', 'base_case')
            
            if calc_type == 'base_case':
                return self._calculate_base_case(data)
            elif calc_type == 'dsa':
                return self._calculate_dsa(data)
            elif calc_type == 'psa':
                return self._calculate_psa(data)
            else:
                return json.dumps({'error': 'Unknown calculation type'})
                
        except Exception as e:
            return json.dumps({'error': str(e)})
    
    def _calculate_base_case(self, data: Dict) -> str:
        """Calculate base case ICER"""
        params = data.get('parameters', {})
        time_horizon = data.get('time_horizon', 10)
        discount_rate = data.get('discount_rate', 0.03)
        wtp = data.get('wtp_threshold', 50000)
        
        # Mock calculation - replace with actual model execution
        intervention_cost = params.get('intervention_cost', 15000) * time_horizon
        comparator_cost = params.get('comparator_cost', 5000) * time_horizon
        intervention_qalys = params.get('utility_intervention', 0.75) * time_horizon
        comparator_qalys = params.get('utility_comparator', 0.65) * time_horizon
        
        # Apply discounting
        discount_factor = sum([1 / (1 + discount_rate) ** t for t in range(time_horizon)])
        intervention_cost *= discount_factor / time_horizon
        comparator_cost *= discount_factor / time_horizon
        intervention_qalys *= discount_factor / time_horizon
        comparator_qalys *= discount_factor / time_horizon
        
        incremental_cost = intervention_cost - comparator_cost
        incremental_qalys = intervention_qalys - comparator_qalys
        icer = incremental_cost / incremental_qalys if incremental_qalys != 0 else float('inf')
        nmb = (incremental_qalys * wtp) - incremental_cost
        
        result = {
            'intervention_cost': round(intervention_cost, 2),
            'intervention_qalys': round(intervention_qalys, 4),
            'comparator_cost': round(comparator_cost, 2),
            'comparator_qalys': round(comparator_qalys, 4),
            'incremental_cost': round(incremental_cost, 2),
            'incremental_qalys': round(incremental_qalys, 4),
            'icer': round(icer, 2),
            'nmb': round(nmb, 2)
        }
        
        return json.dumps(result)
    
    def _calculate_dsa(self, data: Dict) -> str:
        """Calculate DSA tornado data"""
        base_icer = data.get('base_icer', 30000)
        params = data.get('parameters', {})
        
        # Mock tornado data
        tornado_data = []
        for param, value in params.items():
            if isinstance(value, dict) and 'value' in value:
                base_val = value['value']
                low_val = value.get('low', base_val * 0.8)
                high_val = value.get('high', base_val * 1.2)
                
                # Mock impact calculation
                impact = abs(high_val - low_val) / base_val * base_icer * 0.2
                
                tornado_data.append({
                    'parameter': param,
                    'base_value': base_val,
                    'low_value': low_val,
                    'high_value': high_val,
                    'icer_low': base_icer - impact,
                    'icer_high': base_icer + impact,
                    'impact': impact
                })
        
        # Sort by impact
        tornado_data.sort(key=lambda x: x['impact'], reverse=True)
        
        return json.dumps({
            'tornado_data': tornado_data,
            'most_sensitive': [d['parameter'] for d in tornado_data[:5]]
        })
    
    def _calculate_psa(self, data: Dict) -> str:
        """Calculate PSA simulations"""
        n_sims = data.get('n_simulations', 1000)
        base_results = data.get('base_case', {})
        
        # Mock PSA - replace with actual simulation
        mean_cost = base_results.get('incremental_cost', 10000)
        mean_qalys = base_results.get('incremental_qalys', 0.5)
        
        costs = np.random.normal(mean_cost, mean_cost * 0.2, n_sims)
        qalys = np.random.normal(mean_qalys, mean_qalys * 0.15, n_sims)
        
        # CEAC calculation
        wtp_thresholds = np.linspace(0, 150000, 31)
        prob_ce = []
        for wtp in wtp_thresholds:
            nmb = (qalys * wtp) - costs
            prob_ce.append((nmb > 0).sum() / n_sims)
        
        result = {
            'simulations': [
                {'cost': float(c), 'qalys': float(q)} 
                for c, q in zip(costs[:100], qalys[:100])  # First 100 for size
            ],
            'scatter_data': {
                'costs': costs.tolist(),
                'qalys': qalys.tolist()
            },
            'ceac_data': {
                'wtp_thresholds': wtp_thresholds.tolist(),
                'prob_ce': prob_ce
            },
            'mean_icer': float(mean_cost / mean_qalys) if mean_qalys != 0 else 0,
            'credible_interval': [
                float(np.percentile(costs / qalys, 2.5)),
                float(np.percentile(costs / qalys, 97.5))
            ]
        }
        
        return json.dumps(result)


class ModelValidationTool(BaseTool):
    """Tool for validating model structure"""
    
    name: str = "Model Structure Validation Tool"
    description: str = """Validate health economics model structure for completeness 
    and consistency. Input should be JSON with model_type and structure."""
    
    def _run(self, input_data: str) -> str:
        """Validate model structure"""
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            model_type = data.get('model_type', 'decision_tree')
            structure = data.get('structure', {})
            
            errors = []
            warnings = []
            
            if model_type == 'markov':
                # Check for required Markov components
                if 'states' not in structure:
                    errors.append("Missing states definition")
                if 'transition_matrix' not in structure:
                    errors.append("Missing transition matrix")
                    
                # Check transition matrix sums to 1
                if 'transition_matrix' in structure:
                    matrix = structure['transition_matrix']
                    for state, transitions in matrix.items():
                        total = sum(transitions.values())
                        if not 0.99 <= total <= 1.01:
                            warnings.append(f"Transitions from {state} sum to {total}, not 1.0")
            
            return json.dumps({
                'errors': errors,
                'warnings': warnings,
                'is_valid': len(errors) == 0
            })
            
        except Exception as e:
            return json.dumps({'errors': [str(e)], 'warnings': [], 'is_valid': False})


class ReportGeneratorTool(BaseTool):
    """Tool for generating formatted reports"""
    
    name: str = "Report Generator Tool"
    description: str = """Generate health economics analysis reports in markdown format. 
    Input should be JSON with all analysis results."""
    
    def _run(self, input_data: str) -> str:
        """Generate report"""
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            # Generate markdown report
            report = f"""# Health Economic Analysis Report

## Executive Summary
**Project:** {data.get('project_name', 'Unnamed')}
**Model Type:** {data.get('model_type', 'Unknown')}
**ICER:** ${data.get('icer', 0):,.0f} per QALY

## Methods
- Model: {data.get('model_type', 'Unknown')}
- Time Horizon: {data.get('time_horizon', 'N/A')} years
- Discount Rate: {data.get('discount_rate', 0.03) * 100}%

## Results
### Base Case
- Incremental Cost: ${data.get('incremental_cost', 0):,.2f}
- Incremental QALYs: {data.get('incremental_qalys', 0):.4f}
- ICER: ${data.get('icer', 0):,.2f} per QALY
- NMB: ${data.get('nmb', 0):,.2f}

## Conclusion
The intervention is {'cost-effective' if data.get('nmb', 0) > 0 else 'not cost-effective'} 
at a willingness-to-pay threshold of ${data.get('wtp', 50000):,.0f} per QALY.
"""
            
            return report
            
        except Exception as e:
            return f"Error generating report: {str(e)}"


class HealthEconTools:
    """Factory for health economics tools"""
    
    @staticmethod
    def literature_search_tool() -> LiteratureSearchTool:
        return LiteratureSearchTool()
    
    @staticmethod
    def parameter_validation_tool() -> ParameterValidationTool:
        return ParameterValidationTool()
    
    @staticmethod
    def calculation_tool() -> CalculationTool:
        return CalculationTool()
    
    @staticmethod
    def model_validation_tool() -> ModelValidationTool:
        return ModelValidationTool()
    
    @staticmethod
    def report_generator_tool() -> ReportGeneratorTool:
        return ReportGeneratorTool()
