# 🚀 NASA Technical Manual QA System (Advanced RAG + Azure AI)

An advanced **Retrieval-Augmented Generation (RAG)** system designed to answer complex engineering questions from the **NASA Systems Engineering Handbook (SP-2016-6105 Rev2)**.

---

## 🖼️ System Overview

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/ccaeda13-1e64-4006-ae50-d552aa8e1b7b" />


This system transforms a **270-page technical handbook** into an intelligent AI assistant capable of:

- Multi-hop reasoning  
- Cross-chapter understanding  
- Table-aware retrieval  
- Source-grounded answers  

---

## 🧠 Problem Statement: Complex Technical Manual QA

> "I have a 270-page technical handbook with diagrams, tables, and cross-references. I need a chatbot that can answer questions — not just retrieve text."

### Challenges

- Cross-chapter dependencies  
- Multi-page tables  
- Diagram-based knowledge  
- Heavy acronym usage (TRL, PDR, CDR, SRR)  
- Deep hierarchical structure (e.g., 6.3.2.1)  

---

## 🔷 RAG Pipeline Flow

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/05d57625-aa0a-4c6f-8ef0-6cb5eed29df6" />


```
User Query 
   ↓
Query Expansion (Acronyms + LLM refinement)
   ↓
Initial Retrieval (Azure AI Search)
   ↓
Multi-hop Retrieval
   ↓
LLM Reranking
   ↓
Context Aggregation
   ↓
Answer Generation (GPT-4o)
```

---

## ☁️ Azure Cloud Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/baa1551c-f217-410a-91ff-4e51f5395403" />


### Services Used

#### Azure OpenAI
- GPT-4o → reasoning + answer generation  
- Used for multi-hop QA and reranking  

#### Azure OpenAI Embeddings
- Model: `text-embedding-3-large`  
- Used for semantic search  

#### Azure AI Search
- Vector database + keyword search  
- Stores embeddings and metadata  

---

## 🧩 System Components

### 📄 Ingestion Layer
- PDF parsing (`parse_pdf.py`)  
- Section-aware chunking  
- Table extraction  
- Hierarchical structure detection  

### 🧠 Indexing Layer
- Embedding generation (`embedder.py`)  
- Azure AI Search indexing (`indexer.py`)  

### 🔍 Retrieval Layer
- Query expansion (`query_expander.py`)  
- Multi-stage retrieval  
- LLM reranking (`retriever.py`)  

### 🤖 Generation Layer
- Prompt engineering (`prompt.py`)  
- Answer generation (`llm.py`)  

### 💬 UI Layer
<img width="613" height="713" alt="Screenshot 2026-03-29 082622" src="https://github.com/user-attachments/assets/2f084a37-42d6-4dfe-a084-b006b34452e3" />



- Built using Streamlit  
- Chat-based interface  
- Displays answers with sources  

---

## 🔥 Key Features

- ✔ Multi-hop reasoning  
- ✔ Cross-chapter QA  
- ✔ Table-aware parsing  
- ✔ Hierarchical chunking  
- ✔ Acronym expansion  
- ✔ LLM reranking  
- ✔ Source citations  

---

## 📊 Example Queries

- How does verification relate to system design?  
- What are the entry criteria for PDR?  
- Explain TRL levels  
- How does risk management affect reviews?  

---

## 📚 Data Source

- NASA Systems Engineering Handbook  
- https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf  
- Public domain  

---

## ⚙️ Setup

```bash
git clone https://github.com/KesavaAI/rag-azure-nasa.git
cd rag-azure-nasa
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_DEPLOYMENT=gpt-4o

AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large

SEARCH_ENDPOINT=your_search_endpoint
SEARCH_KEY=your_search_key
INDEX_NAME=nasa-index
```

⚠️ Do NOT commit `.env`

---

## ▶️ Run the App

```bash
python ingestion/parse_pdf.py
python -m indexing.indexer
streamlit run ui.py
```

---

## 📈 Capabilities

| Feature                     | Status |
|---------------------------|--------|
| Multi-hop QA              | ✅     |
| Cross-chapter reasoning   | ✅     |
| Table understanding       | ✅     |
| Diagram awareness         | ✅     |
| Reranking                 | ✅     |

---

## 🏆 Final Result

Transforms a **complex NASA handbook** into an AI assistant capable of:

- Deep reasoning  
- Context-aware answers  
- Structured explanations  

---

## 👨‍💻 Author

**Kesav**  
AI/ML Engineer | RAG Systems | Azure AI  

---

## ⭐ If you like this project

Give it a star ⭐
