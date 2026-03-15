# Geçici kullanıcı deposu
# İleride MongoDB ile değiştirilecek
fake_db = {}

def get_user(username: str):
    """Kullanıcıyı veritabanından getirir"""
    return fake_db.get(username)

def save_user(username: str, email: str, hashed_password: str):
    """Yeni kullanıcıyı veritabanına kaydeder"""
    fake_db[username] = {
        "username": username,
        "email": email,
        "password": hashed_password
    }

def user_exists(username: str) -> bool:
    """Kullanıcı zaten var mı kontrol eder"""
    return username in fake_db