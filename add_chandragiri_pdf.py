#!/usr/bin/env python3
"""
Script to add Chandragiri Municipality Citizen Charter PDF to Pinecone
"""

import pdfplumber
import os
from vector_store_free import PineconeVectorStoreFree
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file, handling tables and Nepali text"""
    try:
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract regular text
                text = page.extract_text()
                if text:
                    text_content.append(f"Page {page_num}:\n{text}\n")
                
                # Extract tables
                tables = page.extract_tables()
                for table_num, table in enumerate(tables, 1):
                    if table:
                        table_text = f"\nTable {table_num} from Page {page_num}:\n"
                        for row in table:
                            if row:
                                # Filter out None values and join
                                row_text = " | ".join([str(cell) if cell else "" for cell in row if cell])
                                if row_text.strip():
                                    table_text += row_text + "\n"
                        text_content.append(table_text + "\n")
        
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def chunk_text(text, max_chunk_size=5000):
    """Split text into smaller chunks to avoid metadata size limits"""
    chunks = []
    current_chunk = []
    current_size = 0
    
    lines = text.split('\n')
    
    for line in lines:
        line_size = len(line.encode('utf-8'))
        
        if current_size + line_size > max_chunk_size and current_chunk:
            # Save current chunk
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size + 1  # +1 for newline
    
    # Add last chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

def structure_citizen_charter_content(text):
    """Structure the citizen charter content into logical sections"""
    sections = []
    
    # Split by common section markers
    section_patterns = [
        r'महिला.*बालबालिका.*अपांगता.*जेष्ठ नागरिक',
        r'बातावारण.*विपद.*व्यवस्थापन',
        r'रोजगार सेवा',
        r'सेवाको प्रकार',
        r'सि\.नं\.'
    ]
    
    lines = text.split('\n')
    current_section = []
    section_title = "Chandragiri Municipality Citizen Charter"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a new section
        is_section_header = any(re.search(pattern, line, re.IGNORECASE) for pattern in section_patterns)
        
        if is_section_header and current_section:
            # Save previous section
            sections.append({
                'title': section_title,
                'content': '\n'.join(current_section)
            })
            current_section = [line]
            section_title = line[:100]  # Use first 100 chars as title
        else:
            current_section.append(line)
    
    # Add last section
    if current_section:
        sections.append({
            'title': section_title,
            'content': '\n'.join(current_section)
        })
    
    return sections

def add_chandragiri_pdf_to_pinecone(pdf_path=None):
    """Add Chandragiri Municipality Citizen Charter PDF to Pinecone"""
    
    # Try to find the PDF file
    if not pdf_path:
        possible_paths = [
            "नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf",
            "./नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf",
            "../नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf",
            "/Users/biratthapa/Pictures/नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf",
            "/Users/biratthapa/Downloads/नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pdf_path = path
                break
    
    if not pdf_path or not os.path.exists(pdf_path):
        print("❌ PDF file not found. Please provide the file path.")
        pdf_path = input("Enter the full path to the PDF file: ").strip()
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
    
    print(f"📄 Processing PDF: {pdf_path}")
    print("=" * 60)
    
    try:
        # Extract text from PDF
        print("📖 Extracting text from PDF...")
        text_content = extract_text_from_pdf(pdf_path)
        
        if not text_content:
            print("❌ Failed to extract text from PDF")
            return False
        
        print(f"✅ Extracted {len(text_content)} characters from PDF")
        
        # Structure the content
        print("📋 Structuring content...")
        sections = structure_citizen_charter_content(text_content)
        
        if not sections:
            # If structuring fails, use the whole text as one document
            sections = [{
                'title': 'Chandragiri Municipality Citizen Charter - Complete',
                'content': text_content
            }]
        
        print(f"✅ Structured into {len(sections)} sections")
        
        # Initialize vector store
        print("🔄 Initializing vector store...")
        vector_store = PineconeVectorStoreFree()
        
        # Prepare documents for Pinecone with proper chunking
        documents = []
        for i, section in enumerate(sections, 1):
            if section['content'].strip():
                # Chunk large sections to avoid metadata size limits
                content_chunks = chunk_text(section['content'], max_chunk_size=3000)
                
                for chunk_num, chunk in enumerate(content_chunks, 1):
                    # Limit metadata content to avoid size issues
                    metadata_content = chunk[:2000] if len(chunk) > 2000 else chunk
                    
                    documents.append({
                        'title': f"{section['title']} - Part {chunk_num}" if len(content_chunks) > 1 else section['title'],
                        'content': chunk,  # Full content for embedding
                        'source': 'नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf',
                        'category': 'Government Services/Citizen Charter'
                    })
        
        print(f"📝 Adding {len(documents)} document sections to Pinecone...")
        
        # Add to Pinecone
        success = vector_store.add_documents(documents)
        
        if success:
            print("✅ Successfully added Chandragiri Municipality Citizen Charter PDF to Pinecone!")
            
            # Get stats
            stats = vector_store.get_index_stats()
            print(f"📊 Total vectors in Pinecone: {stats.get('total_vector_count', 0)}")
            
            print("\n🎉 Success! The comprehensive citizen charter is now in your knowledge base!")
            print("You can now ask questions about:")
            print("- Services for women, children, disabled, and senior citizens")
            print("- Disaster management services")
            print("- Employment services")
            print("- And all other services mentioned in the charter")
            
            return True
        else:
            print("❌ Failed to add documents to Pinecone")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    add_chandragiri_pdf_to_pinecone(pdf_path)
