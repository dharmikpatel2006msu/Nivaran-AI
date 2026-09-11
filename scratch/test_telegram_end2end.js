const { Pool } = require('pg');
const { GoogleGenAI } = require('@google/genai');
const Groq = require('groq-sdk');
const { Bot } = require('node-telegram-bot-api');
require('dotenv').config();

const pool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: { rejectUnauthorized: false } });
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

const bot = new Bot(process.env.TELEGRAM_BOT_TOKEN);

bot.on('message', async (ctx) => {
  const incomingMsg = ctx.message.text;
  if (!incomingMsg || incomingMsg.startsWith('/')) return;

  console.log(`RECEIVED: "${incomingMsg}"`);
  
  const embeddingResponse = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: incomingMsg,
    config: { outputDimensionality: 768 },
  });
  const embedding = embeddingResponse.embedding ? embeddingResponse.embedding.values : embeddingResponse.embeddings[0].values;
  const embeddingString = JSON.stringify(embedding);

  const { rows: documents } = await pool.query(
    'SELECT content FROM documentation WHERE 1 - (embedding <=> $1::vector) >= 0.5 LIMIT 3',
    [embeddingString]
  );
  console.log(`FOUND ${documents.length} docs`);

  const contextText = documents.map(d => d.content).join('\n');
  const completion = await groq.chat.completions.create({
    messages: [
      { role: 'system', content: 'You are helpful support assistant.' },
      { role: 'user', content: `Context:\n${contextText}\n\nQuestion: ${incomingMsg}` }
    ],
    model: 'qwen/qwen3.6-27b'
  });
  let text = completion.choices[0]?.message?.content || '';
  text = text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
  console.log('AI RESPONSE:', text);
  pool.end();
});

(async () => {
  await bot.handleUpdate({
    update_id: 100,
    message: {
      message_id: 100,
      date: 1000,
      chat: { id: 12345, type: 'private' },
      from: { id: 12345, first_name: 'TestUser', username: 'testuser' },
      text: 'What are your store hours?'
    }
  });
})();
