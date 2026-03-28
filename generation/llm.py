from openai import AzureOpenAI
from config import *

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-01"
)

def refine_query(query, context):
    prompt = f"""
Generate 2 related queries.

Question: {query}

Context:
{context}
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.split("\n")

def generate_answer(context, query):
    prompt = f"""
You are a NASA systems engineering expert.

Steps:
1. Identify sections
2. Extract key facts
3. Connect them logically

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content