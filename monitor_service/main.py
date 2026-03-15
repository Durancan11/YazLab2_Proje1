from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Sistem durumunu ve logları simüle eden bir dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <head><title>KOU YazLab - Sistem Monitörü</title></head>
        <body style="font-family: Arial; background-color: #1a1a1a; color: white; padding: 20px;">
            <h1 style="color: #4CAF50;">🛡️ Microservices Monitoring Dashboard</h1>
            <hr>
            <h3>✅ Sistem Durumu (Health Check)</h3>
            <ul>
                <li>Dispatcher (Port 8080): <b style="color: #4CAF50;">ONLINE</b></li>
                <li>Auth Service (Port 8001): <b style="color: #4CAF50;">ONLINE</b></li>
                <li>Borrowing Service (Port 8002): <b style="color: #4CAF50;">ONLINE</b></li>
                <li>Book Service (Port 8003): <b style="color: #4CAF50;">ONLINE</b></li>
            </ul>
            <h3>📊 Son Trafik Akışı (Logs)</h3>
            <table border="1" style="width:100%; text-align:left; border-collapse: collapse;">
                <tr style="background-color: #333;"><th>Timestamp</th><th>Service</th><th>Endpoint</th><th>Status</th></tr>
                <tr><td>18:45:01</td><td>DISPATCHER</td><td>/books/list</td><td>200 OK</td></tr>
                <tr><td>18:45:10</td><td>AUTH</td><td>/auth/login</td><td>201 Created</td></tr>
                <tr><td>18:45:22</td><td>BORROW</td><td>/borrow/create</td><td>201 Created</td></tr>
            </table>
        </body>
    </html>
    """