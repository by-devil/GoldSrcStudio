# GoldSrc Studio

Counter-Strike 1.6 / GoldSrc motoru için modlama araçları.

🌐 Web: https://by-devil.github.io/GoldSrcStudio/ · https://bydevil.com/tools/

## Araçlar

| Araç | Açıklama | Bağlantılar |
| --- | --- | --- |
| **CS 1.6 Skin Studio** | Model, doku ve sprite düzenleme aracı (.mdl, PNG/JPG, 3D önizleme) | [GitHub](https://github.com/sodej33-lang/CS16-Skin-Studio) · [İndir](https://github.com/sodej33-lang/CS16-Skin-Studio/releases) · [GameBanana](https://gamebanana.com/tools/24053) |

## Yeni araç ekleme

1. Web tabanlı araçsa dosyalarını `tools/<arac-adi>/` klasörüne koy.
2. `tools.json` dosyasına bir kayıt ekle:

```json
{
  "name": "Araç Adı",
  "description": "Kısa açıklama",
  "tags": ["GoldSrc"],
  "github": "https://github.com/by-devil/GoldSrcStudio/tree/main/tools/arac-adi",
  "demo": "tools/arac-adi/"
}
```

`download` (indirme sayfası), `demo` (tarayıcıda açılan araç) ve `links` (ek bağlantılar) alanları isteğe bağlıdır. Ana sayfa (`index.html`) listeyi bu dosyadan otomatik oluşturur.

## Yasal uyarı

Bu araçlar topluluk tarafından yapılmıştır; Valve Corporation, Steam veya Counter-Strike geliştirme ekibiyle bağlantılı değildir.
