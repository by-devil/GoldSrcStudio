**English** · [Türkçe](README.tr.md)

# Motd-fit

**CS 1.6 MOTD kit · free**

![Motd-fit](img/motdfit-1920.jpg)

Reads your existing CSS and generates scale-down rules for every resolution. Your design stays the same on big screens; on small ones text and spacing shrink step by step.

`Python 3` · `CSS` · `13 steps` · `Single file`

## Features

**How it works**  
The MOTD window is about 0.6× the game height (1024x768 → ~460px, 800x600 → ~360px, 640x480 → ~288px). It generates 13 steps from 525px down to 265px.

**Click-safe output**  
No transform or zoom; real CSS values change, so buttons are clicked where they appear. Small text stays readable (min 9px) and icons keep their space.

**Usage**  
python3 motd_fit.py style.css — re-run after editing your CSS, the old block is replaced. A demo/ folder with before and after pages is included.

## Download

**[⬇ motd-fit-kit.zip](motd-fit-kit.zip?raw=1)** · 10 KB · no password

<sub>SHA-256: `85a257aa08e2471e4a682bf3e9ae425f52fca4d9cba54607014fb46e1b536f59`</sub>

Browse the files: [`motd-fit-kit/`](motd-fit-kit)

[Forum topic (webailesi.com)](https://www.webailesi.com/konu-kit-motd-fit-motd-sayfalarinizi-her-cozunurluge-otomatik-sigdirma-37546)

## Screenshots

### 1920x1080 before / after

![1920x1080 before / after](img/motdfit-1920.jpg)

### 1024x768 before / after

![1024x768 before / after](img/motdfit-1024.jpg)

### 800x600 before / after

![800x600 before / after](img/motdfit-800.jpg)

### 640x480 before / after

![640x480 before / after](img/motdfit-640.jpg)

[← All kits](../README.md)
