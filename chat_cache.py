import mysql.connector

class ChatCache:
    def __init__(self, host="localhost", user="root", password="Nihar", database="education_chatbot"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.create_cache_table()

    def get_connection(self):
        """Establish MySQL connection"""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_cache_table(self):
        """Create chat cache table if it doesn't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_cache (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                user_query TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def get_cached_response(self, user_id, user_prompt):
        """Retrieve cached response if available"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT bot_response FROM chat_cache WHERE user_id = %s AND user_query = %s", (user_id, user_prompt))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"❌ Error retrieving cached response: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def save_response(self, user_id, user_prompt, bot_response):
        """Save bot response to cache"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO chat_cache (user_id, user_query, bot_response) VALUES (%s, %s, %s)", (user_id, user_prompt, bot_response))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"❌ Error saving response: {e}")
        finally:
            cursor.close()
            conn.close()
