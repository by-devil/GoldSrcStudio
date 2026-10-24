**English** · [Türkçe](README.tr.md)

# Studio Modeler

**Turn map brushes into GoldSrc models.**

![Studio Modeler](../../assets/studio-modeler.jpg)

Select brushes from Hammer, J.A.C.K. or Jackhammer maps and convert them into GoldSrc-compatible low-poly .mdl models. Pick entities, groups or visgroups with a live preview and build models directly, without studiomdl.

## Key features

- Reads .map, .rmf and .jmf
- Entity, group and visgroup selection
- Live textured 3D preview
- Hidden face removal and polygon merging
- Direct .mdl export

## Details

| | |
| --- | --- |
| Category | Map → model |
| Version | Beta / Test |
| Platform | Windows |
| File types | `.MAP / .RMF / .JMF / .MDL` |
| Last updated | Oct 11, 2026 |

## Download

**[⬇ GoldSrcStudioModeler_v0.1_test.zip](https://github.com/by-devil/GoldSrcStudio/releases/download/studio-modeler-beta-test/GoldSrcStudioModeler_v0.1_test.zip)** · 1.3 MB

<sub>SHA-256: `fb26d664cd645f8a56dd52e16ac4e9217825a5361bfa6639f8bd66562d0a1844`</sub>

Other links: [GameBanana](https://gamebanana.com/tools/24469)

<details>
<summary><b>User manual</b></summary>

```
GoldSrc Studio Modeler  v0.1 (TEST BUILD)
=========================================

What does it do?
  Builds an optimised, GoldSrc-compatible .mdl model from the brushes in a
  .map / .rmf / .jmf file.

How to use
  1) Open GoldSrcStudioModeler.exe.
  2) Drag and drop the map onto the window (or "Open", O key).
  3) Select the object you want to turn into a model:
       - "Objects" tab : entities (func_wall, func_detail ...)
       - "Groups" tab  : groups inside the RMF/JMF
       - "Visgrp" tab  : visgroup names from Hammer (DOOR, LADDER ...)
       - Click a brush in 3D = select/deselect, Ctrl+click = select the whole object
  4) See the result live in the "Model" view (Live preview on).
  5) Save it as .mdl with "Export MDL".

Textures:
  Found automatically from the map's "wad" path. If not found, pick a .wad
  with "+WAD" (other wads in the same folder load automatically). Missing
  textures are shown with a checkered placeholder and a warning.

Settings (right panel, click to change):
  Origin        : model centre (bottom centre / centre / position in the map)
  Triangle limit: reduces the triangle count to the target (keeping the shape)
  Merge flat    : merges faces on the same plane
  Smooth shading: normal smoothing for a rounded look
  Texture pages : maximum number of texture pages (max 512x512 each)
  Tiling        : bake = safe (bakes texture repeats into the page)
                  repeat = large repeating surfaces stay sharp BUT relies on
                  the engine repeating the UVs -> test it in game.

Keys: O open | E save | F focus | H hide unselected | 1/2/3 view
      right button rotate | middle button pan | wheel zoom | L language

Known gaps (next versions):
  - No in-app object DRAWING tool yet (coming next).
  - The model has not been tested in a real game client yet; the structure
    was verified against Valve's 211 original models. Tell me if you see a
    problem in game.
```

</details>

> The tools are in beta. We recommend backing up your files before editing them.

[← All tools](../../README.md)
