import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')
conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute('SELECT username, section, registration_number FROM "user"')
rows = cur.fetchall()
print(f"USERS FOUND: {rows}")
cur.close()
conn.close()
