# Dockerfile for Streamlit frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Streamlit configuration
RUN mkdir -p ~/.streamlit && \
    echo "[server]\n\
    headless = true\n\
    port = 8501\n\
    enableCORS = false\n\
    [browser]\n\
    gatherUsageStats = false" > ~/.streamlit/config.toml

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
