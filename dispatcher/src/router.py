import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# Hangi URL hangi servise gidecek
ROUTES = {
    "books": os.getenv("BOOK_SERVICE_URL", "http://localhost:8002"),
    "members": os.getenv("MEMBER_SERVICE_URL", "http://localhost:8003"),
    "borrow": os.getenv("BORROW_SERVICE_URL", "http://localhost:8004"),
    "auth": os.getenv("LOGIN_SERVICE_URL", "http://localhost:8001"),
}

def find_target_url(path: str):
    """
    Gelen URL'e bakarak hangi servise gideceğini bulur.
    Örnek: 'books/1' → BOOK_SERVICE_URL
    """
    for route, url in ROUTES.items():
        if path.startswith(route):
            return url
    return None

async def forward_request(request, path: str):
    """
    İsteği ilgili servise iletir ve cevabı geri döner.
    """
    target_url = find_target_url(path)

    if not target_url:
        return None, "Servis bulunamadı"

    full_url = f"{target_url}/{path}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=full_url,
                headers=dict(request.headers),
                content=await request.body()
            )
            return response, None
    except httpx.ConnectError:
        return None, "Servis şu an ulaşılamıyor"