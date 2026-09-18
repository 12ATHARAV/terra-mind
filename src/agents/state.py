from typing import TypedDict, Optional, List, Dict, Any
from src.schemas.ecosystem_input import EcosystemQueryPayload
from src.schemas.scientific_output import EcosystemAnalysisResult


class AgentGraphState(TypedDict):
    payload: EcosystemQueryPayload
    spatial_profile: Optional[Dict[str, Any]]
    completeness_score: float
    is_clarification_required: bool
    clarification_details: Optional[Dict[str, Any]]
    coupled_analysis: Optional[Dict[str, Any]]
    retrieved_docs: List[Any]
    final_analysis: Optional[EcosystemAnalysisResult]
