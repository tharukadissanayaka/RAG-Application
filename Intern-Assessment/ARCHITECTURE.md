# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Streamlit Web Interface                             │   │
│  │  - Document Upload UI                               │   │
│  │  - Chat Interface                                    │   │
│  │  - Context Visualization                            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                    API Layer                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Application                                 │   │
│  │  - /ingest    - Document ingestion                   │   │
│  │  - /ask       - Question answering                   │   │
│  │  - /stats     - Statistics                           │   │
│  │  - /clear     - Vector store management              │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴──────────────────┐
        │                                   │
┌───────▼──────────┐          ┌────────────▼──────────┐
│  Processing      │          │  LLM Integration      │
│  Layer           │          │  Layer                │
├──────────────────┤          ├─────────────────────┤
│ Document         │          │ Groq API             │
│ Loader           │          │ - mixtral-8x7b      │
│ - TextLoader     │          │ - Temperature: 0.7   │
│ - PyPDFLoader    │          │ - Max Tokens: 500    │
│                  │          │                      │
│ Text Splitter    │          │ System Prompt:       │
│ - Chunk: 1000ch  │          │ "Only use context"   │
│ - Overlap: 200ch │          │                      │
└───────┬──────────┘          └────────┬─────────────┘
        │                              │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼──────────────┐
        │  Vector Store & Embeddings  │
        ├─────────────────────────────┤
        │ ChromaDB                    │
        │ - In-memory + persistent    │
        │ - Similarity search         │
        │                             │
        │ HuggingFace Embeddings      │
        │ - all-MiniLM-L6-v2          │
        │ - Lightweight               │
        │ - 384 dimensions            │
        └─────────────────────────────┘
```

## Component Architecture

### 1. Frontend Layer (Streamlit)

**File**: `frontend/app.py`

**Responsibilities**:

- Provide user interface for document upload
- Display chat interface for Q&A
- Show retrieved context documents
- Manage session state and chat history

**Features**:

- Responsive UI with sidebar controls
- Real-time chat with streaming responses
- Document management (upload, clear, view stats)
- Context visualization with similarity scores

### 2. API Layer (FastAPI)

**File**: `backend/main.py`

**Responsibilities**:

- Handle HTTP requests
- Route to appropriate handlers
- Perform input validation
- Return JSON responses

**Features**:

- CORS middleware for frontend communication
- File upload handling with validation
- Error handling and logging
- Health checks and statistics

### 3. Configuration Layer

**File**: `backend/config.py`

**Responsibilities**:

- Manage environment variables
- Define system prompts
- Configure chunk sizes
- Set API limits

**Key Settings**:

```python
CHUNK_SIZE = 1000           # Characters per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
SIMILARITY_TOP_K = 3        # Top results to retrieve
MODEL_NAME = "mixtral-8x7b-32768"  # Groq model
SYSTEM_PROMPT = "..."       # Instruction prompt
```

### 4. Document Ingestion Module

**File**: `backend/ingestion.py`

**Class**: `DocumentIngester`

**Responsibilities**:

- Load documents (TXT, PDF)
- Split documents into chunks
- Generate embeddings
- Store in vector database

**Process**:

```
File Upload
    ↓
Validation
    ↓
Load Document
    ↓
Split into Chunks
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
```

### 5. Retrieval & RAG Module

**File**: `backend/retrieval.py`

**Class**: `RAGRetriever`

**Responsibilities**:

- Retrieve relevant context
- Construct prompts
- Query LLM
- Format responses

**Process**:

```
User Question
    ↓
Generate Embedding
    ↓
Search Vector Store (Similarity)
    ↓
Retrieve Top-3 Chunks
    ↓
Build Prompt with Context
    ↓
Query Groq LLM
    ↓
Format & Return Answer
```

## Data Flow

### Document Ingestion Flow

```
1. POST /ingest
   └─ File Upload (multipart/form-data)
      └─ DocumentIngester.ingest_file()
         ├─ Load: TextLoader | PyPDFLoader
         ├─ Split: RecursiveCharacterTextSplitter
         ├─ Embed: HuggingFaceEmbeddings
         └─ Store: Chroma.add_documents()
            └─ Vector Store (chroma_db/)
```

### Question Answering Flow

```
1. POST /ask?question="..."
   └─ RAGRetriever.query()
      ├─ Embed question
      ├─ Search vector store
      │  └─ Similarity search (top-3)
      ├─ Retrieve context chunks
      ├─ Build prompt
      │  ├─ System prompt
      │  ├─ Context
      │  └─ Question
      ├─ Call Groq API
      └─ Return answer + context
```

## Technology Stack

| Layer            | Technology     | Purpose               |
| ---------------- | -------------- | --------------------- |
| Frontend         | Streamlit      | Web UI                |
| API              | FastAPI        | REST endpoints        |
| Document Loading | LangChain      | Text/PDF parsing      |
| Text Splitting   | LangChain      | Chunking              |
| Embeddings       | HuggingFace    | Vector generation     |
| Vector Store     | ChromaDB       | Similarity search     |
| LLM              | Groq API       | Text generation       |
| Containerization | Docker         | Deployment            |
| Orchestration    | Docker Compose | Local multi-container |
| CI/CD            | GitHub Actions | Automated builds      |

## Storage Architecture

### Local Storage

```
project/
├── chroma_db/           # Vector store (persistent)
│   ├── index/
│   ├── chroma-embeddings.parquet
│   └── metadata.parquet
└── uploads/             # Temporary uploaded files (cleanup after ingest)
```

### Vector Store Details

- **Database**: ChromaDB (SQLite backend)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (384 dims)
- **Persistence**: Disk-based in `chroma_db/` directory
- **Capacity**: ~100GB+ per shard (plenty for free tier)

## Performance Characteristics

### Memory Usage

| Component              | Memory            |
| ---------------------- | ----------------- |
| FastAPI Runtime        | ~200MB            |
| Streamlit Runtime      | ~150MB            |
| ChromaDB (empty)       | ~50MB             |
| Embeddings Model       | ~100MB            |
| Per 10K documents      | ~500MB additional |
| **Total (minimal)**    | **~500MB**        |
| **Total (heavy load)** | **~1GB**          |

### Processing Time

| Operation                         | Time                  |
| --------------------------------- | --------------------- |
| Upload & ingest (1MB PDF)         | 2-5s                  |
| Generate embeddings (1000 chunks) | 3-10s                 |
| Similarity search                 | <100ms                |
| LLM inference                     | 1-5s (Groq free tier) |
| **Total Q&A response**            | **2-10s**             |

## Scalability Considerations

### Vertical Scaling (Single Instance)

- Handle ~100GB+ documents
- Support 1000+ concurrent requests (FastAPI async)
- Use free-tier hosting (1GB RAM)

### Horizontal Scaling

For production:

1. Use cloud storage (S3) for vectors
2. Implement PostgreSQL + pgvector
3. Add caching layer (Redis)
4. Load balance across multiple API instances
5. Separate embedding generation

## Security Architecture

### Data Security

- ✅ API key stored in environment
- ✅ CORS properly configured
- ✅ Input validation on all endpoints
- ✅ File type and size validation
- ✅ No sensitive data in logs

### Network Security

- ✅ HTTPS in production (via cloud provider)
- ✅ No hardcoded credentials
- ✅ Environment-based configuration

### Future Security

- [ ] JWT authentication
- [ ] Rate limiting per user
- [ ] Request signing
- [ ] Audit logging
- [ ] Encryption at rest

## Deployment Architecture

### Docker Multi-Stage Build

```
Stage 1: Builder
├─ Python 3.11-slim
├─ Install build dependencies
├─ Create virtual environment
└─ Install Python packages

Stage 2: Runtime
├─ Python 3.11-slim
├─ Copy venv from stage 1
├─ Copy application code
└─ Final image ~2GB
```

### Container Orchestration

```
docker-compose.yml
├─ Backend Service
│  ├─ Port: 8000
│  ├─ Volume: chroma_db/
│  └─ Health check: /health
├─ Frontend Service
│  ├─ Port: 8501
│  ├─ Depends on: backend
│  └─ Environment: API_BASE_URL
└─ Network: rag_network
```

## Monitoring & Observability

### Built-in Monitoring

- Health check endpoint: `/health`
- Statistics endpoint: `/stats`
- FastAPI auto documentation: `/docs`
- Container health checks

### Recommended Tools

- **Logging**: CloudWatch (AWS), Google Logs (GCP)
- **Metrics**: Prometheus + Grafana
- **Tracing**: Jaeger or Datadog
- **Error Tracking**: Sentry

## Disaster Recovery

### Backup Strategy

```
Daily Backups:
├─ Vector Store (chroma_db/) → Cloud Storage
├─ Configuration (.env) → Secrets Manager
└─ Application Code → GitHub
```

### Recovery Steps

1. Restore code from GitHub
2. Restore vector store from backup
3. Deploy container
4. Verify with /health endpoint

## Future Architecture Improvements

1. **Multi-tenant Support**: Separate vector stores per user
2. **Advanced Caching**: Redis for frequently asked questions
3. **Streaming Responses**: Use FastAPI streaming
4. **Distributed Embeddings**: GPU acceleration
5. **Custom Models**: Support for proprietary LLMs
6. **Analytics**: Track questions, answers, usage
7. **A/B Testing**: Compare different models/prompts
