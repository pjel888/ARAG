# Import required modules
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter  # UPDATED
from langchain_huggingface import HuggingFaceEmbeddings             # UPDATED
from langchain_chroma import Chroma                                 # UPDATED
from langchain_ollama import ChatOllama                             # UPDATED
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# 1. Load PDF documents
loader = DirectoryLoader(
    "./RAG - ALE ARCHITECTURE BOARD EXAM",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)
docs = loader.load()

# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(docs)

# 3. Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
# Note: Chroma auto-persists in newer versions, but explicitly calling it is fine if using older versions.

# 4. Connect to local DeepSeek-R1 (via Ollama)
llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)

# 5. Define the prompt
prompt_template = """
You are a research assistant writing an article. Use the following pieces of context to answer the query.
If you don't know the answer, just say so. Cite the sources when possible.

Context:
{context}

Query: {question}
Article:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# 6. Create the retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True,
)

# 7. Ask a question (write an article)
query = "Write a 500-word article about the latest building code requirements for fire exits, citing the provided documents."
result = qa_chain.invoke({"query": query})

# Print the article
print("\n" + "="*50)
print("ARTICLE:")
print("="*50)
print(result["result"])
print("\n" + "="*50)
print("SOURCES:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata.get('source', 'unknown')}")
