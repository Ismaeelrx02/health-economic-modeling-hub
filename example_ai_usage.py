"""
Example script demonstrating AI agentic framework usage
Shows how to integrate CrewAI + LangGraph workflow into the application
"""

import os
from dotenv import load_dotenv
from ai.graph import HealthEconGraph
from ai.state import create_initial_state
import json

# Load environment variables
load_dotenv()


def example_automated_workflow():
    """
    Example: Fully automated workflow
    AI handles everything from query to final report
    """
    print("=" * 80)
    print("EXAMPLE 1: AI-Automated Workflow")
    print("=" * 80)
    
    # Initialize graph in automated mode
    graph = HealthEconGraph(ai_mode="ai-automated")
    
    # User query
    query = """
    Evaluate the cost-effectiveness of a new anticoagulant drug (Drug X) 
    compared to warfarin for atrial fibrillation patients. 
    The target population is adults over 65. 
    Use a 10-year time horizon.
    """
    
    print(f"\nUser Query: {query.strip()}\n")
    print("Running automated workflow...\n")
    
    # Run complete workflow
    result = graph.run(user_query=query)
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"\nProject: {result.get('project_name', 'N/A')}")
    print(f"Disease Area: {result.get('disease_area', 'N/A')}")
    print(f"Model Type: {result.get('model_type', 'N/A')}")
    print(f"Time Horizon: {result.get('time_horizon', 'N/A')} years")
    
    if result.get('base_case_results'):
        base = result['base_case_results']
        print(f"\nBase Case Results:")
        print(f"  ICER: ${base.get('icer', 0):,.2f} per QALY")
        print(f"  NMB: ${base.get('nmb', 0):,.2f}")
        print(f"  Incremental Cost: ${base.get('incremental_cost', 0):,.2f}")
        print(f"  Incremental QALYs: {base.get('incremental_qalys', 0):.4f}")
    
    if result.get('dsa_results'):
        print(f"\nDSA: Analyzed {len(result['dsa_results'].get('tornado_data', []))} parameters")
    
    if result.get('psa_results'):
        print(f"\nPSA: Ran {len(result['psa_results'].get('simulations', []))} simulations")
    
    print(f"\nFinal Report: {len(result.get('final_report', ''))} characters\n")


def example_interactive_workflow():
    """
    Example: Interactive workflow with approval checkpoint
    AI suggests parameters, user approves before analysis
    """
    print("=" * 80)
    print("EXAMPLE 2: AI-Augmented Workflow (Interactive)")
    print("=" * 80)
    
    # Initialize graph in augmented mode
    graph = HealthEconGraph(ai_mode="ai-augmented")
    
    query = "Compare Drug Y to standard care for Type 2 Diabetes"
    
    print(f"\nUser Query: {query}\n")
    print("Running workflow until approval checkpoint...\n")
    
    # Run until approval is needed
    result = graph.run_until_approval(user_query=query)
    
    # Display validation results
    print("\n" + "=" * 80)
    print("VALIDATION RESULTS (Awaiting Approval)")
    print("=" * 80)
    
    validation = result.get('validation_results', {})
    errors = validation.get('errors', [])
    warnings = validation.get('warnings', [])
    suggestions = validation.get('suggestions', [])
    
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    else:
        print("\n✓ No errors found")
    
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    else:
        print("\n✓ No warnings")
    
    if suggestions:
        print(f"\nSUGGESTIONS ({len(suggestions)}):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    # Simulate user approval
    print("\n" + "=" * 80)
    print("USER DECISION")
    print("=" * 80)
    
    # In real application, this would be user input
    # For demo, auto-approve
    user_approves = True
    print(f"\nUser Decision: {'APPROVED ✓' if user_approves else 'REJECTED ✗'}\n")
    
    if user_approves:
        print("Resuming workflow...\n")
        
        # Continue workflow after approval
        final_result = graph.resume_after_approval(result, approved=True)
        
        print("\n" + "=" * 80)
        print("FINAL RESULTS")
        print("=" * 80)
        
        if final_result.get('base_case_results'):
            base = final_result['base_case_results']
            print(f"\nICER: ${base.get('icer', 0):,.2f} per QALY")
            print(f"NMB: ${base.get('nmb', 0):,.2f}")
        
        print(f"\nWorkflow Status: {final_result.get('current_step', 'unknown')}")
    else:
        print("Workflow terminated by user.\n")


def example_assisted_workflow():
    """
    Example: AI-Assisted mode
    AI provides suggestions but user maintains control
    """
    print("=" * 80)
    print("EXAMPLE 3: AI-Assisted Workflow")
    print("=" * 80)
    
    graph = HealthEconGraph(ai_mode="ai-assisted")
    
    query = "Cost-effectiveness analysis for new immunotherapy in lung cancer"
    
    print(f"\nUser Query: {query}\n")
    print("In assisted mode, AI provides suggestions but user controls execution.\n")
    
    # Create initial state
    state = create_initial_state(user_query=query, ai_mode="ai-assisted")
    
    print("State initialized with:")
    print(f"  - AI Mode: {state['ai_mode']}")
    print(f"  - Current Step: {state['current_step']}")
    print(f"  - Requires Approval: {state['requires_user_approval']}")
    
    print("\nIn assisted mode, workflow would:")
    print("  1. Parse query and suggest project structure")
    print("  2. Search literature and suggest parameters")
    print("  3. Build model structure with user inputs")
    print("  4. Wait for user approval at each step")
    print("  5. Execute analysis only after explicit user confirmation")
    
    print("\nThis mode is ideal for:")
    print("  - Learning health economics modeling")
    print("  - Sensitive analyses requiring oversight")
    print("  - When transparency is critical\n")


def example_state_visualization():
    """
    Example: Visualize the workflow graph
    """
    print("=" * 80)
    print("EXAMPLE 4: Workflow Visualization")
    print("=" * 80)
    
    graph = HealthEconGraph()
    
    print("\nGenerating Mermaid diagram...\n")
    
    mermaid = graph.visualize()
    
    print(mermaid)
    
    print("\n" + "=" * 80)
    print("Copy the above Mermaid code to: https://mermaid.live")
    print("=" * 80 + "\n")


def example_direct_crew_usage():
    """
    Example: Use CrewAI crew directly without LangGraph
    For single-task execution
    """
    print("=" * 80)
    print("EXAMPLE 5: Direct Crew Usage (Single Task)")
    print("=" * 80)
    
    from ai.crew.crew import HealthEconCrew
    
    # Initialize crew
    crew = HealthEconCrew(ai_mode="ai-augmented")
    
    print("\nExecuting literature research task...\n")
    
    # Execute single task
    result = crew.run_literature_research_task(
        disease_area="cardiovascular disease",
        intervention="Novel PCSK9 inhibitor",
        comparator="Statin therapy",
        model_type="markov"
    )
    
    print("Literature Research Results:")
    print(f"  Parameters found: {len(result.get('parameters', {}))}")
    print(f"  Sources: {len(result.get('sources', []))}")
    print(f"  Missing: {len(result.get('missing_parameters', []))}")
    
    if result.get('parameters'):
        print("\n  Sample Parameters:")
        for key, value in list(result['parameters'].items())[:3]:
            if isinstance(value, dict):
                print(f"    - {key}: {value.get('value', 'N/A')} (Source: {value.get('source', 'N/A')})")
    
    print("\nThis approach is useful for:")
    print("  - Running individual analysis tasks")
    print("  - Testing specific agents")
    print("  - Custom workflow implementations\n")


def main():
    """Run all examples"""
    
    print("\n" + "=" * 80)
    print("HEALTH ECONOMIC MODELING HUB")
    print("AI Agentic Framework Examples")
    print("=" * 80 + "\n")
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment")
        print("   Set it in .env file for full functionality")
        print("   Examples will run with mock data.\n")
    
    try:
        # Run examples
        example_automated_workflow()
        print("\n" * 2)
        
        example_interactive_workflow()
        print("\n" * 2)
        
        example_assisted_workflow()
        print("\n" * 2)
        
        example_state_visualization()
        print("\n" * 2)
        
        example_direct_crew_usage()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("\nNote: Examples may require API keys and dependencies.")
        print("See AI_FRAMEWORK_GUIDE.md for setup instructions.\n")
    
    print("\n" + "=" * 80)
    print("Examples Complete!")
    print("=" * 80)
    print("\nNext Steps:")
    print("  1. Review AI_FRAMEWORK_GUIDE.md for detailed documentation")
    print("  2. Set up API keys in .env file")
    print("  3. Install dependencies: pip install -r requirements-dash.txt")
    print("  4. Integrate AI framework into Dash callbacks")
    print("  5. Test with real health economics queries\n")


if __name__ == "__main__":
    main()
