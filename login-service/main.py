import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import RegisterRequest, LoginRequest
from src.auth import hash_password, check_password, create_token
from src.database import get_user, save_user, user_exists

app = FastAPI()

# ----------------------------
# SAĞLIK KONTROLÜ
# ----------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ----------------------------
# KAYIT
# ----------------------------
@app.post("/register", status_code=201)
async def register(request: RegisterRequest):
    if await user_exists(request.username):
        return JSONResponse(
            status_code=400,
            content={"detail": "Kullanıcı zaten mevcut"}
        )

    await save_user(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password)
    )

    return {"message": "Kullanıcı başarıyla oluşturuldu"}

# ----------------------------
# GİRİŞ
# ----------------------------
@app.post("/login")
async def login(request: LoginRequest):
    user = await get_user(request.username)

    if not user or not check_password(request.password, user["password"]):
        return JSONResponse(
            status_code=401,
            content={"detail": "Kullanıcı adı veya şifre hatalı"}
        )

    token = create_token(str(request.username), request.username)
    return {"token": token}