<?php
/**
 * csduragi.com / oyunyoneticisi.com gibi 3. parti CS 1.6 client'lari MOTD
 * panelini "MSIE 7.0 ... Trident/7.0" User-Agent'iyla aciyor - gercekte
 * IE11'in Trident motoru ama IE7 uyumluluk modunda calisiyor, rgba(),
 * gradient, flexbox, box-shadow/text-shadow gibi modern CSS'i gormuyor.
 *
 * Kullanim: MOTD sayfanin en ustunde require et, sonra:
 *
 *   <?php if (is_trident_client()): ?>
 *   <link rel="stylesheet" href="trident-fix.css?v=<?= filemtime(__DIR__.'/trident-fix.css') ?>">
 *   <?php endif; ?>
 *
 * Boylece Steam MOTD / gercek tarayicilar bu ekstra dosyayi hic indirmez,
 * ana stylesheet'ine dokunulmaz.
 */
function is_trident_client(): bool {
    $ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
    return (bool)preg_match('/MSIE|Trident/i', $ua);
}
