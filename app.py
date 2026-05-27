import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

st.set_page_config(
    page_title="AI Business Operations Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1f4e79;
    }
    .metric-card {
        background-color: #f7f9fc;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e1e5ee;
        text-align: center;
    }
    .risk-low {
        color: green;
        font-weight: bold;
    }
    .risk-medium {
        color: orange;
        font-weight: bold;
    }
    .risk-high {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">AI Business Operations Chatbot</div>', unsafe_allow_html=True)

st.caption(
    "Search internal SOPs, policies, controls, and operational documentation using lightweight AI retrieval."
)

# -----------------------------
# Load SOP Document
# -----------------------------
@st.cache_data
def load_document():
    with open("data/company_sop.txt", "r") as f:
        return f.read()

document = load_document()
sections = [s.strip() for s in document.split("\n\n") if s.strip()]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙️ Assistant Controls")

top_k = st.sidebar.slider(
    "Number of source matches",
    min_value=1,
    max_value=5,
    value=3
)

confidence_threshold = st.sidebar.slider(
    "Confidence warning threshold",
    min_value=0.00,
    max_value=1.00,
    value=0.15,
    step=0.01
)

show_full_kb = st.sidebar.toggle("Show full knowledge base", value=False)

st.sidebar.divider()

st.sidebar.markdown("### Suggested Questions")

suggested_questions = [
    "What checks are required before releasing a data pipeline?",
    "What should happen when a data quality issue is found?",
    "Who approves production deployment?",
    "What documentation is required for operational changes?",
    "How should incidents be escalated?",
    "What controls are required before month-end reporting?",
    "How should failed jobs be handled?",
    "What evidence should be logged for audit purposes?"
]

selected_question = st.sidebar.radio(
    "Pick a sample question",
    suggested_questions
)

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Knowledge Sections", len(sections))

with col2:
    st.metric("Retrieval Engine", "TF-IDF")

with col3:
    st.metric("Use Case", "SOP Q&A")

with col4:
    st.metric("Status", "Prototype")

# -----------------------------
# Knowledge Base Viewer
# -----------------------------
st.divider()
st.subheader("📚 Knowledge Base")

if show_full_kb:
    st.text_area(
        "Loaded SOP Document",
        document,
        height=300
    )
else:
    with st.expander("Preview sample SOP knowledge base"):
        st.write(document[:1500] + "..." if len(document) > 1500 else document)

# -----------------------------
# User Question Input
# -----------------------------
st.divider()
st.subheader("💬 Ask the Operations Assistant")

question = st.text_input(
    "Enter your business operations question",
    selected_question
)

# -----------------------------
# Retrieval Function
# -----------------------------
def retrieve_matches(question, sections, top_k):
    corpus = sections + [question]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(
        matrix[-1],
        matrix[:-1]
    ).flatten()

    ranked_indexes = similarities.argsort()[::-1][:top_k]

    results = []

    for idx in ranked_indexes:
        results.append({
            "section": sections[idx],
            "score": similarities[idx]
        })

    return results

# -----------------------------
# Main Chatbot Output
# -----------------------------
if question:

    results = retrieve_matches(question, sections, top_k)

    best_match = results[0]
    confidence = best_match["score"]

    st.divider()

    st.subheader("🎯 AI-Style Answer")

    if confidence < confidence_threshold:
        st.warning(
            "Low confidence result. The knowledge base may not contain enough information to answer this clearly."
        )

    answer = f"""
Based on the internal documentation, the best available guidance is:

**Source Guidance**

{best_match["section"]}

**Operational Recommendation**

Convert this guidance into a repeatable checklist, assign an accountable owner, automate validation where possible, and log evidence before approval, release, or handoff.

**Suggested Next Step**

Create a control record showing who reviewed the process, what evidence was checked, and whether the activity is ready for production or escalation.
"""

    st.markdown(answer)

    # -----------------------------
    # Confidence / Risk Indicator
    # -----------------------------
    st.subheader("📊 Confidence & Risk Assessment")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Retrieval Confidence", f"{confidence:.2f}")

    with c2:
        if confidence >= 0.35:
            risk = "Low"
            st.markdown('<p class="risk-low">Low Risk</p>', unsafe_allow_html=True)
        elif confidence >= confidence_threshold:
            risk = "Medium"
            st.markdown('<p class="risk-medium">Medium Risk</p>', unsafe_allow_html=True)
        else:
            risk = "High"
            st.markdown('<p class="risk-high">High Risk</p>', unsafe_allow_html=True)

    with c3:
        st.metric("Recommended Action", "Review Evidence")

    # -----------------------------
    # Source Matches
    # -----------------------------
    st.subheader("🔎 Retrieved Source Matches")

    for i, result in enumerate(results, start=1):
        with st.expander(f"Match {i} — Confidence: {result['score']:.2f}"):
            st.write(result["section"])

    # -----------------------------
    # Audit Trail
    # -----------------------------
    st.subheader("🧾 Audit Trail")

    audit_record = {
        "Question": question,
        "Top Confidence Score": round(confidence, 4),
        "Risk Level": risk,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Recommended Action": "Review source guidance, validate evidence, and document approval."
    }

    st.json(audit_record)

    # -----------------------------
    # Downloadable Response
    # -----------------------------
    report = f"""
AI Business Operations Chatbot Report

Question:
{question}

Answer:
{answer}

Confidence Score:
{confidence:.2f}

Risk Level:
{risk}

Generated:
{audit_record["Timestamp"]}
"""

    st.download_button(
        label="⬇️ Download Response Report",
        data=report,
        file_name="business_operations_ai_response.txt",
        mime="text/plain"
    )

# -----------------------------
# Enterprise Roadmap Section
# -----------------------------
st.divider()

with st.expander("🚀 Enterprise Upgrade Roadmap", expanded=False):

    st.markdown("""
These enhancements would evolve this prototype into a production-ready enterprise AI operations platform.

### Planned Enhancements

- **OpenAI / Azure OpenAI Integration**  
  Add enterprise-grade natural language responses and conversational reasoning.

- **Vector Database Support**  
  Add ChromaDB, Pinecone, FAISS, or Azure AI Search for scalable semantic search and RAG.

- **PDF & Document Upload Support**  
  Allow ingestion of SOPs, policies, contracts, runbooks, and operational documentation.

- **Source Citations**  
  Return document names, sections, timestamps, owners, and page references.

- **Authentication & Role-Based Access Control**  
  Restrict answers based on team, department, or business function.

- **Conversation Memory**  
  Support contextual follow-up questions and session persistence.

- **Analytics Dashboard**  
  Track query volume, low-confidence questions, most searched policies, and adoption metrics.

- **Workflow Automation Integration**  
  Connect with Slack, Teams, Jira, ServiceNow, email, or approval workflows.

- **Audit & Compliance Logging**  
  Store who asked what, what source was used, and what recommendation was generated.

- **Human-in-the-Loop Review**  
  Route low-confidence or high-risk answers to an operations lead for approval.
""")

    st.caption(
        "This roadmap demonstrates how the prototype could scale into an enterprise-ready internal AI assistant."
    )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Built as a lightweight AI operations assistant prototype using Streamlit, scikit-learn, and TF-IDF retrieval."
)