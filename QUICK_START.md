# 🚀 Quick Start Guide - Sarkari Sathi

## Prerequisites Checklist

Before running the project, make sure you have:

- ✅ Python 3.8 or higher installed
- ✅ Pinecone API key (get from https://app.pinecone.io)
- ✅ Pinecone environment name
- ✅ Virtual environment activated

## Step-by-Step Instructions

### Step 1: Activate Virtual Environment

```bash
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

### Step 2: Verify Environment Variables

Make sure your `.env` file exists in the project root with:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
PINECONE_INDEX_NAME=rag-chatbot-free
OPENAI_API_KEY=your_openai_api_key_here  # Optional
APP_HOST=0.0.0.0
APP_PORT=8000
```

### Step 3: Check Knowledge Base (Optional)

If you haven't set up the knowledge base yet, run:

```bash
python setup_knowledge_base_free.py
```

This will add sample documents to Pinecone.

### Step 4: Start the Chatbot

Run the free version (recommended):

```bash
python main_free.py
```

Or if you have OpenAI credits, you can use:

```bash
python main.py
```

### Step 5: Access the Web Interface

Open your web browser and go to:

**http://localhost:8000**

You should see the Sarkari Sathi chat interface! 🇳🇵

## Troubleshooting

### Port Already in Use

If you see "Address already in use" error:

```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Then try again
python main_free.py
```

### Missing Dependencies

If you get import errors:

```bash
pip install -r requirements.txt
```

### Pinecone Connection Issues

- Verify your API key is correct in `.env`
- Check your Pinecone environment name
- Ensure you have internet connection

### Knowledge Base Empty

If the chatbot says "no information found":

```bash
# Re-initialize the knowledge base
python setup_knowledge_base_free.py
```

## Testing the Chatbot

Once running, try these queries:

- "Tell me about Nepal"
- "What services are available?"
- "What documents are needed for senior citizen ID?"
- "नेपाल कहाँ छ?" (Where is Nepal?)

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

## Need Help?

Check the main documentation:
- `Sarkari_Sathi_Project_Documentation.pdf`
- `Sarkari_Sathi_Project_Documentation.docx`
- `README.md`

