import mysql.connector

class BotDatabase:
    def __init__(self, host="localhost", user="root", password="Nihar", database="education_chatbot"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.create_database()
        self.create_bot_table()

    def get_connection(self):
        """Establish MySQL connection"""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_database(self):
        """Create database if it does not exist"""
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.close()
        conn.close()

    def create_bot_table(self):
        """Create bot responses table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bot_responses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)
        conn.commit()
        cursor.close()  # ✅ Close cursor
        conn.close()  # ✅ Close connection
