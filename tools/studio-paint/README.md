# Studio Paint

**Modelinin sadece istediğin parçasını boya.**

![Studio Paint](../../assets/studio-paint.jpg)

GoldSrc .mdl modellerini 3D olarak aç, yüzey seç ve renk, degrade, desen veya kendi görselinle katman katman boya. Orijinal dosyana dokunmadan yeni bir .mdl olarak dışa aktar.

## Öne çıkan özellikler

- 3D yüzey ve UV seçimi
- Katmanlı ve tahribatsız boyama
- Degrade, desen ve 3D fırça
- Görsel içe aktarma
- Yeni _skin.mdl olarak dışa aktarma

## Bilgiler

| | |
| --- | --- |
| Kategori | Model boyama |
| Sürüm | Beta / Test |
| Platform | Windows |
| Dosya türleri | `.MDL / .GSP` |
| Son güncelleme | 11 Ekim 2026 |

## İndir

**[⬇ GoldSrcStudioPaint_v0.1_test.zip](GoldSrcStudioPaint_v0.1_test.zip?raw=1)** · 1.5 MB

<sub>SHA-256: `1cabbe9e1f1e82fbe7ba12a1cecd5544163d7ee6a9085bdd96904fd07c26ae97`</sub>

Diğer bağlantılar: [GameBanana](https://gamebanana.com/tools/24470)

<details>
<summary><b>Kullanım kılavuzu (OKU-BENI.txt)</b></summary>

```
GoldSrc Studio Paint  v0.1 (TEST SURUMU)
=========================================

Ne yapar?
  Mevcut bir GoldSrc .mdl modelini (silah, bicak, eldiven, oyuncu...) acar ve
  SADECE sectigin bolgeleri boyamani saglar: sarjor, dipcik, namlu, bicagin
  yuzeyi... Sonucu yine ayni .mdl olarak kaydeder.

Onemli: model icindeki texture'lar YERINDE degistirilir. Geometri, kemikler,
  animasyonlar, hitbox'lar BAYT BAYT AYNI kalir. Ek bir derleyiciye
  (studiomdl) gerek yok. Orijinal dosyana dokunulmaz (_skin.mdl olarak kaydeder).

Kullanim
  1) .mdl'yi pencereye surukle (veya Open / O).
  2) Sol panel, "Select" araci:
       Surf   : tikladigin yuzeyi, keskin koseye kadar secer (Angle limit ile ayarla)
       Island : UV adasini secer (texture uzerinde bagli parca)
       Tri    : tek ucgen; surukleyerek ucgen ucgen ekler
       Tik = degistir, Shift = ekle, Ctrl = cikar. Grow/Shrink/Invert/All/Clear.
       "Save current selection" ile secimi isimle sakla (sarjor, dipcik...).
  3) Sag panel: "Fill / Grad / Patt / Paint" ile katman ekle. Katman SECILI bolgeye
       uygulanir (maske). Her katmanin: opaklik, karisim modu, renkler, olcek,
       dondurme, kayma, tekrar, tohum...
       Desen: hazir (camo, noise, stripes, checker, dots, waves, flames) veya
       "+Pattern" ile kendi PNG/JPG/BMP/TGA resmin/logon.
       Projection: UV (texture uzayi) veya X/Y/Z ekseni (3D'den duz izdusum -
       UV dikislerinden bagimsiz, desen kesintisiz gorunur).
  4) "Paint" araci (2 tusu): modelin uzerine fircayla boya. Ctrl = sil. Secim
       varsa boya secimin disina cikmaz.
  5) Altta texture listesi + UV paneli: UV select (dikdortgenle ucgen sec),
       UV mask (secili katmana elle maske ekle, Ctrl ile cikar), UV paint.
  6) "Save MDL" (Ctrl+E) = oyunda kullanilacak model. "BMP" = degisen texture'lari
       256 renkli BMP olarak kaydeder. "Save project" (Ctrl+S) = .gsp: katmanlar,
       desenler, secimler; tekrar acinca devam edersin (model dosyasi yaninda olmali).

GoldSrc kisitlari
  Katmanlar RGBA olarak calisir; kayit sirasinda 256 renge indirilir. Dokunulmayan
  pikseller ORIJINAL renklerini korur, yeni boya palette kalan yeri kullanir.

UYARI: ust uste binen / aynali UV
  Bazi modellerde iki farkli parca texture'in AYNI piksellerini paylasir (ornegin
  sag-sol aynali parcalar). Birini boyarsan oburu de boyanir. Program bunu secimde
  kirmizi uyariyla gosterir ("N baska ucgen ayni pikselleri kullaniyor"); cozum
  UV duzenlemesi gerektirir (sonraki surum).

Bilinen eksikler (sonraki surumler)
  - Geometri duzenleme (kose tasima, yuz silme...) henuz yok.
  - Animasyon oynatma yok; model ilk idle karesinde gosterilir.
  - Skin family / bodygroup secimi yok (ilk alt model gosterilir).
  - "T" yardimci modeller (texture ayri dosyada) acilmaz, ana modeli ac.
  - Gercek oyunda henuz denenmedi; yapi Valve modelleriyle dogrulandi.

Klavye: O ac | 1/2 arac | G buyut | H kucult | I ters | A hepsi | Esc temizle |
        F odakla | W tel | Ctrl+Z / Ctrl+Y | Ctrl+S proje | Ctrl+E MDL | L dil
```

</details>

> Araçlar beta aşamasındadır. Dosyalarını düzenlemeden önce yedeklemeni öneririz.

[← Tüm araçlar](../../README.md)
