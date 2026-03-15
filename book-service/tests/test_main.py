import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import ASGITransport, AsyncClient
from main import app

# ----------------------------
# 1. SAĞLIK KONTROLÜ
# ----------------------------
@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ----------------------------
# 2. KİTAP EKLEME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_add_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books", json={
            "title": "Suç ve Ceza",
            "author": "Dostoyevski",
            "isbn": "978-1234567890",
            "quantity": 3
        })
    assert response.status_code == 201
    assert response.json()["message"] == "Kitap başarıyla eklendi"

# ----------------------------
# 3. KİTAP LİSTELEME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_list_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------------------
# 4. TEK KİTAP GETİRME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_get_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Önce kitap ekle
        await ac.post("/books", json={
            "title": "Savaş ve Barış",
            "author": "Tolstoy",
            "isbn": "978-0987654321",
            "quantity": 2
        })
        # Sonra getir
        response = await ac.get("/books/978-0987654321")
    assert response.status_code == 200
    assert response.json()["title"] == "Savaş ve Barış"

# ----------------------------
# 5. OLMAYAN KİTAP TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_get_book_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books/olmayan-isbn")
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı"

# ----------------------------
# 6. KİTAP GÜNCELLEME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_update_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Önce kitap ekle
        await ac.post("/books", json={
            "title": "Dönüşüm",
            "author": "Kafka",
            "isbn": "978-1111111111",
            "quantity": 1
        })
        # Sonra güncelle
        response = await ac.put("/books/978-1111111111", json={
            "title": "Dönüşüm",
            "author": "Franz Kafka",
            "isbn": "978-1111111111",
            "quantity": 5
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Kitap başarıyla güncellendi"

# ----------------------------
# 7. KİTAP SİLME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_delete_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Önce kitap ekle
        await ac.post("/books", json={
            "title": "Simyacı",
            "author": "Paulo Coelho",
            "isbn": "978-2222222222",
            "quantity": 4
        })
        # Sonra sil
        response = await ac.delete("/books/978-2222222222")
    assert response.status_code == 200
    assert response.json()["message"] == "Kitap başarıyla silindi"