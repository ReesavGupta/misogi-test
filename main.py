import uvicorn
from fastapi import FastAPI
from database.connection import client, get_db
from database.models import User
from database.connection import insert_one_user
from database.connection import setup_client
app = FastAPI()
db = get_db()

@app.get("/health")
def heatlth():
    return {"status": "ok"}

@app.post("/users")
async def create_user(user: User):
    inserted_user = await insert_one_user(user)
    print(inserted_user)


if __name__ == "__main__":
    setup_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)