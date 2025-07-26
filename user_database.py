import mysql.connector

class UserDatabase:
    def __init__(self, host="localhost", user="root", password="Nihar", database="education_chatbot"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.create_database()
        self.create_user_table()

    def get_connection(self):
        """Establish MySQL connection"""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_database(self):
        """Create database if not exists"""
        conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.close()
        conn.close()

    def create_user_table(self):
        """Create users table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def add_user(self, username, password):
        """Add a new user with plain text password (⚠️ Not recommended)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))  # ✅ Store password directly
            conn.commit()
            return "User registered successfully!"
        except mysql.connector.IntegrityError:
            return "❌ Username already exists."
        finally:
            cursor.close()
            conn.close()

    def validate_user(self, username, password):
        """Validate user credentials and return user_id if valid"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            user_id, stored_password = result
            if password == stored_password:  # ✅ Direct password comparison
                return user_id  # ✅ Return user ID
        return None  # ❌ Invalid credentials
