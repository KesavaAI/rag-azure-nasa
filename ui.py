import streamlit as st
from retrieval.retriever import search_documents, rerank_documents
from retrieval.query_expander import expand_query
from generation.llm import generate_answer, refine_query

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="NASA QA System",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>

/* Background */
body {
    background-color: #f5f6fa;
}

.main {
    background-color: #f5f6fa;
}

/* Header */
h1 {
    color: #1f2937;
}

/* Input box FIXED */
.stTextInput > div > div > input {
    background-color: #ffffff;
    color: #111827;   /* 🔥 FIX: text visible */
    border: 1px solid #d1d5db;
    border-radius: 10px;
    padding: 10px;
}

/* Button */
.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 8px 20px;
    border: none;
}

/* Answer card */
.answer-box {
    background-color: #ffffff;
    color: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-top: 20px;
}

/* Source card */
.source-box {
    background-color: #f9fafb;
    color: #111827;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<h1>🚀 NASA Technical Manual QA</h1>
<p style='color: gray;'>Ask questions about the NASA Systems Engineering Handbook</p>
""", unsafe_allow_html=True)

# ------------------ INPUT ------------------
query = st.text_input(
    "🔍 Enter your question",
    placeholder="Ask something like: What is PDR in NASA systems engineering?"
)

# ------------------ MAIN LOGIC ------------------
if st.button("Ask") and query:

    with st.spinner("Thinking..."):

        # Query expansion
        queries = expand_query(query)

        docs_stage1 = []
        for q in queries:
            docs_stage1.extend(search_documents(q))

        context_temp = "\n".join([d["content"] for d in docs_stage1[:5]])

        # Multi-hop refinement
        refined_queries = refine_query(query, context_temp)

        docs_stage2 = []
        for rq in refined_queries:
            docs_stage2.extend(search_documents(rq))

        # Combine + deduplicate
        docs = docs_stage1 + docs_stage2
        unique_docs = {d["content"]: d for d in docs}.values()

        # Rerank
        docs = rerank_documents(query, list(unique_docs))

        # Limit context
        docs = docs[:6]

        # Build context
        context = ""
        sources = []

        for d in docs:
            context += f"""
[{d['section']} | Page {d['page']}]

{d['content']}
"""
            sources.append(f"{d['section']} (Page {d['page']})")

        # Generate answer
        answer = generate_answer(context, query)

    # ------------------ ANSWER ------------------
    st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
    st.markdown("### 💡 Answer")
    st.write(answer)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ SOURCES ------------------
    st.markdown("<div class='source-box'>", unsafe_allow_html=True)
    st.markdown("### 📚 Sources")
    for s in set(sources):
        st.write("•", s)
    st.markdown("</div>", unsafe_allow_html=True)

