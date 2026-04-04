import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

connection = psycopg2.connect(DATABASE_URL)
