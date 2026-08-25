import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = "data/processed/chroma_db"
COLLECTION_NAME = "ley_27551"
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"


def build_index(chunks: list[str]):
    model = SentenceTransformer(EMBEDDING_MODEL)
    passages = [f"passage: {chunk}" for chunk in chunks]
    embeddings = model.encode(passages, normalize_embeddings=True)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(name=COLLECTION_NAME)
    collection = client.create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"art_{i}" for i in range(len(chunks))],
    )

    return collection


if __name__ == "__main__":
    from src.ingestion.chunking import chunk_by_article

    with open("data/raw/ley_27551.txt", encoding="utf-8") as f:
        texto = f.read()

    chunks = chunk_by_article(texto)
    collection = build_index(chunks)
    print(f"Colección '{collection.name}' creada con {collection.count()} chunks.")
