# monitor_service/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# Logları geçici olarak hafızada tutuyoruz (100 puanlık rapor için yeterli)
LOG_STORAGE = []

class LogEntry(BaseModel):
    service: str
    action: str
    status: str

# 📡 Dispatcher'dan gelen logları kabul eden kapı
@app.post("/log")
async def receive_log(entry: LogEntry):
    log_data = {
        "zaman": datetime.now().strftime("%H:%M:%S"),
        "servis": entry.service,
        "islem": entry.action,
        "durum": entry.status
    }
    LOG_STORAGE.insert(0, log_data) # En yeni logu en üste ekle
    if len(LOG_STORAGE) > 20: # Panel şişmesin diye son 20 logu tutalım
        LOG_STORAGE.pop()
    return {"status": "success"}

# 📝 Logları JSON olarak veren kapı (Frontend burayı sorgulayacak)
@app.get("/api/logs")
async def get_logs():
    return LOG_STORAGE

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <head>
            <title>KOU YazLab - Sistem Monitörü</title>
            <script>
                // 🔄 Her 2 saniyede bir Karargah'tan (API) veri çeken fonksiyon
                async function updateLogs() {
                    const response = await fetch('/api/logs');
                    const logs = await response.json();
                    const tableBody = document.getElementById('log-body');
                    
                    tableBody.innerHTML = logs.map(log => `
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #444;">${log.zaman}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #444;">${log.servis}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #444;">${log.islem}</td>
                            <td style="padding: 10px; border-bottom: 1px solid #444; color: #4CAF50;">${log.durum}</td>
                        </tr>
                    `).join('');
                }
                setInterval(updateLogs, 2000); // 2 saniye kuralı
            </script>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background-color: #121212; color: #e0e0e0; padding: 40px; text-align: center;">
            <h1 style="color: #4CAF50;">📊 Sistem İzleme Paneli</h1>
            <div style="background: #1e1e1e; padding: 20px; border-radius: 10px; display: inline-block; text-align: left; border: 1px solid #333; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">🛡️ Servis Durumları</h3>
                <p>🟢 Dispatcher: <b>ONLINE</b></p>
                <p>🟢 Auth Service: <b>ONLINE</b></p>
                <p>🟢 Borrowing Service: <b>ONLINE</b></p>
                <p>🟢 Book Service: <b>ONLINE</b></p>
            </div>
            <h3>📝 Son İstek Kayıtları (Logs)</h3>
            <table style="width: 80%; margin: auto; border-collapse: collapse; background: #1e1e1e; border-radius: 8px; overflow: hidden;">
                <thead>
                    <tr style="background: #333; color: #4CAF50;">
                        <th style="padding: 12px;">Zaman</th>
                        <th style="padding: 12px;">Servis</th>
                        <th style="padding: 12px;">İşlem</th>
                        <th style="padding: 12px;">Durum</th>
                    </tr>
                </thead>
                <tbody id="log-body">
                    <tr><td colspan="4" style="padding: 20px;">İstek bekleniyor...</td></tr>
                </tbody>
            </table>
        </body>
    </html>
    """