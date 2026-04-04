import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    """
    This is the function app/main.py is looking for.
    It creates and returns a connection to your Supabase DB.
    """
    # Note: Using the connection string directly from Render environment
    return psycopg2.connect(DATABASE_URL)
