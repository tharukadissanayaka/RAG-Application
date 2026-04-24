# RAG Application - Complete Requirements

## Backend Requirements (`backend/requirements.txt`)

### Core Framework

- fastapi==0.104.1 # API framework
- uvicorn==0.24.0 # ASGI server

### LangChain & LLM Integration

- langchain==0.1.0 # RAG framework
- langchain-groq==0.1.0 # Groq LLM integration
- langchain-chroma==0.1.1 # ChromaDB integration
- langchain-community==0.0.24 # Additional tools

### Vector Stores & Embeddings

- chromadb==0.4.21 # Vector database
- sentence-transformers==2.2.2 # Embedding model

### Document Processing

- pypdf==3.17.1 # PDF parsing
- pydantic==2.5.0 # Data validation

### Utilities

- python-multipart==0.0.6 # File upload handling
- python-dotenv==1.0.0 # Environment variables

## Frontend Requirements (`frontend/requirements.txt`)

- streamlit==1.30.0 # Web UI framework
- requests==2.31.0 # HTTP client

## Development Requirements

```bash
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Code Quality
flake8==6.1.0
black==23.12.1
mypy==1.7.1

# Type Hints
types-requests==2.31.0.10
```

## Installation

### Option 1: From Requirements Files

```bash
# Backend
pip install -r backend/requirements.txt

# Frontend (optional)
pip install -r frontend/requirements.txt

# Development
pip install pytest pytest-asyncio httpx flake8 black mypy
```

### Option 2: Using Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install all dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### Option 3: Docker

```bash
# Docker Compose automatically installs all dependencies
docker-compose up --build
```

## Version Compatibility

- **Python**: 3.11+ (required)
- **Docker**: 20.10+ (recommended)
- **Docker Compose**: 2.0+ (recommended)

## Dependency Notes

### LangChain Ecosystem

- **langchain**: Core RAG framework for document processing
- **langchain-groq**: Integration with Groq API
- **langchain-chroma**: ChromaDB integration for vector storage
- **langchain-community**: Additional utilities and tools

### FastAPI & Uvicorn

- **fastapi**: Modern async API framework
- **uvicorn**: ASGI server for FastAPI
- Supports automatic API documentation (Swagger UI)

### Vector Storage

- **chromadb**: Lightweight vector database
- In-memory with SQLite backend (production-ready)
- Supports ~100GB+ of vectors per instance

### Text Processing

- **sentence-transformers**: Pre-trained embedding models
- Using "all-MiniLM-L6-v2" for low-resource environments
- 384-dimensional embeddings

### Document Loading

- **pypdf**: PDF parsing and extraction
- Built-in Python UTF-8 text support

## Outdated Dependencies & Replacements

If any dependency becomes outdated:

| Old             | New    | Reason             |
| --------------- | ------ | ------------------ |
| langchain 0.1.0 | 0.2.x  | Latest features    |
| chromadb 0.4    | 0.5.x  | Better performance |
| fastapi 0.104   | 0.110+ | Security patches   |

## Security Updates

Check for vulnerabilities:

```bash
# pip audit
pip install pip-audit
pip-audit

# Safety check
pip install safety
safety check
```

## Performance Tips

1. **Virtual Environment**: Always use a virtual environment
2. **Pinned Versions**: Use exact versions for reproducibility
3. **Lightweight Models**: Using all-MiniLM-L6-v2 saves ~500MB
4. **Async Processing**: FastAPI handles concurrent requests
5. **Caching**: ChromaDB caches embeddings automatically

## Troubleshooting Installation

### Issue: ImportError for langchain modules

```bash
# Solution: Reinstall langchain ecosystem
pip uninstall langchain langchain-groq langchain-chroma langchain-community -y
pip install langchain==0.1.0 langchain-groq==0.1.0 langchain-chroma==0.1.1 langchain-community==0.0.24
```

### Issue: chromadb compatibility

```bash
# Solution: Ensure compatibility
pip install --upgrade chromadb
```

### Issue: pypdf errors

```bash
# Solution: Use latest version
pip install --upgrade pypdf
```

### Issue: CUDA/GPU support (optional)

For GPU acceleration:

```bash
# Install torch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Then reinstall sentence-transformers
pip install --force-reinstall sentence-transformers
```

## Production Dependencies

For production deployments, also consider:

```bash
# Database
psycopg2-binary==2.9.9      # PostgreSQL adapter (for pgvector)

# Caching
redis==5.0.1                 # Redis client

# Monitoring
prometheus-client==0.19.0    # Prometheus metrics

# Logging
structlog==23.3.0            # Structured logging

# Error Tracking
sentry-sdk==1.40.2           # Sentry integration

# Rate Limiting
slowapi==0.1.9               # FastAPI rate limiting
```

## Updating Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages (not recommended)
pip install --upgrade -r requirements.txt

# Create updated requirements.txt
pip freeze > requirements-updated.txt
```

## License & Compliance

All dependencies are open-source with compatible licenses:

- **MIT**: FastAPI, uvicorn, requests, streamlit, python-dotenv
- **Apache 2.0**: LangChain, ChromaDB, sentence-transformers
- **Other open licenses**: Check individual packages

No GPL dependencies that would enforce open-sourcing your code.
