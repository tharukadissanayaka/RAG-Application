"""FastAPI RAG application."""
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import UPLOADS_DIR, MAX_UPLOAD_SIZE
from ingestion import DocumentIngester
from retrieval import RAGRetriever

app = FastAPI(
    title="RAG API",
    description="A Retrieval-Augmented Generation API for document-based Q&A",
    version="1.0.0",
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ingester and retriever
ingester = DocumentIngester()
retriever = RAGRetriever()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "RAG API",
    }


@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Upload and ingest a document (.txt or .pdf).
    
    Args:
        file: The document file to ingest
        
    Returns:
        Ingestion status and metadata
    """
    # Validate file type
    allowed_extensions = {".txt", ".pdf"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed: {allowed_extensions}",
        )

    # Validate file size
    file_size = len(await file.read())
    await file.seek(0)  # Reset file pointer
    
    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE} bytes",
        )

    try:
        # Save uploaded file
        file_path = UPLOADS_DIR / file.filename
        contents = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(contents)

        # Ingest the file
        result = ingester.ingest_file(file_path)
        
        return JSONResponse(
            status_code=200 if result["success"] else 400,
            content=result,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}",
        )
    finally:
        # Cleanup uploaded file (optional - can keep for reference)
        if file_path.exists():
            file_path.unlink()


@app.post("/ask")
async def ask_question(question: str):
    """
    Ask a question based on ingested documents.
    
    Args:
        question: The question to ask
        
    Returns:
        Answer with context and metadata
    """
    if not question or not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    # Check if vector store has documents
    status = retriever.check_vector_store_status()
    if not status["has_documents"]:
        return JSONResponse(
            status_code=400,
            content={
                "answer": "I don't know. (No documents ingested yet)",
                "context": [],
                "error": "Please ingest documents first using the /ingest endpoint",
            },
        )

    # Get answer
    result = retriever.query(question)
    
    return JSONResponse(
        status_code=200 if result.get("success", False) else 400,
        content=result,
    )


@app.get("/stats")
async def get_stats():
    """Get statistics about ingested documents."""
    ingest_stats = ingester.get_vector_store_stats()
    retriever_status = retriever.check_vector_store_status()
    
    return JSONResponse(
        status_code=200,
        content={
            "vector_store": ingest_stats,
            "documents_count": retriever_status["document_count"],
        },
    )


@app.delete("/clear")
async def clear_documents():
    """Clear all ingested documents from the vector store."""
    result = ingester.clear_vector_store()
    
    return JSONResponse(
        status_code=200 if result["success"] else 500,
        content=result,
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the RAG API",
        "endpoints": {
            "health": "/health (GET)",
            "ingest": "/ingest (POST) - Upload .txt or .pdf files",
            "ask": "/ask (POST) - Ask questions based on ingested documents",
            "stats": "/stats (GET) - Get vector store statistics",
            "clear": "/clear (DELETE) - Clear all documents",
            "docs": "/docs (GET) - Interactive API documentation (Swagger UI)",
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
    )
