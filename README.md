# Nivaran AI — Monorepo Architecture

Nivaran AI is an AI-driven, Retrieval-Augmented Generation (RAG) Customer Support Agent for E-commerce & Retail applications. 

This repository is organized as a monorepo supporting a 5-person engineering team.

---

## 👥 Team & Workstream Structure

| Component | Responsibility | Technical Stack | Documentation |
| :--- | :--- | :--- | :--- |
| **Backend Team (2)** | Python API, RAG Pipeline, Vector DB, Telegram Bot, In-house Ticketing | Python 3.10+, FastAPI, Supabase pgvector, Google Gemini, Groq | [backend/README.md](backend/README.md) |
| **Frontend Team (2)** | Admin Dashboard UI for Support Staff | React / Next.js / Vue (Independent Scaffold) | `frontend/` directory |
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

## 🚀 Quick Start for Developers

- **Backend Developers:** Follow the setup guide in [backend/README.md](backend/README.md).
- **Frontend Developers:** Build your admin panel inside `frontend/`. The backend exposes REST endpoints at `http://localhost:8000/api/admin`. Interactive API documentation is available at `http://localhost:8000/docs`.
- **Knowledge Base Author:** Place formatted markdown files into `backend/knowledge/`.
