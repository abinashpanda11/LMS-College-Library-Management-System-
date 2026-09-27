import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print(f"CONNECTING TO: {uri.split('@')[-1]}")

real_hash = generate_password_hash('password123')

conn = psycopg2.connect(uri)
cur = conn.cursor()
try:
    cur.execute("SELECT password_hash FROM \"user\" WHERE username = 'section_user'")
    row = cur.fetchone()
    print(f"Current Hash: {row[0]}")
    
    cur.execute("UPDATE \"user\" SET password_hash = %s WHERE username = 'section_user'", (real_hash,))
    conn.commit()
    print("UPDATE EXECUTED.")
    
    cur.execute("SELECT password_hash FROM \"user\" WHERE username = 'section_user'")
    row = cur.fetchone()
    print(f"New Hash in DB: {row[0]}")
    
except Exception as e:
    print(f"Update failed: {e}")

cur.close()
conn.close()
