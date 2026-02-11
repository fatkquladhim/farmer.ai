import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Setup Persist Directory
PERSIST_DIR = "faiss_index"

def load_documents(data_dir="data/manuals"):
    documents = []
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        return []

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
            
    return documents

def build_vector_store():
    documents = load_documents()
    if not documents:
        return None
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    # Use Gemini Embeddings
    if "GOOGLE_API_KEY" not in os.environ:
        print("GOOGLE_API_KEY not found. RAG will not work.")
        return None
        
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    try:
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        vectorstore.save_local(PERSIST_DIR)
        return vectorstore
    except Exception as e:
        print(f"Error building vector store: {e}")
        return None

def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    if os.path.exists(PERSIST_DIR):
        try:
            # allow_dangerous_deserialization is needed for local pickles
            vectorstore = FAISS.load_local(PERSIST_DIR, embeddings, allow_dangerous_deserialization=True)
            return vectorstore.as_retriever(search_kwargs={"k": 3})
        except Exception as e:
            print(f"Error loading vector store: {e}")
            pass
            
    # Rebuild if not found or error
    vectorstore = build_vector_store()
    if vectorstore:
        return vectorstore.as_retriever(search_kwargs={"k": 3})
    return None
