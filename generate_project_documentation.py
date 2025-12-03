#!/usr/bin/env python3
"""
Generate comprehensive project documentation PDF
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

def generate_project_documentation():
    """Generate comprehensive project documentation PDF"""
    
    # Create PDF
    pdf_path = "Sarkari_Sathi_Project_Documentation.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=8,
        spaceBefore=8
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    # Title
    elements.append(Paragraph("Sarkari Sathi", title_style))
    elements.append(Paragraph("RAG-based Government Information Chatbot", 
                              ParagraphStyle('Subtitle', parent=styles['Heading2'], 
                                            fontSize=16, alignment=TA_CENTER, 
                                            textColor=colors.HexColor('#5c6bc0'))))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"<b>Project Documentation</b><br/>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              ParagraphStyle('Date', parent=styles['Normal'], 
                                            alignment=TA_CENTER, fontSize=10)))
    elements.append(Spacer(1, 0.5*inch))
    
    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading_style))
    toc_items = [
        "1. Project Overview",
        "2. Technologies and Tools",
        "3. API Keys and Configuration",
        "4. Project Structure",
        "5. Core Components",
        "6. Implementation Details",
        "7. Features and Capabilities",
        "8. Data Flow",
        "9. Deployment Information"
    ]
    for item in toc_items:
        elements.append(Paragraph(f"• {item}", normal_style))
    elements.append(PageBreak())
    
    # 1. Project Overview
    elements.append(Paragraph("1. Project Overview", heading_style))
    elements.append(Paragraph(
        "<b>Sarkari Sathi</b> is a Retrieval-Augmented Generation (RAG) chatbot designed to provide "
        "citizens with accurate, up-to-date information about government services. The system uses "
        "semantic vector search to retrieve relevant information from government documents and provides "
        "structured, source-grounded answers to user queries.",
        normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>Key Objectives:</b>", subheading_style))
    objectives = [
        "Enable 24/7 access to government service information",
        "Support multilingual queries (English and Nepali)",
        "Provide accurate, source-attributed answers",
        "Handle diverse document formats (PDF, DOCX, tables)",
        "Operate cost-effectively without external API dependencies"
    ]
    for obj in objectives:
        elements.append(Paragraph(f"• {obj}", normal_style))
    elements.append(PageBreak())
    
    # 2. Technologies and Tools
    elements.append(Paragraph("2. Technologies and Tools", heading_style))
    
    tech_data = [
        ['Technology/Tool', 'Version', 'Purpose'],
        ['Python', '3.13', 'Core programming language'],
        ['FastAPI', '0.118.2', 'Web framework for REST API backend'],
        ['Uvicorn', '0.37.0', 'ASGI server for FastAPI'],
        ['Pinecone', '7.3.0', 'Vector database for semantic search'],
        ['Sentence Transformers', '5.1.1', 'Local embedding model (all-MiniLM-L6-v2)'],
        ['PyTorch', '2.8.0', 'Deep learning framework for embeddings'],
        ['pdfplumber', '0.11.8', 'PDF text extraction'],
        ['python-docx', '1.2.0', 'DOCX file processing'],
        ['python-dotenv', '1.1.1', 'Environment variable management'],
        ['Pydantic', '2.12.0', 'Data validation and settings'],
        ['Jinja2', '3.1.6', 'HTML templating'],
        ['NumPy', '2.3.3', 'Numerical computations'],
        ['Transformers', '4.57.0', 'Hugging Face transformers library'],
        ['Hugging Face Hub', '0.35.3', 'Model downloading and management']
    ]
    
    tech_table = Table(tech_data, colWidths=[3*inch, 1.5*inch, 3*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    elements.append(tech_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("<b>Embedding Model:</b>", subheading_style))
    elements.append(Paragraph(
        "• <b>Model:</b> sentence-transformers/all-MiniLM-L6-v2<br/>"
        "• <b>Dimensions:</b> 384<br/>"
        "• <b>Purpose:</b> Converts text (queries and documents) into dense vector representations<br/>"
        "• <b>Advantages:</b> Fast, lightweight, free to use, good semantic understanding",
        normal_style))
    elements.append(PageBreak())
    
    # 3. API Keys and Configuration
    elements.append(Paragraph("3. API Keys and Configuration", heading_style))
    
    elements.append(Paragraph("<b>Required API Keys:</b>", subheading_style))
    api_keys_data = [
        ['Service', 'Environment Variable', 'Purpose', 'Where to Get'],
        ['Pinecone', 'PINECONE_API_KEY', 'Access to vector database', 'https://app.pinecone.io'],
        ['Pinecone', 'PINECONE_ENVIRONMENT', 'Pinecone environment/region', 'Pinecone dashboard'],
        ['OpenAI', 'OPENAI_API_KEY', 'Optional: for paid version', 'https://platform.openai.com']
    ]
    
    api_table = Table(api_keys_data, colWidths=[1.5*inch, 2*inch, 2.5*inch, 2*inch])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    elements.append(api_table)
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>Configuration File (config.py):</b>", subheading_style))
    config_items = [
        "PINECONE_API_KEY: Your Pinecone API key",
        "PINECONE_ENVIRONMENT: Your Pinecone environment",
        "PINECONE_INDEX_NAME: Name of the index (default: 'rag-chatbot')",
        "FREE_INDEX_NAME: Name for free version index (default: 'rag-chatbot-free')",
        "OPENAI_API_KEY: OpenAI API key (optional, for paid version)",
        "APP_HOST: Server host (default: '0.0.0.0')",
        "APP_PORT: Server port (default: 8000)",
        "EMBEDDING_MODEL: Embedding model name (default: 'text-embedding-ada-002')",
        "FREE_EMBEDDING_MODEL: Free model name (default: 'all-MiniLM-L6-v2')",
        "TOP_K_RESULTS: Number of documents to retrieve (default: 5)",
        "SIMILARITY_THRESHOLD: Minimum similarity score (default: 0.3)"
    ]
    for item in config_items:
        elements.append(Paragraph(f"• {item}", normal_style))
    elements.append(PageBreak())
    
    # 4. Project Structure
    elements.append(Paragraph("4. Project Structure", heading_style))
    
    structure_data = [
        ['File/Directory', 'Purpose'],
        ['main.py', 'FastAPI application entry point'],
        ['main_free.py', 'Free version (no OpenAI) entry point'],
        ['rag_chatbot_free.py', 'RAG chatbot logic with rule-based generation'],
        ['vector_store_free.py', 'Pinecone vector store operations'],
        ['config.py', 'Configuration and environment variables'],
        ['sample_data.py', 'Sample documents for testing'],
        ['setup_knowledge_base_free.py', 'Initialize knowledge base with sample data'],
        ['add_chandragiri_pdf.py', 'Add PDF documents to Pinecone'],
        ['add_nepal_docx.py', 'Add DOCX files to Pinecone'],
        ['templates/index.html', 'Web chat interface'],
        ['requirements.txt', 'Python dependencies'],
        ['.env', 'Environment variables (API keys)'],
        ['.venv/', 'Python virtual environment']
    ]
    
    struct_table = Table(structure_data, colWidths=[3*inch, 4.5*inch])
    struct_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    elements.append(struct_table)
    elements.append(PageBreak())
    
    # 5. Core Components
    elements.append(Paragraph("5. Core Components", heading_style))
    
    elements.append(Paragraph("<b>5.1 Vector Store (vector_store_free.py)</b>", subheading_style))
    elements.append(Paragraph(
        "<b>Purpose:</b> Manages all interactions with Pinecone vector database<br/><br/>"
        "<b>Key Methods:</b><br/>"
        "• <b>create_embedding(text):</b> Converts text to 384-dimensional vector using MiniLM-L6-v2<br/>"
        "• <b>add_documents(documents):</b> Embeds and stores documents in Pinecone<br/>"
        "• <b>search_similar(query, top_k):</b> Finds most similar documents using cosine similarity<br/>"
        "• <b>get_index_stats():</b> Returns index statistics (vector count, dimensions)<br/><br/>"
        "<b>Technical Details:</b><br/>"
        "• Uses sentence-transformers for local embeddings (no API costs)<br/>"
        "• Handles metadata size limits (40KB per vector)<br/>"
        "• Supports chunking large documents automatically",
        normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>5.2 RAG Chatbot (rag_chatbot_free.py)</b>", subheading_style))
    elements.append(Paragraph(
        "<b>Purpose:</b> Orchestrates the RAG pipeline: retrieval + generation<br/><br/>"
        "<b>Key Methods:</b><br/>"
        "• <b>chat(query):</b> Main entry point - processes user queries<br/>"
        "• <b>retrieve_relevant_documents(query):</b> Searches Pinecone for relevant chunks<br/>"
        "• <b>generate_response(query, context):</b> Rule-based answer extraction<br/>"
        "• <b>_handle_nepali_query():</b> Special handling for Nepali language queries<br/><br/>"
        "<b>Response Extraction Types:</b><br/>"
        "• Fee/Cost information<br/>"
        "• Required documents (lists)<br/>"
        "• Process/Steps<br/>"
        "• Time/Duration<br/>"
        "• Services available<br/>"
        "• Location information<br/>"
        "• Nepal-specific facts",
        normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>5.3 FastAPI Backend (main_free.py)</b>", subheading_style))
    elements.append(Paragraph(
        "<b>Purpose:</b> RESTful API server for the chatbot<br/><br/>"
        "<b>Endpoints:</b><br/>"
        "• <b>GET /:</b> Serves the web chat interface<br/>"
        "• <b>POST /chat:</b> Processes chat queries, returns responses<br/>"
        "• <b>POST /add-documents:</b> Adds new documents to knowledge base<br/>"
        "• <b>GET /stats:</b> Returns knowledge base statistics<br/>"
        "• <b>GET /health:</b> Health check endpoint",
        normal_style))
    elements.append(PageBreak())
    
    # 6. Implementation Details
    elements.append(Paragraph("6. Implementation Details", heading_style))
    
    elements.append(Paragraph("<b>6.1 Document Processing Pipeline</b>", subheading_style))
    pipeline_steps = [
        "1. <b>Ingestion:</b> Documents are loaded from various sources (PDF, DOCX, text files)",
        "2. <b>Text Extraction:</b> pdfplumber extracts text from PDFs, python-docx from DOCX files",
        "3. <b>Cleaning:</b> Remove headers, footers, extra spaces, normalize formatting",
        "4. <b>Chunking:</b> Split large documents into smaller chunks (max 3000 chars) to avoid metadata limits",
        "5. <b>Embedding:</b> Each chunk is converted to 384-dimensional vector using MiniLM-L6-v2",
        "6. <b>Indexing:</b> Vectors stored in Pinecone with metadata (title, source, category, content preview)",
        "7. <b>Metadata Limiting:</b> Content in metadata limited to 2000 chars to stay under 40KB limit"
    ]
    for step in pipeline_steps:
        elements.append(Paragraph(step, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>6.2 Query Processing Flow</b>", subheading_style))
    query_steps = [
        "1. <b>Query Reception:</b> User query received via FastAPI /chat endpoint",
        "2. <b>Preprocessing:</b> Query is preprocessed (Nepali keyword expansion, normalization)",
        "3. <b>Embedding:</b> Query converted to vector using same embedding model",
        "4. <b>Vector Search:</b> Cosine similarity search in Pinecone (top-k=5, threshold=0.3)",
        "5. <b>Context Assembly:</b> Retrieved document chunks combined into context",
        "6. <b>Query Classification:</b> System identifies query type (fee, documents, process, etc.)",
        "7. <b>Answer Extraction:</b> Rule-based extractor pulls relevant information",
        "8. <b>Response Formatting:</b> Answer formatted with bullets, citations, source attribution",
        "9. <b>Delivery:</b> JSON response sent to frontend for display"
    ]
    for step in query_steps:
        elements.append(Paragraph(step, normal_style))
    elements.append(PageBreak())
    
    # 7. Features and Capabilities
    elements.append(Paragraph("7. Features and Capabilities", heading_style))
    
    elements.append(Paragraph("<b>7.1 Multilingual Support</b>", subheading_style))
    elements.append(Paragraph(
        "• <b>Nepali Language Detection:</b> Detects Devanagari script in queries<br/>"
        "• <b>Keyword Mapping:</b> Maps Nepali question words to extraction methods<br/>"
        "• <b>Query Preprocessing:</b> Adds English translations to Nepali queries for better embedding<br/>"
        "• <b>Supported Nepali Terms:</b> कहाँ (where), कहिले (when), कति (how much), कसरी (how), "
        "के (what), कागजात (documents), शुल्क (fee), सेवा (service), etc.",
        normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>7.2 Document Types Supported</b>", subheading_style))
    doc_types = [
        "• <b>PDF Files:</b> Text extraction using pdfplumber, table extraction support",
        "• <b>DOCX Files:</b> Full text extraction using python-docx",
        "• <b>Text Files:</b> Direct text processing",
        "• <b>Tabular Data:</b> Tables converted to structured text format",
        "• <b>Mixed Content:</b> Handles documents with both text and tables"
    ]
    for doc_type in doc_types:
        elements.append(Paragraph(doc_type, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>7.3 Answer Extraction Capabilities</b>", subheading_style))
    extraction_capabilities = [
        "• <b>Fee Information:</b> Extracts cost/fee details (including 'निःशुल्क' - free)",
        "• <b>Document Lists:</b> Extracts numbered lists of required documents",
        "• <b>Process Steps:</b> Identifies and extracts procedure information",
        "• <b>Time Information:</b> Extracts duration, deadlines, service times",
        "• <b>Service Lists:</b> Identifies available services from context",
        "• <b>Location Data:</b> Extracts geographical and location information",
        "• <b>General Summaries:</b> Fallback to general information extraction"
    ]
    for capability in extraction_capabilities:
        elements.append(Paragraph(capability, normal_style))
    elements.append(PageBreak())
    
    # 8. Data Flow
    elements.append(Paragraph("8. Data Flow", heading_style))
    
    elements.append(Paragraph("<b>8.1 Document Ingestion Flow</b>", subheading_style))
    elements.append(Paragraph(
        "Document → Text Extraction → Cleaning → Chunking → Embedding → Pinecone Storage",
        ParagraphStyle('Flow', parent=normal_style, alignment=TA_CENTER, 
                      textColor=colors.HexColor('#3949ab'), fontSize=12)))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>8.2 Query Processing Flow</b>", subheading_style))
    elements.append(Paragraph(
        "User Query → Preprocessing → Embedding → Pinecone Search → Context Retrieval → "
        "Answer Extraction → Response Formatting → User",
        ParagraphStyle('Flow', parent=normal_style, alignment=TA_CENTER, 
                      textColor=colors.HexColor('#3949ab'), fontSize=12)))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>8.3 Current Knowledge Base</b>", subheading_style))
    kb_data = [
        ['Document Type', 'Count', 'Source'],
        ['Sample Documents', '10', 'sample_data.py'],
        ['Nepal Information', '1', 'nepal.docx'],
        ['Citizen Charter (Basic)', '1', 'Manual entry'],
        ['Citizen Charter (Complete PDF)', '151 chunks', 'नागरिक वडापत्र विषयक्षेत्रगतरुपमा.pdf'],
        ['Total Vectors', '163', 'Pinecone index: rag-chatbot-free']
    ]
    
    kb_table = Table(kb_data, colWidths=[2.5*inch, 1.5*inch, 3.5*inch])
    kb_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    elements.append(kb_table)
    elements.append(PageBreak())
    
    # 9. Deployment Information
    elements.append(Paragraph("9. Deployment Information", heading_style))
    
    elements.append(Paragraph("<b>9.1 Setup Steps</b>", subheading_style))
    setup_steps = [
        "1. Create virtual environment: <b>python -m venv .venv</b>",
        "2. Activate virtual environment: <b>source .venv/bin/activate</b> (Mac/Linux)",
        "3. Install dependencies: <b>pip install -r requirements.txt</b>",
        "4. Create .env file with API keys (PINECONE_API_KEY, PINECONE_ENVIRONMENT)",
        "5. Initialize knowledge base: <b>python setup_knowledge_base_free.py</b>",
        "6. Start server: <b>python main_free.py</b>",
        "7. Access web interface: <b>http://localhost:8000</b>"
    ]
    for step in setup_steps:
        elements.append(Paragraph(step, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>9.2 Adding Documents</b>", subheading_style))
    add_doc_methods = [
        "• <b>PDF Files:</b> python add_chandragiri_pdf.py [path_to_pdf]",
        "• <b>DOCX Files:</b> python add_nepal_docx.py",
        "• <b>Via API:</b> POST /add-documents with JSON payload",
        "• <b>Interactive:</b> python interactive_add_documents.py"
    ]
    for method in add_doc_methods:
        elements.append(Paragraph(method, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>9.3 System Requirements</b>", subheading_style))
    requirements = [
        "• <b>Python:</b> 3.8 or higher",
        "• <b>RAM:</b> Minimum 4GB (8GB recommended for embedding model)",
        "• <b>Storage:</b> ~500MB for dependencies and models",
        "• <b>Internet:</b> Required for Pinecone API and initial model download",
        "• <b>OS:</b> macOS, Linux, or Windows"
    ]
    for req in requirements:
        elements.append(Paragraph(req, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>9.4 Cost Analysis</b>", subheading_style))
    elements.append(Paragraph(
        "• <b>Embedding Model:</b> Free (local, no API calls)<br/>"
        "• <b>Pinecone:</b> Free tier available (limited to 1 index, 100K vectors)<br/>"
        "• <b>Response Generation:</b> Free (rule-based, no LLM API calls)<br/>"
        "• <b>Total Operating Cost:</b> $0 (within free tier limits)<br/><br/>"
        "<b>Note:</b> For production scale, Pinecone paid plans start at $70/month",
        normal_style))
    elements.append(PageBreak())
    
    # 10. Technical Specifications
    elements.append(Paragraph("10. Technical Specifications", heading_style))
    
    elements.append(Paragraph("<b>10.1 Vector Database Configuration</b>", subheading_style))
    vector_specs = [
        "• <b>Index Name:</b> rag-chatbot-free",
        "• <b>Dimensions:</b> 384 (MiniLM-L6-v2)",
        "• <b>Metric:</b> Cosine Similarity",
        "• <b>Cloud Provider:</b> AWS",
        "• <b>Region:</b> us-east-1",
        "• <b>Metadata Limit:</b> 40KB per vector",
        "• <b>Current Vectors:</b> 163"
    ]
    for spec in vector_specs:
        elements.append(Paragraph(spec, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>10.2 API Endpoints</b>", subheading_style))
    endpoint_data = [
        ['Method', 'Endpoint', 'Purpose', 'Request/Response'],
        ['GET', '/', 'Web UI', 'Returns HTML chat interface'],
        ['POST', '/chat', 'Chat query', '{"message": "query"} → {"response": "...", "sources": [...]}'],
        ['POST', '/add-documents', 'Add docs', '{"documents": [...]} → {"success": true}'],
        ['GET', '/stats', 'Statistics', 'Returns index stats'],
        ['GET', '/health', 'Health check', 'Returns system status']
    ]
    
    endpoint_table = Table(endpoint_data, colWidths=[1*inch, 2*inch, 2*inch, 2.5*inch])
    endpoint_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    elements.append(endpoint_table)
    elements.append(PageBreak())
    
    # 11. Known Issues and Limitations
    elements.append(Paragraph("11. Known Issues and Limitations", heading_style))
    
    elements.append(Paragraph("<b>11.1 Current Limitations</b>", subheading_style))
    limitations = [
        "• <b>Multilingual Support:</b> Embedding model is English-centric, affecting Nepali query accuracy",
        "• <b>Response Quality:</b> Rule-based extraction may miss nuanced queries",
        "• <b>Context Window:</b> Limited to top-5 retrieved documents",
        "• <b>No Conversation Memory:</b> Each query is independent, no context retention",
        "• <b>Metadata Size:</b> Large documents must be chunked to fit 40KB metadata limit",
        "• <b>No OCR Support:</b> Scanned PDFs with images not yet supported",
        "• <b>Similarity Threshold:</b> Fixed at 0.3, may need tuning for different query types"
    ]
    for limitation in limitations:
        elements.append(Paragraph(limitation, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("<b>11.2 Future Improvements</b>", subheading_style))
    improvements = [
        "• Integrate multilingual embedding models (multilingual-MiniLM)",
        "• Add OCR support for scanned documents",
        "• Implement conversation memory and context retention",
        "• Add hybrid search (keyword + semantic)",
        "• Integrate local LLM for better response generation",
        "• Add user authentication and query history",
        "• Implement caching for frequently asked questions"
    ]
    for improvement in improvements:
        elements.append(Paragraph(improvement, normal_style))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF generated successfully: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    generate_project_documentation()
