import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch

# ----------------------------
# SAHTE VERİTABANI KURULUMU
# ----------------------------
fake_db = {}

async def mock_get_member(member_id):
    return fake_db.get(member_id)

async def mock_get_all_members():
    return list(fake_db.values())

async def mock_save_member(member_id, name, email, phone):
    fake_db[member_id] = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone
    }

async def mock_update_member(member_id, name, email, phone):
    if member_id not in fake_db:
        return False
    fake_db[member_id] = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone
    }
    return True

async def mock_delete_member(member_id):
    if member_id not in fake_db:
        return False
    del fake_db[member_id]
    return True

async def mock_member_exists(member_id):
    return member_id in fake_db

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
    with patch("main.save_member", mock_save_member), \
         patch("main.member_exists", mock_member_exists):
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
    with patch("main.get_all_members", mock_get_all_members):
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
    with patch("main.save_member", mock_save_member), \
         patch("main.member_exists", mock_member_exists), \
         patch("main.get_member", mock_get_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post("/members", json={
                "member_id": "M002",
                "name": "Ayşe Kaya",
                "email": "ayse@test.com",
                "phone": "05559876543"
            })
            response = await ac.get("/members/M002")
    assert response.status_code == 200
    assert response.json()["name"] == "Ayşe Kaya"

# ----------------------------
# 5. OLMAYAN ÜYE TESTİ
# ----------------------------
@pytest.mark.asyncio
async def test_get_member_not_found():
    fake_db.clear()
    with patch("main.get_member", mock_get_member):
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
    with patch("main.save_member", mock_save_member), \
         patch("main.member_exists", mock_member_exists), \
         patch("main.update_member", mock_update_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post("/members", json={
                "member_id": "M003",
                "name": "Mehmet Demir",
                "email": "mehmet@test.com",
                "phone": "05551111111"
            })
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
    with patch("main.save_member", mock_save_member), \
         patch("main.member_exists", mock_member_exists), \
         patch("main.delete_member", mock_delete_member):
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post("/members", json={
                "member_id": "M004",
                "name": "Fatma Şahin",
                "email": "fatma@test.com",
                "phone": "05553333333"
            })
            response = await ac.delete("/members/M004")
    assert response.status_code == 200
    assert response.json()["message"] == "Üye başarıyla silindi"