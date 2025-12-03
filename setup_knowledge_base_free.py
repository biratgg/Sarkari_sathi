#!/usr/bin/env python3
"""
Setup script to initialize the knowledge base with sample data (FREE VERSION)
"""

import os
import sys
from dotenv import load_dotenv
from rag_chatbot_free import RAGChatbotFree
from sample_data import get_sample_documents
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_knowledge_base():
    """Initialize the knowledge base with sample documents"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if required environment variables are set
        required_vars = ["PINECONE_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            logger.error("Please create a .env file with the required variables")
            return False
        
        # Initialize chatbot
        logger.info("Initializing RAG chatbot (FREE VERSION)...")
        chatbot = RAGChatbotFree()
        
        # Get sample documents
        sample_docs = get_sample_documents()
        logger.info(f"Found {len(sample_docs)} sample documents")
        
        # Add documents to knowledge base
        logger.info("Adding sample documents to knowledge base...")
        success = chatbot.add_knowledge(sample_docs)
        
        if success:
            logger.info("✅ Knowledge base setup completed successfully!")
            
            # Get and display stats
            stats = chatbot.get_knowledge_stats()
            logger.info(f"📊 Knowledge base stats: {stats}")
            
            return True
        else:
            logger.error("❌ Failed to add documents to knowledge base")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error setting up knowledge base: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Setting up RAG Chatbot Knowledge Base (FREE VERSION)")
    print("=" * 60)
    print("✅ No OpenAI credits required!")
    print("✅ Uses free local embeddings!")
    print("=" * 60)
    
    success = setup_knowledge_base()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("You can now run the FREE chatbot with: python main_free.py")
        print("🌐 Open your browser to: http://localhost:8000")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
