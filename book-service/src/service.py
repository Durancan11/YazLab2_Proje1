from src.database import (
    get_all_books, get_book, save_book,
    update_book, delete_book, book_exists
)

def fetch_all_books():
    """Tüm kitapları getirir"""
    return get_all_books()

def fetch_book(isbn: str):
    """ISBN'e göre kitap getirir, yoksa None döner"""
    return get_book(isbn)

def add_book(title: str, author: str, isbn: str, quantity: int):
    """
    Yeni kitap ekler.
    İş kuralları:
    - Aynı ISBN ile kitap eklenemez
    - Stok miktarı 0'dan küçük olamaz
    """
    if book_exists(isbn):
        return False, "Bu ISBN ile kitap zaten mevcut"
    if quantity < 0:
        return False, "Stok miktarı 0'dan küçük olamaz"
    save_book(title, author, isbn, quantity)
    return True, "Kitap başarıyla eklendi"

def modify_book(isbn: str, title: str, author: str, quantity: int):
    """
    Kitap bilgilerini günceller.
    İş kuralları:
    - Olmayan kitap güncellenemez
    - Stok miktarı 0'dan küçük olamaz
    """
    if not book_exists(isbn):
        return False, "Kitap bulunamadı"
    if quantity < 0:
        return False, "Stok miktarı 0'dan küçük olamaz"
    update_book(isbn, title, author, quantity)
    return True, "Kitap başarıyla güncellendi"

def remove_book(isbn: str):
    """
    Kitabı siler.
    İş kuralları:
    - Olmayan kitap silinemez
    """
    if not book_exists(isbn):
        return False, "Kitap bulunamadı"
    delete_book(isbn)
    return True, "Kitap başarıyla silindi"