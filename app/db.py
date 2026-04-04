import psycopg
import os
from dotenv import load_dotenv

load_dotenv()



def get_conn():
    return psycopg.connect("postgresql://postgres:ETXIm8Oq5TQ9jIbp@db.iqermjanhbuaocgyiamn.supabase.co:5432/postgres?sslmode=require")
