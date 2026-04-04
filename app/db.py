import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DB URL:", DATABASE_URL)  # ← add this temporarily

def get_conn():
    return psycopg.connect(DATABASE_URL)
