from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class MetricDelta(BaseModel):
    metric_name: str = Field(..., description="Target environmental parameter")
    baseline_value: str = Field(..., description="Current baseline estimate")
    projected_value: str = Field(..., description="Projected value post-intervention")
    delta_percentage: str = Field(..., description="Estimated quantitative improvement")
    mechanism: str = Field(..., description="Biophysical cause-and-effect mechanism")

class AcademicCitation(BaseModel):
    citation_id: str
    source_title: str
    authors_or_organization: str
    year: int
    doi_or_url: str
    evidence_quote: str

class InterventionRecommendation(BaseModel):
    intervention_name: str
    priority_level: Literal["Immediate (Tier 1)", "Strategic (Tier 2)", "Long-term (Tier 3)"]
    actionable_protocol: List[str]
    scientific_mechanism: str
    coupled_variables: List[str] = Field(..., min_length=3, description="Must connect at least 3 environmental metrics")
    time_horizon: Literal["Short-term (0-12 months)", "Medium-term (1-3 years)", "Long-term (3-7+ years)"]
    impacted_metrics: List[MetricDelta]
    citations: List[AcademicCitation]
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class ClarificationQuestion(BaseModel):
    missing_variables: List[str]
    reason_needed: str
    suggested_questions: List[str]

class EcosystemAnalysisResult(BaseModel):
    status: Literal["completed", "clarification_needed"]
    summary: str
    clarification: Optional[ClarificationQuestion] = None
    recommendations: Optional[List[InterventionRecommendation]] = None
    synthesized_reasoning: Optional[str] = None
