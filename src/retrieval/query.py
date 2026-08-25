import chromadb
from sentence_transformers import SentenceTransformer

from src.retrieval.indexer import CHROMA_DB_PATH, COLLECTION_NAME


def query_index(pregunta: str, n_results: int = 3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([pregunta])

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
