Geliştiriciler: 
Duran Can Demirezen 211307037
Ömer Şerif Yapıcıoğlu 211307062

📚 YazLab 2 - Mikroservis Tabanlı Kütüphane Yönetim Sistemi
Bu proje, Kocaeli Üniversitesi Bilişim Sistemleri Mühendisliği Yazılım Geliştirme Laboratuvarı II kapsamında geliştirilmiş; yüksek erişilebilirlik, güvenlik ve izlenebilirlik odaklı bir mikroservis mimarisidir.

🏗️ Sistem Mimarisi
Sistem, birbirleriyle izole ağlar üzerinden haberleşen 5 ana servis ve 3 NoSQL veritabanından oluşmaktadır:

Dispatcher (API Gateway): Sistemin giriş kapısıdır. Tüm istekleri karşılar, JWT (JSON Web Token) doğrulaması yapar ve istekleri ilgili servislere yönlendirir.

Auth Service: Kullanıcı kayıt (Register) ve giriş (Login) işlemlerini yönetir, güvenli token üretir.

Book Service: Kitap envanterini ve CRUD işlemlerini yönetir.

Borrowing Service: Kitap ödünç alma ve iade süreçlerini takip eder.

Monitor Service (Dashboard): Sistemdeki tüm trafiği (başarılı/başarısız) gerçek zamanlı olarak izleyen merkezi log merkezidir.

🛠️ Kullanılan Teknolojiler
Backend: Python 3.14, FastAPI (Asenkron mimari)

Konteynerizasyon: Docker & Docker Compose

Veritabanı: MongoDB (Her servis için izole veritabanı)

Test & Analiz: Locust (Yük ve Stres Testi)

Haberleşme: HTTP/REST & Asenkron Loglama

🚀 Sistemi Çalıştırma
Tüm sistemi tek bir komutla ayağa kaldırabilirsiniz:

Bash
docker-compose up --build -d
API Gateway: http://localhost:8080

İzleme Paneli (Dashboard): http://localhost:8081

Locust Test Arayüzü: http://localhost:8089

🔒 Güvenlik ve Doğrulama (JWT)
Sistem "Zero Trust" prensibiyle çalışır. auth/ dışındaki tüm servislere erişim için geçerli bir Bearer Token zorunludur.

POST /auth/register ile kayıt olunur.

POST /auth/login ile giriş yapılıp access_token alınır.

İsteklerin Authorization başlığına Bearer <token> eklenerek servislere erişilir.

📊 İzlenebilirlik (Monitoring)
Geliştirilen Monitor Service, sistemdeki tüm mikroservislerden gelen sinyalleri yakalar.

401 Unauthorized: Yetkisiz erişim denemeleri anında loglanır.

200 OK: Başarılı işlemler yeşil statüyle takip edilir.

422 Unprocessable Entity: Hatalı veri girişleri (Validation) izlenebilir.

💣 Performans ve Stres Testi (Locust)
Sistem, 100 eşzamanlı kullanıcı ve saniyede 10 yeni kullanıcı artış hızıyla test edilmiştir.

Ortalama RPS: ~55-60

Başarı Oranı: %100 (Doğru token ile yapılan isteklerde)

Güvenlik Testi: Tokensız yapılan binlerce istek, Dispatcher tarafından başarıyla bloklanmış ve izleme panelinde raporlanmıştır.
