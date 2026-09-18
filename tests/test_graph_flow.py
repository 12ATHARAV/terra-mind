import pytest
from src.schemas.ecosystem_input import EcosystemQueryPayload, SoilMetrics, ClimateMetrics, LandUseMetrics, SpatialContext
from src.agents.graph import graph


def _state(payload):
    return {
        "payload": payload, "spatial_profile": None, "completeness_score": 0.0,
        "is_clarification_required": False, "clarification_details": None,
        "coupled_analysis": None, "retrieved_docs": [], "final_analysis": None
    }


def test_graph_clarification_on_vague_input():
    state = graph.invoke(_state(EcosystemQueryPayload(query_text="help land dying")))
    assert state["final_analysis"].status == "clarification_needed"
    assert len(state["final_analysis"].clarification.suggested_questions) > 0


def test_graph_scientific_reasoning():
    payload = EcosystemQueryPayload(
        query_text="Biodiversity declining, soil organic carbon 0.3%, rainfall low, monoculture wheat, semi-arid",
        soil=SoilMetrics(organic_carbon_pct=0.3),
        climate=ClimateMetrics(annual_rainfall_mm=450.0),
        land_use=LandUseMetrics(land_cover_type="Monoculture wheat")
    )
    state = graph.invoke(_state(payload))
    result = state["final_analysis"]
    assert result.status == "completed"
    assert len(result.recommendations) > 0
    assert len(result.recommendations[0].coupled_variables) >= 3
    assert len(result.recommendations[0].citations) > 0


def test_graph_spatial_resolution():
    payload = EcosystemQueryPayload(
        query_text="Ecosystem degradation with low soil carbon and biodiversity decline near Pune",
        soil=SoilMetrics(organic_carbon_pct=0.4),
        spatial=SpatialContext(latitude=18.52, longitude=73.85),
    )
    state = graph.invoke(_state(payload))
    assert state["spatial_profile"] is not None
    assert "ecoregion" in state["spatial_profile"]
