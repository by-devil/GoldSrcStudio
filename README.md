<p align="center">
  <img src="assets/goldsrc-mark.png" width="88" alt="GoldSrc Studio">
</p>

<h1 align="center">GoldSrc Studio</h1>

<p align="center">
  Counter-Strike 1.6 ve GoldSrc topluluğu için bağımsız modlama araçları.<br>
  <a href="https://tools.bydevil.com"><b>tools.bydevil.com</b></a> ·
  <a href="https://www.goldsrcstudio.com">goldsrcstudio.com</a> ·
  <a href="https://bydevil.com">bydevil.com</a>
</p>

<p align="center">
  <img src="assets/map-optimization.jpg" width="820" alt="Map Optimization">
</p>

---

## Araçlar

<table>
  <tr>
    <td width="50%" valign="top">
      <img src="assets/map-optimization.jpg" alt="Map Optimization"><br>
      <b>Map Optimization</b> · <sub>Beta · Windows</sub><br>
      Haritanda performansın nereye gittiğini gör. wpoly/visleaf analizi, 3D hata katmanları, HINT denemeleri ve HTML rapor.<br>
      <a href="https://gamebanana.com/tools/24466">GameBanana →</a>
    </td>
    <td width="50%" valign="top">
      <img src="assets/studio-paint.jpg" alt="Studio Paint"><br>
      <b>Studio Paint</b> · <sub>Beta / Test · Windows</sub><br>
      Modelinin sadece istediğin parçasını boya. Katmanlı, tahribatsız boyama ve yeni <code>_skin.mdl</code> çıktısı.<br>
      <a href="https://gamebanana.com/tools/24470">GameBanana →</a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="assets/studio-nav.jpg" alt="Studio Nav"><br>
      <b>Studio Nav</b> · <sub>v0.30.0 Beta · Windows</sub><br>
      Botların yolunu oyunu açmadan test et. NAV/PWF düzenleme, otomatik navigasyon ve bot rota simülasyonu.<br>
      <a href="https://gamebanana.com/tools/24109">GameBanana →</a>
    </td>
    <td width="50%" valign="top">
      <img src="assets/skin-studio.jpg" alt="Skin Studio"><br>
      <b>Skin Studio</b> · <sub>v1.20.1 · Windows</sub><br>
      Silah skinlerini ve texture'ları tek yerden yönet. Gömülü texture düzenleme, 3D önizleme, glow sprite.<br>
      <a href="https://gamebanana.com/tools/24053">GameBanana →</a> ·
      <a href="https://github.com/sodej33-lang/CS16-Skin-Studio">GitHub →</a> ·
      <a href="https://github.com/sodej33-lang/CS16-Skin-Studio/releases">İndir →</a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="assets/studio-modeler.jpg" alt="Studio Modeler"><br>
      <b>Studio Modeler</b> · <sub>Beta / Test · Windows</sub><br>
      Harita fırçalarını GoldSrc modele dönüştür. .map/.rmf/.jmf okuma, canlı önizleme, doğrudan .mdl çıktısı.<br>
      <a href="https://gamebanana.com/tools/24469">GameBanana →</a>
    </td>
    <td width="50%" valign="top"></td>
  </tr>
</table>

## Hata bildirimi ve öneriler

Bir sorun bulduysan ya da yeni bir araç fikrin varsa [issue aç](../../issues).

## Yeni araç ekleme

Site, araç listesini [`tools.json`](tools.json) dosyasından otomatik oluşturur. Yeni bir araç için bu dosyaya kayıt ekle ve ekran görüntüsünü `assets/` klasörüne koy:

```json
{
  "name": "Araç Adı",
  "category": "Kategori",
  "version": "v1.0",
  "platform": "Windows",
  "updated": "1 Ocak 2027",
  "summary": "Tek cümlelik açıklama",
  "description": "Uzun açıklama",
  "fileTypes": ".MDL / .BSP",
  "features": ["Özellik 1", "Özellik 2"],
  "image": "assets/arac-adi.jpg",
  "gamebanana": "https://gamebanana.com/tools/00000",
  "github": "https://github.com/by-devil/arac-adi",
  "download": "https://github.com/by-devil/arac-adi/releases"
}
```

`gamebanana`, `github` ve `download` isteğe bağlıdır; hangisi varsa sitede o buton görünür.

---

<sub>GoldSrc Studio topluluk tarafından geliştirilen bağımsız araçlar sunar; Valve Corporation veya Steam ile bağlantılı değildir.</sub>
