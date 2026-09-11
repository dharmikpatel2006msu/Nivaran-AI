# Nivaran AI — Monorepo Architecture

Nivaran AI is an AI-driven, Retrieval-Augmented Generation (RAG) Customer Support Agent for E-commerce & Retail applications. 

This repository is organized as a monorepo supporting a 5-person engineering team.

---

## 👥 Team & Workstream Structure

| Component | Responsibility | Technical Stack | Documentation |
| :--- | :--- | :--- | :--- |
| **Backend Team (2)** | Python API, RAG Pipeline, Vector DB, Telegram Bot, In-house Ticketing | Python 3.10+, FastAPI, Supabase pgvector, Google Gemini, Groq | [backend/README.md](backend/README.md) |
| **Frontend Team (2)** | Admin Dashboard UI for Support Staff | React / Next.js / Vite | `frontend/` directory |
| **Knowledge Base (1)** | Markdown Knowledge Docs & Heading Metadata | Markdown (`backend/knowledge/`) | `backend/knowledge/` |

---

## 📁 Repository Structure

```text
nivaran_ai/
├── backend/
│   ├── knowledge/           # Markdown KB files land here
│   ├── migrations/          # PostgreSQL & pgvector schema DDL migrations
│   ├── src/                 # Python FastAPI backend core source code
│   │   ├── main.py          # Server & Telegram bot entrypoint
│   │   ├── ingest_knowledge.py # Vector ingestion script for KB markdown files
│   │   ├── system_prompt.py # System prompt template & red-flag rules
│   │   ├── rag/             # Vector retriever & LLM generator
│   │   ├── db/              # Supabase client & Pydantic models
│   │   ├── services/        # Pipeline orchestration & escalation service
│   │   ├── integrations/    # Telegram bot integration
│   │   └── api/             # Admin REST API endpoints
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md            # Backend developer setup guide
├── frontend/                # Frontend team workspace
│   └── .gitkeep
├── .gitignore
└── README.md                # Top-level monorepo documentation
```

---

## 🛠️ Step-by-Step Developer Guides

### 1. How to Run the Backend (Python FastAPI)

#### Step 1: Open Terminal & Navigate to `backend/`
```bash
cd backend
```

#### Step 2: Create & Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

#### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

#### Step 5: Start the Backend Server & Telegram Bot
```bash
python src/main.py
```
*(Or run via Uvicorn directly: `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`)*

- **Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`
- **Health Check Endpoint:** `http://localhost:8000/health`

---

### 2. How to Set Up & Run the Frontend (Admin Panel)

*(The frontend team owns the `frontend/` directory)*

#### Step 1: Navigate to `frontend/` Folder
```bash
cd frontend
```

#### Step 2: Initialize Framework (e.g., Vite + React)
```bash
npx create-vite@latest ./ --template react
```

#### Step 3: Install Dependencies & Run Development Server
```bash
npm install
npm run dev
```
- **Frontend App URL:** `http://localhost:5173`
- **Backend Admin REST Base URL:** `http://localhost:8000/api/admin`

---

### 3. How to Add & Ingest Vector Data (Knowledge Base)

When new Markdown files (e.g., `shipping_delivery.md`, `returns_refunds.md`) are added to `backend/knowledge/`:

#### Step 1: Place Markdown File in `backend/knowledge/`
Example format for `backend/knowledge/shipping_delivery.md`:

```markdown
## Standard Shipping Options
<!-- category: shipping, escalate: false, keywords: delivery time, rates -->
Standard shipping takes 3-5 business days. Free shipping applies to orders over $50.

## Damaged or Stolen Packages
<!-- category: shipping, escalate: true, keywords: damaged, stolen, missing -->
If a package is delivered damaged or stolen, please report it immediately for support escalation.
```

#### Step 2: Run the Ingestion Script
With your backend virtual environment active:

```bash
cd backend
python src/ingest_knowledge.py
```

#### How Vector Ingestion Works:
1. Scans all `.md` files inside `backend/knowledge/`.
2. Splits text into chunks by `##` headings.
3. Extracts metadata tags inside `<!-- category: ..., escalate: true ... -->`.
4. Generates 768-dimensional vector embeddings via Google Gemini (`gemini-embedding-001`).
5. Ingests content, metadata, and vector embeddings directly into the Supabase `documentation` pgvector table.
