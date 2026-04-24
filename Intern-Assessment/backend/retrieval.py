"""RAG retrieval and LLM integration."""
import random
from typing import Optional, List, Tuple

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import (
    GROQ_API_KEY,
    VECTOR_STORE_PATH,
    MODEL_NAME,
    SYSTEM_PROMPT,
    SIMILARITY_TOP_K,
)


class LocalEmbeddings(Embeddings):
    """Deterministic, lightweight embeddings for local startup."""

    def __init__(self, size: int = 384):
        self.size = size

    def _embed(self, text: str) -> List[float]:
        seed = hash(text) & 0xFFFFFFFF
        generator = random.Random(seed)
        return [generator.uniform(-1.0, 1.0) for _ in range(self.size)]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)


class RAGRetriever:
    """Handles RAG retrieval and LLM querying."""

    def __init__(self):
        """Initialize the RAG retriever with LLM and vector store."""
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        self.embeddings = LocalEmbeddings()
        self.vector_store = Chroma(
            persist_directory=VECTOR_STORE_PATH,
            embedding_function=self.embeddings,
        )
        
        # Initialize LLM
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.7,
            max_tokens=500,
        )

    def retrieve_context(self, query: str, k: int = SIMILARITY_TOP_K) -> List[dict]:
        """
        Retrieve relevant context chunks from the vector store.
        
        Args:
            query: User's query
            k: Number of top chunks to retrieve
            
        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Retrieve documents
            docs = self.vector_store.similarity_search_with_score(query, k=k)
            
            results = []
            for doc, score in docs:
                results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source_file", "unknown"),
                    "similarity_score": float(score),
                })
            
            return results
        except Exception as e:
            return [{"error": str(e)}]

    def query(self, question: str) -> dict:
        """
        Query the RAG system with a question.
        
        Args:
            question: User's question
            
        Returns:
            dict with answer, context, and metadata
        """
        try:
            # Retrieve context
            context_docs = self.retrieve_context(question)
            
            if not context_docs or "error" in context_docs[0]:
                return {
                    "answer": "I don't know. (No relevant context found)",
                    "context": [],
                    "error": "No documents in vector store",
                }

            # Combine context
            context_text = "\n\n".join(
                [f"Source: {doc['source']}\n{doc['content']}" for doc in context_docs]
            )

            # Create prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                ("user", "Context:\n{context}\n\nQuestion: {question}")
            ])

            # Create RAG chain
            rag_chain = (
                {
                    "context": lambda x: context_text,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )

            # Get answer
            answer = rag_chain.invoke(question)

            return {
                "answer": answer,
                "context": context_docs,
                "question": question,
                "success": True,
            }

        except Exception as e:
            return {
                "answer": "I don't know. (Error processing query)",
                "error": str(e),
                "success": False,
            }

    def check_vector_store_status(self) -> dict:
        """Check if vector store has documents."""
        try:
            doc_count = len(self.vector_store.get()["ids"])
            return {
                "has_documents": doc_count > 0,
                "document_count": doc_count,
            }
        except Exception as e:
            return {
                "has_documents": False,
                "document_count": 0,
                "error": str(e),
            }
