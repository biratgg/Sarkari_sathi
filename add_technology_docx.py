#!/usr/bin/env python3
"""
Script to add technology.docx document to Pinecone with chunking and overlap
"""

import os
from docx import Document
from vector_store_free import PineconeVectorStoreFree

def chunk_paragraphs(paragraphs, chunk_size=500, overlap=100):
    """Chunk paragraphs into overlapping segments for better retrieval."""
    chunks = []
    current_chunk = []
    current_length = 0
    for para in paragraphs:
        words = para.split()
        if current_length + len(words) > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            # Overlap: keep last N words for next chunk
            if overlap < len(current_chunk):
                current_chunk = current_chunk[-overlap:]
            else:
                current_chunk = current_chunk[:]
            current_length = len(current_chunk)
        current_chunk.extend(words)
        current_length += len(words)
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def read_docx_file(file_path):
    """Read a .docx file and extract text, then chunk into overlapping pieces for better retrieval."""
    try:
        doc = Document(file_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return chunk_paragraphs(paragraphs)
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return []

def add_technology_docx_to_pinecone():
    """Add technology.docx document to Pinecone, chunked for better retrieval."""
    file_path = "technology.docx"
    print("🖥️ Adding Technology DOCX Document to Pinecone")
    print("=" * 40)
    print(f"📁 File path: {file_path}")
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    try:
        print("📖 Reading technology.docx file...")
        chunks = read_docx_file(file_path)
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
                "source": "technology.docx",
                "category": "Technology",
                "chunk": i+1
            })
        print(f"\n🚀 Adding {len(documents)} technology document chunks to Pinecone...")
        success = vector_store.add_documents(documents)
        if success:
            print("✅ Technology DOCX document chunks added successfully to Pinecone!")
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
    add_technology_docx_to_pinecone()
