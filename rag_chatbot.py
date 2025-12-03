import openai
from typing import List, Dict, Any, Optional
from vector_store import PineconeVectorStore
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGChatbot:
    def __init__(self):
        """Initialize RAG Chatbot with vector store and OpenAI"""
        self.config = Config()
        self.vector_store = PineconeVectorStore()
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client"""
        try:
            self.openai_client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
            logger.info("OpenAI initialized for RAG chatbot")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
            raise
    
    def retrieve_relevant_documents(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for the given query"""
        try:
            relevant_docs = self.vector_store.search_similar(query)
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents")
            return relevant_docs
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")
            return []
    
    def create_context_from_documents(self, documents: List[Dict[str, Any]]) -> str:
        """Create context string from retrieved documents"""
        if not documents:
            return "No relevant information found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Document {i}:\n{doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using OpenAI with retrieved context"""
        try:
            system_prompt = """You are a helpful AI assistant that answers questions based on the provided context. 
            Use the context information to provide accurate and helpful responses. If the context doesn't contain 
            relevant information to answer the question, say so politely and suggest what information might be helpful.
            
            Guidelines:
            - Base your answers primarily on the provided context
            - Be concise but comprehensive
            - If you're unsure about something, say so
            - Cite relevant parts of the context when appropriate
            - Maintain a helpful and professional tone"""
            
            user_prompt = f"""Context:
            {context}
            
            Question: {query}
            
            Please provide a helpful answer based on the context above."""
            
            response = self.openai_client.chat.completions.create(
                model=self.config.CHAT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again later."
    
    def chat(self, query: str) -> Dict[str, Any]:
        """Main chat function that implements RAG pipeline"""
        try:
            # Step 1: Retrieve relevant documents
            relevant_docs = self.retrieve_relevant_documents(query)
            
            # Step 2: Create context from documents
            context = self.create_context_from_documents(relevant_docs)
            
            # Step 3: Generate response using context
            response = self.generate_response(query, context)
            
            # Step 4: Return response with metadata
            return {
                'response': response,
                'relevant_documents': relevant_docs,
                'context_used': len(relevant_docs) > 0,
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Error in chat function: {e}")
            return {
                'response': "I apologize, but I encountered an error while processing your request. Please try again.",
                'relevant_documents': [],
                'context_used': False,
                'query': query,
                'error': str(e)
            }
    
    def add_knowledge(self, documents: List[Dict[str, Any]]) -> bool:
        """Add new knowledge to the vector store"""
        try:
            success = self.vector_store.add_documents(documents)
            if success:
                logger.info(f"Successfully added {len(documents)} documents to knowledge base")
            return success
        except Exception as e:
            logger.error(f"Failed to add knowledge: {e}")
            return False
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            return self.vector_store.get_index_stats()
        except Exception as e:
            logger.error(f"Failed to get knowledge stats: {e}")
            return {}
    
    def clear_knowledge_base(self) -> bool:
        """Clear all documents from the knowledge base"""
        try:
            # This would require deleting all vectors from the index
            # For now, we'll return False as this is a destructive operation
            logger.warning("Clear knowledge base operation not implemented for safety")
            return False
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            return False
