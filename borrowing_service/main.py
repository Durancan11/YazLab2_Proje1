import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# ----------------------------
# VERİTABANI BAĞLANTISI (Kritik Kısım!)
# ----------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://borrowing_db:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("borrowing_system") # Veritabanı adı

# Veri Modeli
class BorrowRequest(BaseModel):
    user_id: int
    book_id: int
    days: int

# ----------------------------
# POST: KİTAP ÖDÜNÇ AL
# ----------------------------
@app.post("/borrow")
async def borrow_book(request: BorrowRequest):
    new_borrow = request.dict()
    result = await db.borrows.insert_one(new_borrow)
    return {
        "user_id": request.user_id,
        "book_id": request.book_id,
        "status": "borrowed",
        "message": f"{request.book_id} numaralı kitap {request.days} günlüğüne alındı.",
        "db_id": str(result.inserted_id)
    }

# ----------------------------
# GET: TÜM KAYITLARI LİSTELE
# ----------------------------
@app.get("/borrow")
async def list_borrows():
    borrows = []
    # MongoDB'deki 'borrows' koleksiyonundan tüm kayıtları çek
    cursor = db.borrows.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"]) # ObjectId'yi string'e çevir
        borrows.append(document)
    return borrows