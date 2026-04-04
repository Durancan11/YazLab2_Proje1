import pytest
from httpx import AsyncClient, ASGITransport
from dispatcher.main import app

@pytest.mark.asyncio
async def test_health_check():
    """TDD - Red: Sağlık kontrolü çalışıyor mu?"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_unauthorized_access():
    """TDD - Green: Token olmadan erişim engelleniyor mu?"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/books")
    
    # Dispatcher token bulamadığında 401 dönmeli
    assert response.status_code == 401