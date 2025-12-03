#!/usr/bin/env python3
"""
Add documents using the existing vector store class
"""

from vector_store_free import PineconeVectorStoreFree

def add_documents_via_vector_store(documents):
    """
    Add documents using the existing vector store class
    """
    try:
        # Initialize vector store
        print("🔄 Initializing vector store...")
        vector_store = PineconeVectorStoreFree()
        
        # Add documents
        print(f"📝 Adding {len(documents)} documents...")
        success = vector_store.add_documents(documents)
        
        if success:
            print("✅ Documents added successfully!")
            
            # Get stats
            stats = vector_store.get_index_stats()
            print(f"📊 Total vectors in index: {stats.get('total_vector_count', 0)}")
            
            return True
        else:
            print("❌ Failed to add documents")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Example usage"""
    
    # Your documents
    my_documents = [
        {
            "title": "Product Roadmap 2024",
            "content": "Our 2024 product roadmap includes: Q1 - Enhanced AI features, Q2 - Mobile app launch, Q3 - Enterprise integrations, Q4 - Advanced analytics dashboard. Each quarter will have specific milestones and deliverables.",
            "source": "Product Team",
            "category": "Product Planning"
        },
        {
            "title": "Security Best Practices",
            "content": "Security guidelines: Use strong passwords, enable 2FA, regular security audits, encrypt sensitive data, keep software updated, monitor access logs, and conduct security training for all employees.",
            "source": "Security Team",
            "category": "Security"
        }
    ]
    
    print("🚀 Adding documents via vector store...")
    print("=" * 50)
    
    success = add_documents_via_vector_store(my_documents)
    
    if success:
        print("\n✅ Success! Documents added to Pinecone via vector store.")
    else:
        print("\n❌ Failed to add documents.")

if __name__ == "__main__":
    main()
