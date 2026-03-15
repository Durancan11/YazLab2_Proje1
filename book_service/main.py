import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# İzole NoSQL Bağlantısı 
MONGO_URL = os.getenv("MONGO_URL", "mongodb://book_db:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("library_catalog")

class Book(BaseModel):
    title: str
    author: str
    isbn: str

@app.post("/books", status_code=201)
async def add_book(book: Book):
    new_book = book.dict()
    result = await db.books.insert_one(new_book)
    return {"id": str(result.inserted_id), "message": "Kitap başarıyla eklendi."}

@app.get("/books")
async def list_books():
    books = []
    cursor = db.books.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        books.append(document)
    return books

@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    try:
        delete_result = await db.books.delete_one({"_id": ObjectId(book_id)})
        if delete_result.deleted_count == 1:
            return {"message": "Kitap silindi."}
        # Doğru HTTP 404 kodu kullanımı [cite: 41, 59]
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz ID formatı.")