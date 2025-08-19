from motor.motor_asyncio import AsyncIOMotorClient
from database.models import User
client = None
def setup_client():
    global client
    client = AsyncIOMotorClient(host="localhost", port=27017)
    print("inside setup client: ", client)
 
def get_db():
    
    global client
    if client:
        print(client.test_db)
        return client.test_db

async def close_db():
    global client
    if client:
        client.close()
    

async def get_user(user: User):
    email = user.email
    db = get_db()
    collection = db.get_collection("users") #type: ignore
    new_user= await collection.find_one({email: email})
    print(new_user)


async def insert_one_user(user: User):
    db = get_db()
    # print("this is the db: ", db)
    collection = db.get_collection("users") #type: ignore
    new_user= await collection.insert_one(user.__dict__)
    print(new_user)
