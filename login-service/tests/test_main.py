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
# 2. KAYIT TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_register_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/register", json={
            "username": "testuser",
            "password": "testpass123",
            "email": "test@test.com"
        })
    assert response.status_code == 201
    assert response.json()["message"] == "Kullanıcı başarıyla oluşturuldu"

# ----------------------------
# 3. EKSİK BİLGİYLE KAYIT TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_register_missing_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/register", json={
            "username": "testuser"
        })
    assert response.status_code == 422

# ----------------------------
# 4. GİRİŞ TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
    assert response.status_code == 200
    assert "token" in response.json()

# ----------------------------
# 5. YANLIŞ ŞİFREYLE GİRİŞ TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", json={
            "username": "testuser",
            "password": "yanlis_sifre"
        })
    assert response.status_code == 401
    assert response.json()["detail"] == "Kullanıcı adı veya şifre hatalı"

# ----------------------------
# 6. OLMAYAN KULLANICI TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_login_user_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", json={
            "username": "olmayan_kullanici",
            "password": "testpass123"
        })
    assert response.status_code == 401
    assert response.json()["detail"] == "Kullanıcı adı veya şifre hatalı"