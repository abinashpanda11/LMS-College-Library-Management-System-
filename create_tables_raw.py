import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('SQLALCHEMY_DATABASE_URI')
print(f"CONNECTING TO: {uri.split('@')[-1]}")

conn = psycopg2.connect(uri)
cur = conn.cursor()

# User Table
cur.execute("""
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    full_name VARCHAR(100),
    dob DATE,
    registration_number VARCHAR(20) UNIQUE,
    section VARCHAR(10),
    semester INTEGER,
    photo_filename VARCHAR(100),
    is_blocked BOOLEAN DEFAULT FALSE,
    mobile_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Book Table
cur.execute("""
CREATE TABLE IF NOT EXISTS book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    available INTEGER NOT NULL DEFAULT 1,
    cover_image VARCHAR(100)
);
""")

# Transaction Table
cur.execute("""
CREATE TABLE IF NOT EXISTS transaction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    book_id INTEGER NOT NULL REFERENCES book(id),
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'issued',
    penalty FLOAT DEFAULT 0.0
);
""")

conn.commit()
print("TABLES CREATED SUCCESSFULLY (Raw SQL).")
cur.close()
conn.close()
