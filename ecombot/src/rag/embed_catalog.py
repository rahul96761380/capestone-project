import json
import os
from pathlib import Path

import chromadb
import litellm
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "openrouter/openai/text-embedding-3-small"
COLLECTION_NAME = "ecombot_kb"

BASE_DIR = Path(__file__).resolve().parents[2]

PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
FAQ_FILE = BASE_DIR / "data" / "faq.json"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(COLLECTION_NAME)


def embed(texts):
    response = litellm.embedding(
        model=EMBEDDING_MODEL,
        input=texts,
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    return [item["embedding"] for item in response.data]


def load_documents():
    docs = []

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

        for p in products:
            docs.append(
                {
                    "id": p["product_id"],
                    "text": (
                        f"Product: {p['name']}. "
                        f"Price: {p['price']}. "
                        f"Warranty: {p['warranty']}. "
                        f"Shipping: {p['shipping']}."
                    ),
                }
            )

    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        faqs = json.load(f)

        for i, faq in enumerate(faqs):
            docs.append(
                {
                    "id": f"faq-{i}",
                    "text": (
                        f"Question: {faq['question']} "
                        f"Answer: {faq['answer']}"
                    ),
                }
            )

    return docs


def build_catalog():
    docs = load_documents()

    texts = [doc["text"] for doc in docs]
    ids = [doc["id"] for doc in docs]

    try:
        collection.delete(ids=ids)
    except Exception:
        pass

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embed(texts),
    )

    print(f"Successfully indexed {len(docs)} documents into '{COLLECTION_NAME}'")


if __name__ == "__main__":
    build_catalog()