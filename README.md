# 🛡️ Secure E-Commerce Simulation (Hybrid Encryption)

Bu proje, Python kullanılarak geliştirilmiş, **Hibrit Kriptografi** (Simetrik ve Asimetrik şifreleme) prensiplerini simüle eden bir E-Ticaret ve Dijital Hak Yönetimi (DRM) sistemidir.

## 🚀 Özellikler

- **RSA (2048-bit):** Anahtar değişimi (Key Exchange) ve kimlik doğrulama için kullanılır.
- **DES (CBC Mode):** Veri şifreleme (Data Encryption) için kullanılır (Eğitim amaçlı, legacy sistem simülasyonu).
- **PKCS1_OAEP:** RSA şifrelemesi için güvenli dolgu (padding) şeması.
- **Lisanslama Sistemi:** Satın alma işlemi sonrası kullanıcıya özel benzersiz UUID lisans anahtarı üretir.
- **Nesne Yönelimli Programlama (OOP):** Sunucu ve İstemci yapıları sınıf (class) tabanlı ayrılmıştır.

## 🛠️ Kurulum

Projeyi çalıştırmak için gerekli kütüphaneyi yükleyin:

```bash
pip install -r requirements.txt
💻 Kullanım
Sistemi başlatmak için terminalde şu komutu çalıştırın:

Bash

python main.py
📚 Senaryo
Sunucu başlatılır ve RSA anahtar çiftini üretir.

Müşteri, satın almak istediği ürünü seçer.

Kredi kartı bilgileri ve ürün bilgisi DES ile şifrelenir.

DES anahtarı, Sunucunun Public Key'i ile şifrelenir (Hibrit yapı).

Sunucu paketi çözer, ödemeyi onaylar ve kullanıcıya Lisans Anahtarı teslim eder.


---

### 2. Adım: GitHub'da Depo (Repository) Aç

1.  GitHub hesabına gir.
2.  Sağ üstten **+** işaretine tıkla ve **"New repository"** de.
3.  **Repository name:** `Hybrid-Encryption-Payment-System` (veya benzer bir isim).
4.  **Public** seç.
5.  "Add a README file" kutucuğunu **işaretleme** (çünkü biz zaten oluşturduk).
6.  **"Create repository"** butonuna bas.

---

### 3. Adım: Terminal ile Yükle (Mac için)

Mac terminalini aç ve sırasıyla şu komutları gir (Kendi GitHub kullanıcı adını ve repo linkini kullanmayı unutma):

```bash
# 1. Proje klasörüne git (Masaüstündeyse)
cd Desktop/ProjeKlasorununAdi

# 2. Git'i başlat
git init

# 3. Dosyaları sahneye al (Hepsini seçer)
git add .

# 4. İlk kaydı oluştur
git commit -m "Initial commit: Hibrit ödeme sistemi simülasyonu eklendi"

# 5. Ana dalı 'main' olarak ayarla
git branch -M main

# 6. Uzak sunucuyu (GitHub) ekle 
# (GitHub'da repo oluşturunca sana verilen https linkini aşağıya yapıştır)
git remote add origin https://github.com/KULLANICI_ADIN/REPO_ADIN.git

# 7. Kodları gönder
git push -u origin main
