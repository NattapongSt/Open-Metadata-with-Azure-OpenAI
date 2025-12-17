import os
from dotenv import load_dotenv
import pyodbc
import json
import logging
from typing import Optional, Dict, List

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="./logs/conv_logs.log",
    filemode='a',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class HistoryConversationDB:
    def __init__(self):
        """Initialize database connection parameters"""
        self.conversations = []
        self.server = os.getenv("DATABASE_HOST")
        self.database = os.getenv("DATABASE_NAME")
        self.username = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.table_name = os.getenv("DATABASE_HISTORY_TABLE")
        
        if not all([self.server, self.database, self.username, self.password, self.table_name]):
            logger.error("Missing database configuration in .env file.")
            raise ValueError("Database configuration is incomplete.")

        self.conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};"
            f"TrustServerCertificate=yes;Connection Timeout=10;Encrypt=no;"
        )
        self.conn = None
        self.cursor = None
        
    def __enter__(self):
        """Connect to the database when entering the context."""
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            logger.info("Database connection established.")
            return self
        except pyodbc.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection when exiting the context."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed.\n")
            

    def fetch_conversations(self, session_id: str) -> Optional[Dict[str, List[Dict[str, str]]]]:
        """Fetch conversation history from the database based on session_id"""
        
        if not self.cursor:
            logger.error("Database cursor is not available.")
            return None
        
        try:
            query = f"SELECT question, answer FROM {self.table_name} WHERE sessionid = ?"
            self.cursor.execute(query, session_id)
            
            rows = self.cursor.fetchall()
            history = []
            for row in rows:
                history.append({"type": "human", "content": row.question})
                history.append({"type": "ai", "content": row.answer})
            
            logger.info(f"Fetched {len(rows)} conversation pairs for sessionid: {session_id}")
            return {"history": history}
        
        except pyodbc.Error as e:
            logger.error(f"Error fetching conversations for sessionid: {session_id}: {e}")
            return None
        
    def create_conversation(self, 
                            session_id: str, 
                            question: str, 
                            answer: str) -> bool:
        """Insert a new conversation record into the database"""
        if not self.conn or not self.cursor:
            logger.error("Database connection is not active.")
            return False

        try:
            query = f"INSERT INTO {self.table_name} (sessionid, question, answer, crateDate) VALUES (?, ?, ?, GETDATE())"
            self.cursor.execute(query, (session_id, question, answer))
            self.conn.commit()
            logger.info(f"Conversation saved for sessionid: {session_id}")
            return True
            
        except pyodbc.Error as e:
            logger.error(f"Error inserting conversation: {e}")
            # Optional: Rollback หากเกิด error ระหว่าง transaction
            try:
                self.conn.rollback()
            except:
                pass
            return False
        
if __name__ =="__main__":
    try:
        with HistoryConversationDB() as db:
            result = db.fetch_conversations("NULLtest-guid-1234")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # insert_status = db.create_conversation("NULLtest-guid-1234", "Hello, how are you?", "I'm fine, thank you!")
            # print(f"Insert status: {insert_status}")
            
    except Exception as e:
        print(f"Application Error: {e}")