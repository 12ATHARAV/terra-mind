import pytest
from pydantic import ValidationError
from src.schemas.ecosystem_input import EcosystemQueryPayload, SoilMetrics
from src.schemas.scientific_output import (
    EcosystemAnalysisResult, InterventionRecommendation, MetricDelta,
    AcademicCitation, ClarificationQuestion
)


def test_soil_metrics_valid():
    soil = SoilMetrics(ph=6.5, organic_carbon_pct=0.3)
    assert soil.ph == 6.5


def test_soil_metrics_ph_out_of_range():
    with pytest.raises(ValidationError):
        SoilMetrics(ph=15.0)


def test_ecosystem_query_requires_text():
    with pytest.raises(ValidationError):
        EcosystemQueryPayload()


def test_intervention_requires_3_coupled_variables():
    citation = AcademicCitation(citation_id="T", source_title="T", authors_or_organization="T", year=2020, doi_or_url="x", evidence_quote="x")
    delta = MetricDelta(metric_name="SOC", baseline_value="0.3%", projected_value="0.6%", delta_percentage="+20%", mechanism="roots")
    with pytest.raises(ValidationError):
        InterventionRecommendation(
            intervention_name="Test", priority_level="Immediate (Tier 1)",
            actionable_protocol=["Do"], scientific_mechanism="mech",
            coupled_variables=["Only one"],
            time_horizon="Short-term (0-12 months)",
            impacted_metrics=[delta], citations=[citation], confidence_score=0.8
        )


def test_clarification_structure():
    cq = ClarificationQuestion(missing_variables=["SOC"], reason_needed="Need data", suggested_questions=["Q1?"])
    assert len(cq.suggested_questions) == 1
