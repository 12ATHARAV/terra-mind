import pytest
from langchain_core.documents import Document
from src.rag.hybrid_retriever import ScientificHybridRetriever


def test_retriever_returns_documents():
    retriever = ScientificHybridRetriever()
    docs = retriever.retrieve_scientific_evidence("soil organic carbon")
    assert isinstance(docs, list)
    assert len(docs) >= 1


def test_documents_have_metadata():
    retriever = ScientificHybridRetriever()
    docs = retriever.retrieve_scientific_evidence("biodiversity")
    for doc in docs:
        assert isinstance(doc, Document)
        assert "citation_id" in doc.metadata


def test_documents_have_content():
    retriever = ScientificHybridRetriever()
    docs = retriever.retrieve_scientific_evidence("mangrove")
    for doc in docs:
        assert len(doc.page_content) > 20
