-- Migration 03: Create RPC function for pgvector similarity search in documentation table

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
