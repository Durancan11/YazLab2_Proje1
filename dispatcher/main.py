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

    # 1. AUTH SERVİSİ İÇİN (TOKENSIZ) GEÇİŞ
    if path.startswith("auth/"):
        response, error = await forward_request(request, path) 
        if error:
            return JSONResponse(status_code=502, content={"detail": error})
        
        # Güvenli JSON Çözme
        try:
            resp_content = response.json()
        except Exception:
            resp_content = {"detail": response.text or "Auth servisinden gecersiz yanıt."}

        return JSONResponse(
            status_code=response.status_code, 
            content=resp_content
        )

    # 2. DİĞER SERVİSLER İÇİN TOKEN DOĞRULAMA
    payload, error = verify_token(request)
    if error:
        return JSONResponse(status_code=401, content={"detail": error})

    # 3. İSTEĞİ İLGİLİ SERVİSE İLET
    response, error = await forward_request(request, path)
    
    if error == "Servis bulunamadı":
        return JSONResponse(status_code=404, content={"detail": error})
    if error == "Servis şu an ulaşılamıyor":
        return JSONResponse(status_code=502, content={"detail": error})

    # 4. SERVİS CEVABINI GÜVENLİ ŞEKİLDE DÖNDÜR
    try:
        # Eğer servis düzgün bir JSON döndürdüyse onu al
        resp_content = response.json()
    except Exception:
        # Eğer servis boş döndüyse veya JSON değilse patlamadan hatayı al
        resp_content = {"detail": response.text or "Servis bos veya gecersiz bir yanıt döndü."}

    return JSONResponse(
        status_code=response.status_code,
        content=resp_content
    )