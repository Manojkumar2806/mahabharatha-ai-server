POST /api/query

POST http://127.0.0.1:8000/api/query


Description: Asks a question about Mahabharata and returns a structured answer.

Request:

Body (JSON):

{
  "query": "string",
  "n_results": 3
}


Response:

Success (200):

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


Errors:

500 Rate Limit: 🌊 The wisdom of Mahabharata is busy. Pause and ask again.

500 Model Unavailable: 🕉️ The path to Mahabharata wisdom is temporarily closed. Try again shortly.

500 Token Limit: 📝 The scroll cannot hold so many words. Ask a shorter question.

500 Auth Error: 🔐 The divine path is blocked. Make sure your keys are correct.

500 Network Error: 🌐 The path to Mahabharata knowledge is shaky. Check your internet.

500 Unknown Error: ✨ The wisdom of Mahabharata is hidden for now. Please try again.

Example cURL Request:

curl -X POST "https://api.mahabharata.ai:443/api/query" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY_HERE" \
-d '{"query": "Who is Arjuna?", "n_results": 3}'


Example Response (200):

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