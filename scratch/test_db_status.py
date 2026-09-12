import psycopg2
from src.config import DATABASE_URL

print("Connecting to Supabase PostgreSQL...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    print("Tables:", cur.fetchall())
    cur.execute("SELECT routine_name FROM information_schema.routines WHERE routine_schema = 'public';")
    print("Functions:", cur.fetchall())
    conn.close()
except Exception as e:
    print("Error:", e)
