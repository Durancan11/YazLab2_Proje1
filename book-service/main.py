from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import BookRequest
from src.service import (
    fetch_all_books, fetch_book,
    add_book, modify_book, remove_book
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
    return fetch_all_books()

# ----------------------------
# TEK KİTAP GETİR
# ----------------------------
@app.get("/books/{isbn}")
async def get_single_book(isbn: str):
    book = fetch_book(isbn)
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
async def add_single_book(request: BookRequest):
    success, message = add_book(
        title=request.title,
        author=request.author,
        isbn=request.isbn,
        quantity=request.quantity
    )
    if not success:
        return JSONResponse(
            status_code=400,
            content={"detail": message}
        )
    return {"message": message}

# ----------------------------
# KİTAP GÜNCELLE
# ----------------------------
@app.put("/books/{isbn}")
async def update_single_book(isbn: str, request: BookRequest):
    success, message = modify_book(
        isbn=isbn,
        title=request.title,
        author=request.author,
        quantity=request.quantity
    )
    if not success:
        return JSONResponse(
            status_code=404,
            content={"detail": message}
        )
    return {"message": message}

# ----------------------------
# KİTAP SİL
# ----------------------------
@app.delete("/books/{isbn}")
async def delete_single_book(isbn: str):
    success, message = remove_book(isbn)
    if not success:
        return JSONResponse(
            status_code=404,
            content={"detail": message}
        )
    return {"message": message}