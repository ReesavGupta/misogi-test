from motor.motor_asyncio import AsyncIOMotorClient

def setup_db():
    client = AsyncIOMotorClient(host="localhost", port=27017)
    print(client.test_db)

if __name__ == "__main__":
    setup_db()

