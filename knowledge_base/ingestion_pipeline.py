import os
import json
import glob
from src.config import settings
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document


def run_ingestion():
    print("Starting Knowledge Base Ingestion...")
    documents = []
    
    # Load raw documents
    data_dir = os.path.join(os.path.dirname(__file__), 'raw_documents')
    for filepath in glob.glob(os.path.join(data_dir, '*.json')):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Flatten JSON arrays into Langchain Documents
            if isinstance(data, list):
                for item in data:
                    text_content = item.pop("text", "") or item.pop("content", "") or str(item)
                    doc = Document(
                        page_content=text_content,
                        metadata=item
                    )
                    documents.append(doc)
    print(f"[*] Loaded {len(documents)} scientific records.")
    print("[*] Embedding model loading (Gemini API)...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.google_api_key
    )
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=settings.chroma_persist_dir,
        collection_name="darukaa_biodiversity_kb",
    )
    print(f"[+] KB ingested into ChromaDB at: {settings.chroma_persist_dir}")
    return vectorstore


if __name__ == "__main__":
    run_ingestion()
