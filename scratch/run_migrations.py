import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
import psycopg2
from src.config import DATABASE_URL

print("Connecting to Supabase PostgreSQL...")
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

migrations = [
    ("01_init.sql", """
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE TABLE IF NOT EXISTS documentation (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            metadata JSONB,
            embedding vector(768)
        );
    """),
    ("02_schema_additions.sql", """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            last_active_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved')),
            escalation_reason TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMPTZ DEFAULT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
        CREATE INDEX IF NOT EXISTS idx_chat_history_user_id_created ON chat_history(user_id, created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
    """),
    ("03_rpc_match_documentation.sql", """
        CREATE OR REPLACE FUNCTION match_documentation (
          query_embedding vector(768),
          match_threshold float,
          match_count int
        )
        RETURNS TABLE (
          id bigint,
          content text,
          metadata jsonb,
          similarity float
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
          RETURN QUERY
          SELECT
            documentation.id,
            documentation.content,
            documentation.metadata,
            1 - (documentation.embedding <=> query_embedding) AS similarity
          FROM documentation
          WHERE 1 - (documentation.embedding <=> query_embedding) >= match_threshold
          ORDER BY documentation.embedding <=> query_embedding
          LIMIT match_count;
        END;
        $$;
    """)
]

for name, sql in migrations:
    print(f"Applying migration: {name}...")
    try:
        cur.execute(sql)
        print(f"  [SUCCESS] {name} applied successfully.")
    except Exception as e:
        print(f"  [ERROR] Error applying {name}: {e}")

# Verify tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
tables = [row[0] for row in cur.fetchall()]
print(f"\nExisting public tables in PostgreSQL: {tables}")

# Verify functions
cur.execute("SELECT routine_name FROM information_schema.routines WHERE routine_schema = 'public' AND routine_name = 'match_documentation';")
routines = [row[0] for row in cur.fetchall()]
print(f"Existing match_documentation function: {routines}")

cur.close()
conn.close()
print("\nDatabase migration complete!")
