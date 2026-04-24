"""Streamlit frontend for RAG API."""
import os
import requests
import streamlit as st
from pathlib import Path
import time

st.set_page_config(
    page_title="RAG Q&A System",
    page_icon="🤖",
    layout="wide",
)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store_stats" not in st.session_state:
    st.session_state.vector_store_stats = None

# Title and description
st.title("🤖 RAG Q&A System")
st.markdown(
    """
    Upload your documents and ask questions based on their content.
    The system will retrieve relevant information and provide answers.
    """
)

# Sidebar for document management
with st.sidebar:
    st.header("📚 Document Management")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .pdf)",
        type=["txt", "pdf"],
    )
    
    if uploaded_file is not None:
        with st.spinner("Uploading and processing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_BASE_URL}/ingest", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ {result['message']}")
                    st.session_state.chat_history = []  # Clear chat history
                else:
                    error_data = response.json()
                    error_message = (
                        error_data.get("detail")
                        or error_data.get("error")
                        or response.text
                        or "Unknown error"
                    )
                    st.error(f"❌ Error: {error_message}")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Vector Store Stats")
    if st.button("Refresh Stats"):
        try:
            response = requests.get(f"{API_BASE_URL}/stats")
            if response.status_code == 200:
                st.session_state.vector_store_stats = response.json()
        except Exception as e:
            st.error(f"Error fetching stats: {str(e)}")
    
    if st.session_state.vector_store_stats:
        stats = st.session_state.vector_store_stats
        st.metric(
            "Documents in Store",
            stats["documents_count"],
        )
    
    st.divider()
    
    # Clear documents
    if st.button("🗑️ Clear All Documents", type="secondary"):
        try:
            response = requests.delete(f"{API_BASE_URL}/clear")
            if response.status_code == 200:
                st.success("✅ Vector store cleared")
                st.session_state.chat_history = []
                st.session_state.vector_store_stats = None
            else:
                st.error("❌ Error clearing vector store")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    
    # Settings
    st.subheader("⚙️ Settings")
    api_url_input = st.text_input(
        "API URL",
        value=API_BASE_URL,
    )
    if api_url_input:
        API_BASE_URL = api_url_input

# Main chat interface
st.subheader("💬 Ask Questions")

# Chat history display
for idx, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant" and "context" in message:
            with st.expander("📖 View Context"):
                for i, ctx in enumerate(message["context"], 1):
                    st.write(f"**Source:** {ctx['source']}")
                    st.write(f"**Similarity Score:** {ctx['similarity_score']:.3f}")
                    st.write(f"**Content:** {ctx['content'][:300]}...")
                    st.divider()

# Question input
question = st.chat_input("Ask a question about your documents...")

if question:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(question)
    
    # Get response from API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/ask",
                params={"question": question},
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "No answer received")
                context = result.get("context", [])
                
                # Add assistant message to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "context": context,
                })
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.write(answer)
                    
                    if context and not any("error" in ctx for ctx in context):
                        with st.expander("📖 View Context"):
                            for i, ctx in enumerate(context, 1):
                                st.write(f"**Source:** {ctx['source']}")
                                st.write(f"**Similarity Score:** {ctx['similarity_score']:.3f}")
                                st.write(f"**Content:** {ctx['content'][:500]}...")
                                st.divider()
            else:
                error_data = response.json()
                error_msg = (
                    error_data.get("detail")
                    or error_data.get("error")
                    or response.text
                    or "Unknown error"
                )
                st.error(f"❌ Error: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            st.error(
                f"❌ Cannot connect to API at {API_BASE_URL}. "
                "Make sure the backend is running."
            )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    ---
    **RAG Q&A System** | Built with FastAPI + Streamlit + Groq LLM
    """
)
