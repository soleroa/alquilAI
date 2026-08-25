# alquilAI

A Retrieval-Augmented Generation (RAG) system that answers questions about Argentina's rental law (**Ley 27.551 de Alquileres**) using only the text of the law itself.

The law is split into per-article chunks, embedded, and stored in a local vector database. When a user asks a question, the most relevant articles are retrieved and passed as context to an LLM, which answers grounded strictly in that context. A Next.js UI and a NestJS backend sit on top of the Python RAG pipeline.

## How it works

1. **Ingestion** — the raw law text (`data/raw/ley_27551.txt`) is split into chunks, one per article.
2. **Indexing** — each chunk is embedded with a sentence-transformer model and stored in a persistent [ChromaDB](https://www.trychroma.com/) collection.
3. **Retrieval** — a user question is embedded and matched against the indexed articles to find the most relevant ones.
4. **Generation** — the retrieved articles are inserted into a prompt and sent to an LLM (via [Groq](https://groq.com/)), which answers based only on that context.
5. **Serving** — the pipeline is exposed over HTTP (FastAPI), proxied by a NestJS backend, and consumed by a Next.js frontend.

## Architecture

```
┌──────────────┐   POST /query    ┌───────────────┐   POST /query    ┌────────────────────┐
│   frontend    │ ───────────────▶ │    backend     │ ───────────────▶ │   RAG API (src/api) │
│  Next.js :3000 │                 │  NestJS :3001   │                 │  FastAPI  :8000       │
└──────────────┘ ◀─────────────── └───────────────┘ ◀─────────────── └────────────────────┘
                                                                          │
                                                                          ▼
                                                              ChromaDB (data/processed/chroma_db)
                                                              + Groq LLM API
```

- **`frontend/`** (Next.js): the UI — a form to ask a question, shows the answer and the retrieved source articles.
- **`backend/`** (NestJS): thin HTTP proxy between the frontend and the Python RAG API (`QueryModule`).
- **`src/api/`** (FastAPI): wraps the Python RAG pipeline (`generate_answer`) as a `POST /query` endpoint.
- **`src/`** (ingestion/retrieval/generation): the RAG pipeline itself — chunking, embeddings, ChromaDB, and the Groq prompt/call.

## Project structure

```
src/
  ingestion/
    chunking.py     # Splits the law text into per-article chunks
  retrieval/
    indexer.py       # Embeds chunks and builds/persists the Chroma index
    query.py          # Embeds a question and queries the index
  generation/
    generate.py       # Builds the prompt and calls the LLM to produce an answer
  api/
    main.py            # FastAPI app exposing the pipeline as POST /query
data/
  raw/                 # Source law text
  processed/           # Persisted Chroma vector database
backend/                # NestJS API (proxies to src/api)
frontend/               # Next.js UI
```

## Setup

### 1. Python pipeline + RAG API

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your Groq API key:

   ```
   GROQ_API_KEY=your_key_here
   ```

3. Build the vector index from the law text (only needed once, or whenever the source text changes):

   ```bash
   python -m src.retrieval.indexer
   ```

### 2. Backend (NestJS)

```bash
cd backend
npm install
```

Configuration lives in `backend/.env` (already set up to point at the local RAG API):

```
RAG_API_URL=http://localhost:8000
PORT=3001
```

### 3. Frontend (Next.js)

```bash
cd frontend
npm install
```

Configuration lives in `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## Running everything

Three processes, each in its own terminal:

```bash
# 1. RAG API (Python/FastAPI)
source venv/bin/activate
uvicorn src.api.main:app --port 8000

# 2. Backend (NestJS)
cd backend
npm run start:dev

# 3. Frontend (Next.js)
cd frontend
npm run dev
```

Then open **http://localhost:3000**.

## Usage without the web stack

The Python pipeline can also be used directly from the CLI, without starting any server:

Query the index directly (prints the top matching articles):

```bash
python -m src.retrieval.query
```

Ask a question and get an LLM-generated answer grounded in the retrieved articles:

```bash
python -m src.generation.generate
```

## Tech stack

**RAG pipeline (Python)**
- [ChromaDB](https://www.trychroma.com/) — vector database
- [sentence-transformers](https://www.sbert.net/) (`intfloat/multilingual-e5-small`) — text embeddings
- [Groq](https://groq.com/) — LLM inference (`openai/gpt-oss-20b`)
- [FastAPI](https://fastapi.tiangolo.com/) — exposes the pipeline over HTTP

**Backend**
- [NestJS](https://nestjs.com/) — proxies requests from the frontend to the RAG API

**Frontend**
- [Next.js](https://nextjs.org/) (App Router) + [Tailwind CSS](https://tailwindcss.com/)
