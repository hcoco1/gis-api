import psycopg2
from dotenv import load_dotenv
import os
import sys

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables.")
    sys.exit(1)

try:
    connection = psycopg2.connect(DATABASE_URL)
    print("Successfully connected to the database!")
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
