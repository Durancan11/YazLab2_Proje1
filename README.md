# 📚 Micro-Lib: Dağıtık Mikroservis Tabanlı Kütüphane Yönetim Sistemi

![Status](https://img.shields.io/badge/status-active-success)
![Architecture](https://img.shields.io/badge/architecture-microservices-blue)
![Backend](https://img.shields.io/badge/backend-python-yellow)
![Database](https://img.shields.io/badge/database-mongodb-green)

---

## Proje Bilgileri

* **Proje Adı:** Mikroservis Mimarisi ve API Gateway (Dispatcher)
* **Ekip:**

  * Duran Can Demirezen (211307037)
  * Ömer Şerif Yapıcıoğlu (211307062)
* **Tarih:** 4 Nisan 2026
* **Kurum:** Kocaeli Üniversitesi Bilişim Sistemleri Mühendisliği - Yazılım Geliştirme Laboratuvarı II

---

## Proje Amacı

Bu projede monolitik sistemlerin yerine **mikroservis mimarisi** kullanılarak:

* Sistem çökmesini önlemek
* Ölçeklenebilirlik sağlamak
* Güvenliği artırmak
* Servisleri birbirinden bağımsız hale getirmek

amaçlanmıştır.

---

## Problemin Tanımı

Monolitik yapılarda:

* Tek hata tüm sistemi çökertir ❌
* Güncelleme zor ❌
* Ölçekleme sıkıntılı ❌

Bu projede:
✔ Servisler ayrıldı
✔ Gateway eklendi
✔ Sistem modüler hale getirildi

---

## Kullanılan Teknolojiler

* Python (FastAPI / Flask)
* MongoDB (NoSQL)
* REST API
* JWT Authentication
* Locust (Load Test)
* Pytest (Unit Test)

---

## API Yapısı

| Endpoint       | Method | Açıklama         |
| -------------- | ------ | ---------------- |
| /auth/login    | POST   | Kullanıcı girişi |
| /auth/register | POST   | Kullanıcı kayıt  |
| /books         | GET    | Kitap listele    |
| /books/add     | POST   | Kitap ekle       |
| /borrow        | POST   | Kitap ödünç al   |

---

## Sistem Akışı (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    participant U as Kullanıcı
    participant D as Dispatcher
    participant A as Auth Service
    participant B as Book Service

    U->>D: POST /books/add (JWT)
    D->>A: Token doğrula
    A-->>D: OK
    D->>B: isteği ilet
    B-->>D: başarı
    D-->>U: response
```

---

## Mikroservis Mimarisi

```mermaid
graph LR
    D[Dispatcher]

    A[Auth Service]
    B[Book Service]
    BR[Borrow Service]

    DB1[(Auth DB)]
    DB2[(Book DB)]
    DB3[(Borrow DB)]

    D --> A
    D --> B
    D --> BR

    A --> DB1
    B --> DB2
    BR --> DB3
```

---

## Sistem Modülleri

* **Dispatcher:** tüm trafiği yönetir
* **Auth Service:** kullanıcı doğrulama
* **Book Service:** kitap işlemleri
* **Borrow Service:** ödünç sistemi
* **Monitor Service:** log ve analiz

---

## Karmaşıklık Analizi

* Routing: **O(n)**
* Database:

  * Ortalama: **O(1)**
  * Worst: **O(log n)**

---

## Testler

## Pytest Test Sonuçları

<p align="center">
  <img src="images/ss1.png" width="700"/>
</p>

> 📌 Tüm testler başarıyla geçmiştir.

---

### Monitor Paneli (Loglama)

<p align="center">
  <img src="images/ss2.png" width="700"/>
</p>

> 📌 Sistem trafiği anlık olarak izlenmektedir.

---

## Performans Testi (Locust)

## 100 Kullanıcı Testi

<p align="center">
  <img src="images/ss3.png" width="700"/>
</p>

<p align="center">
  <img src="images/ss4.png" width="700"/>
</p>

> 📌 %0 hata oranı ile stabil çalışmıştır.

---

### 500 Kullanıcı (Stres Testi)

<p align="center">
  <img src="images/ss5.png" width="700"/>
</p>

> 📌 Sistem limit noktası gözlemlenmiştir.

---

## Başarılar

✔ Mikroservis izolasyonu
✔ Güvenli API Gateway
✔ Merkezi loglama

---

## Sınırlılıklar

* Gateway bottleneck olabilir
* Yük altında performans düşer

---

## Gelecek Geliştirmeler

* Redis Cache
* Kubernetes deployment
* Load Balancer
* CI/CD pipeline

---

## GitHub

Repo: https://github.com/Durancan11/YazLab2_Proje1

---
