# RAG Q&A Application

This project is a Retrieval-Augmented Generation (RAG) application with:

- FastAPI backend for document ingestion and question answering
- Streamlit frontend for user interaction
- Chroma vector store for retrieval context
- Groq LLM integration for answer generation

The app lets you upload `.txt` and `.pdf` files, indexes them into a vector store, and answers questions using retrieved context from those documents.

## Run Locally with Docker

### 1. Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- A valid Groq API key

### 2. Configure environment variables

Create a `.env` file in the project root (same folder as `docker-compose.yml`).

You can copy from the template:

```bash
cp .env.example .env
```

Then update at least:

```env
GROQ_API_KEY=your_real_groq_api_key
MODEL_NAME=llama-3.1-8b-instant
```

### 3. Build and start containers

From the project root, run:

```bash
docker compose up --build
```

### 4. Open the application

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 5. Stop containers

In the same terminal, press `Ctrl + C`.

To stop and remove containers from another terminal:

```bash
docker compose down
```

### 6. Optional: remove persisted vector data

This project stores vector data in a Docker volume (`rag_data`).

To remove containers and volume:

```bash
docker compose down -v
```
