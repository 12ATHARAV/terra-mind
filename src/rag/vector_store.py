import os
from src.config import settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_vectorstore() -> Chroma:
    if not os.path.exists(settings.chroma_persist_dir) or not os.listdir(settings.chroma_persist_dir):
        print("[!] Local ChromaDB missing. Auto-building from corpus...")
        from knowledge_base.ingestion_pipeline import run_ingestion
        run_ingestion()
        
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model, model_kwargs={'local_files_only': False})
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    return Chroma(
        persist_directory=settings.chroma_persist_dir,
        embedding_function=embeddings,
        collection_name="darukaa_biodiversity_kb",
    )
