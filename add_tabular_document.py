#!/usr/bin/env python3
"""
Script to add tabular/structured documents to Pinecone
"""

from vector_store_free import PineconeVectorStoreFree

def add_tabular_document_to_pinecone():
    """
    Add a tabular document (like the Nepali Citizen Charter) to Pinecone
    """
    
    # Example: Nepali Citizen Charter document
    # You can replace this with your actual document content
    tabular_document = {
        "title": "Chandragiri Municipality Citizen Charter - Women, Children, Disabled and Senior Citizens Services",
        "content": """
        CHANDRAGIRI MUNICIPALITY CITIZEN CHARTER
        Office of the Municipal Executive, Chandragiri, Kathmandu, Bagmati Province, Nepal (2079 BS)
        
        Services for Women, Children, Persons with Disabilities, Senior Citizens and Organizations
        
        SERVICE 1: SENIOR CITIZEN ID CARD PROVISION
        - Responsible Officer: Head of Women and Children Branch
        - Service Branch: Women and Children Branch
        - Required Documents:
          1. Application form with details of the concerned person
          2. Copy of Citizenship Certificate
          3. 2 passport-sized photos
          4. Proof of permanent residence
          5. Other necessary documents/proofs
        - Process: Contact the Women and Children Branch after obtaining an order from the Chief Administrative Officer
        - Grievance Officer: Chief Administrative Officer
        - Time to Receive Service: Same day if possible after all documents are complete, otherwise next day
        - Fee: Free (निःशुल्क)
        
        SERVICE 2: DISABILITY ID CARD PROVISION
        - Responsible Officer: Head of Women and Children Branch
        - Service Branch: Women and Children Branch
        - Required Documents:
          1. Application form with details as per Schedule 1
          2. Copy of Citizenship Certificate
          3. Recommendation from the concerned ward office
          4. Proof of permanent residence
          5. Recommendation from concerned doctor (specialist doctor for eyes, nose, ears, throat)
        - Process: Contact the Women and Children Branch after obtaining an order from the Chief Administrative Officer, along with citizenship certificate copy
        - Grievance Officer: Chief Administrative Officer
        - Time to Receive Service: Same day if documents are in order, or within 3 days from local coordination committee decision after ward recommendation
        - Fee: Free (निःशुल्क)
        
        This charter covers services for vulnerable groups including women, children, persons with disabilities, and senior citizens in Chandragiri Municipality.
        """,
        "source": "Chandragiri Municipality Official Document",
        "category": "Government Services/Citizen Charter"
    }
    
    print("📊 Adding Tabular Document to Pinecone")
    print("=" * 50)
    
    try:
        # Initialize vector store
        print("🔄 Initializing vector store...")
        vector_store = PineconeVectorStoreFree()
        
        # Add document
        print("📝 Adding tabular document...")
        success = vector_store.add_documents([tabular_document])
        
        if success:
            print("✅ Tabular document added successfully!")
            
            # Get stats
            stats = vector_store.get_index_stats()
            print(f"📊 Total vectors in Pinecone: {stats.get('total_vector_count', 0)}")
            
            print("\n🎉 Success! You can now ask questions about the citizen charter!")
            print("Try asking:")
            print("- 'What services are available for senior citizens?'")
            print("- 'How do I get a disability ID card?'")
            print("- 'What documents are needed for senior citizen ID?'")
            print("- 'What is the process for disability services?'")
            
            return True
        else:
            print("❌ Failed to add document")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_tabular_search():
    """Test search functionality with the tabular document"""
    
    print("\n🔍 TESTING SEARCH WITH TABULAR DOCUMENT:")
    print("=" * 50)
    
    try:
        vector_store = PineconeVectorStoreFree()
        
        # Test queries
        test_queries = [
            "What services are available for senior citizens?",
            "How do I get a disability ID card?",
            "What documents are needed for senior citizen ID?",
            "What is the fee for disability services?",
            "Who is the grievance officer?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            results = vector_store.search_similar(query, top_k=2)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result['title']} (score: {result['score']:.3f})")
                    print(f"     {result['content'][:100]}...")
            else:
                print("  No results found")
                
    except Exception as e:
        print(f"❌ Error testing search: {e}")

if __name__ == "__main__":
    # Add the document
    success = add_tabular_document_to_pinecone()
    
    if success:
        # Test the search
        test_tabular_search()
