#!/bin/bash
# Quick start script for RAG application

set -e

echo "🚀 Starting RAG Application..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "❌ Please edit .env and add your GROQ_API_KEY"
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=your_groq_api_key_here" .env; then
    if grep -q "^GROQ_API_KEY=" .env; then
        echo "✅ GROQ_API_KEY is configured"
    else
        echo "❌ GROQ_API_KEY not found in .env"
        exit 1
    fi
fi

echo "📦 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

echo "✅ Docker found"
echo ""

echo "🐳 Building and starting Docker containers..."
docker-compose up --build

echo ""
echo "✅ RAG Application is running!"
echo ""
echo "📍 Access the services at:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
