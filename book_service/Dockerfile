FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Servis 8003 portunda çalışacak şekilde ayarlandı
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]