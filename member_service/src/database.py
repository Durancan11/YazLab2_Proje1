import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("member_system")

async def get_all_members():
    members = []
    async for member in db.members.find({}):
        member["_id"] = str(member["_id"])
        members.append(member)
    return members

async def get_member(member_id: str):
    return await db.members.find_one({"member_id": member_id})

async def save_member(member_id: str, name: str, email: str, phone: str):
    await db.members.insert_one({
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone
    })

async def update_member(member_id: str, name: str, email: str, phone: str):
    result = await db.members.update_one(
        {"member_id": member_id},
        {"$set": {"name": name, "email": email, "phone": phone}}
    )
    return result.modified_count > 0

async def delete_member(member_id: str):
    result = await db.members.delete_one({"member_id": member_id})
    return result.deleted_count > 0

async def member_exists(member_id: str) -> bool:
    member = await db.members.find_one({"member_id": member_id})
    return member is not None