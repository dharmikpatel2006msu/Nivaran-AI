const { Pool } = require('pg');
const { GoogleGenAI } = require('@google/genai');
const Groq = require('groq-sdk');
require('dotenv').config();

const pool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: { rejectUnauthorized: false } });
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

(async () => {
  try {
    console.log('1. Generating embedding...');
    const embResponse = await ai.models.embedContent({
      model: 'gemini-embedding-001',
      contents: 'What are your store hours?',
      config: { outputDimensionality: 768 }
    });
    const embedding = embResponse.embeddings ? embResponse.embeddings[0].values : embResponse.embedding.values;
    const embeddingString = JSON.stringify(embedding);

    console.log('2. Querying Postgres...');
    const { rows: documents } = await pool.query(
      `SELECT id, content, metadata, 1 - (embedding <=> $1::vector) AS similarity
       FROM documentation
       WHERE 1 - (embedding <=> $1::vector) >= $2
       ORDER BY similarity DESC
       LIMIT $3`,
      [embeddingString, 0.5, 3]
    );
    console.log(`Found ${documents.length} document(s).`);

    const contextText = documents.map(d => d.content).join('\n');

    console.log('3. Generating Groq completion...');
    const completion = await groq.chat.completions.create({
      messages: [
        { role: 'system', content: "You are a helpful customer support assistant. Answer the user's question using ONLY the provided context." },
        { role: 'user', content: `Context:\n${contextText}\n\nQuestion: What are your store hours?` }
      ],
      model: 'qwen/qwen3.6-27b',
      max_tokens: 300
    });

    let text = completion.choices[0]?.message?.content || '';
    text = text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
    console.log('SUCCESS! Response:', text);
  } catch (err) {
    console.error('Pipeline Error:', err);
  } finally {
    pool.end();
  }
})();
