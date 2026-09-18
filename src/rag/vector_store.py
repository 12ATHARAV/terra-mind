import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import settings


def get_vectorstore() -> Chroma:
    if not os.path.exists(settings.chroma_persist_dir) or not os.listdir(settings.chroma_persist_dir):
        print("[!] Local ChromaDB missing. Auto-building from corpus...")
        from knowledge_base.ingestion_pipeline import run_ingestion
        run_ingestion()
        
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.google_api_key
    )
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    return Chroma(
        persist_directory=settings.chroma_persist_dir,
        embedding_function=embeddings,
        collection_name="darukaa_biodiversity_kb",
    )
