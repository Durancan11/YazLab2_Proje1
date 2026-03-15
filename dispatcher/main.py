from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.auth import verify_token
from src.router import forward_request

app = FastAPI()

# ----------------------------
# SAĞLIK KONTROLÜ
# ----------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ----------------------------
# ANA YÖNLENDİRİCİ
# ----------------------------
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def dispatcher(request: Request, path: str):

    # 1. Token doğrula
    payload, error = verify_token(request)
    if error:
        return JSONResponse(status_code=401, content={"detail": error})

    # 2. İsteği ilgili servise ilet
    response, error = await forward_request(request, path)
    if error == "Servis bulunamadı":
        return JSONResponse(status_code=404, content={"detail": error})
    if error == "Servis şu an ulaşılamıyor":
        return JSONResponse(status_code=502, content={"detail": error})

    # 3. Servisin cevabını geri döndür
    return JSONResponse(
        status_code=response.status_code,
        content=response.json()
    )