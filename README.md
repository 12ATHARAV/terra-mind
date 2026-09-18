---
title: TERRA-MIND
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: docker
sdk_version: 1.42.2
app_file: app.py
pinned: false
---
# TERRA-MIND: AI Biodiversity & Ecological Intelligence Engine

**Darukaa.Earth Hackathon Submission**

Multi-agent AI system for ecological reasoning built on LangGraph, ChromaDB, and Google Gemini 2.5. Delivers scientifically grounded, citation-backed recommendations for biodiversity restoration.

## Architecture

```
User Input -> LangGraph StateGraph
  triage_node -> [incomplete] -> clarification_node -> END
              -> [complete] -> spatial_reasoning_node -> retrieval_node -> synthesis_auditor_node -> END
-> Pydantic v2 JSON Output (Recommendations + Citations + Metric Deltas + Confidence)
```

| Component | Technology |
|-----------|------------|
| Agent Orchestration | LangGraph StateGraph |
| LLM | Gemini 2.5 Flash/Pro (configurable) |
| Knowledge Base | FAO, IPCC AR6, IPBES, ICRAF, IUCN |
| Vector Store | ChromaDB + HuggingFace Embeddings |
| Schema | Pydantic v2 |
| API | FastAPI + Uvicorn |
| UI | Streamlit + Folium |
| Tests | Pytest |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Set GOOGLE_API_KEY in .env
python knowledge_base/ingestion_pipeline.py
```

## Run

```bash
# FastAPI
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

# Streamlit (separate terminal)
streamlit run ui/streamlit_app.py
```

## Test

```bash
pytest tests/ -v
```

## Docker

```bash
GOOGLE_API_KEY=your_key docker compose up --build
```

## API Example

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query_text": "Low SOC, low rainfall, monoculture wheat", "soil": {"organic_carbon_pct": 0.3}, "climate": {"annual_rainfall_mm": 480}, "land_use": {"land_cover_type": "Monoculture Wheat"}}'
```

## LLM Configuration

Set `LLM_MODEL` in `.env` to switch models:
- `gemini-2.5-flash` (default, fast)
- `gemini-2.5-pro` (deeper reasoning)

## Author
- **Atharav Dhumone**

