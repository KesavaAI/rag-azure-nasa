from retrieval.retriever import search_documents, rerank_documents
from retrieval.query_expander import expand_query
from generation.llm import generate_answer, refine_query

query = input("Ask a question: ")

queries = expand_query(query)

docs_stage1 = []
for q in queries:
    docs_stage1.extend(search_documents(q))

context_temp = "\n".join([d["content"] for d in docs_stage1[:5]])

refined_queries = refine_query(query, context_temp)

docs_stage2 = []
for rq in refined_queries:
    docs_stage2.extend(search_documents(rq))

docs = docs_stage1 + docs_stage2
unique_docs = {d["content"]: d for d in docs}.values()

docs = rerank_documents(query, list(unique_docs))

context = ""
sources = []

for d in docs:
    context += f"""
[{d['section']} | Page {d['page']}]
Hierarchy: {d.get('hierarchy', {})}
Figures: {d.get('figures', [])}

{d['content']}
"""

    sources.append(f"{d['section']} (Page {d['page']})")

answer = generate_answer(context, query)

print("\n💡 Answer:\n", answer)

print("\n📚 Sources:")
for s in set(sources):
    print("-", s)