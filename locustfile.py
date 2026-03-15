from locust import HttpUser, task, between

class LibraryUser(HttpUser):
    # Kullanıcılar arası bekleme süresi (1-2 saniye)
    wait_time = between(1, 2)
    token = ""

    def on_start(self):
        """Her sanal kullanıcı test başında otomatik login olur"""
        payload = {
            "username": "can",
            "password": "123"
        }
        # Auth servisine giriş isteği atıyoruz
        with self.client.post("/auth/login", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                print("Başarıyla giriş yapıldı, token alındı.")
            else:
                response.failure(f"Giriş Başarısız: {response.text}")
                print(f"HATA: Giriş yapılamadı! Durum kodu: {response.status_code}")

    @task(3)
    def check_borrows(self):
        """Ödünç alınan kitapları listeleme testi"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/borrow/borrow", headers=headers)

    @task(1)
    def create_borrow(self):
        """Kitap ödünç alma testi"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "user_id": 1,
                "book_id": 101,
                "days": 14
            }
            self.client.post("/borrow/borrow", json=payload, headers=headers)