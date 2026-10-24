**English** · [Türkçe](README.tr.md)

# Studio Paint

**Paint only the part of your model you want.**

![Studio Paint](../../assets/studio-paint.jpg)

Open GoldSrc .mdl models in 3D, select surfaces and paint them layer by layer with colours, gradients, patterns or your own images. Export as a new .mdl without touching your original file.

## Key features

- 3D surface and UV selection
- Layered, non-destructive painting
- Gradients, patterns and a 3D brush
- Image import
- Export as a new _skin.mdl

## Details

| | |
| --- | --- |
| Category | Model painting |
| Version | Beta / Test |
| Platform | Windows |
| File types | `.MDL / .GSP` |
| Last updated | Oct 11, 2026 |

## Download

**[⬇ GoldSrcStudioPaint_v0.1_test.zip](GoldSrcStudioPaint_v0.1_test.zip?raw=1)** · 1.5 MB

<sub>SHA-256: `1cabbe9e1f1e82fbe7ba12a1cecd5544163d7ee6a9085bdd96904fd07c26ae97`</sub>

Other links: [GameBanana](https://gamebanana.com/tools/24470)

<details>
<summary><b>User manual</b></summary>

```
GoldSrc Studio Paint  v0.1 (TEST BUILD)
=======================================

What does it do?
  Opens an existing GoldSrc .mdl model (weapon, knife, gloves, player...) and
  lets you paint ONLY the areas you select: magazine, stock, barrel, the knife
  blade... The result is saved as the same .mdl again.

Important: textures inside the model are changed IN PLACE. Geometry, bones,
  animations and hitboxes stay BYTE FOR BYTE THE SAME. No extra compiler
  (studiomdl) is needed. Your original file is not touched (saved as _skin.mdl).

Usage
  1) Drag the .mdl onto the window (or Open / O).
  2) Left panel, "Select" tool:
       Surf   : selects the clicked surface up to sharp edges (tune with Angle limit)
       Island : selects a UV island (a connected piece on the texture)
       Tri    : a single triangle; drag to add triangle by triangle
       Click = toggle, Shift = add, Ctrl = remove. Grow/Shrink/Invert/All/Clear.
       "Save current selection" stores the selection by name (magazine, stock...).
  3) Right panel: add a layer with "Fill / Grad / Patt / Paint". The layer is
       applied to the SELECTED area (mask). Each layer has: opacity, blend mode,
       colours, scale, rotation, offset, repeat, seed...
       Pattern: built-in (camo, noise, stripes, checker, dots, waves, flames) or
       your own PNG/JPG/BMP/TGA image/logo with "+Pattern".
       Projection: UV (texture space) or X/Y/Z axis (flat projection from 3D -
       independent of UV seams, the pattern looks seamless).
  4) "Paint" tool (key 2): paint on the model with a brush. Ctrl = erase. If
       there is a selection, paint stays inside it.
  5) Texture list + UV panel at the bottom: UV select (select triangles with a
       rectangle), UV mask (add a mask to the selected layer by hand, Ctrl to
       remove), UV paint.
  6) "Save MDL" (Ctrl+E) = the model to use in game. "BMP" = saves changed
       textures as 256-colour BMPs. "Save project" (Ctrl+S) = .gsp: layers,
       patterns, selections; reopen it to continue (the model file must be next to it).

GoldSrc limits
  Layers work in RGBA; they are reduced to 256 colours when saving. Untouched
  pixels keep their ORIGINAL colours, new paint uses the remaining palette slots.

WARNING: overlapping / mirrored UVs
  In some models two different parts share the SAME pixels of the texture (for
  example mirrored left/right parts). Painting one also paints the other. The
  program shows this with a red warning in the selection ("N other triangles
  use the same pixels"); fixing it needs UV editing (next version).

Known gaps (next versions)
  - No geometry editing (moving vertices, deleting faces...) yet.
  - No animation playback; the model is shown in its first idle frame.
  - No skin family / bodygroup selection (the first submodel is shown).
  - "T" helper models (textures in a separate file) cannot be opened, open the main model.
  - Not tested in the real game yet; the structure was verified with Valve models.

Keys: O open | 1/2 tool | G grow | H shrink | I invert | A all | Esc clear |
      F focus | W wire | Ctrl+Z / Ctrl+Y | Ctrl+S project | Ctrl+E MDL | L language
```

</details>

> The tools are in beta. We recommend backing up your files before editing them.

[← All tools](../../README.md)
