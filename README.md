# GoldSrc Studio

Counter-Strike 1.6 / GoldSrc motoru için modlama araçları.

🌐 Web: https://tools.bydevil.com

## Araçlar

| Araç | Ne yapar | Bağlantılar |
| --- | --- | --- |
| **Map Optimization** | Haritanda performansın nereye gittiğini gör. | [GameBanana](https://gamebanana.com/tools/24466) |
| **Studio Paint** | Modelinin sadece istediğin parçasını boya. | [GameBanana](https://gamebanana.com/tools/24470) |
| **Studio Nav** | Botların yolunu oyunu açmadan test et. | [GameBanana](https://gamebanana.com/tools/24109) |
| **Skin Studio** | Silah skinlerini ve texture'ları tek yerden yönet. | [GameBanana](https://gamebanana.com/tools/24053) · [GitHub](https://github.com/sodej33-lang/CS16-Skin-Studio) · [İndir](https://github.com/sodej33-lang/CS16-Skin-Studio/releases) |
| **Studio Modeler** | Harita fırçalarını GoldSrc modele dönüştür. | [GameBanana](https://gamebanana.com/tools/24469) |

## Yeni araç ekleme

`tools.json` dosyasına bir kayıt ekle:

```json
{
  "name": "Araç Adı",
  "category": "Kategori",
  "version": "v1.0",
  "platform": "Windows",
  "updated": "1 Ocak 2027",
  "summary": "Tek cümlelik açıklama",
  "image": "assets/arac-adi.jpg",
  "gamebanana": "https://gamebanana.com/tools/00000",
  "github": "https://github.com/by-devil/arac-adi"
}
```

`image` için ekran görüntüsünü `assets/` klasörüne koy. `gamebanana`, `github` ve `download` (indirme sayfası) bağlantıları isteğe bağlıdır; hangisi varsa kartta o buton görünür. Ana sayfa (`index.html`) listeyi bu dosyadan otomatik oluşturur.

## Yasal uyarı

Bu araçlar topluluk tarafından yapılmıştır; Valve Corporation, Steam veya Counter-Strike geliştirme ekibiyle bağlantılı değildir.
