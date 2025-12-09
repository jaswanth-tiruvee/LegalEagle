"""
RAG pipeline module for question answering with citation.
Uses Groq for fast, free LLM inference.
"""
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import config
from vector_store import VectorStoreManager


class RAGPipeline:
    """Implements RAG pipeline for legal contract querying."""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store = vector_store_manager
        
        # Use Groq for fast, free LLM
        if not config.GROQ_API_KEY:
            raise ValueError("Groq API key not found. Set GROQ_API_KEY or OPENAI_API_KEY in .env")
        
        self.llm = ChatGroq(
            model_name=config.LLM_MODEL,
            temperature=0,
            groq_api_key=config.GROQ_API_KEY
        )
        
        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a legal assistant specialized in analyzing contracts. 
Your task is to answer questions based ONLY on the provided contract excerpts. 

CRITICAL RULES:
1. Only use information from the provided context excerpts
2. If the answer cannot be found in the context, say "I cannot find this information in the provided contract"
3. Always cite the specific page number(s) where you found the information
4. Be precise and factual - do not make assumptions or infer beyond what is stated
5. Format your response with clear citations like: [Page X] or [Pages X-Y]

Format your response as:
Answer: [Your answer with page citations]
"""),
            ("human", """Context excerpts from the contract:
{context}

Question: {question}

Please provide a concise answer based on the context above, with page citations.""")
        ])
    
    def format_context(self, search_results: List[Dict]) -> str:
        """
        Format search results into context string.
        
        Args:
            search_results: List of search results from vector store
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, result in enumerate(search_results, 1):
            page = result['metadata'].get('page', 'Unknown')
            text = result['text']
            context_parts.append(f"[Excerpt {i} - Page {page}]\n{text}\n")
        
        return "\n".join(context_parts)
    
    def query(self, question: str, top_k: int = None) -> Dict:
        """
        Process a query through the RAG pipeline.
        
        Args:
            question: User's question
            top_k: Number of context chunks to retrieve
            
        Returns:
            Dictionary with answer, citations, and source information
        """
        # Retrieve relevant contexts
        search_results = self.vector_store.similarity_search(question, k=top_k or config.TOP_K_RESULTS)
        
        if not search_results:
            return {
                'answer': "I couldn't find any relevant information in the contract to answer your question.",
                'citations': [],
                'sources': []
            }
        
        # Format context
        context = self.format_context(search_results)
        
        # Generate answer using LLM
        messages = self.prompt_template.format_messages(
            context=context,
            question=question
        )
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        # Extract citations and sources
        citations = [result['metadata'].get('page', 'Unknown') for result in search_results]
        sources = [
            {
                'page': result['metadata'].get('page', 'Unknown'),
                'text_preview': result['text'][:200] + "...",
                'similarity_score': result['score']
            }
            for result in search_results
        ]
        
        return {
            'answer': answer,
            'citations': sorted(list(set(citations))),
            'sources': sources
        }

