# Nivaran AI — Python FastAPI Backend

This directory contains the Python FastAPI backend service for **Nivaran AI**, an AI-driven customer support bot for E-commerce & Retail.

---

## 🏗️ Backend Architecture

- **Framework:** FastAPI & Uvicorn
- **AI Models:** 
  - Vector Embeddings: Google Gemini (`gemini-embedding-001`, 768 dimensions)
  - LLM Text Generation: Groq SDK (`qwen/qwen3.6-27b`)
- **Database & Vector Search:** Supabase Cloud PostgreSQL with `pgvector` extension
- **Channels & Integrations:**
  - Telegram Bot API (`python-telegram-bot` long polling)
  - REST Admin Panel endpoints for escalation ticket management & chat logs

---

## 📁 Directory Structure

```text
backend/
├── knowledge/               # Drop Markdown Knowledge Base files here
├── migrations/
│   ├── 01_init.sql          # pgvector extension & documentation table
│   └── 02_schema_additions.sql # users, chat_history, & tickets tables
├── src/
│   ├── main.py              # FastAPI app & Telegram bot runner entrypoint
│   ├── config.py            # Global settings & threshold constants
│   ├── system_prompt.py     # System prompt template & red-flag criteria
│   ├── rag/
│   │   ├── retriever.py     # Gemini embeddings & Supabase pgvector search
│   │   └── generator.py     # Groq LLM completion generator
│   ├── db/
│   │   ├── supabase_client.py # Supabase client wrapper
│   │   └── models.py        # Pydantic schemas (User, Ticket, ChatMessage)
│   ├── services/
│   │   ├── chat_service.py  # End-to-end pipeline orchestrator
│   │   └── escalation_service.py # In-house ticketing logic
│   ├── integrations/
│   │   └── telegram_client.py # Telegram bot handler
│   └── api/
│       └── admin_routes.py  # Admin REST API endpoints
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

Activate virtual environment:
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` inside the `backend/` directory:
```bash
cp .env.example .env
```
Fill in your API keys:
- `GEMINI_API_KEY`: Google AI Studio Key
- `GROQ_API_KEY`: Groq Cloud Key
- `TELEGRAM_BOT_TOKEN`: Token from Telegram `@BotFather`
- `SUPABASE_URL` & `SUPABASE_KEY` & `DATABASE_URL`: Supabase Project credentials

### 4. Database Setup (Migrations)
Execute the SQL files in `backend/migrations/` in your Supabase SQL Editor:
1. `01_init.sql` — Enables `pgvector` and creates `documentation` table.
2. `02_schema_additions.sql` — Creates `users`, `chat_history`, and `tickets` tables.

---

## 🚀 Running the Server

Start the FastAPI application with auto-reload:
```bash
python src/main.py
```
Or using Uvicorn directly:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 API Documentation & Admin Endpoints

Interactive Swagger UI documentation is available at:
`http://localhost:8000/docs`

Key Admin REST Routes:
- `GET /api/admin/tickets` — List support tickets (filter by status `open`, `in_progress`, `resolved`)
- `PATCH /api/admin/tickets/{id}/status` — Update ticket status manually
- `GET /api/admin/users/{id}/history` — Inspect user chat history log
- `GET /api/admin/stats` — Dashboard aggregate metrics
