"""
Node Functions for LangGraph Workflow
Each node performs a specific task in the health economics modeling pipeline
"""
from typing import Dict, Any
import time
from datetime import datetime

from .state import HealthEconState, WorkflowSteps
from .crew.crew import HealthEconCrew


class HealthEconNodes:
    """
    Node functions for the LangGraph workflow
    Each node modifies the state and returns it
    """
    
    def __init__(self):
        """Initialize nodes with CrewAI crew"""
        self.crew = HealthEconCrew()
    
    def parse_query_node(self, state: HealthEconState) -> HealthEconState:
        """
        Parse user query to extract requirements
        Uses QueryParser agent from CrewAI
        """
        print(f"🔍 [Node: Parse Query] Analyzing: {state['user_query']}")
        
        # Run CrewAI parse_query_task
        result = self.crew.run_parse_query_task(
            user_query=state['user_query'],
            ai_mode=state['ai_mode']
        )
        
        # Update state
        state['project_name'] = result.get('project_name', 'Health Economics Analysis')
        state['disease_area'] = result.get('disease_area', '')
        state['intervention'] = result.get('intervention', '')
        state['comparator'] = result.get('comparator', '')
        state['model_type'] = result.get('model_type', state['model_type'])
        state['messages'].append(f"✅ Parsed query: {result.get('summary', '')}")
        state['current_step'] = WorkflowSteps.RETRIEVE_EVIDENCE
        state['updated_at'] = datetime.now().isoformat()
        
        return state
    
    def retrieve_evidence_node(self, state: HealthEconState) -> HealthEconState:
        """
        Retrieve literature evidence and parameter estimates
        Uses LiteratureResearcher agent from CrewAI
        """
        print(f"📚 [Node: Retrieve Evidence] Searching literature for {state['disease_area']}")
        
        # Run CrewAI literature_research_task
        result = self.crew.run_literature_research_task(
            disease_area=state['disease_area'],
            intervention=state['intervention'],
            comparator=state['comparator'],
            model_type=state['model_type']
        )
        
        # Update state
        state['literature_evidence'] = result.get('evidence', [])
        state['parameter_suggestions'] = result.get('parameters', {})
        state['messages'].append(f"✅ Retrieved {len(state['literature_evidence'])} evidence sources")
        state['current_step'] = WorkflowSteps.BUILD_MODEL
        state['updated_at'] = datetime.now().isoformat()
        
        return state
    
    def build_model_node(self, state: HealthEconState) -> HealthEconState:
        """
        Build model structure based on type
        Uses ModelBuilder agent from CrewAI
        """
        print(f"🏗️ [Node: Build Model] Creating {state['model_type']} structure")
        
        # Run CrewAI build_model_task
        result = self.crew.run_build_model_task(
            model_type=state['model_type'],
            disease_area=state['disease_area'],
            parameter_suggestions=state['parameter_suggestions'],
            ai_mode=state['ai_mode']
        )
        
        # Update state
        state['model_structure'] = result.get('structure', {})
        state['parameters'] = result.get('populated_parameters', {})
        state['suggestions'].extend(result.get('suggestions', []))
        state['messages'].append(f"✅ Built {state['model_type']} model structure")
        state['current_step'] = WorkflowSteps.VALIDATE_PARAMETERS
        state['updated_at'] = datetime.now().isoformat()
        
        return state
    
    def validate_parameters_node(self, state: HealthEconState) -> HealthEconState:
        """
        Validate model parameters and check for issues
        Uses ParameterValidator agent from CrewAI
        """
        print(f"✅ [Node: Validate Parameters] Checking {len(state['parameters'])} parameters")
        
        # Run CrewAI validation_task
        result = self.crew.run_validation_task(
            model_structure=state['model_structure'],
            parameters=state['parameters'],
            model_type=state['model_type']
        )
        
        # Update state
        state['validation_results'] = result
        state['warnings'].extend(result.get('warnings', []))
        state['suggestions'].extend(result.get('suggestions', []))
        
        # Determine if approval needed based on AI mode
        if state['ai_mode'] == 'ai-assisted':
            state['requires_user_approval'] = True
            state['current_step'] = WorkflowSteps.REQUEST_APPROVAL
            state['messages'].append("⏸️ Waiting for user approval (AI-Assisted mode)")
        elif state['ai_mode'] == 'ai-augmented' and result.get('has_warnings', False):
            state['requires_user_approval'] = True
            state['current_step'] = WorkflowSteps.REQUEST_APPROVAL
            state['messages'].append("⏸️ Waiting for user approval (warnings found)")
        else:
            state['user_approved'] = True
            state['current_step'] = WorkflowSteps.RUN_BASE_CASE
            state['messages'].append("✅ Parameters validated, proceeding automatically")
        
        state['updated_at'] = datetime.now().isoformat()
        return state
    
    def request_approval_node(self, state: HealthEconState) -> HealthEconState:
        """
        Request user approval before proceeding
        In real implementation, this would pause and wait for user input
        """
        print(f"⏸️ [Node: Request Approval] Waiting for user decision")
        
        # This is a checkpoint - in real app, workflow pauses here
        # User reviews validation results and either approves or rejects
        
        state['messages'].append("⏸️ User approval required")
        state['current_step'] = WorkflowSteps.REQUEST_APPROVAL
        state['updated_at'] = datetime.now().isoformat()
        
        # For demo purposes, auto-approve in augmented/automated modes
        if state['ai_mode'] in ['ai-augmented', 'ai-automated']:
            state['user_approved'] = True
            state['current_step'] = WorkflowSteps.RUN_BASE_CASE
            state['messages'].append("✅ Auto-approved (AI mode)")
        
        return state
    
    def run_base_case_node(self, state: HealthEconState) -> HealthEconState:
        """
        Run base case analysis
        Uses AnalysisExecutor agent from CrewAI
        """
        print(f"🔬 [Node: Run Base Case] Executing analysis")
        
        # Run CrewAI base_case_analysis_task
        result = self.crew.run_base_case_analysis_task(
            model_type=state['model_type'],
            model_structure=state['model_structure'],
            parameters=state['parameters']
        )
        
        # Update state
        state['base_case_results'] = result
        state['icer'] = result.get('icer', None)
        state['nmb'] = result.get('nmb', None)
        state['messages'].append(f"✅ Base case complete: ICER = ${state['icer']:,.0f}/QALY" if state['icer'] else "✅ Base case complete")
        
        # Determine next step based on AI mode
        if state['ai_mode'] == 'ai-automated':
            state['current_step'] = WorkflowSteps.RUN_DSA
        else:
            state['current_step'] = WorkflowSteps.GENERATE_REPORT
        
        state['updated_at'] = datetime.now().isoformat()
        return state
    
    def run_dsa_node(self, state: HealthEconState) -> HealthEconState:
        """
        Run deterministic sensitivity analysis
        Uses AnalysisExecutor agent from CrewAI
        """
        print(f"📊 [Node: Run DSA] Sensitivity analysis")
        
        # Run CrewAI dsa_task
        result = self.crew.run_dsa_task(
            base_case_results=state['base_case_results'],
            parameters=state['parameters']
        )
        
        # Update state
        state['dsa_results'] = result
        state['charts'].append({'type': 'tornado', 'data': result.get('tornado_data', [])})
        state['messages'].append(f"✅ DSA complete: {len(result.get('parameters_tested', []))} parameters tested")
        state['current_step'] = WorkflowSteps.RUN_PSA
        state['updated_at'] = datetime.now().isoformat()
        
        return state
    
    def run_psa_node(self, state: HealthEconState) -> HealthEconState:
        """
        Run probabilistic sensitivity analysis
        Uses AnalysisExecutor agent from CrewAI
        """
        print(f"🎲 [Node: Run PSA] Probabilistic analysis")
        
        # Run CrewAI psa_task
        result = self.crew.run_psa_task(
            base_case_results=state['base_case_results'],
            parameters=state['parameters'],
            n_simulations=1000
        )
        
        # Update state
        state['psa_results'] = result
        state['ceac_data'] = result.get('ceac', [])
        state['charts'].append({'type': 'ceac', 'data': state['ceac_data']})
        state['charts'].append({'type': 'scatter', 'data': result.get('scatter_data', [])})
        state['messages'].append(f"✅ PSA complete: {result.get('n_simulations', 0)} simulations")
        state['current_step'] = WorkflowSteps.GENERATE_REPORT
        state['updated_at'] = datetime.now().isoformat()
        
        return state
    
    def generate_report_node(self, state: HealthEconState) -> HealthEconState:
        """
        Generate final report with all results
        Uses ReportGenerator agent from CrewAI
        """
        print(f"📄 [Node: Generate Report] Creating final report")
        
        # Run CrewAI report_generation_task
        result = self.crew.run_report_generation_task(
            project_name=state['project_name'],
            model_type=state['model_type'],
            base_case_results=state['base_case_results'],
            dsa_results=state['dsa_results'],
            psa_results=state['psa_results'],
            literature_evidence=state['literature_evidence']
        )
        
        # Update state
        state['final_report'] = result.get('report', '')
        state['messages'].append("✅ Report generated successfully")
        state['current_step'] = WorkflowSteps.END
        state['should_continue'] = False
        state['updated_at'] = datetime.now().isoformat()
        
        return state
    
    def end_node(self, state: HealthEconState) -> HealthEconState:
        """
        Final node - workflow complete
        """
        print(f"🎉 [Node: End] Workflow complete!")
        
        state['execution_time'] = time.time()  # In real impl, calculate from start
        state['messages'].append("🎉 Analysis complete!")
        state['should_continue'] = False
        
        return state
