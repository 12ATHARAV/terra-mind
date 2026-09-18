import os
import json
import glob
from src.config import settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


def run_ingestion():
    print("[*] Initializing Knowledge Ingestion Pipeline...")
    doc_files = glob.glob("knowledge_base/raw_documents/*.json")
    documents = []
    for fpath in doc_files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                doc = Document(
                    page_content=item["content"],
                    metadata={
                        "citation_id": item["id"],
                        "source_title": item["title"],
                        "authors_or_organization": item["source"],
                        "year": item["year"],
                        "doi_or_url": item["doi"],
                        "domain": item.get("domain", "general"),
                        "climate_zone": item.get("climate_zone", "all")
                    }
                )
                documents.append(doc)
    print(f"[*] Loaded {len(documents)} scientific records.")
    print("[*] Embedding model loading (local cache)...")
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model, model_kwargs={'local_files_only': True})
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=settings.chroma_persist_dir,
        collection_name="darukaa_biodiversity_kb"
    )
    print(f"[+] KB ingested into ChromaDB at: {settings.chroma_persist_dir}")
    return vectorstore


if __name__ == "__main__":
    run_ingestion()
