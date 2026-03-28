import re

def extract_references(text):
    return re.findall(r"\d+(\.\d+)+", text)

def chunk_sections(sections):
    chunks = []

    for sec in sections:
        chunks.append({
            "id": sec["section"],
            "content": sec["content"],
            "page": sec["page"],
            "references": extract_references(sec["content"])
        })

    return chunks