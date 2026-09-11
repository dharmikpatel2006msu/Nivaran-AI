require('dotenv').config();
const { Pool } = require('pg');
const { GoogleGenAI } = require('@google/genai');
const Groq = require('groq-sdk');
const { Bot } = require('node-telegram-bot-api');
const axios = require('axios');

// Initialize API Clients and DB Pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

// Check Telegram Token
const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
if (!telegramToken) {
  console.warn('\n⚠️ TELEGRAM_BOT_TOKEN is missing in .env!');
  console.warn('👉 Please add your bot token to .env: TELEGRAM_BOT_TOKEN=your_token_here\n');
}

const bot = telegramToken ? new Bot(telegramToken) : null;

// Helper Function: Create Trello Ticket when Knowledge Base misses
async function createTrelloTicket(userMessage, userSender) {
  try {
    console.log('📋 Escalating to Trello...');
    const listsResponse = await axios.get(
      `https://api.trello.com/1/boards/${process.env.TRELLO_BOARD_ID}/lists?key=${process.env.TRELLO_API_KEY}&token=${process.env.TRELLO_TOKEN}`
    );
    const incomingListId = listsResponse.data[0].id;

    await axios.post(
      `https://api.trello.com/1/cards?key=${process.env.TRELLO_API_KEY}&token=${process.env.TRELLO_TOKEN}`,
      {
        idList: incomingListId,
        name: `Support Request: ${userSender}`,
        desc: `Unresolved User Query:\n${userMessage}`
      }
    );
    console.log('✅ Trello ticket created successfully.');
  } catch (error) {
    console.error('❌ Trello Escalation Error:', error.response ? error.response.data : error.message);
  }
}

if (bot) {
  // Welcome command handler (/start)
  bot.command('start', (ctx) => {
    ctx.reply(
      "👋 Hello! I am Nivaran AI Support Assistant.\n\nAsk me any question about our services, store hours, returns, or order tracking!"
    );
  });

  // Main message handler
  bot.on('message', async (ctx) => {
    const incomingMsg = ctx.message.text;

    // Ignore commands starting with /
    if (!incomingMsg || incomingMsg.startsWith('/')) return;

    const userSender = ctx.from.username ? `@${ctx.from.username}` : `${ctx.from.first_name || 'User'} (${ctx.from.id})`;
    console.log(`\n📩 Incoming Telegram message from ${userSender}: "${incomingMsg}"`);

    try {
      // Step 1: Convert incoming user message to Vector Embedding using Gemini
      console.log('🔍 Generating vector embedding with Gemini (gemini-embedding-001)...');
      const embeddingResponse = await ai.models.embedContent({
        model: 'gemini-embedding-001',
        contents: incomingMsg,
        config: { outputDimensionality: 768 },
      });
      const embedding = embeddingResponse.embedding ? embeddingResponse.embedding.values : (embeddingResponse.embeddings ? embeddingResponse.embeddings[0].values : null);

      // Step 2: Query local PostgreSQL pgvector table using cosine similarity
      console.log('📊 Querying PostgreSQL pgvector database...');
      const embeddingString = JSON.stringify(embedding);
      const query = `
        SELECT id, content, metadata, 1 - (embedding <=> $1::vector) AS similarity
        FROM documentation
        WHERE 1 - (embedding <=> $1::vector) >= $2
        ORDER BY similarity DESC
        LIMIT $3
      `;
      const { rows: documents } = await pool.query(query, [embeddingString, 0.5, 3]);
      console.log(`📚 Found ${documents.length} matching document(s).`);

      let contextText = '';
      if (documents && documents.length > 0) {
        contextText = documents.map(doc => doc.content).join('\n');
      }

      let replyText = '';

      // Step 3: Branch Decision — Found Knowledge vs. Escalate to Trello
      if (contextText) {
        console.log('🤖 Generating completion with Groq (qwen/qwen3.6-27b)...');
        const completion = await groq.chat.completions.create({
          messages: [
            {
              role: 'system',
              content: "You are a helpful customer support assistant. Answer the user's question using ONLY the provided context.",
            },
            {
              role: 'user',
              content: `Context:\n${contextText}\n\nQuestion: ${incomingMsg}`,
            },
          ],
          model: 'qwen/qwen3.6-27b',
          max_tokens: 300,
        });
        let text = completion.choices[0]?.message?.content || '';
        text = text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
        replyText = text;
        console.log(`💡 Generated response: "${replyText}"`);
      } else {
        console.log('❓ No matching knowledge found. Escalating to human support...');
        await createTrelloTicket(incomingMsg, userSender);
        replyText = "Thank you for contacting support. Your query has been logged with our team on Trello, and an agent will assist you shortly.";
      }

      // Step 4: Send response back to Telegram Chat
      console.log(`📤 Sending Telegram reply to ${userSender}...`);
      await ctx.reply(replyText);
      console.log('✅ Telegram reply sent successfully.');
    } catch (err) {
      console.error('❌ Error processing message:', err);
      await ctx.reply("An error occurred while processing your request. Please try again.");
    }
  });

  // Start Telegram bot polling
  bot.startPolling();
  console.log('🚀 Nivaran AI Telegram Bot started and listening for messages!');
}