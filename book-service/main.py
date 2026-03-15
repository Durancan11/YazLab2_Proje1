from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import BookRequest
from src.database import (
    get_all_books, get_book, save_book,
    update_book, delete_book, book_exists
)

app = FastAPI()

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
    return get_all_books()

# ----------------------------
# TEK KİTAP GETİR
# ----------------------------
@app.get("/books/{isbn}")
async def get_single_book(isbn: str):
    book = get_book(isbn)
    if not book:
        return JSONResponse(
            status_code=404,
            content={"detail": "Kitap bulunamadı"}
        )
    return book

# ----------------------------
# KİTAP EKLE
# ----------------------------
@app.post("/books", status_code=201)
async def add_book(request: BookRequest):
    if book_exists(request.isbn):
        return JSONResponse(
            status_code=400,
            content={"detail": "Bu ISBN ile kitap zaten mevcut"}
        )
    save_book(
        title=request.title,
        author=request.author,
        isbn=request.isbn,
        quantity=request.quantity
    )
    return {"message": "Kitap başarıyla eklendi"}

# ----------------------------
# KİTAP GÜNCELLE
# ----------------------------
@app.put("/books/{isbn}")
async def update_single_book(isbn: str, request: BookRequest):
    if not book_exists(isbn):
        return JSONResponse(
            status_code=404,
            content={"detail": "Kitap bulunamadı"}
        )
    update_book(
        isbn=isbn,
        title=request.title,
        author=request.author,
        quantity=request.quantity
    )
    return {"message": "Kitap başarıyla güncellendi"}

# ----------------------------
# KİTAP SİL
# ----------------------------
@app.delete("/books/{isbn}")
async def delete_single_book(isbn: str):
    if not book_exists(isbn):
        return JSONResponse(
            status_code=404,
            content={"detail": "Kitap bulunamadı"}
        )
    delete_book(isbn)
    return {"message": "Kitap başarıyla silindi"}