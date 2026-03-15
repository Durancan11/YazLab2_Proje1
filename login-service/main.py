from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import RegisterRequest, LoginRequest
from src.auth import hash_password, check_password, create_token

app = FastAPI()

# Geçici kullanıcı deposu (MongoDB'ye bağlanana kadar)
fake_db = {}

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
    if request.username in fake_db:
        return JSONResponse(status_code=400, content={"detail": "Kullanıcı zaten mevcut"})

    fake_db[request.username] = {
        "username": request.username,
        "email": request.email,
        "password": hash_password(request.password)
    }

    return {"message": "Kullanıcı başarıyla oluşturuldu"}

# ----------------------------
# GİRİŞ
# ----------------------------
@app.post("/login")
async def login(request: LoginRequest):
    user = fake_db.get(request.username)

    if not user or not check_password(request.password, user["password"]):
        return JSONResponse(status_code=401, content={"detail": "Kullanıcı adı veya şifre hatalı"})

    token = create_token(str(request.username), request.username)
    return {"token": token}