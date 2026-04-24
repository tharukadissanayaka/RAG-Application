#!/bin/bash
# Windows batch equivalent

@echo off
echo.
echo 🚀 Starting RAG Application...
echo.

if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    copy .env.example .env
    echo ❌ Please edit .env and add your GROQ_API_KEY
    exit /b 1
)

echo 🐳 Building and starting Docker containers...
docker-compose up --build

echo.
echo ✅ RAG Application is running!
echo.
echo 📍 Access the services at:
echo    - API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Frontend: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
