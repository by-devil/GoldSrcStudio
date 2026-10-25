# motd-fit — CS 1.6 MOTD Otomatik Sığdırma Kiti

CS 1.6 MOTD penceresi oyunun çözünürlüğüne göre küçülür. Web sayfanız 1920x1080'de düzgün
görünürken 800x600 veya 640x480'de taşar, kaydırma çubuğu çıkar. **motd-fit**, CSS dosyanızdaki
boyutları okuyup her çözünürlük için otomatik küçültme kuralları üretir.

## Nasıl çalışır?

MOTD penceresinin yüksekliği ≈ ekran yüksekliğinin **0.6 katı**:

| Oyun çözünürlüğü | MOTD yüksekliği |
|---|---|
| 1920x1080 | ~650px |
| 1280x720 | ~432px |
| 1024x768 | ~460px |
| 800x600 | ~360px |
| 640x480 | ~288px |

Araç 13 adet `@media screen and (max-height:Npx)` basamağı üretir
(525, 515, 500, 455, 450, 432, 400, 385, 360, 335, 330, 288, 265).
Her basamak "bu yükseklik **veya altı**" demektir; yani listede olmayan çözünürlükler de
en yakın basamağı alır. Değiştirilen tek şey `font-size`, `line-height`, `padding`, `margin`
içindeki **px** değerleridir.

- **transform / zoom kullanılmaz.** Eski MOTD tarayıcısında (Chromium 535, 2012) bunlar
  tıklama noktasını kaydırır. Gerçek CSS değerleri değiştiği için tıklamalar doğru yere düşer.
- Küçük yazılar yavaş, büyük başlıklar ve boşluklar hızlı küçülür; en küçük yazı 9px.
- Üst/alt boşluklar çok, sağ/sol boşluklar az küçülür.
- **30px ve üstü** padding/margin değerlerine dokunulmaz (genelde ikon/avatar yeri; küçülürse yazı ikonun üstüne biner).
- Kuralda sabit px `height` varsa `line-height` değişmez (dikey ortalama bozulmasın).
- Aynı seçici birden çok kez yazıldıysa birleştirilir; bir önceki basamakla aynı kalan değer tekrar yazılmaz (çıktı küçük kalır).
- `!important` ve yüzde (%) değerlere dokunulmaz.

## Kullanım

Python 3 yeterli, ek paket gerekmez.

```bash
python3 motd_fit.py style.css
```

Çıktı dosyanın sonuna `/* motd-fit:start */ … /* motd-fit:end */` arasına yazılır.
CSS'i değiştirdikten sonra tekrar çalıştırın, eski blok yenisiyle değişir.

| Seçenek | Açıklama |
|---|---|
| `--only ".nav a\|.card\|body"` | Sadece bu seçiciler (tam eşleşme, `\|` ile ayırın) |
| `--skip ".logo\|.icon"` | Bu metni içeren seçicileri atla |
| `--stdout` | Dosyaya yazma, ekrana bas (ör. `> motd-fit.css` ile ayrı dosya yapıp `</head>` öncesine link verin) |

**İpucu:** İlk denemede `--only` ile ana kapsayıcıları (body, başlık, menü, kart, satır, buton)
verin. Her şeyi küçültmek ikonları/görselleri bozabilir.

## Kaydırma çubuğu

Sayfanız sabit uzunluktaysa (ör. 15 satırlık sıralama) `html,body{overflow:hidden}` ekleyerek
çubuğu tamamen kaldırabilirsiniz. Uzun/değişken listelerde (market, envanter) **eklemeyin**,
alttaki içerik erişilemez olur.

## Tuzaklar

- **Genişlik kuralı sayfayı uzatır:** `@media (max-width:720px){.card{width:100%}}` gibi "dar ekranda tek sütun"
  kuralları 800x600'de de devreye girer (MOTD ~620px genişlikte). Yan yana kartlar alt alta dizilir,
  sayfa iki kat uzar. Çözüm: yüksekliği de şart koşun:
  `@media (max-width:720px) and (min-height:471px){ ... }`. Araç böyle bir kural görürse uyarır.
- **Satır içi (inline) boyutlar küçülmez:** `style="font-size:34px"` CSS'ten ezilemez. Bir sınıfa taşıyın
  (`class="val big"` + `.val.big{font-size:34px}`) ve `--only` listesine ekleyin.

## Eski WebKit notları

- `overflow:hidden` + açılır menü kesiliyorsa: `html,body{height:100%} body{min-height:100%}`
- Yerel `<select>` açılır listesi MOTD'de kesilir; div tabanlı açılır menü kullanın.
- Değişiklik görünmüyorsa CSS bağlantısına sürüm ekleyin: `style.css?v=2`.

## Demo (önce / sonra)

`demo/` klasörünü web sunucunuza yükleyin. Mevcut MOTD menünüze iki link ekleyin:
`demo/once.html` (motd-fit olmadan) ve `demo/sonra.html` (motd-fit ile). Ek eklenti gerekmez.
Sayfa sağ üstte MOTD boyutunu gösterir; aynı çözünürlükte iki ekran görüntüsü alıp karşılaştırın.

## Test

`example.html` dosyasını tarayıcıda açıp pencere yüksekliğini küçültün, sonra oyunda
800x600 ve 640x480'de MOTD'yi açarak kontrol edin.

---

## English (short)

Generates 13 `@media (max-height)` steps from the px values in your CSS so CS 1.6 MOTD pages fit
every in-game resolution (MOTD height ≈ 0.6 × screen height). No transform/zoom, so clicks stay
accurate in the old MOTD browser. `python3 motd_fit.py style.css [--only "a|b"] [--skip "x"] [--stdout]`.

Basamak düzeni Rank System Ultimate top15 sayfasındaki yaklaşımdan esinlenmiştir.
Lisans: OSR (bkz. `LICENSE`).
