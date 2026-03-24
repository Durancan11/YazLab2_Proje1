import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://book_db:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("library_catalog")

class Book(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int

# ----------------------------
# SAĞLIK KONTROLÜ
# ----------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ----------------------------
# TÜM KİTAPLARI LİSTELE
# ----------------------------
@app.get("/books")
async def list_books():
    books = []
    cursor = db.books.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        books.append(document)
    return books

# ----------------------------
# TEK KİTAP GETİR
# ----------------------------
@app.get("/books/{isbn}")
async def get_book(isbn: str):
    book = await db.books.find_one({"isbn": isbn})
    if not book:
        return JSONResponse(
            status_code=404,
            content={"detail": "Kitap bulunamadı"}
        )
    book["_id"] = str(book["_id"])
    return book

# ----------------------------
# KİTAP EKLE
# ----------------------------
@app.post("/books", status_code=201)
async def add_book(book: Book):
    existing = await db.books.find_one({"isbn": book.isbn})
    if existing:
        return JSONResponse(
            status_code=400,
            content={"detail": "Bu ISBN ile kitap zaten mevcut"}
        )
    new_book = book.dict()
    await db.books.insert_one(new_book)
    return {"message": "Kitap başarıyla eklendi"}

# ----------------------------
# KİTAP GÜNCELLE
# ----------------------------
@app.put("/books/{isbn}")
async def update_book(isbn: str, book: Book):
    existing = await db.books.find_one({"isbn": isbn})
    if not existing:
        return JSONResponse(
            status_code=404,
            content={"detail": "Kitap bulunamadı"}
        )
    await db.books.update_one(
        {"isbn": isbn},
        {"$set": book.dict()}
    )
    return {"message": "Kitap başarıyla güncellendi"}

# ----------------------------
# KİTAP SİL
# ----------------------------
@app.delete("/books/{isbn}")
async def delete_book(isbn: str):
    existing = await db.books.find_one({"isbn": isbn})
    if not existing:
        return JSONResponse(
            status_code=404,
            content={"detail": "Kitap bulunamadı"}
        )
    await db.books.delete_one({"isbn": isbn})
    return {"message": "Kitap başarıyla silindi"}