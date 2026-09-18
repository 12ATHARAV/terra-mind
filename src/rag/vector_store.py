import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import settings


def get_vectorstore() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    return Chroma(
        persist_directory=settings.chroma_persist_dir,
        embedding_function=embeddings,
        collection_name="darukaa_biodiversity_kb",
    )
