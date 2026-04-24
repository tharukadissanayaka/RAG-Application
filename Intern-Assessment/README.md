# RAG Q&A Application

A lightweight, production-ready Retrieval-Augmented Generation (RAG) system built with FastAPI, Streamlit, and Groq LLM. Perfect for internship assessments and free-tier cloud deployments.

## 🚀 Features

- **Document Ingestion**: Upload and process `.txt` and `.pdf` files
- **Vector Search**: Semantic similarity search using ChromaDB and sentence transformers
- **LLM Integration**: Uses Groq API for fast, free-tier LLM access
- **RESTful API**: FastAPI with automatic Swagger documentation
- **Web Frontend**: Interactive Streamlit interface for easy access
- **Docker Support**: Multi-stage Dockerfile optimized for low-resource environments (1GB RAM)
- **CI/CD Pipeline**: GitHub Actions for automated builds and tests
- **System Prompt Control**: Explicit instructions to prevent hallucinations

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Groq API Key (free at [console.groq.com](https://console.groq.com))

## 🔑 Getting API Keys

### Groq API (Free)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up with your email
3. Navigate to API Keys
4. Create a new API key
5. Copy and save it to `.env`

## ⚙️ Installation

### Local Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Intern-Assessment
   ```

2. **Create environment file**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install backend dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Install frontend dependencies (optional)**
   ```bash
   pip install -r frontend/requirements.txt
   ```

### Docker Setup

1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

2. **Access the services**
   - API: http://localhost:8000
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 🚀 Running the Application

### Option 1: FastAPI Backend Only

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### Option 2: With Streamlit Frontend

**Terminal 1 (Backend):**

```bash
cd backend
python -m uvicorn main:app --port 8000
```

**Terminal 2 (Frontend):**

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`.

### Option 3: Docker Compose

```bash
docker-compose up
```

## 📚 API Endpoints

### Health Check

```bash
GET /health
```

### Ingest Document

```bash
POST /ingest
Content-Type: multipart/form-data

# Example:
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"
```

**Response:**

```json
{
  "success": true,
  "file_name": "document.pdf",
  "chunks_created": 42,
  "message": "Successfully ingested document.pdf (42 chunks)"
}
```

### Ask Question

```bash
POST /ask?question=What+is+the+document+about?
```

**Response:**

```json
{
  "answer": "The document discusses...",
  "context": [
    {
      "content": "Relevant excerpt...",
      "source": "document.pdf",
      "similarity_score": 0.95
    }
  ],
  "question": "What is the document about?",
  "success": true
}
```

### Get Statistics

```bash
GET /stats
```

**Response:**

```json
{
  "vector_store": {
    "success": true,
    "total_documents": 42,
    "vector_store_path": "./chroma_db"
  },
  "documents_count": 42
}
```

### Clear Vector Store

```bash
DELETE /clear
```

## 🎯 System Prompt

The RAG system uses a strict system prompt to prevent hallucinations:

> "You are a helpful assistant that answers questions based exclusively on the provided context. Only use information from the provided context to answer questions. If the answer is not in the context, respond with exactly: 'I don't know.' Do not use any external knowledge or make assumptions."

## 📦 Architecture

### Backend Structure

```
backend/
├── main.py           # FastAPI application
├── config.py         # Configuration and environment variables
├── ingestion.py      # Document ingestion and vector store
├── retrieval.py      # RAG retrieval and LLM querying
└── requirements.txt  # Python dependencies
```

### Frontend Structure

```
frontend/
├── app.py            # Streamlit application
├── Dockerfile        # Frontend container
└── requirements.txt  # Python dependencies
```

### Key Components

**1. Document Ingestion (`ingestion.py`)**

- Loads PDF and TXT files
- Splits documents into chunks (1000 chars, 200 overlap)
- Stores embeddings in ChromaDB
- Uses lightweight sentence-transformers model

**2. RAG Retrieval (`retrieval.py`)**

- Retrieves top-3 similar chunks for each query
- Uses Groq API for LLM inference
- Enforces system prompt for accurate, context-only responses

**3. FastAPI Application (`main.py`)**

- RESTful endpoints for document management
- File upload with validation
- Error handling and CORS support

**4. Streamlit Frontend (`app.py`)**

- Interactive chat interface
- Document upload and management
- Context visualization
- Chat history tracking

## 🐳 Docker Optimization

The multi-stage Dockerfile optimizes for low-resource environments:

- **Stage 1 (Builder)**: Installs dependencies in a virtual environment
- **Stage 2 (Runtime)**: Uses only the venv, reducing final image size to ~2GB
- **Health Checks**: Automatic service monitoring
- **Volume Mounts**: Persistent vector store storage

## 🚀 Deployment

### Render.com (Free Tier)

1. Connect your GitHub repository
2. Create a new Web Service
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GROQ_API_KEY=your_key`
6. Deploy!

### Koyeb (Free Tier)

1. Connect GitHub repository
2. Configure Docker build
3. Set PORT to 8000
4. Add `GROQ_API_KEY` environment variable
5. Deploy!

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

## 📞 Support

For issues and questions, create a GitHub issue or contact the development team.

---

**Built for**: Internship Assessment  
**Stack**: FastAPI • Streamlit • Groq • ChromaDB • Docker • GitHub Actions  
**Status**: Production-Ready ✅
