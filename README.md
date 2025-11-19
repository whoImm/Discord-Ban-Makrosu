![Banner](https://i.hizliresim.com/3zhwn12.png)

# DİSCORD BAN MAKROSU

---

**Discord Oto Ban Makrosu**, Discord sunucuları için Python ile yazılmış otomatik ban yönetim aracıdır. Modern koyu temalı arayüzü ile kullanıcıların toplu ban işlemlerini klavye makroları ile gerçekleştirmesine olanak tanır.
| | |
| - | - |
| **Temel İşlevler** | **Sistem Tasarımı** |
| <table><tr><td>Otomatik Ban</td><td>/yasakla komutu ile klavye makrosu</td></tr><tr><td>Toplu İşlem</td><td>Çoklu kullanıcı ID'leri için sıralı ban</td></tr><tr><td>ID Yönetimi</td><td>JSON tabanlı kullanıcı ID depolama sistemi</td></tr><tr><td>Hız Kontrolü</td><td>Ayarlanabilir ban aralıkları (0.5-10 saniye)</td></tr></table> | <table><tr><td>Platform</td><td>Windows (Python 3.11+)</td></tr><tr><td>Arayüz</td><td>Tkinter tabanlı koyu tema GUI</td></tr><tr><td>Makro Sistemi</td><td>Modüler makro desteği</td></tr><tr><td>Güvenlik Özellikleri</td><td>3 saniye hazırlık süresi</td></tr></table> |
---

## Özellikler
| | | |
| - | - | - |
| **Otomasyon** | **Güvenlik & Kontrol** | **Arayüz & Kullanıcı Deneyimi** |
| <table><tr><td>Otomatik Komut</td><td>/yasakla + tab + ID + enter dizisi</td></tr><tr><td>Toplu İşlemler</td><td>Çoklu ID'leri otomatik işleme</td></tr><tr><td>Makro Sistemi</td><td>Özelleştirilebilir komut dizileri</td></tr><tr><td>Zamanlı Gecikmeler</td><td>Her adım arasında 0.5s bekleme</td></tr></table> | <table><tr><td>Güvenlik Gecikmesi</td><td>3 saniye hazırlık penceresi</td></tr><tr><td>Hata Yönetimi</td><td>Kapsamlı hata tespiti</td></tr><tr><td>Hız Kontrolü</td><td>Ayarlanabilir işlem hızı</td></tr><tr><td>Giriş Doğrulama</td><td>ID formatı doğrulaması</td></tr></table> | <table><tr><td>Koyu Tema</td><td>Gri-siyah modern arayüz</td></tr><tr><td>Sayfa Sistemi</td><td>Ana ve bilgi sayfası geçişi</td></tr><tr><td>Türkçe Arayüz</td><td>Tamamen Türkçe kullanıcı arayüzü</td></tr><tr><td>Responsive Tasarım</td><td>600x650 pencere boyutu</td></tr></table> |
---


| Bileşen | Açıklama |
|------------|-------------|
|  **Dil** | Python 3.11+ |
|  **GUI Framework** | Tkinter |
|  **Otomasyon** | pynput, keyboard |
|  **Görüntü İşleme** | Pillow (PIL) |
|  **Veri Depolama** | JSON |
|  **Platform** | Windows |
---
## Kurulum
### Otomatik Kurulum
1. Tüm dosyaları bir klasöre çıkarın
2. "baslat.bat" dosyasına çift tıklayın
3. Otomatik kurulumun tamamlanmasını bekleyin
4. Ana uygulama otomatik olarak başlayacak

# Kullanım

1. `baslat.bat` dosyasını çalıştırın.
2. Program kullanılabilir makroları içeren bir menü gösterecek:
   - Otoban Saniye - 0.5sn Beklemeli
   - (Ek makrolar sunucular/ klasörüne eklenebilir)
3. İstediğiniz işleme karşılık gelen makroyu seçin.
4. "Yeni Kullanıcı ID Ekle" kısmına banlamak istediğiniz kullanıcı ID'lerini girin.
5. "Ban Aralığı"nı ayarlayın (önerilen: 0.5-1 saniye).
6. "MAKROYU BAŞLAT" butonuna tıklayın ve 3 saniye içinde Discord penceresinede bota komut girilen chat kısmına tıklayın.
7. Program tüm ID'leri otomatik olarak işleyecek veya bir hata oluşursa hata mesajı gösterecek.
8. İşlem tamamlandığında "Tamamlandı" mesajı gösterilecek.

