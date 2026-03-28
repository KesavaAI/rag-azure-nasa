import json
from indexing.embedder import get_embedding
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from config import *

print("🚀 Starting indexing...")

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY)
)

def index_documents():
    with open("data/processed.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"📄 Loaded {len(data)} documents")

    docs = []

    for i, item in enumerate(data):
        print(f"🔄 Embedding {i+1}/{len(data)}")

        embedding = get_embedding(item["content"])

        docs.append({
            "id": str(i),
            "content": item["content"],
            "embedding": embedding,
            "section": item["section"],
            "page": item["page"],
            "references": []
        })

        # Upload in batches of 10
        if len(docs) >= 10:
            print("⬆️ Uploading batch...")
            search_client.upload_documents(documents=docs)
            docs = []

    if docs:
        print("⬆️ Uploading final batch...")
        search_client.upload_documents(documents=docs)

    print("✅ Indexing complete!")


if __name__ == "__main__":
    index_documents()