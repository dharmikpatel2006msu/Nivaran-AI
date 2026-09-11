const { Pool } = require('pg');
const { GoogleGenAI } = require('@google/genai');
require('dotenv').config();

// 1. Connect to Supabase Cloud PostgreSQL database
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

// 2. Initialize Gemini Client
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// 3. Define sample knowledge base documents
const sampleKnowledge = [
    "Our store hours are Monday through Friday, 9:00 AM to 6:00 PM.",
    "Returns and refunds are accepted within 30 days of the original purchase date.",
    "We offer free shipping on all orders over $50.",
    "You can track your order by logging into your account and clicking 'Order History'."
];

async function seedDatabase() {
    console.log('Starting data ingestion...');

    for (const text of sampleKnowledge) {
        try {
            // Generate the vector embedding using Gemini text-embedding-004
            const response = await ai.models.embedContent({
                model: 'gemini-embedding-001',
                contents: text,
                config: { outputDimensionality: 768 },
            });

            // Extract the numeric array and format it for pgvector syntax: "[0.1, 0.2, ...]"
            const vectorArray = response.embeddings ? response.embeddings[0].values : response.embedding.values;
            const vectorString = `[${vectorArray.join(',')}]`;

            // Insert the text and the vector into the local Postgres table
            await pool.query(
                'INSERT INTO documentation (content, metadata, embedding) VALUES ($1, $2, $3)',
                [text, { category: 'faq' }, vectorString]
            );

            console.log(`✅ Seeded: "${text.substring(0, 40)}..."`);
        } catch (error) {
            console.error('Error inserting row:', error);
        }
    }

    console.log('Done! Knowledge base is ready.');
    pool.end();
}

seedDatabase();