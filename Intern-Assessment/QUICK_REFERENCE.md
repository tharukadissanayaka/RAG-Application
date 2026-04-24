# Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

### 1. Prerequisites

- Python 3.11+ or Docker installed
- Groq API key (free at https://console.groq.com)

### 2. Setup

```bash
# Clone repository
cd Intern-Assessment

# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here
```

### 3. Run with Docker

```bash
docker-compose up --build
```

### 4. Access Services

- **Frontend**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📖 Common Commands

### Backend Development

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run API server
cd backend
python -m uvicorn main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Check code quality
flake8 backend
```

### Frontend Development

```bash
# Install dependencies
pip install -r frontend/requirements.txt

# Run Streamlit
cd frontend
streamlit run app.py
```

### Docker Commands

```bash
# Build and run all services
docker-compose up --build

# Run specific service
docker-compose up backend

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Clean up
docker system prune -a
```

---

## 🔑 API Quick Reference

### Upload Document

```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"
```

### Ask Question

```bash
curl -X POST "http://localhost:8000/ask?question=What+is+this+about?"
```

### Get Stats

```bash
curl "http://localhost:8000/stats"
```

### Clear Vector Store

```bash
curl -X DELETE "http://localhost:8000/clear"
```

### Check Health

```bash
curl "http://localhost:8000/health"
```

---

## 📁 File Structure

```
Intern-Assessment/
│
├── backend/                    # FastAPI backend
│   ├── main.py                # API application
│   ├── config.py              # Configuration
│   ├── ingestion.py           # Document processing
│   ├── retrieval.py           # RAG logic
│   └── requirements.txt        # Dependencies
│
├── frontend/                   # Streamlit frontend
│   ├── app.py                 # Web interface
│   ├── Dockerfile             # Container
│   ├── requirements.txt        # Dependencies
│   └── .streamlit/             # Config
│
├── tests/                      # Test suite
│   └── test_api.py            # API tests
│
├── .github/workflows/         # CI/CD
│   ├── docker-build.yml       # Docker build
│   └── tests.yml              # Tests
│
├── Dockerfile                 # Backend container
├── docker-compose.yml         # Container orchestration
├── .env.example              # Environment template
├── .dockerignore              # Docker ignore
├── .gitignore                # Git ignore
│
├── README.md                 # Main documentation
├── API.md                    # API specification
├── ARCHITECTURE.md           # System design
├── DEVELOPMENT.md            # Dev guide
├── DEPLOYMENT.md             # Deploy guide
├── REQUIREMENTS.md           # Dependencies
├── CHECKLIST.md             # Completion status
└── QUICK_REFERENCE.md       # This file
```

---

## 🔧 Configuration

### Environment Variables

```env
# Required
GROQ_API_KEY=your_key_here

# Optional (defaults shown)
MODEL_NAME=mixtral-8x7b-32768
VECTOR_STORE_PATH=./chroma_db
PORT=8000
MAX_UPLOAD_SIZE=10485760  # 10MB
```

### Chunk Settings

Edit `backend/config.py`:

```python
CHUNK_SIZE = 1000           # Characters per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
SIMILARITY_TOP_K = 3        # Results per question
```

### LLM Configuration

Edit `backend/config.py`:

```python
SYSTEM_PROMPT = "..."       # Instructions for LLM
MODEL_NAME = "mixtral..."   # Groq model name
```

---

## 🐛 Troubleshooting

### API Won't Start

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r backend/requirements.txt --force-reinstall

# Check port
lsof -i :8000  # Kill process if needed
```

### Frontend Won't Connect

```bash
# Ensure backend is running on port 8000
curl http://localhost:8000/health

# Check firewall
# Windows: Check Windows Defender Firewall
# Linux: Check iptables/firewalld
```

### No API Key

```bash
# Create .env file
cp .env.example .env

# Add your Groq API key
# https://console.groq.com → API Keys
```

### Docker Issues

```bash
# Rebuild without cache
docker-compose build --no-cache

# Clean up
docker system prune -a

# Check Docker daemon
docker ps
```

### Out of Memory

```bash
# Reduce chunk size in config.py
CHUNK_SIZE = 500  # Default: 1000

# Clear vector store
curl -X DELETE http://localhost:8000/clear

# Use lighter embedding model (see ARCHITECTURE.md)
```

---

## 📊 Performance Tips

| Action                    | Impact                   |
| ------------------------- | ------------------------ |
| Increase CHUNK_SIZE       | Faster but less accurate |
| Decrease CHUNK_SIZE       | More accurate but slower |
| Increase SIMILARITY_TOP_K | More context, slower     |
| Use SSD storage           | 2-3x faster embeddings   |
| Parallel requests         | Better resource usage    |

---

## 🚀 Deployment in 10 Minutes

### Render.com (Recommended)

1. Connect GitHub repo
2. Create Web Service
3. Set build: `pip install -r backend/requirements.txt`
4. Set start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add env: `GROQ_API_KEY=your_key`
6. Deploy!

### Koyeb

1. Connect GitHub repo
2. Select Docker
3. Set PORT: 8000
4. Add env: `GROQ_API_KEY=your_key`
5. Deploy!

### Local Docker

```bash
docker-compose up --build
```

---

## 📚 Documentation Links

| Document                           | Purpose                 |
| ---------------------------------- | ----------------------- |
| [README.md](README.md)             | Overview and features   |
| [API.md](API.md)                   | Complete API reference  |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design           |
| [DEVELOPMENT.md](DEVELOPMENT.md)   | Development guide       |
| [DEPLOYMENT.md](DEPLOYMENT.md)     | Deployment instructions |
| [REQUIREMENTS.md](REQUIREMENTS.md) | Dependencies            |
| [CHECKLIST.md](CHECKLIST.md)       | Completion status       |

---

## 🎯 Workflow Examples

### Typical User Workflow

1. Upload document via Streamlit
2. Ask questions about the document
3. Review context and answers
4. Upload more documents or clear

### Developer Workflow

1. Make code changes
2. Test locally: `pytest tests/ -v`
3. Check quality: `flake8 backend`
4. Git commit and push
5. GitHub Actions auto-builds Docker image

### Deployment Workflow

1. Prepare .env with API key
2. Push to GitHub
3. GitHub Actions builds Docker image
4. Deploy to Render/Koyeb/Railway
5. Monitor at cloud dashboard

---

## 💡 Pro Tips

### 1. API Documentation

Always check `/docs` endpoint for interactive docs:

```
http://localhost:8000/docs
```

### 2. Chat History

Streamlit persists chat in session state. Refresh page to reset.

### 3. Vector Store

ChromaDB stores vectors in `chroma_db/` directory. Back this up!

### 4. Large Documents

For files >10MB, split before uploading or increase MAX_UPLOAD_SIZE.

### 5. Rate Limiting

Groq free tier: 30 requests/minute. Plan accordingly.

### 6. Embeddings

Using lightweight model (all-MiniLM-L6-v2) saves memory vs larger models.

### 7. System Prompt

Modify in `backend/config.py` to change LLM behavior.

---

## 🆘 Getting Help

1. **Check Documentation**: Start with README.md
2. **Check Logs**: `docker-compose logs -f backend`
3. **Check Tests**: `pytest tests/ -v`
4. **Check API Docs**: http://localhost:8000/docs
5. **Create GitHub Issue**: Include logs and steps to reproduce

---

## 📞 Useful Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [Groq API](https://console.groq.com/docs)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Docker Docs](https://docs.docker.com/)

---

**Last Updated**: April 2026  
**Status**: ✅ Production Ready
