import sys
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import json
import folium
from streamlit_folium import st_folium
from src.schemas.ecosystem_input import (
    EcosystemQueryPayload, SoilMetrics, ClimateMetrics, LandUseMetrics, SpatialContext
)
from src.agents.graph import graph

st.set_page_config(page_title="TERRA-MIND | Biodiversity Intelligence", layout="wide", page_icon="\U0001F331")
st.title("\U0001F331 TERRA-MIND: AI Biodiversity & Ecological Intelligence Engine")
st.markdown("**Darukaa.Earth Hackathon** | Multi-Agent LangGraph \u00b7 Hybrid RAG \u00b7 Pydantic v2 Outputs")

with st.sidebar:
    st.header("\u2699\ufe0f Scientific Input Parameters")
    st.subheader("\U0001F331 Pillar 1: Soil Metrics")
    soc = st.slider("Soil Organic Carbon (SOC %)", 0.0, 5.0, 0.3, step=0.05)
    ph = st.slider("Soil pH", 4.0, 10.0, 7.2, step=0.1)
    st.subheader("\U0001F326\ufe0f Pillar 2: Climate")
    rainfall = st.number_input("Annual Precipitation (mm)", min_value=50.0, max_value=4000.0, value=480.0)
    temperature = st.number_input("Mean Temperature (\u00b0C)", min_value=-10.0, max_value=50.0, value=28.0)
    st.subheader("\U0001F33E Pillar 3: Land Cover")
    crop = st.selectbox("Land Cover", ["Monoculture Wheat", "Monoculture Cotton", "Degraded Fallow", "Degraded Pasture", "Silvopasture", "Agroforestry", "Mangrove Wetland"])
    canopy = st.slider("Canopy Cover (%)", 0.0, 100.0, 15.0, step=1.0)
    frag = st.slider("Fragmentation (0=contiguous, 1=fragmented)", 0.0, 1.0, 0.6, step=0.05)
    st.subheader("\U0001F4CD Pillar 4: Spatial")
    lat = st.number_input("Latitude", value=19.7515, format="%.4f")
    lon = st.number_input("Longitude", value=75.7139, format="%.4f")

tab_query, tab_map, tab_json = st.tabs(["\U0001F52C Query & Analysis", "\U0001F5FA\ufe0f Map", "\U0001F4E6 JSON Output"])

with tab_map:
    st.subheader("Interactive Geo-Coordinate Picker")
    m = folium.Map(location=[lat, lon], zoom_start=6)
    folium.Marker([lat, lon], popup=f"({lat:.4f}, {lon:.4f})", icon=folium.Icon(color="green", icon="leaf")).add_to(m)
    st_folium(m, width=900, height=450)

with tab_query:
    query_text = st.text_area("\U0001F30D Environmental Problem Query:", value="Biodiversity is declining on my land. Soil organic carbon is low at 0.3%, annual rainfall ~480mm (semi-arid), monoculture wheat, fragmented landscape with 15% canopy cover.", height=120)
    if st.button("\U0001F680 Run Scientific Ecosystem Analysis", type="primary", use_container_width=True):
        payload = EcosystemQueryPayload(
            query_text=query_text,
            soil=SoilMetrics(organic_carbon_pct=soc, ph=ph),
            climate=ClimateMetrics(annual_rainfall_mm=rainfall, mean_temperature_c=temperature),
            land_use=LandUseMetrics(land_cover_type=crop, canopy_cover_pct=canopy, fragmentation_index=frag),
            spatial=SpatialContext(latitude=lat, longitude=lon)
        )
        with st.spinner("\u2699\ufe0f Executing LangGraph Multi-Agent Reasoning..."):
            initial_state = {
                "payload": payload, "spatial_profile": None, "completeness_score": 0.0,
                "is_clarification_required": False, "clarification_details": None,
                "coupled_analysis": None, "retrieved_docs": [], "final_analysis": None
            }
            res = graph.invoke(initial_state)["final_analysis"]
        st.session_state["last_result"] = res
        if res.status == "clarification_needed":
            st.warning("\u26a0\ufe0f Input Incomplete for Scientific Calibration")
            st.write(f"**Reason:** {res.clarification.reason_needed}")
            for q in res.clarification.suggested_questions:
                st.info(f"\U0001F449 {q}")
        else:
            st.success("\u2705 Multi-Metric Scientific Analysis Complete")
            st.info(f"**Summary:** {res.summary}")
            if res.synthesized_reasoning:
                with st.expander("\U0001F52C Synthesized Reasoning", expanded=True):
                    st.write(res.synthesized_reasoning)
            for i, rec in enumerate(res.recommendations, 1):
                with st.expander(f"\U0001F4CC Rec {i}: {rec.intervention_name} [{rec.priority_level}]", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Time Horizon", rec.time_horizon.split(" ")[0])
                    c2.metric("Confidence", f"{rec.confidence_score*100:.1f}%")
                    c3.metric("Coupled Vars", len(rec.coupled_variables))
                    st.write(f"**Rationale:** {rec.scientific_mechanism}")
                    st.write(f"**Variables:** `{', '.join(rec.coupled_variables)}`")
                    st.markdown("#### \U0001F4CA Metric Deltas")
                    if rec.impacted_metrics:
                        cols = st.columns(min(len(rec.impacted_metrics), 3))
                        for idx, met in enumerate(rec.impacted_metrics):
                            with cols[idx % 3]:
                                st.metric(met.metric_name, met.projected_value, met.delta_percentage)
                                st.caption(f"Baseline: {met.baseline_value}")
                    st.markdown("#### \U0001F4DA Citations")
                    for cite in rec.citations:
                        st.markdown(f"- **{cite.authors_or_organization} ({cite.year})** *{cite.source_title}* [DOI]({cite.doi_or_url})")

with tab_json:
    if "last_result" in st.session_state:
        st.subheader("Raw Pydantic v2 JSON Output")
        st.json(st.session_state["last_result"].model_dump())
    else:
        st.info("Run an analysis first to see JSON output.")
