#!/usr/bin/env python3
"""
Script to add Nepal document to Pinecone
"""

import os
from vector_store_free import PineconeVectorStoreFree

def read_text_file(file_path):
    """Read a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def add_nepal_document_to_pinecone(file_path=None, content=None, title="Nepal Document"):
    """
    Add Nepal document to Pinecone
    
    You can provide either:
    - file_path: Path to the file
    - content: Direct content as string
    """
    
    try:
        # Get content
        if file_path and os.path.exists(file_path):
            print(f"📖 Reading file: {file_path}")
            content = read_text_file(file_path)
            if not content:
                print("❌ Could not read file content")
                return False
        elif content:
            print("📝 Using provided content")
        else:
            print("❌ No file path or content provided")
            return False
        
        # Initialize vector store
        print("🔄 Initializing vector store...")
        vector_store = PineconeVectorStoreFree()
        
        # Create document
        document = {
            "title": title,
            "content": content,
            "source": "Nepal Document",
            "category": "Geography/Country Info"
        }
        
        # Add to Pinecone
        print("🚀 Adding Nepal document to Pinecone...")
        success = vector_store.add_documents([document])
        
        if success:
            print("✅ Nepal document added successfully!")
            
            # Get stats
            stats = vector_store.get_index_stats()
            print(f"📊 Total vectors in Pinecone: {stats.get('total_vector_count', 0)}")
            
            return True
        else:
            print("❌ Failed to add document")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🇳🇵 Adding Nepal Document to Pinecone")
    print("=" * 40)
    
    # Option 1: If you have a file path
    file_path = input("📁 Enter file path (or press Enter to skip): ").strip()
    
    if file_path:
        if os.path.exists(file_path):
            success = add_nepal_document_to_pinecone(file_path=file_path)
        else:
            print(f"❌ File not found: {file_path}")
            return
    else:
        # Option 2: Manual content input
        print("\n📝 Enter Nepal document content manually:")
        print("(Press Enter twice when done)")
        
        content_lines = []
        while True:
            line = input()
            if line == "" and content_lines and content_lines[-1] == "":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines[:-1])  # Remove last empty line
        
        if content.strip():
            success = add_nepal_document_to_pinecone(content=content)
        else:
            print("❌ No content provided")
            return
    
    if success:
        print("\n🎉 Success! Your Nepal document is now in Pinecone!")
        print("You can ask questions about Nepal to your chatbot.")
    else:
        print("\n❌ Failed to add Nepal document.")

if __name__ == "__main__":
    main()
