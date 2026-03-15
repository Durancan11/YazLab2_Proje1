import os
import jwt
from fastapi import Request
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "test_secret")

def verify_token(request: Request):
    """
    İstekteki JWT token'ı doğrular.
    Geçerliyse payload döner, geçersizse hata mesajı döner.
    """
    auth_header = request.headers.get("Authorization")

    # Token hiç gönderilmemiş
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, "Token bulunamadı"

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token süresi dolmuş"
    except jwt.InvalidTokenError:
        return None, "Geçersiz token"