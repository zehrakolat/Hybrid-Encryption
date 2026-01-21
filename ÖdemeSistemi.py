import uuid
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# --- 1. SATIŞ SUNUCUSU (VERİTABANI VE İŞLEM MERKEZİ) ---
class SatisSunucusu:
    def __init__(self):
        print("[Sunucu] Sistem başlatılıyor... RSA anahtarları üretiliyor.")
        self._private_key = RSA.generate(2048)
        self.public_key = self._private_key.publickey()

        # Basit Veritabanı (Kim ne aldı?)
        self.urun_katalogu = {
            "Urun-A": 100,
            "Urun-B": 250
        }
        # Kullanıcı ve Sahip Olduğu Ürünler Eşleşmesi
        self.satis_kayitlari = {}

    def get_public_key(self):
        return self.public_key

    def satin_alma_islemini_yap(self, kullanici_adi, sifreli_paket):
        print(f"\n[Sunucu] {kullanici_adi} tarafından bir satın alma isteği geldi...")

        try:
            # 1. RSA ile DES anahtarını çöz
            rsa_cipher = PKCS1_OAEP.new(self._private_key)
            des_key = rsa_cipher.decrypt(sifreli_paket['enc_session_key'])

            # 2. DES ile ödeme verisini çöz
            des_iv = sifreli_paket['iv']
            des_cipher = DES.new(des_key, DES.MODE_CBC, des_iv)
            ham_veri = unpad(des_cipher.decrypt(sifreli_paket['sifreli_veri']), DES.block_size)

            # Veriyi parçala: "Urun-A|KartNo"
            veri_str = ham_veri.decode('utf-8')
            istenen_urun, kart_bilgisi = veri_str.split('|')

            print(f"[Sunucu] Ödeme Çözüldü: {kart_bilgisi} ile '{istenen_urun}' alınıyor.")

            # 3. Ürün Stok/Fiyat Kontrolü (Simülasyon)
            if istenen_urun in self.urun_katalogu:
                # --- EŞLEŞTİRME KISMI BURASI ---
                print(f"[Sunucu] ✅ Ödeme Onaylandı. Ürün kullanıcıya tanımlanıyor...")

                # Benzersiz bir lisans kodu üret (UUID)
                lisans_kodu = str(uuid.uuid4()).upper()

                # Veritabanına kaydet (Kullanıcı <-> Ürün Eşleşmesi)
                if kullanici_adi not in self.satis_kayitlari:
                    self.satis_kayitlari[kullanici_adi] = []

                kayit_detayi = {"urun": istenen_urun, "lisans": lisans_kodu}
                self.satis_kayitlari[kullanici_adi].append(kayit_detayi)

                return f"BAŞARILI! '{istenen_urun}' hesabınıza tanımlandı. Lisans Kodunuz: {lisans_kodu}"
            else:
                return "HATA: Böyle bir ürün yok!"

        except Exception as e:
            return f"HATA: İşlem başarısız. ({e})"

    def veritabanini_goster(self):
        print("\n--- GÜNCEL VERİTABANI (KİM NE ALDI?) ---")
        for k, v in self.satis_kayitlari.items():
            print(f"👤 Kullanıcı: {k}")
            for urun in v:
                print(f"   └─ 📦 Ürün: {urun['urun']} (Lisans: {urun['lisans']})")
        print("------------------------------------------")


# --- 2. KULLANICI (MÜŞTERİ) ---
class Kullanici:
    def __init__(self, isim, server_key):
        self.isim = isim
        self.server_key = server_key

    def urun_satin_al(self, urun_adi, kredi_karti):
        print(f"\n[Müşteri: {self.isim}] '{urun_adi}' için ödeme paketi hazırlıyor...")

        # Paketlenecek veri: "UrunAdi|KrediKarti"
        veri = f"{urun_adi}|{kredi_karti}"

        # A. Rastgele DES anahtarı oluştur (8 Byte)
        session_key = get_random_bytes(8)
        iv = get_random_bytes(8)

        # B. DES ile veriyi şifrele
        cipher_des = DES.new(session_key, DES.MODE_CBC, iv)
        sifreli_veri = cipher_des.encrypt(pad(veri.encode('utf-8'), DES.block_size))

        # C. DES anahtarını RSA ile şifrele
        cipher_rsa = PKCS1_OAEP.new(self.server_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Paketi oluştur
        paket = {
            'enc_session_key': enc_session_key,
            'sifreli_veri': sifreli_veri,
            'iv': iv
        }
        return paket


# --- SİMÜLASYON BAŞLIYOR ---

if __name__ == "__main__":
    # 1. Sistemi Kur
    market_sistemi = SatisSunucusu()

    # 2. Kullanıcı Gelir (Ahmet)
    ahmet = Kullanici("Ahmet Yilmaz", market_sistemi.get_public_key())

    # 3. Ahmet, Ürün-A satın alır
    # Ahmet ödeme paketini oluşturur ve gönderir
    odeme_paketi = ahmet.urun_satin_al("Urun-A", "4545-1111-2222-3333")

    # Sunucu işlemi yapar
    sonuc_mesaji = market_sistemi.satin_alma_islemini_yap(ahmet.isim, odeme_paketi)
    print(f"[Müşteri Ekranı]: {sonuc_mesaji}")

    # 4. Başka Bir Kullanıcı Gelir (Ayşe) ve Ürün-B alır
    ayse = Kullanici("Ayse Demir", market_sistemi.get_public_key())
    paket_ayse = ayse.urun_satin_al("Urun-B", "5555-6666-7777-8888")
    sonuc_ayse = market_sistemi.satin_alma_islemini_yap(ayse.isim, paket_ayse)
    print(f"[Müşteri Ekranı]: {sonuc_ayse}")

    # 5. SON DURUM: Veritabanını kontrol edelim
    market_sistemi.veritabanini_goster()