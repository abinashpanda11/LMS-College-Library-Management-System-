import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')

print(f"CONNECTING TO: {uri.split('@')[-1]}")
conn = psycopg2.connect(uri)
cur = conn.cursor()

try:
    print("Altering password_hash column length...")
    cur.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(500);')
    conn.commit()
    print("SUCCESS: Column altered.")
except Exception as e:
    print(f"FAILURE: {e}")

cur.close()
conn.close()
