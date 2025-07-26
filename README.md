# EDBot: An Educational AI Chatbot

A secure educational chatbot powered by Python, Flask, and the Groq Llama 3 API. Designed to answer questions on science, math, and programming, it features a robust user authentication system. The MySQL database backend handles user data and an intelligent caching mechanism to deliver fast, formatted responses and minimize API calls.

## Key Features

- **Secure User Authentication**: Complete user management with signup, login, and session handling for a personalized experience.
- **Focused Educational Content**: Strictly guided to answer questions on Science, Mathematics, Programming, and AI/ML, ensuring relevant and productive interactions.
- [cite_start]**Intelligent Caching**: Caches previous queries and responses in a MySQL database to deliver faster answers and minimize API calls[cite: 3].
- [cite_start]**Structured and Readable Responses**: Formats information with proper spacing and styling for code blocks and lists to enhance readability[cite: 4].
- [cite_start]**Powered by Groq API**: Utilizes the high-performance Llama 3 model via the Groq API for fast and accurate content generation[cite: 4].
- **Modular Codebase**: Well-organized project structure with separate modules for chatbot logic, user management, and database interactions.

## Tech Stack

- **Backend**: Python, Flask
- [cite_start]**AI Integration**: Groq API (Llama 3 Model) [cite: 4]
- [cite_start]**Database**: MySQL [cite: 3]
- **Frontend**: HTML, CSS, JavaScript (for the chat interface)
- **Libraries**:
    - `flask`: Web framework
    - [cite_start]`groq`: AI API client [cite: 4]
    - [cite_start]`mysql-connector-python`: Database connectivity [cite: 3, 5, 8]

## Setup and Installation

Follow these steps to set up the project locally.

#### 1. Clone the Repository
```bash
git clone [https://github.com/StartAutomating/Education-Chatbot.git](https://github.com/StartAutomating/Education-Chatbot.git)
cd Education-Chatbot

#### 2. Create and Activate a Virtual Environment
```bash
- Windows:
    python -m venv venv
    .\venv\Scripts\activate
