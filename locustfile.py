from locust import HttpUser, task, between

class YazLabUser(HttpUser):
    wait_time = between(1, 2)
    token = ""

    def on_start(self):
        """Her bot önce kayıt olur ve giriş yapıp token alır"""
        # Önce kayıt (Eğer varsa hata verir ama sorun değil)
        self.client.post("/auth/register", json={
            "username": "bot_user", "password": "123", "email": "bot@test.com"
        })
        # Giriş yap ve tokenı al
        response = self.client.post("/auth/login", json={
            "username": "bot_user", "password": "123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")

    @task(3)
    def list_books(self):
        """Kitapları listele (Token ile)"""
        self.client.get("/books/books", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def check_health(self):
        """Sistem sağlığını kontrol et"""
        self.client.get("/health")