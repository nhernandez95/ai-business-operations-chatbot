import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Business Operations Chatbot", layout="wide")
st.title("AI Business Operations Chatbot")
st.caption("Ask questions against internal SOPs, policies, and operational documentation.")

with open("data/company_sop.txt", "r") as f:
    document = f.read()

sections = [s.strip() for s in document.split("\n\n") if s.strip()]

st.subheader("Knowledge Base")
with st.expander("View sample SOP knowledge base"):
    st.write(document)

question = st.text_input("Ask a business operations question", "What checks are required before releasing a data pipeline?")

if question:
    corpus = sections + [question]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    similarities = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    best_idx = similarities.argmax()
    best_section = sections[best_idx]
    confidence = similarities[best_idx]

    st.subheader("Retrieved Source Context")
    st.info(best_section)

    st.subheader("AI-Style Answer")
    st.write(f"""
    Based on the internal documentation, the process requires the team to follow the guidance below:

    **{best_section}**

    **Operational recommendation:** Convert this policy into a checklist, automate validation where possible, and log evidence before approval or production release.
    """)

    st.caption(f"Retrieval confidence score: {confidence:.2f}")

st.subheader("Portfolio Upgrade Ideas")
st.write("""
- Add OpenAI or Azure OpenAI for natural language responses.
- Add ChromaDB or Pinecone for vector search.
- Add PDF upload support.
- Add source citations by document and page.
- Add authentication for internal company use.
""")
