import psycopg2

# Neon URI (Billowing Dew)
URI = "postgresql://neondb_owner:npg_eUXW9pihjD6H@ep-billowing-dew-ah1d3t7z-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

print(f"CONNECTING TO: {URI.split('@')[-1]}")
conn = psycopg2.connect(URI)
cur = conn.cursor()

try:
    print("Dropping tables...")
    # Order matters due to foreign keys
    cur.execute('DROP TABLE IF EXISTS "transaction" CASCADE;')
    cur.execute('DROP TABLE IF EXISTS "book" CASCADE;')
    cur.execute('DROP TABLE IF EXISTS "user" CASCADE;')
    cur.execute('DROP TABLE IF EXISTS "alembic_version" CASCADE;')
    conn.commit()
    print("SUCCESS: Cloud database is empty.")
except Exception as e:
    print(f"FAILURE: {e}")

cur.close()
conn.close()
