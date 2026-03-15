from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Veri modeli (RMM Seviye 2 için JSON gövdesi)
class BorrowRequest(BaseModel):
    user_id: int
    book_id: int
    days: int

@app.post("/borrow", status_code=201)
async def borrow_book(request: BorrowRequest):
    # Şimdilik veritabanı yok, sadece testin geçmesi için başarılı dönüyoruz.
    # Bir sonraki adımda buraya NoSQL (MongoDB) ekleyeceğiz.
    return {
        "user_id": request.user_id,
        "book_id": request.book_id,
        "status": "borrowed",
        "message": f"{request.book_id} numaralı kitap {request.days} günlüğüne alındı."
    }