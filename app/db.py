import psycopg2.pool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create a shared pool (min 1, max 3 connections)
_pool = psycopg2.pool.ThreadedConnectionPool(1, 3, DATABASE_URL, sslmode="require")

def get_conn():
    return _pool.getconn()

def release_conn(conn):
    _pool.putconn(conn)
