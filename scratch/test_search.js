const { Pool } = require('pg');
const { GoogleGenAI } = require('@google/genai');
require('dotenv').config();

const pool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: { rejectUnauthorized: false } });
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

(async () => {
  const res = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: 'What are your store hours?',
    config: { outputDimensionality: 768 }
  });
  const vec = res.embeddings ? res.embeddings[0].values : res.embedding.values;
  const embeddingString = JSON.stringify(vec);
  const { rows } = await pool.query(
    'SELECT content, 1 - (embedding <=> $1::vector) as sim FROM documentation ORDER BY sim DESC LIMIT 2',
    [embeddingString]
  );
  console.log('Search Results:', rows);
  pool.end();
})();
