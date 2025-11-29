"""
CrewAI Tasks for Health Economics Analysis
Defines specific tasks that agents perform
"""
from crewai import Task
from typing import Dict, Any, Optional


class HealthEconTasks:
    """Factory class for creating health economics tasks"""
    
    @staticmethod
    def parse_query_task(agent, user_query: str, ai_mode: str) -> Task:
        """Task to parse user query and extract requirements"""
        return Task(
            description=f"""
            Analyze the following user query and extract structured information:
            
            Query: "{user_query}"
            AI Mode: {ai_mode}
            
            Extract and structure the following information:
            1. Disease area / health condition
            2. Intervention being evaluated
            3. Comparator(s)
            4. Target population
            5. Recommended model type (decision tree, Markov, PSM)
            6. Analysis perspective (healthcare system, societal, etc.)
            7. Time horizon
            8. Any specific requirements or constraints
            
            Provide a clear summary of the analysis objectives.
            """,
            agent=agent,
            expected_output="""A structured JSON with: disease_area, intervention, 
            comparator, model_type, time_horizon, perspective, project_name, summary"""
        )
    
    @staticmethod
    def literature_research_task(agent, disease_area: str, intervention: str, 
                                 comparator: str, model_type: str) -> Task:
        """Task to research literature and find parameter estimates"""
        return Task(
            description=f"""
            Conduct a literature search for health economics model parameters:
            
            Disease Area: {disease_area}
            Intervention: {intervention}
            Comparator: {comparator}
            Model Type: {model_type}
            
            Find and synthesize evidence for:
            1. Clinical efficacy (relative risks, hazard ratios, response rates)
            2. Utility values (EQ-5D, SF-6D) for health states
            3. Cost estimates (intervention costs, healthcare utilization, adverse events)
            4. Transition probabilities (if Markov model)
            5. Survival parameters (if PSM model)
            6. Patient characteristics (age, baseline risk)
            
            For each parameter:
            - Provide point estimate
            - Provide uncertainty range (95% CI or SD)
            - Cite source (author, year, journal)
            - Assess quality (high/moderate/low)
            
            Flag any missing critical parameters.
            """,
            agent=agent,
            expected_output="""A structured dataset of parameters with point estimates, 
            uncertainty, sources, and quality ratings. List of missing parameters."""
        )
    
    @staticmethod
    def build_model_task(agent, model_type: str, disease_area: str, 
                        parameters: Dict[str, Any], ai_mode: str) -> Task:
        """Task to build model structure"""
        return Task(
            description=f"""
            Build a {model_type} model structure for {disease_area} analysis:
            
            Model Type: {model_type}
            Disease Area: {disease_area}
            AI Mode: {ai_mode}
            Available Parameters: {len(parameters)} parameters
            
            For Decision Tree:
            - Define decision nodes, chance nodes, and terminal nodes
            - Specify probabilities and outcomes
            - Structure the tree logically
            
            For Markov Model:
            - Define health states
            - Create transition probability matrix
            - Specify cycle length
            - Define absorbing states
            
            For PSM Model:
            - Define health states (PF, PD, Dead)
            - Specify survival distributions
            - Define treatment duration
            
            Populate the structure with available parameters.
            If AI mode is 'ai-augmented' or 'ai-automated', auto-fill missing parameters.
            If AI mode is 'ai-assisted', flag missing parameters for user input.
            """,
            agent=agent,
            expected_output="""Complete model structure as nested dict/JSON with all 
            states, transitions, parameters populated. List of suggestions for user."""
        )
    
    @staticmethod
    def validation_task(agent, model_structure: Dict[str, Any], 
                       parameters: Dict[str, Any], model_type: str) -> Task:
        """Task to validate model and parameters"""
        return Task(
            description=f"""
            Validate the {model_type} model for errors and issues:
            
            Model Structure: {model_structure}
            Parameters: {parameters}
            
            Check for:
            1. Mathematical consistency
               - Probabilities sum to 1.0
               - Rates are non-negative
               - Utilities between 0 and 1
            
            2. Clinical plausibility
               - Transition rates reasonable for disease
               - Costs realistic
               - Utilities aligned with health states
            
            3. Completeness
               - All required parameters present
               - No missing data
               - All states connected
            
            4. Best practices
               - Appropriate cycle length
               - Half-cycle correction applied
               - Discount rates standard (3-5%)
            
            Generate:
            - List of errors (must fix)
            - List of warnings (should review)
            - List of suggestions (optional improvements)
            - Overall validation status (pass/fail/review)
            """,
            agent=agent,
            expected_output="""Validation report with errors, warnings, suggestions, 
            and overall status. Flag has_warnings boolean."""
        )
    
    @staticmethod
    def base_case_analysis_task(agent, model_type: str, model_structure: Dict[str, Any],
                                parameters: Dict[str, Any]) -> Task:
        """Task to run base case analysis"""
        return Task(
            description=f"""
            Execute base case analysis for {model_type} model:
            
            Model: {model_structure}
            Parameters: {parameters}
            
            Calculate:
            1. Total costs (intervention vs comparator)
            2. Total QALYs (intervention vs comparator)
            3. Incremental costs (difference)
            4. Incremental QALYs (difference)
            5. ICER (incremental cost per QALY)
            6. NMB at WTP threshold ($50,000/QALY)
            
            Apply:
            - Discounting (3% for costs and outcomes)
            - Half-cycle correction (if Markov)
            - Proper time horizon
            
            Generate results table with deterministic results.
            """,
            agent=agent,
            expected_output="""Results dict with costs, QALYs, incremental values, 
            ICER, NMB for intervention and comparator."""
        )
    
    @staticmethod
    def dsa_task(agent, base_case_results: Dict[str, Any], 
                parameters: Dict[str, Any]) -> Task:
        """Task to run deterministic sensitivity analysis"""
        return Task(
            description=f"""
            Perform one-way deterministic sensitivity analysis:
            
            Base Case Results: {base_case_results}
            Parameters: {parameters}
            
            For each uncertain parameter:
            1. Identify reasonable range (±20% or confidence interval)
            2. Calculate ICER at low value
            3. Calculate ICER at high value
            4. Calculate range of ICER variation
            
            Rank parameters by impact on ICER (tornado diagram data).
            
            Test at minimum:
            - Utility values
            - Cost estimates  
            - Efficacy parameters
            - Discount rates
            
            Generate tornado diagram data sorted by impact.
            """,
            agent=agent,
            expected_output="""DSA results with parameter ranges, ICER ranges, and 
            tornado diagram data sorted by impact."""
        )
    
    @staticmethod
    def psa_task(agent, base_case_results: Dict[str, Any], 
                parameters: Dict[str, Any], n_simulations: int = 1000) -> Task:
        """Task to run probabilistic sensitivity analysis"""
        return Task(
            description=f"""
            Perform probabilistic sensitivity analysis with {n_simulations} iterations:
            
            Base Case: {base_case_results}
            Parameters: {parameters}
            
            For each parameter:
            1. Define appropriate distribution (beta for utilities/probabilities, 
               gamma for costs, lognormal for relative risks)
            2. Sample from distributions
            3. Run model iteration
            4. Store costs and QALYs
            
            Calculate:
            1. Mean costs and QALYs
            2. 95% credible intervals
            3. Cost-effectiveness plane scatter plot data
            4. CEAC (cost-effectiveness acceptability curve) data
               - Test WTP thresholds from $0 to $150,000
               - Calculate probability cost-effective at each threshold
            
            Generate PSA summary statistics and chart data.
            """,
            agent=agent,
            expected_output="""PSA results with simulations array, summary stats, 
            scatter plot data, and CEAC data."""
        )
    
    @staticmethod
    def report_generation_task(agent, project_name: str, model_type: str,
                               base_case_results: Optional[Dict],
                               dsa_results: Optional[Dict],
                               psa_results: Optional[Dict],
                               literature_evidence: list) -> Task:
        """Task to generate comprehensive report"""
        return Task(
            description=f"""
            Generate a comprehensive health economic analysis report:
            
            Project: {project_name}
            Model Type: {model_type}
            
            Report Structure (following CHEERS guidelines):
            
            1. EXECUTIVE SUMMARY
               - Research question
               - Model type
               - Key results (ICER, decision)
            
            2. BACKGROUND
               - Disease area
               - Intervention and comparator
               - Analysis rationale
            
            3. METHODS
               - Model structure description
               - Data sources
               - Parameters (table)
               - Analysis perspective
               - Time horizon
               - Discounting
            
            4. RESULTS
               - Base case results (table)
               - Cost-effectiveness interpretation
               - DSA results (if available)
               - PSA results (if available)
            
            5. DISCUSSION
               - Key findings
               - Comparison to published studies
               - Limitations
               - Implications
            
            6. CONCLUSION
               - Recommendation
               - Value for money assessment
            
            Use professional language. Include all numerical results.
            Cite literature sources: {len(literature_evidence)} sources available.
            """,
            agent=agent,
            expected_output="""Complete markdown report following CHEERS structure 
            with all sections, tables, and interpretations."""
        )
