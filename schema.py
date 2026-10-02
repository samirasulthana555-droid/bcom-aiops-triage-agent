from pydantic import BaseModel, Field
from typing import List

class AIOpsAlertSchema(BaseModel):
    """Production schema for deep alert triage, validation, and automated remediation workflow routing."""
    
    alert_id: str = Field(description="The structural identifier from the runbook context.")
    alert_name: str = Field(description="The operational name of the failure event.")
    priority: str = Field(description="The incident priority tier, e.g., P1, P2, P3.")
    escalation_classification: str = Field(description="The tracking team classification category.")
    
    alarm_validation_steps: List[str] = Field(
        description="Step-by-step verification rules, including Google Cloud Monitoring links and baseline status commands."
    )
    remediation_steps: List[str] = Field(
        description="The exact engineering actions or local gcloud / kubectl SDK commands to fix the issue."
    )
    escalation_details: str = Field(
        description="Detailed routing path containing the precise team name, Slack channel, or on-call communication channel."
    )

