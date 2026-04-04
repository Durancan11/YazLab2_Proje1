📚 Micro-Lib: Dağıtık Mikroservis Tabanlı Kütüphane Yönetim Sistemi

1. Proje Bilgileri
Proje Adı: Mikroservis Mimarisi ve API Gateway (Dispatcher) Uygulaması
Ekip Üyeleri:
Duran Can Demirezen (211307037)
Ömer Şerif Yapıcıoğlu (211307062)
Tarih: 4 Nisan 2026
Kurum: Kocaeli Üniversitesi - Bilişim Sistemleri Mühendisliği (Yazılım Geliştirme Laboratuvarı II - Proje I)

2. Giriş
Problemin Tanımı

Geleneksel monolitik mimarilerde tüm sistem tek bir yapı altında çalıştığı için, herhangi bir modülde oluşan hata tüm sistemi etkileyebilmektedir. Ayrıca bu mimarilerde ölçeklendirme ve bakım süreçleri oldukça zordur.

Bu projede kütüphane yönetim sistemi; kitap işlemleri, kullanıcı yönetimi ve ödünç alma gibi temel fonksiyonlar birbirinden bağımsız mikroservisler halinde tasarlanmıştır. Böylece sistemde oluşabilecek hataların yayılması engellenmiş ve "Single Point of Failure" riski azaltılmıştır.

Amaç
Merkezi kontrol: Dispatcher (API Gateway) ile tüm istekleri tek noktadan yönetmek
Güvenlik: Mikroservisleri dış dünyadan izole ederek sadece gateway üzerinden erişim sağlamak
Veri izolasyonu: Her mikroservisin kendi bağımsız NoSQL (MongoDB) veritabanına sahip olması

3. Tasarım ve Teknik Altyapı

RESTful Servisler

REST (Representational State Transfer), istemci-sunucu iletişimini standart HTTP metotları üzerinden gerçekleştiren bir mimari yaklaşımdır.

Bu projede kullanılan HTTP metotları:

GET → veri alma
POST → veri ekleme
PUT → veri güncelleme
DELETE → veri silme
Richardson Olgunluk Modeli (RMM)

Sistem, Richardson Olgunluk Modeli’ne göre Level 2 seviyesinde tasarlanmıştır:

Level 0-1: Kaynaklar URL ile ayrılmıştır
/books, /auth, /borrow
Level 2: HTTP metotları ve durum kodları aktif kullanılmıştır
200 OK
401 Unauthorized
502 Bad Gateway

Sistem Akışı (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    participant U as Kullanıcı
    participant D as Dispatcher (Gateway)
    participant A as Auth Service (NoSQL)
    participant B as Book Service (NoSQL)

    U->>D: POST /books/add (JWT Token ile)
    D->>D: Yetki Kontrolü (Token parse)
    D->>A: Token Doğrulama Sorgusu
    A-->>D: HTTP 200 (Geçerli Kullanıcı)
    D->>B: İstek Yönlendirme (Forwarding)
    B-->>D: HTTP 201 Created (JSON)
    D-->>U: Başarılı Yanıt

    Sınıf Yapısı (Genel Mantık)

Dispatcher → yönlendirme + yetkilendirme
Auth Service → kullanıcı doğrulama
Book Service → kitap işlemleri
Borrowing Service → ödünç alma işlemleri
Karmaşıklık Analizi
Dispatcher yönlendirme: O(n)
Veritabanı sorguları:
Ortalama: O(1)
En kötü: O(log n)
4. Sistem Modülleri
Mikroservis Mimarisi

```mermaid
graph LR
    subgraph Gateway
        D[Dispatcher]
    end

    subgraph Microservices
        A[Auth Service]
        B[Book Service]
        BR[Borrowing Service]
    end

    subgraph Database
        ADB[(Auth DB)]
        BDB[(Book DB)]
        BRDB[(Borrow DB)]
    end

    D --> A
    D --> B
    D --> BR

    A --> ADB
    B --> BDB
    BR --> BRDB

    Modüllerin Görevleri
Dispatcher:
Tüm istekleri karşılar, doğrular ve ilgili servise yönlendirir
Auth Service:
Kullanıcı kayıt ve giriş işlemlerini yönetir
Book Service:
Kitap ekleme, silme, listeleme işlemlerini yapar
Borrowing Service:
Kitap ödünç alma ve iade işlemlerini yönetir
Monitor Service:
Sistem trafiğini loglar ve görselleştirir

## 5. Uygulama Açıklamaları ve Testler

### 🧪 TDD (Test Driven Development) Yaklaşımı
Projenin en kritik güvenlik katmanları olan Dispatcher ve Yetkilendirme protokolleri, TDD döngüsüne (Red-Green-Refactor) sadık kalınarak geliştirilmiştir. Dağıtım öncesi tüm fonksiyonlar Pytest ile doğrulanmıştır.

> **Test Sonuçları (Pytest):**
> ![Pytest Test Sonuçları](ss1.png)
> *Görsel 1: Dispatcher güvenlik ve sağlık kontrolü testlerinin %100 başarıyla tamamlanması.*

### 📡 Sistem İzleme ve Loglama (Monitor)
Geliştirilen Monitor Service sayesinde, sistem üzerinden geçen tüm trafik (URL, Metot, Durum Kodu ve Zaman Damgası) anlık olarak takip edilebilmektedir. Bu, hata ayıklama ve sistem analizi için kritik öneme sahiptir.

> **Canlı Trafik İzleme:**
> ![Monitor Paneli](ss2.png)
> *Görsel 2: Mikroservisler arası iletişimin ve kullanıcı isteklerinin anlık loglanması.*

### 💣 Performans ve Yük Testleri (Locust)
Sistemin dayanıklılık sınırlarını belirlemek amacıyla Locust aracı ile iki farklı senaryo uygulanmıştır.

#### Senaryo 1: Stabilite Testi (100 Eşzamanlı Kullanıcı)
Sistem 100 kullanıcı altında stabil çalışmakta, yanıt süreleri kabul edilebilir sınırlarda kalmaktadır.
> ![Locust 100 User](ss3.png)
![Locust 500 User](ss4.png)
> *Görsel 3-4: 100 kullanıcı simülasyonunda %0 hata oranı ve RPS değerleri.*

#### Senaryo 2: Stres ve Limit Testi (500 Eşzamanlı Kullanıcı)
Sistemin limit noktası (Break-point) tespit edilmiştir. Donanım kaynaklı darboğazlar ve artan gecikme süreleri raporlanmıştır.
> ![Locust 500 User](ss5.png)
> *Görsel 5: 500 kullanıcı altında sistemin stres durumu ve hata grafiklerinin analizi.*


6. Sonuç ve Tartışma
Başarılar
Mikroservisler tamamen izole edildi
Tüm trafik tek noktadan kontrol edildi
Merkezi loglama sağlandı
Sınırlılıklar
500+ kullanıcıda performans düşüşü
Gateway tek noktada darboğaz oluşturabilir
Gelecek Geliştirmeler
Redis ile caching eklenebilir
Kubernetes ile yatay ölçekleme yapılabilir
Load balancer entegrasyonu sağlanabilir