# AI Business Operations Chatbot

An enterprise-style AI assistant prototype designed to help teams search internal SOPs, operational policies, controls, and business documentation using lightweight AI retrieval.

Built with Streamlit and scikit-learn, this project demonstrates how organizations can transform static operational documentation into an interactive internal knowledge assistant.

---

# 🚀 Features

## AI-Powered SOP Retrieval
Uses TF-IDF vectorization and cosine similarity to retrieve the most relevant operational guidance based on user questions.

## Enterprise-Style UI
Modern Streamlit interface with:
- KPI metric cards
- Sidebar controls
- Confidence scoring
- Risk indicators
- Expandable source matches
- Downloadable response reports

## Retrieval Confidence Scoring
Displays similarity confidence scores and operational risk indicators to help users evaluate answer reliability.

## Multi-Match Source Retrieval
Returns multiple ranked source matches instead of a single result for better transparency and auditability.

## Suggested Operational Questions
Includes built-in sample prompts for:
- Data pipeline release controls
- Incident escalation
- Data quality management
- Audit evidence
- Production approvals
- Operational governance

## Audit Trail Generation
Automatically creates:
- Timestamped response logs
- Confidence tracking
- Risk classification
- Recommended operational actions

## Enterprise Roadmap Simulation
Demonstrates how the prototype could evolve into a production-ready enterprise AI assistant with:
- OpenAI / Azure OpenAI
- Vector databases
- RAG pipelines
- Role-based access
- Workflow integrations
- Compliance logging
- Conversation memory

---

# 🧠 Business Problem

Companies store critical operational knowledge across:
- SOPs
- Policies
- Runbooks
- Operational manuals
- Internal process documentation

Employees waste significant time:
- Searching for information
- Asking repetitive questions
- Navigating fragmented documentation
- Verifying operational procedures manually

This creates operational inefficiencies, inconsistent execution, and increased compliance risk.

---

# ✅ Solution

This chatbot transforms static documentation into an interactive AI-powered operational assistant capable of:

- Retrieving relevant policy sections
- Providing operational guidance
- Surfacing source context
- Highlighting confidence levels
- Supporting audit and governance workflows

The project demonstrates the foundation of a Retrieval-Augmented Generation (RAG) architecture for enterprise knowledge management.

---

# 💼 What This Project Demonstrates

- Retrieval-Augmented Generation (RAG) concepts
- Internal AI knowledge assistant architecture
- Enterprise operations automation
- Semantic search workflows
- Operational governance support
- Lightweight AI search pipelines
- Audit-friendly AI responses
- Streamlit enterprise dashboard design
- AI product prototyping for business operations

---

# 🛠️ Tech Stack

- Python
- Streamlit
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- Lightweight NLP Retrieval

---

# 📂 Project Structure

```bash
├── app.py
├── requirements.txt
├── data/
│   └── company_sop.txt
└── README.md
```

## Chatbot Images

![Dashboard1](images/Dashboard1)

![Dashboard2](images/Dashboard2)

![Dashboard3](images/Dashboard3)

![Dashboard4](images/Dashboard4)

![Dashboard5](images/Dashboard5)


## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
