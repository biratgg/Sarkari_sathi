import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-chatbot")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Application Configuration
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    
    # Model Configuration
    EMBEDDING_MODEL = "text-embedding-ada-002"
    CHAT_MODEL = "gpt-3.5-turbo"
    
    # Free version configuration
    FREE_INDEX_NAME = "rag-chatbot-free"
    FREE_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    FREE_EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 embedding dimension
    
    # RAG Configuration
    TOP_K_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.3
