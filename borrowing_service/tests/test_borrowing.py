import pytest
from httpx import ASGITransport, AsyncClient

# Henüz main.py içinde 'app' nesnesini ve '/borrow' yolunu tanımlamadık.
# Bu yüzden bu test şu an ÇALIŞMAYACAK (RED).
try:
    from borrowing_service.main import app
except ImportError:
    app = None

@pytest.mark.asyncio
async def test_borrow_book_success():
    if app is None:
        pytest.fail("Borrowing Service ana dosyası henüz hazır değil!")
        
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # RMM Seviye 2: Yeni bir kaynak oluştururken POST kullanıyoruz
        payload = {"user_id": 1, "book_id": 101, "days": 14}
        response = await ac.post("/borrow", json=payload)
    
    assert response.status_code == 201 # Created
    assert response.json()["status"] == "borrowed"