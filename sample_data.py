"""
Sample data for the RAG chatbot knowledge base
"""

SAMPLE_DOCUMENTS = [
    {
        "title": "Introduction to Machine Learning",
        "content": "Machine Learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. It enables computers to make predictions or decisions without being explicitly programmed for every scenario. There are three main types: supervised learning, unsupervised learning, and reinforcement learning.",
        "source": "ML Basics Guide",
        "category": "Machine Learning"
    },
    {
        "title": "Python Programming Fundamentals",
        "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python is widely used in web development, data science, artificial intelligence, and automation.",
        "source": "Python Documentation",
        "category": "Programming"
    },
    {
        "title": "Vector Databases and Embeddings",
        "content": "Vector databases are specialized databases designed to store and query high-dimensional vectors efficiently. They are essential for applications like semantic search, recommendation systems, and RAG (Retrieval-Augmented Generation). Embeddings are numerical representations of text, images, or other data that capture semantic meaning.",
        "source": "Vector DB Guide",
        "category": "Database"
    },
    {
        "title": "Natural Language Processing",
        "content": "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language. It involves tasks like text classification, sentiment analysis, machine translation, and question answering. Modern NLP relies heavily on transformer models and large language models.",
        "source": "NLP Handbook",
        "category": "AI"
    },
    {
        "title": "FastAPI Web Framework",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python. It's based on standard Python type hints and provides automatic interactive API documentation. FastAPI is designed to be easy to use and learn, with high performance comparable to NodeJS and Go.",
        "source": "FastAPI Documentation",
        "category": "Web Development"
    },
    {
        "title": "Pinecone Vector Database",
        "content": "Pinecone is a managed vector database service that makes it easy to build AI applications with vector search. It provides a simple API for storing and querying vectors, with features like real-time updates, filtering, and hybrid search. Pinecone is commonly used for semantic search and RAG applications.",
        "source": "Pinecone Documentation",
        "category": "Database"
    },
    {
        "title": "OpenAI API and GPT Models",
        "content": "OpenAI provides powerful language models through their API, including GPT-3.5, GPT-4, and embedding models. These models can be used for text generation, completion, summarization, and more. The API also provides embedding models like text-embedding-ada-002 for converting text to vectors.",
        "source": "OpenAI Documentation",
        "category": "AI"
    },
    {
        "title": "RAG Architecture",
        "content": "Retrieval-Augmented Generation (RAG) is an AI architecture that combines retrieval of relevant information with text generation. It works by first retrieving relevant documents from a knowledge base, then using that context to generate more accurate and informed responses. This approach reduces hallucinations and improves answer quality.",
        "source": "RAG Research Paper",
        "category": "AI Architecture"
    },
    {
        "title": "Docker Containerization",
        "content": "Docker is a containerization platform that allows you to package applications and their dependencies into lightweight, portable containers. Containers ensure consistency across different environments and make deployment easier. Docker uses images to create containers and provides tools for managing containerized applications.",
        "source": "Docker Documentation",
        "category": "DevOps"
    },
    {
        "title": "RESTful API Design",
        "content": "REST (Representational State Transfer) is an architectural style for designing web services. RESTful APIs use HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources. They are stateless, cacheable, and follow a client-server architecture. Good REST APIs are intuitive, consistent, and well-documented.",
        "source": "API Design Guide",
        "category": "Web Development"
    }
]

def get_sample_documents():
    """Return sample documents for testing"""
    return SAMPLE_DOCUMENTS

def get_documents_by_category(category: str):
    """Return documents filtered by category"""
    return [doc for doc in SAMPLE_DOCUMENTS if doc.get("category", "").lower() == category.lower()]

def get_document_titles():
    """Return list of document titles"""
    return [doc["title"] for doc in SAMPLE_DOCUMENTS]
