from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional
import openai
from config import Config
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PineconeVectorStore:
    def __init__(self):
        """Initialize Pinecone vector store"""
        self.config = Config()
        self._initialize_pinecone()
        self._initialize_openai()
        self.index = None
        self._connect_to_index()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client"""
        try:
            self.pc = Pinecone(api_key=self.config.PINECONE_API_KEY)
            logger.info("Pinecone initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise
    
    def _initialize_openai(self):
        """Initialize OpenAI client"""
        try:
            openai.api_key = self.config.OPENAI_API_KEY
            logger.info("OpenAI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
            raise
    
    def _connect_to_index(self):
        """Connect to or create Pinecone index"""
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.config.PINECONE_INDEX_NAME not in existing_indexes:
                # Create index if it doesn't exist
                self.pc.create_index(
                    name=self.config.PINECONE_INDEX_NAME,
                    dimension=1536,  # OpenAI ada-002 embedding dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"Created new index: {self.config.PINECONE_INDEX_NAME}")
            
            # Connect to index
            self.index = self.pc.Index(self.config.PINECONE_INDEX_NAME)
            logger.info(f"Connected to index: {self.config.PINECONE_INDEX_NAME}")
            
        except Exception as e:
            logger.error(f"Failed to connect to index: {e}")
            raise
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for given text using OpenAI"""
        try:
            client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
            response = client.embeddings.create(
                input=text,
                model=self.config.EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to create embedding: {e}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to the vector store"""
        try:
            vectors_to_upsert = []
            
            for doc in documents:
                # Create embedding for the document content
                embedding = self.create_embedding(doc['content'])
                
                # Create vector with metadata
                vector = {
                    'id': str(uuid.uuid4()),
                    'values': embedding,
                    'metadata': {
                        'content': doc['content'],
                        'title': doc.get('title', ''),
                        'source': doc.get('source', ''),
                        'category': doc.get('category', '')
                    }
                }
                vectors_to_upsert.append(vector)
            
            # Upsert vectors to Pinecone
            self.index.upsert(vectors=vectors_to_upsert)
            logger.info(f"Successfully added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def search_similar(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        try:
            if top_k is None:
                top_k = self.config.TOP_K_RESULTS
            
            # Create embedding for the query
            query_embedding = self.create_embedding(query)
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            formatted_results = []
            for match in results['matches']:
                if match['score'] >= self.config.SIMILARITY_THRESHOLD:
                    formatted_results.append({
                        'id': match['id'],
                        'score': match['score'],
                        'content': match['metadata']['content'],
                        'title': match['metadata'].get('title', ''),
                        'source': match['metadata'].get('source', ''),
                        'category': match['metadata'].get('category', '')
                    })
            
            logger.info(f"Found {len(formatted_results)} similar documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search similar documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the vector store"""
        try:
            self.index.delete(ids=[document_id])
            logger.info(f"Deleted document with ID: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the index"""
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vector_count': stats.total_vector_count,
                'dimension': stats.dimension,
                'index_fullness': stats.index_fullness
            }
        except Exception as e:
            logger.error(f"Failed to get index stats: {e}")
            return {}
