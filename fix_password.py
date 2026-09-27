import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')

real_hash = generate_password_hash('password123')
print(f"Generated Hash: {real_hash}")

conn = psycopg2.connect(uri)
cur = conn.cursor()
try:
    cur.execute("UPDATE \"user\" SET password_hash = %s WHERE username = 'section_user'", (real_hash,))
    conn.commit()
    print("Password updated successfully!")
except Exception as e:
    print(f"Update failed: {e}")

cur.close()
conn.close()
