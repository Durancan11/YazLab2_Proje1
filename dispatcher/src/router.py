# dispatcher/src/router.py
import httpx

SERVICES = {
    "auth": "http://auth_service:8001",
    "borrow": "http://borrowing_service:8002", # Docker-compose'daki servis adı ve portu
    "books": "http://book_service:8003"
}

async def forward_request(request, path):
    parts = path.split("/", 1)
    service_key = parts[0]
    sub_path = parts[1] if len(parts) > 1 else ""

    if service_key not in SERVICES:
        return None, "Servis bulunamadı"

    target_url = f"{SERVICES[service_key]}/{sub_path}"
    
    # 🟢 HATA AYIKLAMA İÇİN LOG EKLEYELİM
    print(f"DEBUG: {target_url} adresine istek atılıyor...")

    async with httpx.AsyncClient() as client:
        try:
            # ÖNEMLİ: 'host' başlığını silelim ki hedef servis şaşırmasın
            headers = dict(request.headers)
            headers.pop("host", None) 
            
            resp = await client.request(
                method=request.method,
                url=target_url,
                content=await request.body(),
                headers=headers,
                timeout=10.0
            )
            return resp, None
        except Exception as e:
            # 🔴 TAM HATAYI TERMİNALDE GÖRMEK İÇİN:
            print(f"BAĞLANTI HATASI: {str(e)}")
            return None, "Servis şu an ulaşılamıyor"