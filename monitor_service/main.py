from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <head><title>KOU YazLab - Sistem Monitörü</title></head>
        <body style="font-family: sans-serif; background-color: #121212; color: #e0e0e0; padding: 40px; text-align: center;">
            <h1 style="color: #4CAF50;">📊 Sistem İzleme Paneli</h1>
            <div style="background: #1e1e1e; padding: 20px; border-radius: 10px; display: inline-block; text-align: left;">
                <h3>🛡️ Servis Durumları</h3>
                <p>🟢 Dispatcher: <b>ONLINE</b></p>
                <p>🟢 Auth Service: <b>ONLINE</b></p>
                <p>🟢 Borrowing Service: <b>ONLINE</b></p>
                <p>🟢 Book Service: <b>ONLINE</b></p>
            </div>
            <h3>📝 Son İstek Kayıtları (Logs)</h3>
            <table border="1" style="width: 80%; margin: auto; border-collapse: collapse;">
                <tr style="background: #333;"><th>Zaman</th><th>Servis</th><th>İşlem</th><th>Durum</th></tr>
                <tr><td>18:55</td><td>DISPATCHER</td><td>GET /books</td><td>200 OK</td></tr>
                <tr><td>18:56</td><td>AUTH</td><td>POST /login</td><td>201 Created</td></tr>
            </table>
        </body>
    </html>
    """