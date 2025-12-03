#!/usr/bin/env python3
"""
Script to add your own documents to the RAG chatbot knowledge base
"""

import requests
import json

def add_documents_to_chatbot(documents):
    """
    Add documents to the chatbot via API
    
    documents should be a list of dictionaries with:
    - title: Document title
    - content: Document content
    - source: Source name (optional)
    - category: Category (optional)
    """
    try:
        # Make sure the chatbot is running first
        response = requests.post(
            "http://localhost:8000/add-documents",
            json={"documents": documents},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully added {result['documents_added']} documents!")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to chatbot. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Example of how to add your documents"""
    
    # Example documents - replace these with your own!
    my_documents = [
        {
            "title": "My Company Handbook",
            "content": "Our company was founded in 2020 and specializes in AI solutions. We have 50 employees and our main office is in San Francisco. Our core values include innovation, collaboration, and customer satisfaction.",
            "source": "Company Internal",
            "category": "Company Info"
        },
        {
            "title": "Project Guidelines",
            "content": "When starting a new project, always follow these steps: 1) Define requirements, 2) Create a timeline, 3) Assign team members, 4) Set up development environment, 5) Begin implementation with regular check-ins.",
            "source": "Project Management",
            "category": "Processes"
        },
        {
            "title": "Technical Standards",
            "content": "All code must follow our coding standards: Use Python 3.8+, follow PEP 8 style guide, write unit tests for all functions, document all APIs, and use version control with meaningful commit messages.",
            "source": "Engineering Team",
            "category": "Development"
        }
    ]
    
    print("🚀 Adding your documents to the RAG chatbot...")
    print("=" * 50)
    
    # Add the documents
    success = add_documents_to_chatbot(my_documents)
    
    if success:
        print("\n✅ Documents added successfully!")
        print("You can now ask the chatbot questions about your documents.")
        print("Try asking: 'What are our company values?' or 'What are the project guidelines?'")
    else:
        print("\n❌ Failed to add documents. Please check the error messages above.")

if __name__ == "__main__":
    main()
