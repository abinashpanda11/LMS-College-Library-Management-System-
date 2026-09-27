import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')

print(f"CONNECTING TO: {uri.split('@')[-1]}")
conn = psycopg2.connect(uri)
cur = conn.cursor()

try:
    print("Attempting INSERT...")
    cur.execute("""
        INSERT INTO "user" (
            username, email, password_hash, role, full_name, dob, 
            registration_number, section, semester, mobile_number, photo_filename
        ) VALUES (
            'section_user', 'test2j3@library.com', 'hashed_pw', 'student', 'Test User 2J3', '2005-05-20',
            'REG2J3', '2J3', 4, '9876543210', 'profile.png'
        )
    """)
    conn.commit()
    print("INSERT SUCCESS!")
except Exception as e:
    print(f"INSERT FAILED: {e}")

cur.close()
conn.close()
