from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from config import *
from generation.llm import client

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_KEY)
)

def search_documents(query, top_k=8):
    results = search_client.search(search_text=query, top=top_k)

    docs = []
    for doc in results:
        docs.append({
            "content": doc["content"],
            "section": doc["section"],
            "page": doc["page"],
            "figures": doc.get("figures", []),
            "hierarchy": doc.get("hierarchy", {})
        })

    return docs


def rerank_documents(query, docs, top_k=5):
    scored_docs = []

    for d in docs:
        prompt = f"""
Rate relevance (1-10):

Query: {query}
Document: {d['content'][:500]}

Score only:
"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            score = int(response.choices[0].message.content.strip())
        except:
            score = 5

        scored_docs.append((score, d))

    scored_docs.sort(reverse=True, key=lambda x: x[0])

    return [d for _, d in scored_docs[:top_k]]