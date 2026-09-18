from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.schemas.ecosystem_input import EcosystemQueryPayload
from src.schemas.scientific_output import EcosystemAnalysisResult
from src.agents.graph import graph

app = FastAPI(
    title="TERRA-MIND: AI Biodiversity Intelligence Engine",
    description="Scientific conversational AI for ecosystem restoration (Darukaa.Earth)",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "engine": "TERRA-MIND Multi-Agent LangGraph v1.0"}


@app.post("/api/v1/analyze", response_model=EcosystemAnalysisResult)
def analyze_ecosystem(payload: EcosystemQueryPayload):
    try:
        initial_state = {
            "payload": payload, "spatial_profile": None, "completeness_score": 0.0,
            "is_clarification_required": False, "clarification_details": None,
            "coupled_analysis": None, "retrieved_docs": [], "final_analysis": None
        }
        final_state = graph.invoke(initial_state)
        result = final_state.get("final_analysis")
        if result is None:
            raise ValueError("Graph returned no analysis result.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
