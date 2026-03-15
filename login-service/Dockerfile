FROM python:3.12-slim
WORKDIR /app
# requirements.txt dosyasını kopyalıyoruz
COPY requirements.txt .
# Tüm kütüphaneleri listeden yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]