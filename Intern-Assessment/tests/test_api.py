"""
Tests for the RAG API backend.
Run with: pytest tests/ -v
"""
import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile

# Add backend to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.main import app
from backend.config import UPLOADS_DIR

client = TestClient(app)


@pytest.fixture
def cleanup_uploads():
    """Clean up uploaded files after tests."""
    yield
    # Cleanup
    for file in UPLOADS_DIR.glob("*"):
        if file.is_file():
            file.unlink()


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test that health check endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestRoot:
    """Test root endpoint."""

    def test_root_endpoint(self):
        """Test that root endpoint returns available endpoints."""
        response = client.get("/")
        assert response.status_code == 200
        assert "endpoints" in response.json()


class TestIngest:
    """Test document ingestion endpoint."""

    def test_ingest_txt_file(self, cleanup_uploads):
        """Test ingesting a text file."""
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document. It contains test content.")
            temp_path = f.name

        try:
            with open(temp_path, 'rb') as f:
                response = client.post(
                    "/ingest",
                    files={"file": ("test.txt", f, "text/plain")}
                )
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "chunks_created" in response.json()
        finally:
            os.unlink(temp_path)

    def test_ingest_unsupported_file(self, cleanup_uploads):
        """Test that unsupported file types are rejected."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            with open(temp_path, 'rb') as f:
                response = client.post(
                    "/ingest",
                    files={"file": ("test.xyz", f, "application/octet-stream")}
                )
            assert response.status_code == 400
            assert "not supported" in response.json()["detail"]
        finally:
            os.unlink(temp_path)

    def test_ingest_empty_file(self, cleanup_uploads):
        """Test ingesting an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            with open(temp_path, 'rb') as f:
                response = client.post(
                    "/ingest",
                    files={"file": ("empty.txt", f, "text/plain")}
                )
            # Should succeed but create 0 chunks
            assert response.status_code in [200, 400]
        finally:
            os.unlink(temp_path)


class TestAsk:
    """Test question asking endpoint."""

    def test_ask_without_documents(self):
        """Test asking a question without any ingested documents."""
        response = client.post("/ask?question=What+is+this?")
        assert response.status_code in [200, 400]
        result = response.json()
        assert "I don't know" in result.get("answer", "")

    def test_ask_empty_question(self):
        """Test asking an empty question."""
        response = client.post("/ask?question=")
        assert response.status_code == 400


class TestStats:
    """Test statistics endpoint."""

    def test_get_stats(self):
        """Test getting vector store statistics."""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "vector_store" in data
        assert "documents_count" in data


class TestClear:
    """Test clear endpoint."""

    def test_clear_documents(self):
        """Test clearing vector store."""
        response = client.delete("/clear")
        assert response.status_code == 200
        assert response.json()["success"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
