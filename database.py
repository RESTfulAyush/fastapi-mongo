from motor.motor_asyncio import AsyncIOMotorClient
import logging

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "assignmentDb"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
employees_collection = db["employees"]

async def check_db_connection():
    try:
        await client.admin.command("ping")
        logging.info("✅ MongoDB connection successful")
        return True
    except Exception as e:
        logging.error(f"❌ MongoDB connection failed: {e}")
        return False
