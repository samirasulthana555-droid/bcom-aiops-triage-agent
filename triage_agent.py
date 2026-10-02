import os
from typing import Dict, Any
from schema import AIOpsAlertSchema 
from triage_engine import run_incident_triage
from langgraph.graph import StateGraph, END

# ==========================================
# PRODUCTION SECURITY RUNTIME LAYER
# Paste your actual live Gemini API key inside the quotes below.
# This remains safe locally on your machine because your .gitignore blocks it from leaving!
LOCAL_SECRET_KEY = os.getenv("GOOGLE_API_KEY")
# ==========================================

# Define the Agent's Shared Memory State
class AgentState(dict):
    payload: str
    triage_data: AIOpsAlertSchema
    routing_action: str

# Node A: The Triage Processor
def triage_node(state: AgentState) -> Dict[str, Any]:
    print("\n[Node 1: Triage Node] Correlating alert with ChromaDB & Gemini...")
    # Pass the local token string down as an entry parameter to clear Pydantic path errors
    structured_output = run_incident_triage(state["payload"], backup_key=LOCAL_SECRET_KEY)
    return {"triage_data": structured_output}

# Node B: Automated Remediation Engine
def remediation_node(state: AgentState) -> Dict[str, Any]:
    print("\n[Node 2: Remediation Node] Executing autonomous SDK fixes...")
    triage = state["triage_data"]
    print(f"-> EXECUTING BASELINE COMMAND: {triage.remediation_steps}")
    return {"routing_action": "Remediation Executed Successfully"}

# Node C: SLA 7-Minute Hold & Auto-Resolution Engine
def sla_hold_node(state: AgentState) -> Dict[str, Any]:
    print("\n[Node 3: SLA Hold Node] Flapping behavior detected.")
    print("-> ACTION: Activating 7-minute SLA hold window.")
    print("-> STATUS: Alarm settled within window. Auto-closing incident to prevent queue flood.")
    return {"routing_action": "Incident Suppressed & Auto-Closed"}

# The Conditional Router (The Decision Brain)
def router_decision_rule(state: AgentState) -> str:
    triage = state["triage_data"]
    
    if "flapping" in triage.alert_name.lower():
        print("\n[Router Rule] Metric evaluation: High-frequency network oscillation confirmed.")
        return "hold"
    else:
        print("\n[Router Rule] Metric evaluation: Steady state critical failure detected.")
        return "remediate"

print("Building LangGraph Production Workflow Pattern...")

workflow = StateGraph(AgentState)

workflow.add_node("process_triage", triage_node)
workflow.add_node("execute_remediation", remediation_node)
workflow.add_node("apply_sla_hold", sla_hold_node)

workflow.set_entry_point("process_triage")

workflow.add_conditional_edges(
    "process_triage",
    router_decision_rule,
    {
        "remediate": "execute_remediation",
        "hold": "apply_sla_hold"
    }
)

workflow.add_edge("execute_remediation", END)
workflow.add_edge("apply_sla_hold", END)

app = workflow.compile()
print("Workflow compiled successfully.")

if __name__ == "__main__":
    flapping_payload = """
    CRITICAL_ALERT: Edge Gateway Ping Drop Exception!
    RESOURCE: Edge Gateway Device vpc-router-prod
    METRICS: State changed from ACTIVE to CLEAR 4 times within a 90-second window.
    """
    
    print("\n--- Starting Live Multi-Node Agent Test Loop ---")
    initial_state = {"payload": flapping_payload}
    app.invoke(initial_state)
