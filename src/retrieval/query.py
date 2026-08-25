import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval.indexer import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL


def query_index(pregunta: str, n_results: int = 5):
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding = model.encode([f"query: {pregunta}"], normalize_embeddings=True)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(query_embeddings=query_embedding, n_results=n_results)

    for i, (doc, dist) in enumerate(zip(results["documents"][0], results["distances"][0])):
        print(f"--- resultado {i + 1} (distancia={dist:.4f}) ---")
        print(doc)
        print()

    return results


if __name__ == "__main__":
    pregunta = "¿cuánto puede pedir de depósito el dueño del departamento?"
    query_index(pregunta)
