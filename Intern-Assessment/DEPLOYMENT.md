# Deployment Guide

## Quick Start

### Local Deployment

1. **Set up environment**

   ```bash
   cp .env.example .env
   # Edit .env with your Groq API key
   ```

2. **Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

3. **Access services**
   - API: http://localhost:8000
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## Cloud Deployment

### Render.com (Recommended for Free Tier)

#### Backend Deployment

1. **Create Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free (512 MB RAM)

3. **Add Environment Variables**
   - Go to "Environment"
   - Add: `GROQ_API_KEY` = your_key
   - Add: `PORT` = 8000

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Note your service URL

#### Frontend Deployment

1. **Create Static Site** (Alternative: Create another Web Service)
   - Click "New +" → "Static Site"
   - Connect repository
   - Build Command: `cd frontend && pip install -r requirements.txt`
   - Publish Directory: `frontend`

2. **Alternative: Web Service for Streamlit**
   - Create Web Service
   - Build Command: `pip install -r frontend/requirements.txt`
   - Start Command: `streamlit run frontend/app.py --server.port=$PORT`
   - Add Environment: `API_BASE_URL` = your_backend_url

### Koyeb (Free Tier)

1. **Prepare Repository**
   - Ensure Dockerfile exists
   - Push to GitHub

2. **Create Application**
   - Go to https://koyeb.com
   - Click "Create Web Service"
   - Select "Docker"
   - Select "GitHub"
   - Choose repository and branch

3. **Configure**
   - **Build command**: `docker build -t rag-backend:latest .`
   - **Run command**: Default
   - **Port**: 8000

4. **Environment Variables**
   - GROQ_API_KEY: your_key
   - VECTOR_STORE_PATH: /tmp/chroma_db (for ephemeral storage)

5. **Deploy**
   - Click "Create"
   - Monitor logs
   - Access via provided URL

### Railway.app

1. **Connect Repository**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Services**
   - Click "Add" → "Dockerfile"
   - Railway auto-detects Dockerfile
   - Set PORT: 8000

3. **Add Variables**
   - Go to "Variables"
   - GROQ_API_KEY = your_key

4. **Deploy**
   - Automatic on push to main
   - View logs in dashboard

## Production Considerations

### Database Persistence

For persistent vector storage, use cloud storage:

**Option 1: Cloud Storage + Local Directory**

```python
# Sync to S3 periodically
import boto3

def sync_vector_store_to_s3():
    s3 = boto3.client('s3')
    bucket = os.getenv('S3_BUCKET')
    # Upload files from chroma_db/
```

**Option 2: PostgreSQL + pgvector**

- More reliable for production
- Supports full-text search
- Requires PostgreSQL database

### Performance Optimization

```python
# In config.py
CHUNK_SIZE = 800  # Reduce for faster processing
SIMILARITY_TOP_K = 2  # Fewer results = faster
```

### Rate Limiting

```python
# Add to main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("30/minute")
async def ask_question(request: Request, question: str):
    # Implementation
```

### Monitoring

1. **Render.com**
   - View logs in dashboard
   - Set up alerts

2. **Koyeb**
   - Monitor CPU/Memory usage
   - View deployment logs

3. **Railway**
   - Real-time metrics
   - Error tracking

### Logging

```python
# In main.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/ask")
async def ask_question(question: str):
    logger.info(f"Question received: {question}")
    # Implementation
```

### Security for Production

1. **API Key Rotation**
   - Store in secrets manager
   - Rotate monthly

2. **CORS Configuration**

   ```python
   # Limit to your frontend domain
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **HTTPS**
   - Render, Railway, Koyeb provide HTTPS by default
   - All traffic encrypted

4. **Input Validation**
   - Already implemented
   - Validate file types and sizes
   - Sanitize user input

## Troubleshooting

### Service Won't Start

1. Check logs
2. Verify environment variables
3. Check available disk space
4. Ensure GROQ_API_KEY is valid

### Out of Memory

Solutions:

- Reduce CHUNK_SIZE
- Reduce SIMILARITY_TOP_K
- Use smaller embedding model
- Implement caching layer

### Slow Response Times

Solutions:

- Check API rate limits (30/min for free Groq)
- Reduce vector store size
- Implement response caching
- Use faster embedding model

### File Upload Fails

Check:

- Max file size (default 10MB)
- Disk space available
- Supported file types (.txt, .pdf)

## Monitoring Dashboard

### Key Metrics to Track

1. **API Response Time**
   - Target: < 5 seconds
   - Alert if > 10 seconds

2. **Vector Store Size**
   - Monitor disk usage
   - Plan cleanup strategy

3. **Error Rate**
   - Monitor 4xx and 5xx errors
   - Alert if > 5%

4. **Uptime**
   - Target: > 99%
   - Monitor with external service

## Backup and Recovery

### Vector Store Backup

```bash
# Manual backup
tar -czf backup.tar.gz chroma_db/

# Schedule with cron (Linux/Mac)
# 0 0 * * * tar -czf backup_$(date +\%Y\%m\%d).tar.gz chroma_db/
```

### Recovery

```bash
# Restore from backup
tar -xzf backup.tar.gz
docker-compose restart backend
```

## Cost Estimation

### Free Tier Services

- **Render**: 750 hours/month of free dyno time
- **Koyeb**: 100GB/month bandwidth, 500 deployed hours/month
- **Railway**: $5 credit/month
- **Groq API**: Unlimited free requests (rate limited)

### Scaling to Paid

When you exceed free tier:

- **Render**: ~$7/month for small dyno
- **Koyeb**: ~$0.15/hour for basic container
- **Railway**: ~$0.50/hour for container
- **Groq API**: Pay-as-you-go (generous free tier)

## Next Steps

1. Deploy backend first
2. Test API endpoints
3. Deploy frontend
4. Configure custom domain
5. Set up monitoring
6. Plan backup strategy
