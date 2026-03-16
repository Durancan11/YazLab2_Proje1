# dispatcher/src/router.py
import httpx
import asyncio

SERVICES = {
    "auth": "http://auth_service:8001",
    "borrow": "http://borrowing_service:8002",
    "books": "http://book_service:8003",
    "members": "http://member_service:8004"
}

# Monitor servisinin Docker içindeki adresi
MONITOR_URL = "http://monitor_service:8000/log"

async def send_to_monitor(service, action, status):
    """Monitor servisine arka planda log gönderir"""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(MONITOR_URL, json={
                "service": service.upper(),
                "action": action,
                "status": str(status)
            }, timeout=1.0)
            print(f"📡 Monitor'e log gönderildi: {service} {action}")
    except Exception as e:
        print(f"⚠️ MONITOR HATASI: {e}")

async def forward_request(request, path):
    parts = path.split("/", 1)
    service_key = parts[0]
    sub_path = parts[1] if len(parts) > 1 else ""

    if service_key not in SERVICES:
        return None, "Servis bulunamadı"

    target_url = f"{SERVICES[service_key]}/{sub_path}"
    
    async with httpx.AsyncClient() as client:
        try:
            headers = dict(request.headers)
            headers.pop("host", None) 
            
            resp = await client.request(
                method=request.method,
                url=target_url,
                content=await request.body(),
                headers=headers,
                timeout=15.0
            )
            
            # 🔥 O 's' harfi silindi ve log görevi temizce eklendi
            asyncio.create_task(send_to_monitor(service_key, f"{request.method} /{sub_path}", resp.status_code))
            
            return resp, None
        except Exception as e:
            # Hata durumunda da monitor'e haber verelim
            asyncio.create_task(send_to_monitor(service_key, f"{request.method} /{sub_path}", "Error"))
            print(f"❌ Forward Hatası: {e}")
            return None, "Servis şu an ulaşılamıyor"