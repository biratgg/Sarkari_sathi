#!/usr/bin/env python3
"""
Interactive script to add documents to Pinecone
"""

from vector_store_free import PineconeVectorStoreFree

def interactive_add_documents():
    """
    Interactive way to add documents to Pinecone
    """
    print("🚀 Interactive Document Addition to Pinecone")
    print("=" * 50)
    
    try:
        # Initialize vector store
        vector_store = PineconeVectorStoreFree()
        
        documents = []
        
        while True:
            print("\n📝 Add a new document:")
            print("(Press Enter with empty title to finish)")
            
            title = input("📋 Title: ").strip()
            if not title:
                break
                
            print("📄 Content (press Enter twice when done):")
            content_lines = []
            while True:
                line = input()
                if line == "" and content_lines and content_lines[-1] == "":
                    break
                content_lines.append(line)
            
            content = "\n".join(content_lines[:-1])  # Remove last empty line
            
            source = input("📚 Source (optional): ").strip() or "User Input"
            category = input("🏷️  Category (optional): ").strip() or "General"
            
            document = {
                "title": title,
                "content": content,
                "source": source,
                "category": category
            }
            
            documents.append(document)
            print(f"✅ Added: {title}")
        
        if documents:
            print(f"\n🚀 Adding {len(documents)} documents to Pinecone...")
            success = vector_store.add_documents(documents)
            
            if success:
                print("✅ All documents added successfully!")
                
                # Show stats
                stats = vector_store.get_index_stats()
                print(f"📊 Total vectors in Pinecone: {stats.get('total_vector_count', 0)}")
            else:
                print("❌ Failed to add documents")
        else:
            print("No documents to add.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_add_documents()
