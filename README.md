# Enterprise AIOps Log Correlation & Triage Agent

An automated infrastructure monitoring and operational incident triage pipeline engineered for tier-1 high-availability enterprise accounts (Broadcom topology). This framework ingests dirty, unstructured real-time streaming infrastructure payloads (e.g., GKE container failures, gateway oscillations, database timeouts) and correlates them against internal operational runbooks via a semantic vector storage retrieval layer using **LangChain Expression Language (LCEL)**, **ChromaDB**, and **Google Gemini 3.8 Flash**.

## 🏗️ Architecture Design Patterns
- **Localized Vector Indexing Layer:** Parses unstructured runbook wikis utilizing `RecursiveCharacterTextSplitter` mechanics and generates localized high-dimensional embeddings via an open-source transformer (`all-MiniLM-L6-v2`) to maintain zero-egress data privacy pipelines.
- **Contextual Semantic Matcher:** Intakes live telemetry data streams and executes vector-similarity lookups against the local data cluster to pull appropriate diagnostic files, dropping MTTA from minutes to sub-seconds.
- **Deterministic Orchestration Layer:** Pipes matched operational manuals and messy failure payloads into a generative reasoning layer using LCEL (`Prompt | Model`).
- **Strict Data Validation Schemas:** Utilizes comprehensive **Pydantic Models** to constrain the model outputs into predictable, machine-readable JSON targets (priorities, specific SDK commands, validation links, and precise on-call Slack escalation matrices) to prevent system crashes downstream.

## 🛠️ Production Stack
- **Orchestration Layer:** LangChain Core, LCEL Layouts
- **Reasoning Engine:** Google Gemini Pro / Flash APIs
- **Data Vector Layer:** ChromaDB Indexing Clusters
- **Validation Engine:** Pydantic Validation Schemas
- **Environment:** Pure-Python Runtime Environment, Virtual Environments (`venv`)

## 🚀 Execution & Local Verification

### 1. Environment Activation
```cmd
python -m venv venv
venv\Scripts\activate
pip install -y langchain langchain-google-genai langchain-community chromadb pydantic python-dotenv sentence-transformers
```

### 2. Ingest Reference Runbooks
```cmd
python ingest.py
```

### 3. Trigger Core Incident Triage Agent
```cmd
python triage_engine.py
```
