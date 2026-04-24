# Development Guide

## Project Structure

```
Intern-Assessment/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application
│   ├── config.py              # Configuration
│   ├── ingestion.py           # Document processing
│   ├── retrieval.py           # RAG logic
│   └── requirements.txt        # Dependencies
├── frontend/                   # Streamlit frontend
│   ├── app.py                 # Streamlit interface
│   ├── Dockerfile             # Frontend container
│   └── requirements.txt        # Dependencies
├── .github/workflows/         # CI/CD pipelines
│   ├── docker-build.yml       # Docker build workflow
│   └── tests.yml              # Test workflow
├── Dockerfile                 # Backend container
├── docker-compose.yml         # Docker compose config
├── .env.example               # Environment template
├── .dockerignore               # Docker ignore file
└── README.md                  # Documentation
```

## Development Workflow

### 1. Local Development

```bash
# Backend development
cd backend
python -m uvicorn main:app --reload

# Frontend development (in another terminal)
cd frontend
streamlit run app.py
```

### 2. Code Quality

```bash
# Lint code
flake8 backend frontend

# Format code
black backend frontend

# Type checking
mypy backend
```

### 3. Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html
```

## Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Required variables:

- `GROQ_API_KEY`: Your Groq API key

Optional variables:

- `MODEL_NAME`: LLM model (default: mixtral-8x7b-32768)
- `VECTOR_STORE_PATH`: Path to ChromaDB (default: ./chroma_db)
- `PORT`: API port (default: 8000)
- `MAX_UPLOAD_SIZE`: Max file size in bytes (default: 10485760)

## Adding New Features

### Adding a New Endpoint

1. Add the endpoint to `backend/main.py`
2. Implement the logic in the appropriate module
3. Add error handling
4. Document in docstrings

Example:

```python
@app.post("/new-endpoint")
async def new_endpoint(data: SomeModel):
    """
    Description of the endpoint.

    Args:
        data: Input data

    Returns:
        Response data
    """
    # Implementation
    return {"result": "success"}
```

### Updating Dependencies

1. Update the requirements file
2. Test locally
3. Update Docker build
4. Tag a new version

## Docker Development

### Build Images

```bash
# Backend
docker build -t rag-backend:latest .

# Frontend
docker build -t rag-frontend:latest -f frontend/Dockerfile ./frontend

# Using Docker Compose
docker-compose build
```

### Run Containers

```bash
# Run all services
docker-compose up

# Run specific service
docker-compose up backend

# Rebuild and run
docker-compose up --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

## Performance Optimization

### Memory Optimization

1. **Vector Store**: ChromaDB is in-memory; configure persistence
2. **Embeddings**: Using lightweight sentence-transformers/all-MiniLM-L6-v2
3. **LLM**: Using Groq for fast inference
4. **Chunking**: 1000 chars with 200 overlap balances accuracy and efficiency

### Speed Optimization

1. **Caching**: Vector store caches embeddings
2. **Async**: FastAPI handles concurrent requests
3. **Pruning**: Only retrieve top-3 similar chunks
4. **Streaming**: Consider implementing streaming responses

### Monitoring

```bash
# Check resource usage
docker stats

# Check logs
docker logs -f <container-name>

# API health
curl http://localhost:8000/health
```

## Deployment Checklist

- [ ] All environment variables set
- [ ] `.env` file not committed to git
- [ ] Dependencies pinned to specific versions
- [ ] Docker build passes
- [ ] Tests pass
- [ ] API documentation updated
- [ ] README updated
- [ ] Health checks configured
- [ ] Error handling complete
- [ ] Security reviewed

## Common Issues

### Import Errors

```bash
# Reinstall dependencies
pip install -r backend/requirements.txt --force-reinstall
```

### Port Already in Use

```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

### Vector Store Not Persisting

```bash
# Check volume mount in docker-compose.yml
# Ensure VECTOR_STORE_PATH is set correctly
```

### GROQ API Rate Limiting

- Free tier: 30 requests/minute
- Implement request queuing for production
- Consider batch processing

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Docker Documentation](https://docs.docker.com/)

## Support

For questions or issues:

1. Check README.md
2. Review code comments
3. Check GitHub issues
4. Create a new issue with reproduction steps
