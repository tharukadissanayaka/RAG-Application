"""Document ingestion and vector store management."""
import os
import random
from pathlib import Path
from typing import List
import shutil

from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import VECTOR_STORE_PATH, CHUNK_SIZE, CHUNK_OVERLAP, UPLOADS_DIR


class LocalEmbeddings(Embeddings):
    """Deterministic, lightweight embeddings for local startup."""

    def __init__(self, size: int = 384):
        self.size = size

    def _embed(self, text: str) -> List[float]:
        seed = hash(text) & 0xFFFFFFFF
        generator = random.Random(seed)
        return [generator.uniform(-1.0, 1.0) for _ in range(self.size)]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)


class DocumentIngester:
    """Handles document ingestion and vector store management."""

    def __init__(self):
        """Initialize the ingester with embeddings and vector store."""
        self.embeddings = LocalEmbeddings()
        self.vector_store = Chroma(
            persist_directory=VECTOR_STORE_PATH,
            embedding_function=self.embeddings,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""],
        )

    def ingest_file(self, file_path: Path) -> dict:
        """
        Ingest a text or PDF file into the vector store.
        
        Args:
            file_path: Path to the file to ingest
            
        Returns:
            dict with ingestion status and metadata
        """
        try:
            file_ext = file_path.suffix.lower()
            
            if file_ext == ".txt":
                loader = TextLoader(str(file_path))
            elif file_ext == ".pdf":
                loader = PyPDFLoader(str(file_path))
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_ext}",
                }

            documents = loader.load()
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["source_file"] = file_path.name
                chunk.metadata["chunk_id"] = i

            # Add to vector store
            self.vector_store.add_documents(chunks)

            return {
                "success": True,
                "file_name": file_path.name,
                "chunks_created": len(chunks),
                "message": f"Successfully ingested {file_path.name} ({len(chunks)} chunks)",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def clear_vector_store(self) -> dict:
        """Clear all documents from the vector store."""
        try:
            data = self.vector_store.get()
            ids = data.get("ids", [])
            if ids:
                self.vector_store.delete(ids=ids)
            
            return {
                "success": True,
                "message": "Vector store cleared successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def get_vector_store_stats(self) -> dict:
        """Get statistics about the vector store."""
        try:
            # Get the number of documents in the vector store
            doc_count = len(self.vector_store.get()["ids"])
            
            return {
                "success": True,
                "total_documents": doc_count,
                "vector_store_path": VECTOR_STORE_PATH,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
