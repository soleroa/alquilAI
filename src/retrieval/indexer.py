import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = "data/processed/chroma_db"
COLLECTION_NAME = "ley_27551"


def build_index(chunks: list[str]):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

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
