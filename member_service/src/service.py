from src.database import (
    get_all_members, get_member, save_member,
    update_member, delete_member, member_exists
)

async def fetch_all_members():
    """Tüm üyeleri getirir"""
    return await get_all_members()

async def fetch_member(member_id: str):
    """ID'ye göre üye getirir, yoksa None döner"""
    return await get_member(member_id)

async def add_member(member_id: str, name: str, email: str, phone: str):
    """
    Yeni üye ekler.
    İş kuralları:
    - Aynı ID ile üye eklenemez
    - Email boş olamaz
    """
    if await member_exists(member_id):
        return False, "Bu ID ile üye zaten mevcut"
    if not email or "@" not in email:
        return False, "Geçerli bir email adresi giriniz"
    await save_member(member_id, name, email, phone)
    return True, "Üye başarıyla eklendi"

async def modify_member(member_id: str, name: str, email: str, phone: str):
    """
    Üye bilgilerini günceller.
    İş kuralları:
    - Olmayan üye güncellenemez
    """
    if not await member_exists(member_id):
        return False, "Üye bulunamadı"
    await update_member(member_id, name, email, phone)
    return True, "Üye başarıyla güncellendi"

async def remove_member(member_id: str):
    """
    Üyeyi siler.
    İş kuralları:
    - Olmayan üye silinemez
    """
    if not await member_exists(member_id):
        return False, "Üye bulunamadı"
    await delete_member(member_id)
    return True, "Üye başarıyla silindi"