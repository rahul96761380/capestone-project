import json
import os
from pathlib import Path
from pypdf import PdfReader

import chromadb
import litellm
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "openrouter/openai/text-embedding-3-small"
COLLECTION_NAME = "ecombot_kb"

BASE_DIR = Path(__file__).resolve().parents[2]

PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
FAQ_FILE = BASE_DIR / "data" / "faq.json"
PDF_FILE = BASE_DIR / "data" / "ecom_faq.pdf"

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

def load_pdf():
    docs = []

    reader = PdfReader(PDF_FILE)

    for page_num, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        docs.append(
            {
                "id": f"pdf-page-{page_num}",
                "text": text,
                "metadata": {
                    "source_file": "ecom_faq.pdf",
                    "document_title": "E-Commerce Support FAQ",
                    "section": f"Page {page_num}",
                    "page": page_num,
                    "doc_type": "pdf",
                },
            }
        )

    return docs


def build_catalog():

    global collection

    docs = load_documents()
    docs.extend(load_pdf())

    texts = [doc["text"] for doc in docs]
    ids = [doc["id"] for doc in docs]

    metadatas = [
        doc.get(
            "metadata",
            {
                "source_file": "json",
                "document_title": "JSON Knowledge Base",
                "section": "General",
                "page": 0,
                "doc_type": "json",
            },
        )
        for doc in docs
    ]

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embed(texts),
    )

    print(
        f"Successfully indexed {len(docs)} documents into '{COLLECTION_NAME}'"
    )


if __name__ == "__main__":
    build_catalog()