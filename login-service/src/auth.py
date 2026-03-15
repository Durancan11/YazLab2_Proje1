import os
import jwt
import bcrypt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "test_secret")

def hash_password(password: str) -> str:
    """Şifreyi güvenli hale getirir"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password: str, hashed: str) -> bool:
    """Girilen şifre ile kayıtlı şifreyi karşılaştırır"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_token(user_id: str, username: str) -> str:
    """Kullanıcı için JWT token oluşturur"""
    payload = {
        "user_id": user_id,
        "username": username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")