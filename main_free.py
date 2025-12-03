from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from rag_chatbot_free import RAGChatbotFree
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API (Free Version)",
    description="A RAG-based chatbot using Pinecone vector store with free local embeddings",
    version="1.0.0"
)

# Initialize chatbot
try:
    chatbot = RAGChatbotFree()
    logger.info("RAG Chatbot (Free) initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize chatbot: {e}")
    chatbot = None

# Pydantic models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    relevant_documents: List[Dict[str, Any]]
    context_used: bool
    query: str

class DocumentRequest(BaseModel):
    documents: List[Dict[str, Any]]

class DocumentResponse(BaseModel):
    success: bool
    message: str
    documents_added: int

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chat interface"""
    try:
        with open("templates/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Chatbot interface not found</h1>", status_code=404)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat requests"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        result = chatbot.chat(request.message)
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-documents", response_model=DocumentResponse)
async def add_documents(request: DocumentRequest):
    """Add documents to the knowledge base"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        success = chatbot.add_knowledge(request.documents)
        if success:
            return DocumentResponse(
                success=True,
                message="Documents added successfully",
                documents_added=len(request.documents)
            )
        else:
            return DocumentResponse(
                success=False,
                message="Failed to add documents",
                documents_added=0
            )
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get knowledge base statistics"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        stats = chatbot.get_knowledge_stats()
        return {"stats": stats}
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chatbot_initialized": chatbot is not None,
        "version": "free",
        "config": {
            "pinecone_index": Config.FREE_INDEX_NAME,
            "embedding_model": "all-MiniLM-L6-v2 (local)",
            "chat_model": "rule-based (free)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    config = Config()
    uvicorn.run(
        "main_free:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True
    )
