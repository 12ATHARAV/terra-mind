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

<div align="center">
  <h1>🌱 TERRA-MIND</h1>
  <p><b>AI Biodiversity & Ecological Intelligence Engine</b></p>
  <p><i>Built for the <b>Darukaa.Earth Hackathon</b></i></p>

  [![Live Demo](https://img.shields.io/badge/Live_Demo-Hosted_on_Render-46E3B7?style=for-the-badge&logo=render)](https://terra-mind.onrender.com/)
  <br/>
  
  ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
  ![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF4F00?style=flat-square)
  ![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=flat-square&logo=google)
  ![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
  ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F61?style=flat-square)
  ![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=flat-square&logo=fastapi&logoColor=white)
</div>

<br/>

## 🌍 Overview

**TERRA-MIND** is a sophisticated, multi-agent artificial intelligence system designed to combat biodiversity loss, optimize land management, and restore degraded ecosystems.

Traditional ecological analysis relies on static rule-based systems. TERRA-MIND uses **LangGraph** to orchestrate multiple autonomous AI agents that reason over a **Hybrid RAG Knowledge Base** containing real scientific literature from the FAO, IPCC, IPBES, and IUCN. 

The system takes in complex environmental parameters and outputs strictly structured, citation-backed interventions using **Pydantic v2 JSON schema validation**, completely eliminating LLM hallucinations.

---

## 🚀 Live Interactive Demo

The application is deployed live on Render and is accessible via the web browser.
**👉 [Click here to launch the TERRA-MIND Web Interface](https://terra-mind.onrender.com/)**

---

## 🧠 System Architecture

The core of TERRA-MIND is a **LangGraph StateGraph** that orchestrates a pipeline of specialized agents:

1. **Intake Triage Agent**: Evaluates user queries for scientific completeness. If critical data (like Soil pH or Climate) is missing, it dynamically generates clarifying questions instead of hallucinating.
2. **Spatial Reasoning Agent**: Analyzes latitude/longitude inputs to classify the biome (e.g., "Tropical Monsoon", "Semi-Arid Steppe") and applies location-specific ecological constraints.
3. **Scientific Hybrid RAG Agent**: Queries a localized **ChromaDB** vector store embedded via **Google Gemini Embeddings**, retrieving strictly relevant, peer-reviewed intervention methodologies.
4. **Synthesis Auditor Agent**: Synthesizes the retrieved science with the user's input matrix. Forces the LLM (Gemini 2.5) to return a strictly typed **Pydantic v2 JSON** payload containing actionable, citation-backed recommendations, expected metric deltas, and confidence scores.

### The 4 Pillars of Input Data
TERRA-MIND calculates recommendations based on a 4-dimensional matrix:
* **🌱 Soil Metrics**: Organic Carbon (SOC %), pH levels.
* **🌦️ Climate**: Annual Precipitation (mm), Mean Temperature (°C).
* **🌾 Land Cover**: Canopy Cover (%), Fragmentation Index, Crop Type.
* **📍 Spatial Context**: Latitude & Longitude (analyzed via Folium Maps).

---

## 🛠️ Technology Stack

* **AI & Orchestration**: LangChain, LangGraph, Google Gemini 2.5 Flash
* **Vector & Embeddings**: ChromaDB, GoogleGenerativeAIEmbeddings (models/embedding-001)
* **Data Validation**: Pydantic v2
* **Backend**: FastAPI, Uvicorn, Pytest
* **Frontend**: Streamlit, Folium (Maps)
* **Deployment**: Docker, Render.com

---

## 💻 Local Installation & Setup

Want to run TERRA-MIND on your own machine? It takes less than 2 minutes.

### 1. Clone the repository
`ash
git clone https://github.com/12ATHARAV/terra-mind.git
cd terra-mind
`

### 2. Set up your Environment
`ash
# Install dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
`
Open the .env file and add your Google Gemini API Key:
GOOGLE_API_KEY=your_key_here

### 3. Initialize the Vector Database (Optional)
*Note: The app will automatically build the database on first boot if missing!*
`ash
python knowledge_base/ingestion_pipeline.py
`

### 4. Run the User Interface (Streamlit)
`ash
# This script bypasses Anaconda DLL conflicts on Windows
.\RUN_APP.bat

# Or run it manually:
streamlit run ui/streamlit_app.py
`

### 5. Run the Headless API (FastAPI)
`ash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
`

---

## 🧪 Testing

The system is rigorously tested to ensure deterministic behavior and fallback mechanisms.
`ash
pytest tests/ -v
`
*(100% Pass Rate: Includes tests for agent routing, schema validation, and offline zero-crash fallbacks).*

---

## 👨‍💻 Author

**Atharav Dhumone**  
*Hackathon Submission for Darukaa.Earth*
