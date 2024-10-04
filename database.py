from dotenv import load_dotenv 
import mysql.connector
import os 

# Load environment variables from the .env file (if present)
load_dotenv()

class Database:
  def __init__(self) -> None:
    self.db = mysql.connector.connect(
      user=os.getenv('DB_USER'),
      password=os.getenv('DB_PASSWORD'),
      host='localhost',
      database='orders'
    )
    self.cursor = self.db.cursor()
