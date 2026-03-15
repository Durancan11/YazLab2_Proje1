import pytest
from httpx import ASGITransport, AsyncClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# ----------------------------
# 1. SAĞLIK KONTROLÜ TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ----------------------------
# 2. JWT OLMADAN İSTEK TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_request_without_token():
    # JWT token olmadan istek atılırsa 401 dönmeli
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books")
    assert response.status_code == 401
    assert response.json()["detail"] == "Token bulunamadı"

# ----------------------------
# 3. GEÇERSİZ JWT TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_request_with_invalid_token():
    # Geçersiz token ile istek atılırsa 401 dönmeli
    headers = {"Authorization": "Bearer gecersiz_token_123"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Geçersiz token"

# ----------------------------
# 4. GEÇERLİ JWT TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_request_with_valid_token():
    import jwt
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # Geçerli bir token oluşturuyoruz
    secret = os.getenv("SECRET_KEY", "test_secret")
    token = jwt.encode({"user_id": "123", "role": "user"}, secret, algorithm="HS256")
    
    headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books", headers=headers)
    
    # 401 veya 403 dönmemeli (servis kapalı olduğu için 502 olabilir, bu normal)
    assert response.status_code != 401
    assert response.status_code != 403