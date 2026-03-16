import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB bağlantısı
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("auth_system")

# ----------------------------
# KULLANICI İŞLEMLERİ
# ----------------------------

async def get_user(username: str):
    """Kullanıcıyı veritabanından getirir"""
    return await db.users.find_one({"username": username})

async def save_user(username: str, email: str, hashed_password: str):
    """Yeni kullanıcıyı veritabanına kaydeder"""
    await db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

async def user_exists(username: str) -> bool:
    """Kullanıcı zaten var mı kontrol eder"""
    user = await db.users.find_one({"username": username})
    return user is not None