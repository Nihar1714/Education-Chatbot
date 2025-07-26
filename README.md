# AI Educational Chatbot

## Overview
This project is a **Flask-based AI chatbot** designed to answer **only educational questions** (Science, Math, Physics, Chemistry, AI, ML, Deep Learning, and Programming).  
It integrates:
- **Groq API (LLaMA-3-70B model)**
- **MySQL database** for users, bot responses, and chat history.
- **Keyword filtering** to ensure topic-specific answers.

## Features
- **User Authentication:** Signup/Login system with MySQL storage.
- **Session Handling:** Tracks logged-in users.
- **Chat History:** Stores past questions and answers.
- **Response Caching:** Reduces repeated API calls using `chat_cache`.
- **Educational Filtering:** Answers only academic questions.
- **Admin Functions:** Database schema for responses and guidelines.
- **Web Interface:** Built using Flask + HTML templates.

## Project Structure
```
.
├── main.py               # Flask application entry point
├── chatbot.py            # Chatbot logic (Groq API, caching)
├── chat_cache.py         # Chat history caching system
├── user.py               # User management
├── user_database.py      # MySQL-based user database handling
├── bot_database.py       # Stores bot Q&A dataset
├── guideline.py          # Chatbot system instructions
├── keywords.py           # Educational keywords filtering
├── templates/            # HTML files (signup.html, login.html, chat.html)
└── static/               # CSS, JS files (if any)
```

## Requirements
Install dependencies:
```bash
pip install flask mysql-connector-python groq
```

## Database Setup
1. Install MySQL and create a database:
   ```sql
   CREATE DATABASE education_chatbot;
   ```
2. Tables are auto-created by the scripts:
   - `users`
   - `bot_responses`
   - `chat_cache`

## How to Run
1. **Start Flask Server:**
   ```bash
   python main.py
   ```
2. Open `http://127.0.0.1:5000` in your browser.
3. **Signup/Login → Ask questions → Get AI responses.**

## Environment Variables
Store sensitive data securely:
- MySQL credentials
- `api_key` for Groq API
- `SECRET_KEY` for Flask sessions
