import os
from pydantic import SecretStr
from langchain_nomic.embeddings import NomicEmbeddings  
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RagService:
    def __init__(self, llm:ChatOpenAI, vectorstore: PineconeVectorStore, embedding_model ) -> None:
        self.llm = llm
        self.vectorstore = vectorstore
        self.embedding_model = embedding_model

    def load_docs(self,path: str):
        loader = PyPDFLoader(file_path=path)
        docs = loader.load()
        return docs

    def split_docs(self, docs: list[Document]):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        return chunks

    def embed_docs(self, docs: list[Document]):
        _ = self.vectorstore.add_documents(docs)

    def retrieve_docs(self, query: str):
        retriever = self.vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'fetch_k': 50}
        )
        retrieved_docs = retriever.invoke(query)
        return retrieved_docs

    def query(self, query: str, docs: list[Document]):
        formatted_query = f"""based on the list of documents below: {docs}, you are to answer the following question: {query}. Answer precisely and concisely."""        
        result = self.llm.invoke(formatted_query)
        return result

if __name__ == "__main__":
    NOMIC_API_KEY=os.getenv("NOMIC_KEY")
    PINECONE_API_KEY=os.getenv("PINECONE_KEY")
    PINECONE_INDEX_NAME="interview-index"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        raise ValueError("Openai api key does not exist not set")

    llm = ChatOpenAI(model="gpt-4o")
    embedding_model = NomicEmbeddings(nomic_api_key=NOMIC_API_KEY, model="nomic-embed-text-v1.5")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if not pc.has_index(PINECONE_INDEX_NAME):
        pc.create_index(
            name =PINECONE_INDEX_NAME,
            dimension=768,
            metric="cosine",
            spec= ServerlessSpec(
                cloud="aws",
                region="us-east-1"                
            )
        )

    index = pc.Index(PINECONE_INDEX_NAME)
    
    vectorstore = PineconeVectorStore(embedding=embedding_model,index= index )    
    rag_service = RagService(llm=llm,embedding_model=embedding_model, vectorstore=vectorstore)

    loaded_docs = rag_service.load_docs("./docs/downloaded.pdf")
    splitted_docs = rag_service.split_docs(loaded_docs)
    splitted_docs = rag_service.embed_docs(splitted_docs)