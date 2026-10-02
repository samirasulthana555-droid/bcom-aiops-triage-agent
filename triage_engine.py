import os
from schema import AIOpsAlertSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_model, load_dotenv

#1 Automatically look up and load keys from the local .env file
load_dotenv()

print("\n--- [PRODUCTION] Executing Cloud Incident Triage System ---")

# 2. Connect to your active local ChromaDB Vector Store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 3. Test Scenario: Simulating a live production database timeout alert string
sample_payload = """
FATAL ERROR: Connection pooling exhausted on app-server cluster.
RESOURCE: PostgreSQL production database instance.
LOG: 'Socket error: Connection timed out after 30000ms. Handshake failure.'
"""

# 4. Perform an authentic mathematical Semantic Search query to isolate the target operational manual
matched_docs = db.similarity_search(sample_payload, k=1)

# Extracts text from the first matched document in the list result
retrieved_runbook = matched_docs[0].page_content
print("Authoritative infrastructure runbook extracted dynamically from ChromaDB via vector lookup.")

# 5. FIXED: Upgraded to 'gemini-3.8-flash' to match the latest required API endpoint routing cleanly
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
structured_llm = llm.with_structured_output(AIOpsAlertSchema)

# 6. Define the LangChain Expression Language (LCEL) Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a Senior Cloud Automation Engineer monitoring production infrastructure logs for Broadcom. "
        "Examine the incoming real-time alert payload and match it with the specific runbook context below. "
        "Extract the diagnostic validation steps, gcloud/kubectl SDK remediation commands, portal tracking links, "
        "severity classification, priority, and on-call escalation details exactly as mapped in the reference runbook.\n\n"
        "Reference Runbook Data:\n{runbook_context}"
    )),
    ("human", "Incoming Messy Infrastructure Payload:\n{payload}")
])

# 7. Construct and execute the LCEL Chain using the pipe operator (|)
triage_chain = prompt | structured_llm
result = triage_chain.invoke({
    "runbook_context": retrieved_runbook,
    "payload": sample_payload
})

print("\n--- Processed AIOps JSON Output ---")
print(result.model_dump_json(indent=4))
