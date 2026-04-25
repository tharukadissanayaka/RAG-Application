# RAG Q&A Application

A Retrieval-Augmented Generation (RAG) application built with FastAPI, Streamlit, and Groq LLM.

## Prerequisites

- Docker & Docker Compose
- Groq API Key (free at [console.groq.com](https://console.groq.com))

## Running Locally with Docker

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Application.git
cd RAG-Application/Intern-Assessment
```

### 2. Create environment file

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
VECTOR_STORE_PATH=./chroma_db
PORT=8000
MAX_UPLOAD_SIZE=10485760
```

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 4. Access the services

- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Frontend (Streamlit)**: http://localhost:8501

### 5. Test the application

1. Open http://localhost:8000/docs
2. Use `/ingest` endpoint to upload a PDF or TXT file
3. Use `/ask` endpoint to ask questions about the document
4. View the answer with context chunks

### 6. Stop the application

```bash
docker-compose down
```

## API Endpoints

- `POST /ingest` - Upload and process a document
- `POST /ask` - Ask a question based on ingested documents
- `GET /health` - Health check
- `GET /stats` - Vector store statistics
- `DELETE /clear` - Clear all documents

## Architecture

- **Backend**: FastAPI + Python with LangChain RAG pipeline
- **LLM**: Groq API (llama-3.1-8b-instant)
- **Vector Store**: ChromaDB
- **Frontend**: Streamlit web interface
- **Containerization**: Docker multi-stage build

## Environment Variables

| Variable          | Default              | Description                   |
| ----------------- | -------------------- | ----------------------------- |
| GROQ_API_KEY      | -                    | Your Groq API key (required)  |
| MODEL_NAME        | llama-3.1-8b-instant | Groq model to use             |
| VECTOR_STORE_PATH | ./chroma_db          | ChromaDB storage path         |
| PORT              | 8000                 | API port                      |
| MAX_UPLOAD_SIZE   | 10485760             | Max file size in bytes (10MB) |

1. Connect your GitHub repository
2. Create a new Web Service
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GROQ_API_KEY=your_key`
6. Deploy!

### Environment Variables

```env
GROQ_API_KEY=              # Required: Groq API key
MODEL_NAME=mixtral-8x7b-32768  # Optional: LLM model name
VECTOR_STORE_PATH=./chroma_db  # Optional: Vector store path
PORT=8000                  # Optional: API port
MAX_UPLOAD_SIZE=10485760   # Optional: Max file size (10MB)
```

## 📊 Performance

- **Memory Usage**: ~500MB-1GB (optimized for free-tier hosting)
- **Vector Store**: ChromaDB with in-memory caching
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (lightweight)
- **LLM**: Groq API (fast inference via quantized models)
- **Chunk Size**: 1000 characters with 200 character overlap

## 🧪 Testing

```bash
# Run linting
flake8 backend frontend

# Run API tests
pytest tests/ -v
```

## 🔒 Security Best Practices

- ✅ Environment variables for sensitive data
- ✅ File upload validation (type and size)
- ✅ CORS configuration
- ✅ Input validation on all endpoints
- ✅ Error handling without exposing internals
- ✅ No API key logging

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Ensure tests pass
4. Submit a pull request

## 📝 License

This project is provided as-is for educational and assessment purposes.

## 🆘 Troubleshooting

### Issue: "GROQ_API_KEY not set"

**Solution**: Create a `.env` file with your Groq API key:

```bash
cp .env.example .env
# Edit .env and add your key
```

### Issue: "No module named langchain"

**Solution**: Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

### Issue: "Cannot connect to localhost:8000"

**Solution**: Make sure backend is running:

```bash
cd backend
python -m uvicorn main:app --port 8000
```

### Issue: Docker build fails

**Solution**: Ensure Docker daemon is running and try:

```bash
docker system prune -a
docker-compose build --no-cache
```


