from groq import Groq
from chat_cache import ChatCache
from user import User
from flask import session
from guideline import CHATBOT_INSTRUCTIONS  # ✅ Import chatbot instructions
import re

class EducationBot:
    def __init__(self, api_key, host="localhost", user="root", password="Nihar", database="education_chatbot"):
        self.client = Groq(api_key=api_key)
        self.model = "llama3-70b-8192"

        # ✅ Use imported chatbot guidelines
        self.system_message = CHATBOT_INSTRUCTIONS

        self.cache = ChatCache(host, user, password, database)
        self.user = User(host, user, password, database)
        self.current_user_id = None  # Track the logged-in user

    def signup(self, username, password):
        """Signup a new user and get user_id."""
        result = self.user.signup(username, password)
        if result == "User registered successfully!":
            user_id = self.user.db.get_user_id(username)  # ✅ Fix method call
            if user_id:
                session['user_id'] = user_id
                self.current_user_id = user_id
        return result

    def login(self, username, password):
        """Login an existing user and store user_id in session."""
        result = self.user.login(username, password)
        if "Login successful" in result:
            user_id = self.user.db.get_user_id(username)  # ✅ Fix method call
            if user_id:
                session['user_id'] = user_id  # ✅ Store user ID in session
                self.current_user_id = user_id
                print("✅ Session after login:", session)  # 🔍 Debugging
        return result

    def get_response(self, user_prompt):
        """Retrieve response ONLY for educational topics."""
        
        if self.current_user_id is None:
            self.current_user_id = session.get('user_id')  # ✅ Retrieve user_id from session
            print("🔍 Debug: Retrieved user_id from session:", self.current_user_id)  # 🔍 Debugging

        if self.current_user_id is None:
            return "❌ Please login."

        cached_response = self.cache.get_cached_response(self.current_user_id, user_prompt)
        if cached_response:
            return cached_response

        messages = [self.system_message, {"role": "user", "content": user_prompt}]

        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            if not chat_completion.choices:
                return "❌ Sorry, I couldn't process your request."

            response = chat_completion.choices[0].message.content.strip()
            formatted_response = self.format_response(response)
            self.cache.save_response(self.current_user_id, user_prompt, formatted_response)

            return formatted_response

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def format_response(self, response):
        """Formats chatbot responses with clean structure, smooth readability, and better spacing."""
        lines = response.split("\n")
        formatted_response = []
        in_code_block = False
        detected_language = "python"  # Default language for code blocks

        for line in lines:
            line = line.strip()

            if not line:
                continue  # Ignore empty lines for better readability

            # ✅ Detect and format code blocks
            if line.startswith("```"):
                if in_code_block:
                    formatted_response.append("</code></pre>")  # Close code block
                    in_code_block = False
                else:
                    detected_language = line[3:].strip() or "python"  # Detect language
                    formatted_response.append(f"<pre class='code-block'><code class='language-{detected_language}'>")
                    in_code_block = True
                continue  # Skip this line

            if in_code_block:
                formatted_response.append(line)  # Keep code formatting
            else:
                # ✅ Format as bullet points if line starts with "- " or "* "
                if line.startswith("- ") or line.startswith("* "):
                    formatted_response.append(f"<li>{line[2:]}</li>")  
                elif line.endswith(":"):
                    formatted_response.append(f"<h3>{line}</h3>")  # Convert headings (e.g., "Title:")
                else:
                    formatted_response.append(f"<p class='message-text'>{line}</p>")  # Normal paragraph formatting

        if in_code_block:
            formatted_response.append("</code></pre>")  # Close any unclosed code blocks

        # ✅ Wrap lists with <ul> tags for proper display
        formatted_response = "\n".join(formatted_response)
        formatted_response = re.sub(r"(<li>.*?</li>)", r"<ul>\1</ul>", formatted_response)

        return formatted_response


