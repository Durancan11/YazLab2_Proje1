import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch

# ----------------------------
# SAHTE SERVİS FONKSİYONLARI
# Artık database değil service katmanını mock'luyoruz
# ----------------------------
fake_db = {}

async def mock_fetch_all_members():
    return list(fake_db.values())

async def mock_fetch_member(member_id):
    return fake_db.get(member_id)

async def mock_add_member(member_id, name, email, phone):
    if member_id in fake_db:
        return False, "Bu ID ile üye zaten mevcut"
    fake_db[member_id] = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone
    }
    return True, "Üye başarıyla eklendi"

async def mock_modify_member(member_id, name, email, phone):
    if member_id not in fake_db:
        return False, "Üye bulunamadı"
    fake_db[member_id] = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone
    }
    return True, "Üye başarıyla güncellendi"

async def mock_remove_member(member_id):
    if member_id not in fake_db:
        return False, "Üye bulunamadı"
    del fake_db[member_id]
    return True, "Üye başarıyla silindi"

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
# 2. ÜYE EKLEME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_add_member():
    fake_db.clear()
    with patch("main.add_member", mock_add_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/members", json={
                "member_id": "M001",
                "name": "Ahmet Yılmaz",
                "email": "ahmet@test.com",
                "phone": "05551234567"
            })
    assert response.status_code == 201
    assert response.json()["message"] == "Üye başarıyla eklendi"

# ----------------------------
# 3. ÜYE LİSTELEME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_list_members():
    fake_db.clear()
    with patch("main.fetch_all_members", mock_fetch_all_members):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/members")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------------------
# 4. TEK ÜYE GETİRME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_get_member():
    fake_db.clear()
    fake_db["M002"] = {
        "member_id": "M002",
        "name": "Ayşe Kaya",
        "email": "ayse@test.com",
        "phone": "05559876543"
    }
    with patch("main.fetch_member", mock_fetch_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/members/M002")
    assert response.status_code == 200
    assert response.json()["name"] == "Ayşe Kaya"

# ----------------------------
# 5. OLMAYAN ÜYE TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_get_member_not_found():
    fake_db.clear()
    with patch("main.fetch_member", mock_fetch_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/members/olmayan_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Üye bulunamadı"

# ----------------------------
# 6. ÜYE GÜNCELLEME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_update_member():
    fake_db.clear()
    fake_db["M003"] = {
        "member_id": "M003",
        "name": "Mehmet Demir",
        "email": "mehmet@test.com",
        "phone": "05551111111"
    }
    with patch("main.modify_member", mock_modify_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.put("/members/M003", json={
                "member_id": "M003",
                "name": "Mehmet Demir",
                "email": "mehmet_yeni@test.com",
                "phone": "05552222222"
            })
    assert response.status_code == 200
    assert response.json()["message"] == "Üye başarıyla güncellendi"

# ----------------------------
# 7. ÜYE SİLME TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_delete_member():
    fake_db.clear()
    fake_db["M004"] = {
        "member_id": "M004",
        "name": "Fatma Şahin",
        "email": "fatma@test.com",
        "phone": "05553333333"
    }
    with patch("main.remove_member", mock_remove_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.delete("/members/M004")
    assert response.status_code == 200
    assert response.json()["message"] == "Üye başarıyla silindi"