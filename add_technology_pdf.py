#!/usr/bin/env python3
"""
Script to add technology.pdf document to Pinecone
"""

import os
from vector_store_free import PineconeVectorStoreFree
import PyPDF2

def chunk_text(text, chunk_size=500, overlap=100):
    """Chunk text into overlapping segments for better retrieval."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks

def read_pdf_file(file_path):
    """Read a PDF file and extract text, then chunk into overlapping pieces for better retrieval."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    # Remove excessive newlines and spaces
                    cleaned = ' '.join(text.split())
                    full_text.append(cleaned)
            all_text = ' '.join(full_text)
            return chunk_text(all_text)
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return []

def add_technology_pdf_to_pinecone():
    """Add technology.pdf document to Pinecone, chunked for better retrieval."""
    file_path = "technology.pdf"
    print("🖥️ Adding Technology PDF Document to Pinecone")
    print("=" * 40)
    print(f"📁 File path: {file_path}")
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    try:
        print("📖 Reading technology.pdf file...")
        chunks = read_pdf_file(file_path)
        if not chunks:
            print("❌ Could not read file content")
            return False
        print(f"✅ Successfully read {len(chunks)} chunks from the document")
        print(f"📄 First chunk preview: {chunks[0][:200]}...")
        print("\n🔄 Initializing vector store...")
        vector_store = PineconeVectorStoreFree()
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                "title": f"Technology Information (chunk {i+1})",
                "content": chunk,
                "source": "technology.pdf",
                "category": "Technology",
                "chunk": i+1
            })
        print(f"\n🚀 Adding {len(documents)} technology document chunks to Pinecone...")
        success = vector_store.add_documents(documents)
        if success:
            print("✅ Technology document chunks added successfully to Pinecone!")
            stats = vector_store.get_index_stats()
            print(f"📊 Total vectors in Pinecone: {stats.get('total_vector_count', 0)}")
            print("\n🎉 Success! You can now ask questions about technology to your chatbot!")
            return True
        else:
            print("❌ Failed to add document chunks to Pinecone")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    add_technology_pdf_to_pinecone()
