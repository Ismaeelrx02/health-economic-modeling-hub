"""
Health Economics Crew Orchestration
Coordinates agents and tasks for complete workflow
"""
from crewai import Crew, Process
from typing import Dict, Any, Optional
import json

from .agents import HealthEconAgents
from .tasks import HealthEconTasks
from .tools import HealthEconTools


class HealthEconCrew:
    """
    Orchestrates CrewAI agents and tasks for health economics analysis
    """
    
    def __init__(self, ai_mode: str = "ai-assisted"):
        """
        Initialize the crew with specified AI mode
        
        Args:
            ai_mode: One of 'ai-assisted', 'ai-augmented', 'ai-automated'
        """
        self.ai_mode = ai_mode
        self.agents = HealthEconAgents()
        self.tools = HealthEconTools()
        
    def run_parse_query_task(self, user_query: str) -> Dict[str, Any]:
        """
        Parse user query and extract requirements
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Structured requirements dictionary
        """
        agent = self.agents.query_parser_agent()
        task = HealthEconTasks.parse_query_task(agent, user_query, self.ai_mode)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse result into structured format
        try:
            if isinstance(result, str):
                parsed = self._extract_json_from_text(result)
            else:
                parsed = result
            
            return {
                'disease_area': parsed.get('disease_area', ''),
                'intervention': parsed.get('intervention', ''),
                'comparator': parsed.get('comparator', ''),
                'model_type': parsed.get('model_type', 'decision_tree'),
                'time_horizon': parsed.get('time_horizon', 10),
                'perspective': parsed.get('perspective', 'healthcare_system'),
                'project_name': parsed.get('project_name', 'Unnamed Project'),
                'summary': parsed.get('summary', user_query),
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'raw_output': str(result)
            }
    
    def run_literature_research_task(self, disease_area: str, intervention: str,
                                     comparator: str, model_type: str) -> Dict[str, Any]:
        """
        Research literature for parameter estimates
        
        Returns:
            Dictionary with parameters, sources, and missing data
        """
        agent = self.agents.literature_researcher_agent()
        
        # Assign literature search tool
        agent.tools = [self.tools.literature_search_tool()]
        
        task = HealthEconTasks.literature_research_task(
            agent, disease_area, intervention, comparator, model_type
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        try:
            parsed = self._extract_json_from_text(str(result))
            return {
                'parameters': parsed.get('parameters', {}),
                'sources': parsed.get('sources', []),
                'missing_parameters': parsed.get('missing_parameters', []),
                'quality_assessment': parsed.get('quality', 'moderate'),
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'parameters': {},
                'sources': [],
                'missing_parameters': []
            }
    
    def run_build_model_task(self, model_type: str, disease_area: str,
                            parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build model structure with available parameters
        
        Returns:
            Model structure and parameter suggestions
        """
        agent = self.agents.model_builder_agent()
        agent.tools = [self.tools.model_validation_tool()]
        
        task = HealthEconTasks.build_model_task(
            agent, model_type, disease_area, parameters, self.ai_mode
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        try:
            parsed = self._extract_json_from_text(str(result))
            return {
                'model_structure': parsed.get('structure', {}),
                'suggestions': parsed.get('suggestions', []),
                'auto_filled': parsed.get('auto_filled', []),
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'model_structure': {},
                'suggestions': []
            }
    
    def run_validation_task(self, model_structure: Dict[str, Any],
                           parameters: Dict[str, Any], model_type: str) -> Dict[str, Any]:
        """
        Validate model and parameters
        
        Returns:
            Validation results with errors, warnings, suggestions
        """
        agent = self.agents.parameter_validator_agent()
        agent.tools = [self.tools.parameter_validation_tool()]
        
        task = HealthEconTasks.validation_task(
            agent, model_structure, parameters, model_type
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        try:
            parsed = self._extract_json_from_text(str(result))
            return {
                'errors': parsed.get('errors', []),
                'warnings': parsed.get('warnings', []),
                'suggestions': parsed.get('suggestions', []),
                'is_valid': len(parsed.get('errors', [])) == 0,
                'has_warnings': len(parsed.get('warnings', [])) > 0,
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'errors': [str(e)],
                'warnings': [],
                'suggestions': [],
                'is_valid': False,
                'has_warnings': True
            }
    
    def run_base_case_analysis_task(self, model_type: str, model_structure: Dict[str, Any],
                                    parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute base case analysis
        
        Returns:
            Costs, QALYs, ICER, NMB
        """
        agent = self.agents.analysis_executor_agent()
        agent.tools = [self.tools.calculation_tool()]
        
        task = HealthEconTasks.base_case_analysis_task(
            agent, model_type, model_structure, parameters
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        try:
            parsed = self._extract_json_from_text(str(result))
            return {
                'intervention_cost': parsed.get('intervention_cost', 0),
                'intervention_qalys': parsed.get('intervention_qalys', 0),
                'comparator_cost': parsed.get('comparator_cost', 0),
                'comparator_qalys': parsed.get('comparator_qalys', 0),
                'incremental_cost': parsed.get('incremental_cost', 0),
                'incremental_qalys': parsed.get('incremental_qalys', 0),
                'icer': parsed.get('icer', 0),
                'nmb': parsed.get('nmb', 0),
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'intervention_cost': 0,
                'intervention_qalys': 0,
                'comparator_cost': 0,
                'comparator_qalys': 0,
                'incremental_cost': 0,
                'incremental_qalys': 0,
                'icer': 0,
                'nmb': 0
            }
    
    def run_dsa_task(self, base_case_results: Dict[str, Any],
                    parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute deterministic sensitivity analysis
        
        Returns:
            Tornado diagram data
        """
        agent = self.agents.analysis_executor_agent()
        agent.tools = [self.tools.calculation_tool()]
        
        task = HealthEconTasks.dsa_task(agent, base_case_results, parameters)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        try:
            parsed = self._extract_json_from_text(str(result))
            return {
                'tornado_data': parsed.get('tornado_data', []),
                'most_sensitive': parsed.get('most_sensitive', []),
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'tornado_data': [],
                'most_sensitive': []
            }
    
    def run_psa_task(self, base_case_results: Dict[str, Any],
                    parameters: Dict[str, Any], n_simulations: int = 1000) -> Dict[str, Any]:
        """
        Execute probabilistic sensitivity analysis
        
        Returns:
            PSA results with scatter plot and CEAC data
        """
        agent = self.agents.analysis_executor_agent()
        agent.tools = [self.tools.calculation_tool()]
        
        task = HealthEconTasks.psa_task(agent, base_case_results, parameters, n_simulations)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        try:
            parsed = self._extract_json_from_text(str(result))
            return {
                'simulations': parsed.get('simulations', []),
                'scatter_data': parsed.get('scatter_data', {}),
                'ceac_data': parsed.get('ceac_data', {}),
                'mean_icer': parsed.get('mean_icer', 0),
                'credible_interval': parsed.get('credible_interval', []),
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'simulations': [],
                'scatter_data': {},
                'ceac_data': {},
                'mean_icer': 0,
                'credible_interval': []
            }
    
    def run_report_generation_task(self, project_name: str, model_type: str,
                                   base_case_results: Optional[Dict],
                                   dsa_results: Optional[Dict],
                                   psa_results: Optional[Dict],
                                   literature_evidence: list) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report
        
        Returns:
            Formatted report with all sections
        """
        agent = self.agents.report_generator_agent()
        agent.tools = [self.tools.report_generator_tool()]
        
        task = HealthEconTasks.report_generation_task(
            agent, project_name, model_type, base_case_results,
            dsa_results, psa_results, literature_evidence
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            'report': str(result),
            'format': 'markdown',
            'status': 'success'
        }
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from agent output text
        
        Args:
            text: Agent output that may contain JSON
            
        Returns:
            Parsed dictionary
        """
        # Try to find JSON in markdown code blocks
        if '```json' in text:
            start = text.find('```json') + 7
            end = text.find('```', start)
            json_str = text[start:end].strip()
        elif '```' in text:
            start = text.find('```') + 3
            end = text.find('```', start)
            json_str = text[start:end].strip()
        else:
            json_str = text
        
        # Try to parse
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If not valid JSON, try to extract key information manually
            return {'raw_output': text}
