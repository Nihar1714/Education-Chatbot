from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from chatbot import EducationBot
from user import User
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Change this to a secure key

# MySQL Database Credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Nihar"
DB_NAME = "education_chatbot"

# Initialize the bot and user management system
api_key = "gsk_MEoc7rPQ6KhyADQsga1AWGdyb3FYj1JtuGRmbHnpDWuU9wYAqpZ"
bot = EducationBot(api_key, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
user_manager = User(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# @app.route("/")
# def home():
#     session["test"] = "Hello"  # ✅ Test if session works
#     return "Session is set."
@app.route("/")
def home():
    return render_template("signup.html")  # Show signup page by default

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        result = user_manager.signup(username, password)

        if result:  # Successful signup (Assuming `signup()` returns True on success)
            return redirect(url_for("login"))  
        return render_template("signup.html", message="Username already exists!")  
    
    return render_template("signup.html")  

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        login_result = user_manager.login(username, password)  # ✅ Now it validates correctly

        if login_result == "Login successful!":
            user_id = user_manager.db.validate_user(username, password)  # ✅ Get user_id

            if user_id:
                session["user_id"] = user_id  # ✅ Store user_id in session
                session["username"] = username  
                print("✅ Debug: Stored in session:", session)  # 🔍 Debugging
                return redirect(url_for("chat"))  

        return render_template("login.html", message="❌ Invalid username or password!")  

    return render_template("login.html")  # ✅ Ensure GET requests return a valid response

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/chat")
def chat():
    if "username" not in session:  
        return redirect(url_for("login"))  
    return render_template("chat.html")  

@app.route("/ask", methods=["POST"])
def ask():
    print(session)  # Debugging: Check session data
    if "username" not in session:  # Ensure user is logged in
        return jsonify({"response": "❌ Please login first."})

    data = request.get_json()
    user_prompt = data.get("user_prompt")

    # Get response from the bot
    response = bot.get_response(user_prompt)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
