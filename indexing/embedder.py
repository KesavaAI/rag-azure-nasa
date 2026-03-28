from openai import AzureOpenAI
from config import *

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-01"
)

def get_embedding(text):
    text = text[:6000]

    response = client.embeddings.create(
        model=AZURE_EMBEDDING_DEPLOYMENT,
        input=text
    )

    return response.data[0].embedding