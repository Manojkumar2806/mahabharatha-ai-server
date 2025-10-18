# 🕉️ **Mahabharath: The Pathfinder of Dharma in Kaliyug!**

Backend API for a Mahabharata-focused chatbot. Fetches knowledge from **ChromaDB** and generates structured answers using **Perplexity AI**, including character details, lessons, and follow-up questions. Built with **FastAPI** ⚡

---

## ✨ Features

* 🧠 Answers questions about Mahabharata characters, events, and stories.
* 📑 Provides structured responses:

  * **Who** – Brief description of the person/event.
  * **Lesson** – Habits or principles one can learn.
  * **Follow-up questions** – Suggested related questions.
* ⚡ Handles errors gracefully with Mahabharata-themed messages.
* 🌐 Integrates **ChromaDB** for knowledge retrieval and **Perplexity AI** for AI-generated responses.
* 🚀 Built with **FastAPI** for high-performance backend.

---

## 🛠 Technologies Used

* **FastAPI** – Python framework for building APIs.
* **ChromaDB** – Cloud-based vector database for storing Mahabharata knowledge.
* **Perplexity API** – AI-powered question answering.
* **Python** – Backend language.
* **Native Chroma Cloud** – To manage the vector store.

---

## 🔗 API Endpoint

### POST `/api/query`

> **Description:** Ask a question about Mahabharata and receive a structured answer.

**Request Body (JSON):**

```json
{
  "query": "string",
  "n_results": 3 or 4
}
```

**Response (200 Success):**

```json
{
  "answer": {
    "who": "string (Brief description of person/event in Mahabharata)",
    "lesson": "string (Habits or principles to learn from the character/event)",
    "followup_questions": [
      "string",
      "string",
      "string"
    ]
  }
}
```

**Error Responses:**

| Code | Error             | Message                                                                      |
| ---- | ----------------- | ---------------------------------------------------------------------------- |
| 500  | Rate Limit        | 🌊 The wisdom of Mahabharata is busy. Pause and ask again.                   |
| 500  | Model Unavailable | 🕉️ The path to Mahabharata wisdom is temporarily closed. Try again shortly. |
| 500  | Token Limit       | 📝 The scroll cannot hold so many words. Ask a shorter question.             |
| 500  | Auth Error        | 🔐 The divine path is blocked. Make sure your keys are correct.              |
| 500  | Network Error     | 🌐 The path to Mahabharata knowledge is shaky. Check your internet.          |
| 500  | Unknown Error     | ✨ The wisdom of Mahabharata is hidden for now. Please try again.             |

---

## 💻 Example cURL Request

```bash
curl -X POST "https://api.mahabharata.ai:443/api/query" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY_HERE" \
-d '{"query": "Who is Arjuna?", "n_results": 3}'
```

## 📦 Example Response

```json
{
  "answer": {
    "who": "Arjuna, the peerless Kshatriya and foremost warrior of the Pandavas.",
    "lesson": "Learn courage, preparation, focus on duty, and reliance on divine guidance in difficult situations.",
    "followup_questions": [
      "What are the key battles Arjuna fought in Kurukshetra?",
      "What moral lessons does the Bhagavad Gita impart through Arjuna?",
      "How did Krishna guide Arjuna during critical moments?"
    ]
  }
}
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Manojkumar2806/mahabharatha-ai-server.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables in `.env`

```env
PERPLEXITY_API_KEY=your_perplexity_api_key
CHROMA_CLOUD_API_KEY=your_chroma_api_key
CHROMA_CLOUD_TENANT=your_chroma_tenant_id
```

### 4. Run the FastAPI server

```bash
uvicorn main:app 
```
> _**🚀 The server will start at http://127.0.0.1:8000 and is ready to answer divine queries! 🕉️**_




# 🙏 Thank You

> *Thank you for exploring the wisdom of Mahabharata through AI. May knowledge and dharma guide your path!* ✨

May this tool help you uncover the timeless wisdom of the epic and inspire learning, reflection, and curiosity. 🕉️✨

