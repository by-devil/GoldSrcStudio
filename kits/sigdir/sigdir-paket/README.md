# SIĞDIR Kiti + Eksen Eklentisi (CS 1.6 MOTD ekranına sığdırma)

CS 1.6 içinde `show_motd()` ile açılan web sayfaları küçük çözünürlükte (örneğin 800x600 ya da
640x480) taşar ve ekrana sığmaz. Bu paket, sayfaya bir **SIĞDIR** butonu ile **yatay / dikey
ince ayar** ekler. Sadece PHP ve çerez kullanır. Veritabanı, şifre, harici kütüphane ya da dış
adrese istek YOKTUR.

## Paketin içinde neler var?

| Dosya | Ne işe yarar | Kimin |
|---|---|---|
| `sigdir.php` | Asıl kit (motor) | SIĞDIR - OSR / Serhat ondes, DEĞİŞTİRİLMEDİ |
| `sigdir-compact-ornek.css` | Kompakt mod için örnek CSS (kendi temana göre değiştirmelisin) | Asıl kit |
| `sigdir-eksen.php` | **Ek modül:** CSDurağı (Trident) için yatay/dikey ince ayar | Furia Clan |
| `demo.php` | İkisini birlikte kullanan çalışır örnek sayfa | Furia Clan (asıl demodan uyarlandı) |
| `KREDI.txt` | Kredi ve lisans notu | |

## Ne yapar?

**Steam MOTD ve modern tarayıcılarda** (asıl kit):
- SIĞDIR butonuna basınca sağda "EKRANA SIĞDIR" paneli açılır.
- **Otomatik sığdır**, **yatay (↔)**, **dikey (↕)** ve **zoom (Z)** ayrı ayrı `-` ve `+` ile ayarlanır.
- Sağ alt köşeden, sağ ve alt kenardan sürükleyerek de boyutlandırabilirsin.
- Ayarlar çerezde saklanır.

**CSDurağı gibi Trident/MSIE tabanlı eski istemcilerde:**
- Asıl kit orada `transform` kullanmaz (tıklama noktası kaydığı için) ve iki kademeli
  kompakt mod verir (SIĞDIR butonu: 1 → 2 → kapalı).
- **Bu pakette eklenen kısım:** `sigdir-eksen.php` ile CSDurağı'na da **yatay (↔) ve dikey (↕)
  ince ayar** gelir. Yöntem: `transform` ya da `zoom` kullanmaz. Genişlik ve boyut değerleri
  sunucuda gerçek CSS olarak üretilir, bu yüzden **tıklama noktası kaymaz**. Butonlar düz
  bağlantıdır, JavaScript çalışmasa da işler. Ayar aralığı %50 ile %120 arasındadır, 5'er adımla.

## Kurulum

1. `sigdir.php`, `sigdir-eksen.php` ve `sigdir-compact-ornek.css` dosyalarını sitene kopyala.
2. Sayfanın EN BAŞINA (herhangi bir çıktı vermeden önce) şunu yaz:
   ```php
   <?php
   require_once __DIR__ . '/sigdir-eksen.php';
   sigdir_eksen_islem();      // butona basılınca çerezi yazar ve sayfaya geri döner
   ?>
   ```
3. `<html>` etiketini şöyle yaz: `<html<?= sigdir_eksen_html_sinif() ?>>`
4. `<head>` içine şunu ekle:
   ```php
   <?= sigdir_head() ?>
   <?= sigdir_eksen_css(array(
       array('.baslik', 'font-size', 32),   // dikey ayarda ölçeklenecek değerler: seçici, özellik, taban px
       array('.kart',   'padding',   14),
       array('.ikon',   'wh',        46)    // 'wh' = genişlik ve yüksekliği birlikte ölçekler
   ), '.wrap', 96) ?>                        // yatay ayarda daralacak kutu ve %100'deki genişliği (yüzde)
   <link rel="stylesheet" href="sigdir-compact-ornek.css">
   ```
5. Menü çubuğunda `zoom` sınıflı bir kapsayıcı olsun ve içine şunu yaz:
   ```php
   <span class="zoom"><?= sigdir_eksen_nav(true) ?></span>
   ```
   (Steam tarafında kitin kendi JavaScript butonu aynı yere eklenir. Örnek için `demo.php`'ye bak.)
6. Sitenin tüm içeriği `.wrap` gibi tek bir kutunun içinde olsun. Yatay ayar bu kutunun genişliğini daraltır.

## Kendi temana uyarla (ÖNEMLİ)

- `sigdir-compact-ornek.css` örnek bir temanın seçicilerini kullanır. Kendi sayfandaki
  boşlukları ve yazı boyutlarını `html.ck1 ...` (orta) ve `html.ck2 ...` (agresif) kurallarıyla
  küçültmelisin. `ck1` ve `ck2` sınıflarını `<html>` etiketine kit ekler ya da çıkarır.
- `sigdir_eksen_css()` kural listesini de kendi sayfana göre doldur. Dikey ayarın hangi yazı
  boyutlarını, boşlukları ve ikonları küçülteceğini sen belirlersin.
- Kompakt kademe (SIĞDIR 1 ya da 2) açıkken onun kuralları ince ayarın üstüne geçer. İnce ayar
  için SIĞDIR'ı kapat.
- `sigdir_eksen_css()` sadece Trident'te çıktı verir. Steam'de kitin kendi transform paneli var;
  ikisi birlikte ölçeklerse sayfa iki kat küçülürdü.
- Butonların `?fx=-5` gibi parametreleri, sayfanın kendi parametreleriyle birlikte taşınır.
  Sayfanda tekrar çalıştırılmaması gereken bir parametre varsa (örneğin `action=claim`),
  `sigdir_eksen_islem(array('action'))` ve `sigdir_eksen_nav(true, array('action'))` ile
  temizlet.

## Gereksinim ve güvenlik

- PHP 5.4 veya üstü. Ek kütüphane yok.
- Yalnızca şu çerezleri yazar: `fsx`, `fsy` (yatay ve dikey), `pz` (zoom), `ckl` (kompakt kademe).
- Veritabanı, şifre, oturum ya da dış adrese istek yoktur.
- Buton parametreleri sayıya çevrilir ve sınırlandırılır. Yönlendirme adresi yalnızca sayfanın
  kendi yolundan üretilir, dışarıya yönlendirme yapmaz.

## Test durumu

- Steam MOTD ve CSDurağı (Trident, IE7 modu) istemcilerinde Furia Clan sunucusunda, gerçek bir
  sayfada denendi.
- `demo.php` örnek sayfası ayrıca sunucu tarafında (Trident ve diğer tarayıcı kimlikleriyle)
  doğrulandı. Kendi sunucunda da mutlaka dene.

## Lisans ve kredi

Asıl kit serbestçe kullanılabilir, değiştirilebilir ve paylaşılabilir. Kredi verilmesi hoş olur:
**"SIĞDIR - OSR / Serhat ondes"**.
Bu paketteki ek modül (`sigdir-eksen.php`) de aynı şekilde serbesttir. Kredi olarak "Furia Clan"
yazabilirsin. Paylaşırken `KREDI.txt` ve bu README'yi olduğu gibi tut.
