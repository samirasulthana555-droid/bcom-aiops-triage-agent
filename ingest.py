import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

print("--- [PRODUCTION] Starting AIOps Knowledge Base Vector Ingestion ---")

all_documents = []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)

print("Ingesting individual infrastructure runbook logs...")

# GKE Runbook
file_gke = open("infra_runbooks/alr_gke_991.txt", "r", encoding="utf-8")
content_gke = file_gke.read()
file_gke.close()
chunks_gke = text_splitter.create_documents([content_gke], [{"source": "alr_gke_991.txt", "topic": "K8s"}])
all_documents.extend(chunks_gke)

# Network Runbook
file_net = open("infra_runbooks/alr_net_223.txt", "r", encoding="utf-8")
content_net = file_net.read()
file_net.close()
chunks_net = text_splitter.create_documents([content_net], [{"source": "alr_net_223.txt", "topic": "Networking"}])
all_documents.extend(chunks_net)

# Database Runbook
file_db = open("infra_runbooks/alr_db_411.txt", "r", encoding="utf-8")
content_db = file_db.read()
file_db.close()
chunks_db = text_splitter.create_documents([content_db], [{"source": "alr_db_411.txt", "topic": "Database"}])
all_documents.extend(chunks_db)

print("Initializing Local Embedding Framework...")
# FIXED: Using a reliable local transformer model to completely avoid the Google 404 API error
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Building and caching local ChromaDB infrastructure...")
vectorstore = Chroma.from_documents(
    documents=all_documents, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

print("[SUCCESS] ChromaDB vector store successfully created and populated!")
