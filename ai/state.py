"""
State Management for Health Economics AI Agents
Defines the shared state structure for LangGraph workflow
"""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from datetime import datetime
import operator

class HealthEconState(TypedDict):
    """
    Shared state for health economics modeling workflow
    All agents read from and write to this state
    """
    # Input/Request
    user_query: str
    ai_mode: str  # 'ai-assisted', 'ai-augmented', 'ai-automated'
    model_type: str  # 'decision_tree', 'markov', 'psm'
    
    # Project Context
    project_id: Optional[int]
    project_name: str
    disease_area: str
    intervention: str
    comparator: str
    
    # Model Parameters
    parameters: Dict[str, Any]
    time_horizon: int
    discount_rate_cost: float
    discount_rate_outcome: float
    wtp_threshold: float
    
    # Intermediate Results
    model_structure: Optional[Dict[str, Any]]
    literature_evidence: List[Dict[str, Any]]
    parameter_suggestions: Dict[str, Any]
    validation_results: Dict[str, Any]
    
    # Analysis Results
    base_case_results: Optional[Dict[str, Any]]
    dsa_results: Optional[Dict[str, Any]]
    psa_results: Optional[Dict[str, Any]]
    ceac_data: Optional[List[Dict[str, float]]]
    
    # Messages and Feedback
    messages: Annotated[List[str], operator.add]
    warnings: Annotated[List[str], operator.add]
    suggestions: Annotated[List[str], operator.add]
    
    # Workflow Control
    current_step: str
    requires_user_approval: bool
    user_approved: bool
    should_continue: bool
    
    # Output
    final_report: Optional[str]
    charts: List[Dict[str, Any]]
    icer: Optional[float]
    nmb: Optional[float]
    
    # Metadata
    created_at: str
    updated_at: str
    execution_time: float


def create_initial_state(
    user_query: str,
    ai_mode: str = 'ai-assisted',
    model_type: str = 'markov'
) -> HealthEconState:
    """Create initial state with default values"""
    now = datetime.now().isoformat()
    
    return HealthEconState(
        # Input
        user_query=user_query,
        ai_mode=ai_mode,
        model_type=model_type,
        
        # Project Context
        project_id=None,
        project_name="",
        disease_area="",
        intervention="",
        comparator="",
        
        # Parameters
        parameters={},
        time_horizon=10,
        discount_rate_cost=0.03,
        discount_rate_outcome=0.03,
        wtp_threshold=50000.0,
        
        # Intermediate
        model_structure=None,
        literature_evidence=[],
        parameter_suggestions={},
        validation_results={},
        
        # Results
        base_case_results=None,
        dsa_results=None,
        psa_results=None,
        ceac_data=None,
        
        # Messages
        messages=[],
        warnings=[],
        suggestions=[],
        
        # Control
        current_step="start",
        requires_user_approval=False,
        user_approved=False,
        should_continue=True,
        
        # Output
        final_report=None,
        charts=[],
        icer=None,
        nmb=None,
        
        # Metadata
        created_at=now,
        updated_at=now,
        execution_time=0.0
    )


class WorkflowSteps:
    """Constants for workflow step names"""
    START = "start"
    PARSE_QUERY = "parse_query"
    RETRIEVE_EVIDENCE = "retrieve_evidence"
    BUILD_MODEL = "build_model"
    VALIDATE_PARAMETERS = "validate_parameters"
    REQUEST_APPROVAL = "request_approval"
    RUN_BASE_CASE = "run_base_case"
    RUN_DSA = "run_dsa"
    RUN_PSA = "run_psa"
    GENERATE_REPORT = "generate_report"
    END = "end"
