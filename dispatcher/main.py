from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.auth import verify_token
from src.router import forward_request, send_to_monitor # 📡 Habercimizi çağırdık
import asyncio

app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def dispatcher(request: Request, path: str):
    # 1. AUTH SERVİSİ (Zaten log gönderiyor)
    if path.startswith("auth/"):
        response, error = await forward_request(request, path)
        if error: return JSONResponse(status_code=502, content={"detail": error})
        return JSONResponse(status_code=response.status_code, content=response.json())

    # 2. TOKEN DOĞRULAMA (İşte burayı düzelttik!)
    payload, error = verify_token(request)
    if error:
        # 🔥 TOKEN YOKSA BİLE MONİTÖRE HABER VER!
        service_name = path.split("/")[0] if "/" in path else "system"
        asyncio.create_task(send_to_monitor(service_name, f"{request.method} /{path}", "401-Unauthorized"))
        return JSONResponse(status_code=401, content={"detail": error})

    # 3. NORMAL İSTEK İLETİMİ
    response, error = await forward_request(request, path)
    if error: return JSONResponse(status_code=404, content={"detail": error})
    return JSONResponse(status_code=response.status_code, content=response.json())