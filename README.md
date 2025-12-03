# RAG Chatbot with Pinecone

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, Pinecone vector database, and OpenAI. This chatbot can answer questions based on a knowledge base stored in Pinecone.

## Features

- 🤖 **RAG Architecture**: Combines retrieval and generation for accurate responses
- 🔍 **Vector Search**: Uses Pinecone for efficient semantic search
- 🧠 **OpenAI Integration**: Powered by GPT models for natural language generation
- 🌐 **Web Interface**: Beautiful, responsive chat interface
- 📚 **Knowledge Management**: Easy to add and manage documents
- ⚡ **FastAPI Backend**: High-performance API with automatic documentation

## Architecture

```
User Query → Embedding → Pinecone Search → Context Retrieval → OpenAI Generation → Response
```

## Prerequisites

- Python 3.8+
- Pinecone account and API key
- OpenAI API key

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```env
   # Pinecone Configuration
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment_here
   PINECONE_INDEX_NAME=rag-chatbot

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # Application Configuration
   APP_HOST=0.0.0.0
   APP_PORT=8000
   ```

4. **Initialize the knowledge base**:
   ```bash
   python setup_knowledge_base.py
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

6. **Open your browser** and go to `http://localhost:8000`

## Usage

### Web Interface
- Open `http://localhost:8000` in your browser
- Start chatting with the bot
- The bot will search through its knowledge base to provide relevant answers

### API Endpoints

- `GET /` - Chat interface
- `POST /chat` - Send a message to the chatbot
- `POST /add-documents` - Add new documents to the knowledge base
- `GET /stats` - Get knowledge base statistics
- `GET /health` - Health check

### Example API Usage

```python
import requests

# Send a chat message
response = requests.post("http://localhost:8000/chat", 
                        json={"message": "What is machine learning?"})
print(response.json())

# Add documents
documents = [
    {
        "title": "My Document",
        "content": "This is the content of my document",
        "source": "My Source",
        "category": "General"
    }
]
response = requests.post("http://localhost:8000/add-documents", 
                        json={"documents": documents})
print(response.json())
```

## Configuration

The application can be configured through environment variables or by modifying `config.py`:

- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Your Pinecone environment
- `PINECONE_INDEX_NAME`: Name of the Pinecone index
- `OPENAI_API_KEY`: Your OpenAI API key
- `EMBEDDING_MODEL`: OpenAI embedding model (default: text-embedding-ada-002)
- `CHAT_MODEL`: OpenAI chat model (default: gpt-3.5-turbo)
- `TOP_K_RESULTS`: Number of similar documents to retrieve (default: 5)
- `SIMILARITY_THRESHOLD`: Minimum similarity score for documents (default: 0.7)

## Project Structure

```
├── main.py                 # FastAPI application
├── rag_chatbot.py         # RAG chatbot logic
├── vector_store.py        # Pinecone vector store operations
├── config.py              # Configuration settings
├── sample_data.py         # Sample documents
├── setup_knowledge_base.py # Knowledge base setup script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Chat interface
└── README.md             # This file
```

## Adding Your Own Documents

You can add your own documents to the knowledge base in several ways:

1. **Via API**:
   ```python
   documents = [
       {
           "title": "Document Title",
           "content": "Document content here...",
           "source": "Source name",
           "category": "Category"
       }
   ]
   requests.post("http://localhost:8000/add-documents", json={"documents": documents})
   ```

2. **Modify sample_data.py** and run the setup script again

3. **Create a custom script** using the `RAGChatbot` class

## Troubleshooting

### Common Issues

1. **"Chatbot not initialized" error**:
   - Check that all environment variables are set correctly
   - Ensure Pinecone and OpenAI API keys are valid

2. **"Failed to create embedding" error**:
   - Verify your OpenAI API key is correct
   - Check your OpenAI account has sufficient credits

3. **"Failed to connect to index" error**:
   - Verify your Pinecone API key and environment
   - Check that the index name is correct

### Logs

The application logs important information to help with debugging. Check the console output for detailed error messages.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this chatbot!

## License

This project is open source and available under the MIT License.
