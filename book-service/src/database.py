# Geçici kitap deposu
# İleride MongoDB ile değiştirilecek
fake_db = {}

def get_all_books():
    """Tüm kitapları listeler"""
    return list(fake_db.values())

def get_book(isbn: str):
    """ISBN'e göre kitap getirir"""
    return fake_db.get(isbn)

def save_book(title: str, author: str, isbn: str, quantity: int):
    """Yeni kitap ekler"""
    fake_db[isbn] = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "quantity": quantity
    }

def update_book(isbn: str, title: str, author: str, quantity: int):
    """Kitap bilgilerini günceller"""
    if isbn not in fake_db:
        return False
    fake_db[isbn] = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "quantity": quantity
    }
    return True

def delete_book(isbn: str):
    """Kitabı siler"""
    if isbn not in fake_db:
        return False
    del fake_db[isbn]
    return True

def book_exists(isbn: str) -> bool:
    """Kitap zaten var mı kontrol eder"""
    return isbn in fake_db