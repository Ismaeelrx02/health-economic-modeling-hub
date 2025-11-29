"""
LangGraph Workflow Definition
Defines the graph structure with nodes and edges for health economics analysis
"""
from typing import Literal
from langgraph.graph import StateGraph, END

from .state import HealthEconState, WorkflowSteps, create_initial_state
from .nodes import HealthEconNodes


class HealthEconGraph:
    """
    LangGraph workflow for health economics modeling
    Integrates CrewAI agents through node functions
    """
    
    def __init__(self):
        """Initialize the graph with nodes"""
        self.nodes = HealthEconNodes()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow
        Defines nodes and conditional edges
        """
        # Create graph with HealthEconState
        workflow = StateGraph(HealthEconState)
        
        # Add nodes
        workflow.add_node("parse_query", self.nodes.parse_query_node)
        workflow.add_node("retrieve_evidence", self.nodes.retrieve_evidence_node)
        workflow.add_node("build_model", self.nodes.build_model_node)
        workflow.add_node("validate_parameters", self.nodes.validate_parameters_node)
        workflow.add_node("request_approval", self.nodes.request_approval_node)
        workflow.add_node("run_base_case", self.nodes.run_base_case_node)
        workflow.add_node("run_dsa", self.nodes.run_dsa_node)
        workflow.add_node("run_psa", self.nodes.run_psa_node)
        workflow.add_node("generate_report", self.nodes.generate_report_node)
        workflow.add_node("end", self.nodes.end_node)
        
        # Set entry point
        workflow.set_entry_point("parse_query")
        
        # Add edges (linear flow)
        workflow.add_edge("parse_query", "retrieve_evidence")
        workflow.add_edge("retrieve_evidence", "build_model")
        workflow.add_edge("build_model", "validate_parameters")
        
        # Conditional edge from validation
        workflow.add_conditional_edges(
            "validate_parameters",
            self._route_after_validation,
            {
                "approval_needed": "request_approval",
                "proceed": "run_base_case"
            }
        )
        
        # Conditional edge from approval
        workflow.add_conditional_edges(
            "request_approval",
            self._route_after_approval,
            {
                "approved": "run_base_case",
                "wait": END  # Pause workflow
            }
        )
        
        # Conditional edge from base case
        workflow.add_conditional_edges(
            "run_base_case",
            self._route_after_base_case,
            {
                "run_sensitivity": "run_dsa",
                "generate_report": "generate_report"
            }
        )
        
        workflow.add_edge("run_dsa", "run_psa")
        workflow.add_edge("run_psa", "generate_report")
        workflow.add_edge("generate_report", "end")
        workflow.add_edge("end", END)
        
        return workflow.compile()
    
    def _route_after_validation(self, state: HealthEconState) -> Literal["approval_needed", "proceed"]:
        """Determine if user approval is needed after validation"""
        if state['requires_user_approval']:
            return "approval_needed"
        return "proceed"
    
    def _route_after_approval(self, state: HealthEconState) -> Literal["approved", "wait"]:
        """Route after approval request"""
        if state['user_approved']:
            return "approved"
        return "wait"  # Pause here
    
    def _route_after_base_case(self, state: HealthEconState) -> Literal["run_sensitivity", "generate_report"]:
        """Determine if sensitivity analyses should run"""
        if state['ai_mode'] == 'ai-automated':
            return "run_sensitivity"
        return "generate_report"
    
    def run(self, user_query: str, ai_mode: str = 'ai-assisted', model_type: str = 'markov') -> HealthEconState:
        """
        Run the complete workflow
        
        Args:
            user_query: User's analysis request
            ai_mode: AI operating mode ('ai-assisted', 'ai-augmented', 'ai-automated')
            model_type: Type of model to build ('decision_tree', 'markov', 'psm')
        
        Returns:
            Final state with all results
        """
        # Create initial state
        initial_state = create_initial_state(
            user_query=user_query,
            ai_mode=ai_mode,
            model_type=model_type
        )
        
        print(f"\n{'='*70}")
        print(f"🚀 Starting Health Economics Analysis")
        print(f"{'='*70}")
        print(f"Query: {user_query}")
        print(f"AI Mode: {ai_mode}")
        print(f"Model Type: {model_type}")
        print(f"{'='*70}\n")
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        print(f"\n{'='*70}")
        print(f"✅ Workflow Complete!")
        print(f"{'='*70}")
        print(f"Messages: {len(final_state['messages'])}")
        print(f"Warnings: {len(final_state['warnings'])}")
        print(f"Suggestions: {len(final_state['suggestions'])}")
        if final_state.get('icer'):
            print(f"ICER: ${final_state['icer']:,.2f}/QALY")
        print(f"{'='*70}\n")
        
        return final_state
    
    def run_until_approval(self, user_query: str, ai_mode: str = 'ai-assisted', model_type: str = 'markov') -> HealthEconState:
        """
        Run workflow until user approval is needed
        Used for interactive workflows
        
        Returns:
            State at approval checkpoint
        """
        initial_state = create_initial_state(
            user_query=user_query,
            ai_mode=ai_mode,
            model_type=model_type
        )
        
        # Run until approval needed
        state = self.graph.invoke(initial_state)
        
        return state
    
    def resume_after_approval(self, state: HealthEconState, approved: bool = True) -> HealthEconState:
        """
        Resume workflow after user approval
        
        Args:
            state: State from approval checkpoint
            approved: Whether user approved
        
        Returns:
            Final state
        """
        state['user_approved'] = approved
        
        if approved:
            state['current_step'] = WorkflowSteps.RUN_BASE_CASE
            # Continue from current state
            final_state = self.graph.invoke(state)
            return final_state
        else:
            state['should_continue'] = False
            state['messages'].append("❌ Analysis cancelled by user")
            return state
    
    def visualize(self, output_path: str = "workflow.png"):
        """
        Generate visual representation of the workflow graph
        Requires graphviz
        """
        try:
            from langgraph.graph.graph import draw_mermaid
            mermaid_code = draw_mermaid(self.graph)
            
            print(f"📊 Workflow Visualization:")
            print(mermaid_code)
            
            # Save to file
            with open(output_path.replace('.png', '.mmd'), 'w') as f:
                f.write(mermaid_code)
            
            print(f"✅ Saved Mermaid diagram to {output_path.replace('.png', '.mmd')}")
            
        except Exception as e:
            print(f"⚠️ Could not generate visualization: {e}")
