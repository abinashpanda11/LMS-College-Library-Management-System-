import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print(f"CONNECTING TO: {uri.split('@')[-1]}") # Mask password

try:
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_user;")
    db_name, user = cur.fetchone()
    print(f"SUCCESS! Connected to Database: '{db_name}' as User: '{user}'")
    cur.close()
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
