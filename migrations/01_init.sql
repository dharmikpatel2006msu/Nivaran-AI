-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documentation table
CREATE TABLE IF NOT EXISTS documentation (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(768)
);
