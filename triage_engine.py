import os
from schema import AIOpsAlertSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

def run_incident_triage(raw_incoming_payload: str, backup_key: str = None):
    print("\n--- [PRODUCTION] Executing Cloud Incident Triage System ---")

    # 1. Connect to our localized vector database cluster
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

    # 2. Semantic Search lookup to find matching runbooks
    matched_docs = db.similarity_search(raw_incoming_payload, k=1)
    
    if not matched_docs:
        raise ValueError("No matching runbook found in ChromaDB vector store.")
        
    retrieved_runbook = matched_docs[0].page_content
    print("Authoritative infrastructure runbook extracted dynamically from ChromaDB via vector lookup.")

    # 3. Secure Key Extraction Pathway
    # Prioritise the system environment first, then use the backup parameter passed down by the graph
    api_key_val = os.getenv("GOOGLE_API_KEY") or backup_key

    if not api_key_val:
        raise ValueError("System Error: Critical failure to authenticate Gemini API. Key evaluates to empty.")

    # 4. Initialize Gemini 3.8 Flash with structural formatting rules
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash", 
        temperature=0, 
        api_key=api_key_val
    )
    structured_llm = llm.with_structured_output(AIOpsAlertSchema)

    # 5. Define the LangChain Expression Language (LCEL) Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Senior Cloud Automation Engineer monitoring production infrastructure logs for Broadcom. "
            "Examine the incoming real-time alert payload and match it with the specific runbook context below. "
            "Extract the diagnostic validation steps, gcloud/kubectl SDK remediation commands, portal tracking links, "
            "severity classification, priority, and on-call escalation details exactly as mapped in the reference runbook.\n\n"
            "Reference Runbook Data:\n{runbook_context}"
        )),
        ("human", "Analyze this incoming infrastructure payload:\n{payload}")
    ])

    # 6. Execute the declarative chain layer
    triage_chain = prompt | structured_llm
    result = triage_chain.invoke({
        "runbook_context": retrieved_runbook,
        "payload": raw_incoming_payload
    })

    return result
