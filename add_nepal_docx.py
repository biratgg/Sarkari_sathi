#!/usr/bin/env python3
"""
Script to add Nepal .docx document to Pinecone
"""

import os
from docx import Document
from vector_store_free import PineconeVectorStoreFree

def read_docx_file(file_path):
    """Read a .docx file and extract text"""
    try:
        doc = Document(file_path)
        text_content = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Skip empty paragraphs
                text_content.append(paragraph.text.strip())
        
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return None

def add_nepal_docx_to_pinecone():
    """Add Nepal .docx document to Pinecone"""
    
    file_path = "/Users/biratthapa/Pictures/nepal.docx"
    
    print("🇳🇵 Adding Nepal Document to Pinecone")
    print("=" * 40)
    print(f"📁 File path: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        # Read the .docx file
        print("📖 Reading Nepal .docx file...")
        content = read_docx_file(file_path)
        
        if not content:
            print("❌ Could not read file content")
            return False
        
        print(f"✅ Successfully read {len(content)} characters from the document")
        print(f"📄 Content preview: {content[:200]}...")
        
        # Initialize vector store
        print("\n🔄 Initializing vector store...")
        vector_store = PineconeVectorStoreFree()
        
        # Create document
        document = {
            "title": "Nepal Information",
            "content": content,
            "source": "nepal.docx",
            "category": "Geography/Country Info"
        }
        
        # Add to Pinecone
        print("\n🚀 Adding Nepal document to Pinecone...")
        success = vector_store.add_documents([document])
        
        if success:
            print("✅ Nepal document added successfully to Pinecone!")
            
            # Get stats
            stats = vector_store.get_index_stats()
            print(f"📊 Total vectors in Pinecone: {stats.get('total_vector_count', 0)}")
            
            print("\n🎉 Success! You can now ask questions about Nepal to your chatbot!")
            print("Try asking: 'Tell me about Nepal' or 'What do you know about Nepal?'")
            
            return True
        else:
            print("❌ Failed to add document to Pinecone")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    add_nepal_docx_to_pinecone()
