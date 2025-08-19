import os
from langchain_openai import ChatOpenAI
from pinecone import ServerlessSpec
from langchain_nomic import NomicEmbeddings
from langchain_pinecone import PineconeVectorStore
from rag_service import RagService
from pinecone import Pinecone
import json
import uvicorn
from fastapi import FastAPI
from database.connection import client, get_db
from database.models import User
from database.connection import insert_one_user, get_user
from database.connection import setup_client
app = FastAPI()
db = get_db()

@app.get("/health")
def heatlth():
    return {"status": "ok"}

@app.post("/users/signup")
async def create_user(user: User):
    inserted_user = await insert_one_user(user)
    return json.dumps(inserted_user)

@app.post("/users/login/{email}")
async def login_user(email):
    if email:
        user = await get_user(email)
        return user


@app.post("/ask/{question}")
async def ask(question: str):
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
    rag_service = RagService(llm=llm, vectorstore=vectorstore, embedding_model=embedding_model)

    rag_service.retrieve_docs(query=question)


if __name__ == "__main__":
    setup_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)