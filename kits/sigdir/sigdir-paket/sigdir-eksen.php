<?php
/*
 * SIĞDIR EKSEN EKLENTİSİ (ek modül)
 *
 * Asıl kit: SIĞDIR - OSR / Serhat Ondes (sigdir.php, değiştirilmedi).
 * Bu dosya Furia Clan tarafından eklendi ve sigdir.php'yi DEĞİŞTİRMEZ.
 *
 * Ne ekler?
 *   Asıl kit, Steam MOTD'de yatay/dikey ölçek paneli sunar. Trident/MSIE tabanlı istemcilerde
 *   (CSDurağı vb.) ise transform tıklama noktasını kaydırdığı için sadece iki kademeli kompakt
 *   mod verir. Bu modül CSDurağı'na da YATAY ve DİKEY ince ayar getirir: transform ya da zoom
 *   KULLANMAZ, gerçek genişlik ve boyut değerleri sunucuda üretilir, yani tıklama noktası
 *   kaymaz. JavaScript'e de bağlı değildir (butonlar düz bağlantıdır).
 *
 * PHP 5.4 ve üzeriyle çalışır. Çerezler: fsx (yatay), fsy (dikey), pz (zoom), ckl (kompakt kademe).
 */
require_once dirname(__FILE__) . '/sigdir.php';

function sigdir_eksen_trident() {
    $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
    return (bool)preg_match('/MSIE|Trident/i', $ua);
}

/* Sayfanın EN BAŞINDA, çıktı vermeden önce çağır. Butona basılınca çerezi yazar ve sayfaya geri döner. */
function sigdir_eksen_islem($ekstraTemizle = array()) {
    if (!isset($_GET['sg']) && !isset($_GET['pz']) && !isset($_GET['fx']) && !isset($_GET['fy'])) {
        return;
    }
    $sure = time() + 31536000;
    if (isset($_GET['sg'])) {
        $c = isset($_COOKIE['ckl']) ? (int)$_COOKIE['ckl'] : 0;
        setcookie('ckl', (string)(($c + 1) % 3), $sure, '/');
    }
    if (isset($_GET['pz'])) {
        $z = ($_GET['pz'] === 'r') ? 100 : max(60, min(140, sigdir_zoom_pct() + (int)$_GET['pz']));
        setcookie('pz', (string)$z, $sure, '/');
    }
    $eksenler = array('fx' => 'fsx', 'fy' => 'fsy');
    foreach ($eksenler as $param => $cerez) {
        if (isset($_GET[$param])) {
            $v = ($_GET[$param] === 'r') ? 100 : max(50, min(120, sigdir_fit_axis($cerez) + (int)$_GET[$param]));
            setcookie($cerez, (string)$v, $sure, '/');
        }
    }
    $tut = $_GET;
    foreach (array_merge(array('sg', 'pz', 'fx', 'fy'), $ekstraTemizle) as $k) {
        unset($tut[$k]);
    }
    $uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/';
    $yol = '/' . ltrim((string)strtok($uri, '?'), '/');
    $qs = http_build_query($tut);
    header('Location: ' . $yol . ($qs !== '' ? '?' . $qs : ''));
    exit;
}

/* Butonların bağlantı adresi; mevcut sorgu parametrelerini korur. */
function sigdir_eksen_url($ekle, $ekstraTemizle = array()) {
    $q = $_GET;
    foreach (array_merge(array('sg', 'pz', 'fx', 'fy'), $ekstraTemizle) as $k) {
        unset($q[$k]);
    }
    return htmlspecialchars('?' . http_build_query(array_merge($q, $ekle)), ENT_QUOTES);
}

/* <html> etiketine kompakt kademe sınıfını sunucuda ekler: <html<?= sigdir_eksen_html_sinif() ?>> */
function sigdir_eksen_html_sinif() {
    $l = isset($_COOKIE['ckl']) ? (int)$_COOKIE['ckl'] : 0;
    return ($l >= 1 && $l <= 2) ? ' class="ck' . $l . '"' : '';
}

/*
 * <head> içinde çağır. Yalnızca Trident'te çıktı verir (Steam'de kitin kendi transform paneli var,
 * ikisi birlikte ölçeklerse sayfa iki kat küçülür).
 *
 * $kurallar: dikey ayarda ölçeklenecek değerler, her biri array(seçici, özellik, tabanPx).
 *   özellik: font-size | height | min-height | width | padding | margin ... ya da 'wh' (genişlik ve yükseklik birlikte)
 * $kapsayici: yatay ayarda genişliği daralacak ana kutunun seçicisi (örn. '.wrap')
 * $temelGenislik: kapsayıcının %100 ayardaki genişliği (yüzde)
 */
function sigdir_eksen_css($kurallar, $kapsayici = '.wrap', $temelGenislik = 96) {
    if (!sigdir_eksen_trident()) {
        return '';
    }
    $fx = sigdir_fit_axis('fsx');
    $fy = sigdir_fit_axis('fsy');
    $css = '';
    if ($fx !== 100) {
        $css .= $kapsayici . '{width:' . min(100, round($temelGenislik * $fx / 100, 1)) . '%}';
    }
    if ($fy !== 100) {
        $f = $fy / 100;
        foreach ($kurallar as $k) {
            $sec = $k[0];
            $oz = $k[1];
            $d = (int)round($k[2] * $f);
            $d = ($oz === 'font-size') ? max(8, $d) : max(1, $d);
            if ($oz === 'wh') {
                $css .= $sec . '{width:' . $d . 'px;height:' . $d . 'px}';
            } else {
                $css .= $sec . '{' . $oz . ':' . $d . 'px}';
            }
        }
    }
    return ($css === '') ? '' : '<style>' . $css . '</style>' . "\n";
}

/*
 * Menü çubuğuna eklenecek butonlar (yalnızca Trident'te dolu döner).
 * $tam = true ise zoom (- % +) ve SIĞDIR kademe butonu da eklenir; bunlar da sunucu taraflı
 * bağlantıdır, JavaScript çalışmasa da işler.
 */
function sigdir_eksen_nav($tam = false, $ekstraTemizle = array()) {
    if (!sigdir_eksen_trident()) {
        return '';
    }
    $u = 'sigdir_eksen_url';
    $x = sigdir_fit_axis('fsx');
    $y = sigdir_fit_axis('fsy');
    $h = '<span class="axl">&harr;</span>'
       . '<a href="' . $u(array('fx' => '-5'), $ekstraTemizle) . '">&minus;</a>'
       . '<a href="' . $u(array('fx' => 'r'), $ekstraTemizle) . '">' . $x . '%</a>'
       . '<a href="' . $u(array('fx' => '5'), $ekstraTemizle) . '">+</a> '
       . '<span class="axl">&varr;</span>'
       . '<a href="' . $u(array('fy' => '-5'), $ekstraTemizle) . '">&minus;</a>'
       . '<a href="' . $u(array('fy' => 'r'), $ekstraTemizle) . '">' . $y . '%</a>'
       . '<a href="' . $u(array('fy' => '5'), $ekstraTemizle) . '">+</a> ';
    if ($tam) {
        $l = isset($_COOKIE['ckl']) ? (int)$_COOKIE['ckl'] : 0;
        $h .= '<a href="' . $u(array('pz' => '-10'), $ekstraTemizle) . '">&minus;</a>'
            . '<a href="' . $u(array('pz' => 'r'), $ekstraTemizle) . '">' . sigdir_zoom_pct() . '%</a>'
            . '<a href="' . $u(array('pz' => '10'), $ekstraTemizle) . '">+</a>'
            . '<a id="sgbtn" href="' . $u(array('sg' => '1'), $ekstraTemizle) . '">SI&#286;DIR'
            . ($l > 0 ? ' ' . $l : '') . '</a>';
    }
    return $h;
}
