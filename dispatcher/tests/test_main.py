import pytest
from httpx import ASGITransport, AsyncClient

try:
    from dispatcher.main import app
except ImportError:
    from main import app

@pytest.mark.asyncio
async def test_health_check():
    if app is None:
        pytest.fail("Dispatcher ana uygulama dosyası (main.py) henüz yok!")
        
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}