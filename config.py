"""
Configuration module for LegalEagle RAG system.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", os.getenv("OPENAI_API_KEY", ""))  # Support both GROQ_API_KEY and OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Keep for backward compatibility
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")

# Vector Store Configuration
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "faiss").lower()
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "legal-eagle-index")

# Model Configuration - Using Groq (free) and HuggingFace embeddings (free)
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")  # Groq default model (updated from deprecated llama-3.1-70b-versatile)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")  # HuggingFace sentence-transformers model

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Configuration
TOP_K_RESULTS = 3

# FAISS Index Path
FAISS_INDEX_PATH = "faiss_index"

