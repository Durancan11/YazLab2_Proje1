import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, patch

# ----------------------------
# SAHTE VERİTABANI KURULUMU
# Her test gerçek MongoDB yerine bunu kullanır
# ----------------------------
fake_db = {}

async def mock_get_user(username):
    return fake_db.get(username)

async def mock_save_user(username, email, hashed_password):
    fake_db[username] = {
        "username": username,
        "email": email,
        "password": hashed_password
    }

async def mock_user_exists(username):
    return username in fake_db

# ----------------------------
# 1. SAĞLIK KONTROLÜ
# ----------------------------
@pytest.mark.asyncio
async def test_health_check():
    from main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ----------------------------
# 2. KAYIT TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_register_success():
    fake_db.clear()
    with patch("main.get_user", mock_get_user), \
         patch("main.save_user", mock_save_user), \
         patch("main.user_exists", mock_user_exists):
        from main import app
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
    from main import app
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
    fake_db.clear()
    with patch("main.get_user", mock_get_user), \
         patch("main.save_user", mock_save_user), \
         patch("main.user_exists", mock_user_exists):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # Önce kayıt ol
            await ac.post("/register", json={
                "username": "testuser",
                "password": "testpass123",
                "email": "test@test.com"
            })
            # Sonra giriş yap
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
    fake_db.clear()
    with patch("main.get_user", mock_get_user), \
         patch("main.save_user", mock_save_user), \
         patch("main.user_exists", mock_user_exists):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post("/register", json={
                "username": "testuser",
                "password": "testpass123",
                "email": "test@test.com"
            })
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
    fake_db.clear()
    with patch("main.get_user", mock_get_user), \
         patch("main.user_exists", mock_user_exists):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/login", json={
                "username": "olmayan_kullanici",
                "password": "testpass123"
            })
    assert response.status_code == 401
    assert response.json()["detail"] == "Kullanıcı adı veya şifre hatalı"