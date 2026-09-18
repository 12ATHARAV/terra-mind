import pytest
from src.schemas.ecosystem_input import EcosystemQueryPayload, SoilMetrics, ClimateMetrics, LandUseMetrics
from src.engine.multi_metric_matrix import MultiMetricReasoningEngine


def test_multi_metric_coupling_enforcement():
    payload = EcosystemQueryPayload(
        query_text="Monoculture wheat farm with low soil carbon",
        soil=SoilMetrics(organic_carbon_pct=0.3),
        climate=ClimateMetrics(annual_rainfall_mm=450.0),
        land_use=LandUseMetrics(land_cover_type="Monoculture wheat")
    )
    res = MultiMetricReasoningEngine.evaluate_couplings(payload)
    assert res["coupled_interactions_found"] > 0
    assert len(res["interactions"][0]["variables"]) >= 3
    assert "Soil Organic Carbon (SOC %)" in res["interactions"][0]["variables"]


def test_fragmentation_nexus():
    payload = EcosystemQueryPayload(
        query_text="Fragmented landscape",
        land_use=LandUseMetrics(fragmentation_index=0.75, canopy_cover_pct=10.0)
    )
    res = MultiMetricReasoningEngine.evaluate_couplings(payload)
    nexus_ids = [i["id"] for i in res["interactions"]]
    assert any("CANOPY" in nid for nid in nexus_ids)


def test_general_fallback():
    payload = EcosystemQueryPayload(query_text="Some problem")
    res = MultiMetricReasoningEngine.evaluate_couplings(payload)
    assert res["coupled_interactions_found"] >= 1


def test_projected_deltas_present():
    payload = EcosystemQueryPayload(
        query_text="Low carbon soil",
        soil=SoilMetrics(organic_carbon_pct=0.25),
        climate=ClimateMetrics(annual_rainfall_mm=300.0),
        land_use=LandUseMetrics(land_cover_type="Monoculture wheat")
    )
    res = MultiMetricReasoningEngine.evaluate_couplings(payload)
    assert len(res["interactions"][0]["projected_deltas"]) > 0
