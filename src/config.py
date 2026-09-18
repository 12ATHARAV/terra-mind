import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "chroma")
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "biodiversity-corpus")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    llm_temperature: float = 0.1

settings = Settings()
