# fastapi_mahabharata_chatbot.py
import os
import requests
import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import json

# ==========================
# 1. Load environment variables
# ==========================
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
CHROMA_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_CLOUD_TENANT")
CHROMA_DB = "Mahabharath"
CHROMA_COLLECTION = "Mahabharath"

if not PERPLEXITY_API_KEY or not CHROMA_API_KEY or not CHROMA_TENANT:
    raise RuntimeError("❌ Missing required API keys/tenant in environment variables.")

# ==========================
# 2. Initialize FastAPI app
# ==========================
app = FastAPI(title="Mahabharata RAG Chatbot")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# 3. Initialize ChromaDB client
# ==========================
client = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DB
)

try:
    knowledge_collection = client.get_collection(CHROMA_COLLECTION)
except Exception as e:
    raise RuntimeError(f"❌ Failed to access ChromaDB collection '{CHROMA_COLLECTION}': {e}")

# ==========================
# 4. Global Prompt Template (no verse)
# ==========================
PROMPT_TEMPLATE = """
You are Mahabharata-GPT, a divine chatbot that answers only about Mahabharata.

Context:
{context}

Question:
{user_query}

Respond in JSON format ONLY with the following fields:
{{
  "who": "<Brief description of the person/event in Mahabharata>",
  "lesson": "<Key habits or principles one can learn from this character/event, actionable advice>",
  "followup_questions": ["<Q1>", "<Q2>", "<Q3>"]
}}

⚡ Requirements:
- Use Mahabharata language and tone.
- Keep answers concise, clear, and educational.
- Do NOT answer anything outside Mahabharata.
"""

# ==========================
# 5. Request Model
# ==========================
class QueryRequest(BaseModel):
    query: str
    n_results: int = 3

# ==========================
# 6. ChromaDB Retrieval
# ==========================
def query_chroma_collection(query: str, n_results: int = 3) -> str:
    results = knowledge_collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])[0]
    if not docs:
        return ""
    return "\n\n".join(docs)

# ==========================
# 7. Call Perplexity API
# ==========================
def call_perplexity_api(user_query: str, context: str) -> Dict:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = PROMPT_TEMPLATE.format(context=context, user_query=user_query)

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.4,
        "max_tokens": 1024,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Perplexity API error: {response.status_code} {response.text}")

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)  # Parse the JSON string into dict
        return parsed
    except Exception:
        raise Exception(f"Failed to parse Perplexity response as JSON: {response.text}")

# ==========================
# 8. Mahabharata-themed Error Handling
# ==========================
def handle_ai_error(error):
    error_str = str(error)
    
    if "413" in error_str or "rate_limit" in error_str.lower():
        return {
            "error_type": "rate_limit",
            "user_message": "🌊 The wisdom of Mahabharata is busy. Pause a moment and ask again."
        }
    
    if "model not found" in error_str.lower() or "model_decommissioned" in error_str.lower():
        return {
            "error_type": "model_unavailable",
            "user_message": "🕉️ The path to Mahabharata wisdom is temporarily closed. Try shortly."
        }
    
    if "payload too large" in error_str.lower() or "request too large" in error_str.lower():
        return {
            "error_type": "token_limit",
            "user_message": "📝 Your question is too long. Ask a shorter, clear question."
        }

    if "401" in error_str or "unauthorized" in error_str.lower():
        return {
            "error_type": "auth_error",
            "user_message": "🔐 The divine path is blocked. Check your API keys."
        }

    if "timeout" in error_str.lower() or "connection" in error_str.lower():
        return {
            "error_type": "network_error",
            "user_message": "🌐 The path to Mahabharata knowledge is shaky. Check your internet."
        }
    
    return {
        "error_type": "unknown_error",
        "user_message": "✨ The wisdom of Mahabharata is hidden for now. Try again."
    }

# ==========================
# 9. API Endpoint
# ==========================
@app.post("/api/query")
async def query_docs(request: QueryRequest):
    try:
        context = query_chroma_collection(request.query, request.n_results)
        if not context.strip():
            return {"error": "❌ No relevant information found in the Mahabharata knowledge base."}

        response_data = call_perplexity_api(request.query, context)
        return response_data

    except Exception as e:
        error_response = handle_ai_error(e)
        raise HTTPException(status_code=500, detail=error_response["user_message"])

# ==========================
# 10. Health Check
# ==========================
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Mahabharata RAG AI is running"}

