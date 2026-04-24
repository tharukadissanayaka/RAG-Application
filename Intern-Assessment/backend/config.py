"""Configuration and environment variables."""
import os
from pathlib import Path

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./chroma_db")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB default
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

# Paths
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SIMILARITY_TOP_K = 3

# System prompt for LLM
SYSTEM_PROMPT = """You are a helpful assistant that answers questions based exclusively on the provided context. 
Follow these rules strictly:
1. Only use information from the provided context to answer questions.
2. If the answer is not in the context, respond with exactly: "I don't know."
3. Do not use any external knowledge or make assumptions.
4. If the question is unclear, ask for clarification.
5. Always cite the source when possible."""
