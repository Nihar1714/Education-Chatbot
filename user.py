from user_database import UserDatabase

class User:
    def __init__(self, host, user, password, database):
        self.db = UserDatabase(host, user, password, database)

    def signup(self, username, password):
        """Register a new user."""
        return self.db.add_user(username, password)

    def login(self, username, password):
        """Authenticate user and return success message."""
        user_id = self.db.validate_user(username, password)  # ✅ Now returns user_id
        if user_id:
            return "Login successful!"  # ✅ Keep it simple for session storage
        return "❌ Invalid credentials."

