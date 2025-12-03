#!/usr/bin/env python3
"""
Direct Pinecone document addition script
"""

from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import uuid
from config import Config

def add_documents_to_pinecone_direct(documents):
    """
    Add documents directly to Pinecone using the Pinecone API
    
    documents: List of dictionaries with 'title', 'content', 'source', 'category'
    """
    try:
        # Initialize Pinecone
        config = Config()
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        
        # Initialize embedding model
        print("🔄 Loading embedding model...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Connect to index
        index = pc.Index(config.FREE_INDEX_NAME)
        print(f"✅ Connected to Pinecone index: {config.FREE_INDEX_NAME}")
        
        # Prepare vectors for upsert
        vectors_to_upsert = []
        
        for doc in documents:
            print(f"📝 Processing: {doc['title']}")
            
            # Create embedding
            embedding = embedding_model.encode(doc['content']).tolist()
            
            # Create vector
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
        
        # Upsert to Pinecone
        print(f"🚀 Adding {len(vectors_to_upsert)} documents to Pinecone...")
        index.upsert(vectors=vectors_to_upsert)
        
        print("✅ Documents added successfully to Pinecone!")
        
        # Get updated stats
        stats = index.describe_index_stats()
        print(f"📊 Total vectors in index: {stats.total_vector_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding documents to Pinecone: {e}")
        return False

def main():
    """Example usage"""
    
    # Your documents
    my_documents = [
        {
            "title": "Company Mission Statement",
            "content": "Our mission is to revolutionize the way people interact with technology through innovative AI solutions. We believe in making artificial intelligence accessible, ethical, and beneficial for everyone.",
            "source": "Company Handbook",
            "category": "Company Info"
        },
        {
            "title": "Development Workflow",
            "content": "Our development workflow follows these steps: 1) Feature planning and design, 2) Code review process, 3) Automated testing, 4) Staging deployment, 5) Production release with monitoring.",
            "source": "Engineering Guidelines",
            "category": "Development Process"
        },
        {
            "title": "Customer Support Policy",
            "content": "We provide 24/7 customer support through multiple channels: email, chat, and phone. Our response time SLA is 2 hours for critical issues and 24 hours for general inquiries. All support interactions are logged and tracked.",
            "source": "Support Documentation",
            "category": "Customer Service"
        }
    ]
    
    print("🚀 Adding documents directly to Pinecone...")
    print("=" * 50)
    
    success = add_documents_to_pinecone_direct(my_documents)
    
    if success:
        print("\n✅ Success! Your documents are now in Pinecone.")
        print("You can query them through your RAG chatbot!")
    else:
        print("\n❌ Failed to add documents to Pinecone.")

if __name__ == "__main__":
    main()
