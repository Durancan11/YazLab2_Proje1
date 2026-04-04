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