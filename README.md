# alquilAI

A Retrieval-Augmented Generation (RAG) system that answers questions about Argentina's rental law (**Ley 27.551 de Alquileres**) using only the text of the law itself.

The law is split into per-article chunks, embedded, and stored in a local vector database. When a user asks a question, the most relevant articles are retrieved and passed as context to an LLM, which answers grounded strictly in that context.

## How it works

1. **Ingestion** — the raw law text (`data/raw/ley_27551.txt`) is split into chunks, one per article.
2. **Indexing** — each chunk is embedded with a sentence-transformer model and stored in a persistent [ChromaDB](https://www.trychroma.com/) collection.
3. **Retrieval** — a user question is embedded and matched against the indexed articles to find the most relevant ones.
4. **Generation** — the retrieved articles are inserted into a prompt and sent to an LLM (via [Groq](https://groq.com/)), which answers based only on that context.

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
data/
  raw/                 # Source law text
  processed/           # Persisted Chroma vector database
```

## Setup

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

## Usage

Build the vector index from the law text:

```bash
python -m src.retrieval.indexer
```

Query the index directly:

```bash
python -m src.retrieval.query
```

Ask a question and get an LLM-generated answer grounded in the retrieved articles:

```bash
python -m src.generation.generate
```

## Tech stack

- [ChromaDB](https://www.trychroma.com/) — vector database
- [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) — text embeddings
- [Groq](https://groq.com/) — LLM inference (`llama-3.1-8b-instant`)
