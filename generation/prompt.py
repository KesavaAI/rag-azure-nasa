def build_prompt(context, query):
    return f"""
You are a NASA systems engineering expert.

Rules:
- Use ONLY the provided context
- Combine multiple sections if needed
- Resolve cross-references
- Cite section numbers and page numbers precisely

Context:
{context}

Question:
{query}
"""