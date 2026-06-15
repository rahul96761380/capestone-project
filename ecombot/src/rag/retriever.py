from chromadb import PersistentClient
from ecombot.src.rag.embed_catalog import embed

client = PersistentClient(path="./chroma_db")

collection = client.get_collection("ecombot_kb")


def retrieve(query: str, n_results: int = 3):

    if not query.strip():
        return []

    try:
        results = collection.query(
            query_embeddings=embed([query]),
            n_results=n_results,
        )

        return results["documents"][0]

    except Exception:
        return []