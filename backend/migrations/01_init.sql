-- Migration 01: Initial pgvector extension and documentation knowledge table

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documentation table for RAG embeddings (768-dim Google Gemini embeddings)
CREATE TABLE IF NOT EXISTS documentation (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(768)
);
