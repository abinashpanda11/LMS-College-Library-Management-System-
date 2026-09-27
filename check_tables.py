import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print(f"CONNECTING TO: {uri.split('@')[-1]}")

conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
tables = cur.fetchall()
print(f"TABLES FOUND: {tables}")
cur.close()
conn.close()
