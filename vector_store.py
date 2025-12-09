"""
Vector store management module for Pinecone and FAISS.
Uses HuggingFace sentence-transformers for free embeddings.
"""
import os
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import config

# Conditional Pinecone import
try:
    from langchain_community.vectorstores import Pinecone
    try:
        import pinecone
    except Exception:
        # Handle case where pinecone package has issues
        pinecone = None
    PINECONE_AVAILABLE = True
except (ImportError, Exception):
    PINECONE_AVAILABLE = False
    Pinecone = None


class VectorStoreManager:
    """Manages vector store operations for both Pinecone and FAISS."""
    
    def __init__(self):
        # Use HuggingFace embeddings (free, no API key needed)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}  # Use CPU to avoid GPU requirements
        )
        self.vector_store = None
        self.store_type = config.VECTOR_STORE_TYPE
        
        if self.store_type == "pinecone":
            self._initialize_pinecone()
        else:
            self._initialize_faiss()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone vector store."""
        if not PINECONE_AVAILABLE:
            raise ImportError("Pinecone is not installed. Install it with: pip install pinecone-client")
        
        if not config.PINECONE_API_KEY:
            raise ValueError("Pinecone API key not found. Set PINECONE_API_KEY in .env")
        
        try:
            # Try newer Pinecone API (v3+)
            from pinecone import Pinecone as PineconeClient
            pc = PineconeClient(api_key=config.PINECONE_API_KEY)
            
            # Check if index exists, create if not
            existing_indexes = [idx.name for idx in pc.list_indexes()]
            if config.PINECONE_INDEX_NAME not in existing_indexes:
                # Get embedding dimension from the model
                embedding_dim = len(self.embeddings.embed_query("test"))
                pc.create_index(
                    name=config.PINECONE_INDEX_NAME,
                    dimension=embedding_dim,  # Dynamic dimension based on embedding model
                    metric="cosine"
                )
            
            self.vector_store = Pinecone.from_existing_index(
                index_name=config.PINECONE_INDEX_NAME,
                embedding=self.embeddings
            )
        except ImportError:
            # Fallback to older Pinecone API (v2)
            pinecone.init(
                api_key=config.PINECONE_API_KEY,
                environment=config.PINECONE_ENVIRONMENT
            )
            
            # Check if index exists, create if not
            if config.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                # Get embedding dimension from the model
                embedding_dim = len(self.embeddings.embed_query("test"))
                pinecone.create_index(
                    name=config.PINECONE_INDEX_NAME,
                    dimension=embedding_dim,  # Dynamic dimension based on embedding model
                    metric="cosine"
                )
            
            self.vector_store = Pinecone.from_existing_index(
                index_name=config.PINECONE_INDEX_NAME,
                embedding=self.embeddings
            )
    
    def _initialize_faiss(self):
        """Initialize FAISS vector store (local)."""
        if os.path.exists(config.FAISS_INDEX_PATH):
            self.vector_store = FAISS.load_local(
                config.FAISS_INDEX_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # Will be created when documents are added
            self.vector_store = None
    
    def add_documents(self, chunks: List[Dict]):
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of dictionaries with 'text' and 'metadata' keys
        """
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        
        if self.store_type == "pinecone":
            if self.vector_store:
                self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            else:
                self.vector_store = Pinecone.from_texts(
                    texts=texts,
                    embedding=self.embeddings,
                    metadatas=metadatas,
                    index_name=config.PINECONE_INDEX_NAME
                )
        else:
            # FAISS
            if self.vector_store:
                self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            else:
                self.vector_store = FAISS.from_texts(
                    texts=texts,
                    embedding=self.embeddings,
                    metadatas=metadatas
                )
            
            # Save FAISS index locally
            os.makedirs(config.FAISS_INDEX_PATH, exist_ok=True)
            self.vector_store.save_local(config.FAISS_INDEX_PATH)
    
    def similarity_search(self, query: str, k: int = None) -> List[Dict]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of documents with similarity scores and metadata
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please add documents first.")
        
        k = k or config.TOP_K_RESULTS
        
        # Perform similarity search
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        
        results = []
        for doc, score in docs:
            results.append({
                'text': doc.page_content,
                'metadata': doc.metadata,
                'score': float(score)
            })
        
        return results

