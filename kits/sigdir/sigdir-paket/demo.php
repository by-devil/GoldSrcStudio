<?php
require_once __DIR__ . '/sigdir-eksen.php';
sigdir_eksen_islem();
?>
<!DOCTYPE html>
<html<?= sigdir_eksen_html_sinif() ?>>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>SIĞDIR Demo</title>
<style>
body{margin:0;background:#1b1b1b;color:#e6dfcc;font:14px/1.4 Arial,sans-serif}
.wrap{width:96%;margin:0 auto}
.header{padding:18px 26px 12px;background:#242424}
.title{font-size:32px;font-weight:700}
.subtitle,.season{color:#a49c86;margin-top:6px}
.nav{padding:8px 18px;background:#2b2b2b}
.nav a{display:inline-block;padding:7px 12px;color:#e6dfcc;text-decoration:none}
.nav a.on{background:#c1934a;color:#221705}
.nav .zoom{float:right}
.nav .zoom a{padding:7px 8px}
.nav .axl{color:#a49c86;margin-left:6px}
.content{padding:14px 20px}
.tile,.card{background:#262626;border:1px solid #3a3a3a;padding:14px;margin-bottom:8px}
.val{font-size:28px;color:#e6c68a}
</style>
<?= sigdir_head() ?>
<?= sigdir_eksen_css(array(
    array('.title', 'font-size', 32),
    array('.val', 'font-size', 28),
    array('.tile', 'padding', 14),
    array('.card', 'padding', 14)
), '.wrap', 96) ?>
<link rel="stylesheet" href="sigdir-compact-ornek.css">
</head>
<body>
<div class="wrap">
<div class="header"><div class="title">Örnek Panel</div><div class="subtitle">SIĞDIR kiti + eksen eklentisi demosu</div></div>
<div class="nav">
<span class="zoom">
<?php if (sigdir_eksen_trident()) { echo sigdir_eksen_nav(true); } else { ?>
<a href="#" onclick="tzoom(-10);return false">&minus;</a><a href="#" onclick="tzoom('r');return false"><?= sigdir_zoom_pct() ?>%</a><a href="#" onclick="tzoom(10);return false">+</a>
<?php } ?>
</span>
<a class="on" href="#">Menü</a><a href="#">Görevler</a><a href="#">Market</a><a href="#">Sıralama</a>
</div>
<div class="content">
<div class="tile"><div>Puanınız</div><div class="val">12.480</div></div>
<div class="card">Kart 1 - içerik</div><div class="card">Kart 2 - içerik</div>
<div class="card">Kart 3 - içerik</div><div class="card">Kart 4 - içerik</div>
</div>
</div>
</body></html>
