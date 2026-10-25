<?php
/* SIGDIR - CS 1.6 MOTD ekrana sigdirma kiti (motor). Cerez tabanli, DB/sifre yok. */
function sigdir_zoom_pct() {
    $z = isset($_COOKIE['pz']) ? (int)$_COOKIE['pz'] : 100;
    if ($z < 60) $z = 60;
    if ($z > 140) $z = 140;
    return $z;
}
function sigdir_fit_axis($name) {
    $v = isset($_COOKIE[$name]) ? (int)$_COOKIE[$name] : 100;
    if ($v < 50)  $v = 50;
    if ($v > 140) $v = 140;
    return $v;
}
function sigdir_head() {
    $z   = sigdir_zoom_pct();
    $ckl = isset($_COOKIE['ckl']) ? (int)$_COOKIE['ckl'] : 0;
    if ($ckl < 0) $ckl = 0;
    if ($ckl > 2) $ckl = 2;
    $sx = sigdir_fit_axis('fsx');
    $sy = sigdir_fit_axis('fsy');

    // Tekerlek/PageDown scroll yardimcisi VE kompakt-mod SADECE Trident/MSIE (csduragi
    // ve benzeri ucuncu parti client paketleri) icin - onlarin kendi tekerlek scroll'u
    // yok VE transform'lu icerikte tiklama noktasi kayiyor (motor hatasi). Steam'in kendi
    // WebKit MOTD'si (Chrome/18) ve modern tarayicilarda transform/zoom SORUNSUZ calisiyor
    // - o yuzden onlara eski surukle-ayarla/olcekleme kutusunu (fit box) geri verdik.
    $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
    $isTrident = (bool)preg_match('/MSIE|Trident/i', $ua);
    $triFlag = $isTrident ? 'true' : 'false';

    // sunucu tarafi on-uygulama (acilista kayma olmasin)
    $pre = "";
    if ($z !== 100) $pre .= "html{zoom:" . ($z / 100) . "}";
    if (!$isTrident && ($sx !== 100 || $sy !== 100)) {
        $xf = $sx / 100; $yf = $sy / 100;
        $pre .= "body{-webkit-transform:scale($xf,$yf);transform:scale($xf,$yf);"
              . "-webkit-transform-origin:0 0;transform-origin:0 0}";
    }
    $preStyle = ($pre !== "") ? "<style>$pre</style>\n" : "";

    $css = <<<CSS
<style>
#sgbtn{border:0;background:transparent;font-family:"IBM Plex Mono",Consolas,monospace;font-size:10px;letter-spacing:.5px;color:#a49c86;text-decoration:none;padding:4px 6px;cursor:pointer}
#sgbtn:hover{color:#eee7d6}
#sgbtn.on{color:#e6c68a}
#fitclip{position:relative;overflow:hidden}
#fitwrap{position:relative;-webkit-transform-origin:0 0;-ms-transform-origin:0 0;transform-origin:0 0}
.fit-h{position:fixed;z-index:2147483000;border:0;background:#e6c68a;background:rgba(230,198,138,0.92);-webkit-box-shadow:0 0 7px rgba(0,0,0,0.55);box-shadow:0 0 7px rgba(0,0,0,0.55)}
.fit-h:hover{background:#fff2d8}
.fit-hc{right:0;bottom:0;width:26px;height:26px;cursor:nwse-resize;border-radius:6px 0 0 0}
.fit-hc:after{content:"";position:absolute;right:4px;bottom:4px;width:10px;height:10px;border-right:2px solid #6b4f22;border-bottom:2px solid #6b4f22}
.fit-hx{display:none;right:0;top:40%;width:16px;height:66px;cursor:ew-resize;border-radius:5px 0 0 5px}
.fit-hy{display:none;left:40%;bottom:0;width:66px;height:16px;cursor:ns-resize;border-radius:5px 5px 0 0}
.fit-hx.sh,.fit-hy.sh{display:block}
#fithud{display:none;position:fixed;top:44px;right:6px;z-index:2147483001;width:150px;font-family:"IBM Plex Mono",Consolas,monospace;font-size:11px;color:#eee7d6;border:0;background:#0c0a07;background:rgba(12,10,7,0.97);border-radius:6px;-webkit-box-shadow:0 8px 22px rgba(0,0,0,0.55);box-shadow:0 8px 22px rgba(0,0,0,0.55)}
#fithud.op{display:block}
#fithud .hh{display:block;padding:6px 8px 2px;border:0;background:transparent;letter-spacing:1px;font-size:9px;text-transform:uppercase;color:#c1934a;text-align:center}
#fithud .bd{padding:4px 6px 6px}
#fithud .rw{white-space:nowrap;text-align:center;margin:3px 0}
#fithud .rw .ic{display:inline-block;width:15px;color:#a49c86;text-align:left}
#fithud .rw b{display:inline-block;width:42px;color:#e6c68a;font-weight:600}
#fithud .rw a{display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;color:#eee7d6;text-decoration:none;border:0;border-radius:4px;margin:0 1px;background:rgba(255,255,255,0.07)}
#fithud .rw a:hover{background:rgba(193,147,74,0.4);color:#fff}
#fithud .oto{display:block;text-align:center;margin:5px 0 2px;padding:5px 0;color:#221705;text-decoration:none;border:0;border-radius:4px;font-size:10px;font-weight:600;letter-spacing:1px;background:#c1934a}
#fithud .oto:hover{background:#d6a860}
#fithud .rs{display:block;text-align:center;margin-top:3px;padding:5px 0;color:#a49c86;text-decoration:none;border:0;border-radius:4px;font-size:10px;background:rgba(255,255,255,0.05)}
#fithud .rs:hover{background:rgba(193,147,74,0.28);color:#eee7d6}
</style>
CSS;

    $js = <<<JS
<script>
var __TRI=$triFlag; // true = Trident/MSIE (csduragi vb.) -> kompakt mod + tekerlek yardimcisi bunda calisir
var TZ={sx:$sx,sy:$sy};
(function(){var m=document.cookie.match(/(?:^|; )ckl=([0-9])/);var L=m?+m[1]:0;
if(L>0){var h=document.documentElement;h.className=(h.className?h.className+' ':'')+'ck'+L;}})();
var __CKL=(function(){var m=document.cookie.match(/(?:^|; )ckl=([0-9])/);return m?+m[1]:0;})();
function __sgset(L){var h=document.documentElement;
h.className=(' '+h.className+' ').replace(/ ck[12] /g,' ').replace(/^\\s+|\\s+\$/g,'');
if(L>0){h.className=(h.className?h.className+' ':'')+'ck'+L;}
document.cookie='ckl='+L+';path=/;max-age=31536000';__CKL=L;
var b=document.getElementById('sgbtn');if(b){b.className=L>0?'on':'';b.innerHTML=L>0?('SIĞDIR '+L):'SIĞDIR';}}
function tcompact(){__sgset((__CKL+1)%3);}
function __fitbtnlbl(){var b=document.getElementById('sgbtn');if(!b){return;}
var pz=(document.cookie.match(/(?:^|; )pz=(\\d+)/)||[])[1];pz=pz?parseInt(pz):100;
b.innerHTML=(TZ.sx!=100||TZ.sy!=100||pz!=100)?'SIĞDIR •':'SIĞDIR';}
function tzoom(d){var m=document.cookie.match(/(?:^|; )pz=(\\d+)/);var z=m?parseInt(m[1]):100;
if(d==='r'){z=100;}else{z=Math.max(60,Math.min(140,z+d));}
document.cookie='pz='+z+';path=/;max-age=31536000';
try{document.documentElement.style.zoom=z/100;}catch(e){}
var e=document.getElementsByClassName?document.getElementsByClassName('zv'):[];
for(var i=0;i<e.length;i++){e[i].innerHTML=z+'%';}
var lz=document.getElementById('lbl-fz');if(lz){lz.innerHTML=z+'%';}
if(!__TRI){__fitbtnlbl();}}
function __scrl(dy){try{window.scrollBy(0,dy);}catch(e){}
var d=document.documentElement,bo=document.body;
if(d){d.scrollTop=(d.scrollTop||0)+dy;}if(bo){bo.scrollTop=(bo.scrollTop||0)+dy;}}
function __vph(){var d=document.documentElement;var v=(d&&d.clientHeight)||window.innerHeight||420;return v;}
function __wheel(e){e=e||window.event;var d=0;
if(e.deltaY!=null&&e.deltaY!==0){d=e.deltaY;}
else if(e.wheelDelta!=null&&e.wheelDelta!==0){d=-e.wheelDelta;}
else if(e.detail){d=e.detail*40;}
if(d){var st=Math.round(__vph()*0.35);__scrl(d>0?st:-st);if(e.preventDefault){e.preventDefault();}e.returnValue=false;return false;}}
function __key(e){e=e||window.event;var tg=e.target||e.srcElement;
if(tg&&tg.tagName&&/^(INPUT|TEXTAREA|SELECT)\$/.test(tg.tagName)){return;}
var k=e.keyCode||0,s=0,vp=__vph();
if(k==34){s=Math.round(vp*0.9);}else if(k==33){s=-Math.round(vp*0.9);}
else if(k==40){s=Math.round(vp*0.18);}else if(k==38){s=-Math.round(vp*0.18);}
else if(k==32){s=e.shiftKey?-Math.round(vp*0.9):Math.round(vp*0.9);}else{return;}
__scrl(s);if(e.preventDefault){e.preventDefault();}e.returnValue=false;return false;}
// --- fit box (SADECE Trident-disi: Steam WebKit + modern tarayici) ---
function __clf(v){return Math.max(50,Math.min(140,v));}
var __fc=null,__fw=null,__hud=null,__nv=null,__rh,__bh,__ch,__bw=720,__bh0=560;
function __meas(){if(!__fc){return;}
var cw=__fc.style.width,chh=__fc.style.height,ww=__fw.style.width,wt=__fw.style.webkitTransform,wt2=__fw.style.transform,wt3=__fw.style.msTransform;
__fc.style.width='';__fc.style.height='';__fw.style.width='';__fw.style.webkitTransform='none';__fw.style.msTransform='none';__fw.style.transform='none';
__bw=__fw.offsetWidth||__bw;__bh0=__fw.offsetHeight||__bh0;
__fc.style.width=cw;__fc.style.height=chh;__fw.style.width=ww;__fw.style.webkitTransform=wt;__fw.style.msTransform=wt3;__fw.style.transform=wt2;}
function __apply(){if(!__fc){return;}
var sx=TZ.sx/100,sy=TZ.sy/100,t=(sx==1&&sy==1)?'none':('scale('+sx+','+sy+')');
__fw.style.width=__bw+'px';
__fw.style.webkitTransform=t;__fw.style.msTransform=t;__fw.style.transform=t;
__fc.style.width=(sx==1)?'':Math.ceil(__bw*sx)+'px';
__fc.style.height=(sy==1)?'':Math.ceil(__bh0*sy)+'px';
var lx=document.getElementById('lbl-fx');if(lx){lx.innerHTML=TZ.sx+'%';}
var ly=document.getElementById('lbl-fy');if(ly){ly.innerHTML=TZ.sy+'%';}
__fitbtnlbl();}
function __hudpos(){if(!__hud){return;}var y=44;
if(__nv&&__nv.getBoundingClientRect){y=__nv.getBoundingClientRect().bottom+2;}
__hud.style.top=Math.max(2,y)+'px';}
function __hudtog(o){if(!__hud){return;}
var open=(o==null)?(__hud.className!='op'):(!!o);
__hud.className=open?'op':'';
if(__rh){__rh.className='fit-h fit-hx'+(open?' sh':'');__bh.className='fit-h fit-hy'+(open?' sh':'');}
if(open){__meas();__apply();__hudpos();}}
function fset(ax,d){if(d==='r'){TZ.sx=100;TZ.sy=100;}else if(ax==='x'){TZ.sx=__clf(TZ.sx+d);}else{TZ.sy=__clf(TZ.sy+d);}
document.cookie='fsx='+TZ.sx+';path=/;max-age=31536000';document.cookie='fsy='+TZ.sy+';path=/;max-age=31536000';__apply();}
function __calcfit(){__meas();var W=(document.documentElement&&document.documentElement.clientWidth)||window.innerWidth||0;
var H=__vph();if(W<160||H<160||!__bw||!__bh0){return 100;}
var f=Math.min(W/__bw,H/__bh0,1);f=Math.floor(f*20)/20;if(f<0.5){f=0.5;}return Math.round(f*100);}
function fauto(persist){var p=__calcfit();TZ.sx=p;TZ.sy=p;
if(persist){document.cookie='fsx='+p+';path=/;max-age=31536000';document.cookie='fsy='+p+';path=/;max-age=31536000';}__apply();}
function __autofit(){if(TZ.sx!=100||TZ.sy!=100){return;}
if(/(?:^|; )fs[xy]=/.test(document.cookie)){return;}
var p=__calcfit();if(p<100&&p>=70){TZ.sx=p;TZ.sy=p;__apply();}}
function __drag(ev,mode,el){ev=ev||window.event;var x0=ev.clientX,y0=ev.clientY,ax0=TZ.sx,ay0=TZ.sy;
if(el&&el.setCapture){el.setCapture();}
var mv=function(e){e=e||window.event;
if(mode!='y'){TZ.sx=__clf(Math.round((ax0+(e.clientX-x0)/__bw*100)/5)*5);}
if(mode!='x'){TZ.sy=__clf(Math.round((ay0+(e.clientY-y0)/__bh0*100)/5)*5);}
__apply();if(e.preventDefault){e.preventDefault();}return false;};
var up=function(){document.onmousemove=null;document.onmouseup=null;
if(el&&el.releaseCapture){el.releaseCapture();}
if(document.releaseCapture){document.releaseCapture();}
document.body.style.webkitUserSelect='';document.body.style.userSelect='';
document.cookie='fsx='+TZ.sx+';path=/;max-age=31536000';document.cookie='fsy='+TZ.sy+';path=/;max-age=31536000';};
document.onmousemove=mv;document.onmouseup=up;
if(el){el.onmousemove=mv;el.onmouseup=up;}
document.body.style.webkitUserSelect='none';document.body.style.userSelect='none';
if(ev.preventDefault){ev.preventDefault();}return false;}
function __mk(t,c){var e=document.createElement(t);if(c){e.className=c;}return e;}
var __fitdone=false;
function __fitinit(){var b=document.body;if(!b||__fitdone){return;}__fitdone=true;
var clip=__mk('div');clip.id='fitclip';var w=__mk('div');w.id='fitwrap';
while(b.firstChild){w.appendChild(b.firstChild);}clip.appendChild(w);b.appendChild(clip);
__fc=clip;__fw=w;
b.style.webkitTransform='none';b.style.msTransform='none';b.style.transform='none';
__nv=document.getElementsByClassName?document.getElementsByClassName('nav')[0]:null;
__rh=__mk('div','fit-h fit-hx');__rh.title='Yatay olcek';
__bh=__mk('div','fit-h fit-hy');__bh.title='Dikey olcek';
__ch=__mk('div','fit-h fit-hc');__ch.title='Kose - tut, ekrana sigdir';
__rh.onmousedown=function(e){return __drag(e,'x',__rh);};
__bh.onmousedown=function(e){return __drag(e,'y',__bh);};
__ch.onmousedown=function(e){return __drag(e,'xy',__ch);};
b.appendChild(__rh);b.appendChild(__bh);b.appendChild(__ch);
var h=__mk('div');h.id='fithud';
h.innerHTML='<span class="hh">EKRANA SIĞDIR</span><div class="bd">'
+'<a href="#" class="oto" id="b-oto">↧ OTOMATIK SIĞDIR</a>'
+'<div class="rw"><span class="ic">↔</span><a href="#" id="b-fx-">-</a><b id="lbl-fx">'+TZ.sx+'%</b><a href="#" id="b-fx+">+</a></div>'
+'<div class="rw"><span class="ic">↕</span><a href="#" id="b-fy-">-</a><b id="lbl-fy">'+TZ.sy+'%</b><a href="#" id="b-fy+">+</a></div>'
+'<div class="rw"><span class="ic">Z</span><a href="#" id="b-fz-">-</a><b id="lbl-fz">100%</b><a href="#" id="b-fz+">+</a></div>'
+'<a href="#" class="rs" id="b-frs">↺ SIFIRLA</a></div>';
b.appendChild(h);__hud=h;
document.getElementById('b-oto').onclick=function(){fauto(1);return false;};
document.getElementById('b-fx-').onclick=function(){fset('x',-5);return false;};
document.getElementById('b-fx+').onclick=function(){fset('x',5);return false;};
document.getElementById('b-fy-').onclick=function(){fset('y',-5);return false;};
document.getElementById('b-fy+').onclick=function(){fset('y',5);return false;};
document.getElementById('b-fz-').onclick=function(){tzoom(-10);return false;};
document.getElementById('b-fz+').onclick=function(){tzoom(10);return false;};
document.getElementById('b-frs').onclick=function(){fset(null,'r');tzoom('r');return false;};
__meas();__apply();__autofit();}
// ---------------------------------------------------------------
var __w1=false,__w2=false;
function __sginit(){
if(!__w1){__w1=true;
if(__TRI){ // sadece Trident/MSIE - diger motorlarda kendi tekerlek scroll'u zaten var
if(window.addEventListener){
window.addEventListener('wheel',__wheel,false);
window.addEventListener('mousewheel',__wheel,false);
window.addEventListener('DOMMouseScroll',__wheel,false);
window.addEventListener('keydown',__key,false);}
document.onmousewheel=__wheel;
var ok=document.onkeydown;document.onkeydown=function(e){if(__key(e)===false){return false;}if(ok){return ok(e);}};
}}
var host=null;
if(document.getElementsByClassName){host=document.getElementsByClassName('zoom')[0]||document.getElementsByClassName('nav')[0]||null;}
if(host&&!document.getElementById('sgbtn')){
var a=document.createElement('a');a.id='sgbtn';a.href='#';
if(__TRI){
a.title='Ekrana sigdir (kompakt yerlesim)';
a.innerHTML=__CKL>0?('SIĞDIR '+__CKL):'SIĞDIR';if(__CKL>0){a.className='on';}
a.onclick=function(){tcompact();return false;};
}else{
a.title='Ekrana sigdir';a.innerHTML='SIĞDIR';
a.onclick=function(){__hudtog(null);return false;};
}
host.appendChild(a);}
if(!__TRI){__fitinit();}}
function __sgauto(){if(__w2){return;}__w2=true;
if(__TRI){
if(/(?:^|; )ckl=/.test(document.cookie)){return;}
var H=(document.documentElement&&document.documentElement.clientHeight)||window.innerHeight||0;
var SH=(document.body&&document.body.scrollHeight)||0;
var W=(document.documentElement&&document.documentElement.clientWidth)||window.innerWidth||0;
var SW=(document.body&&document.body.scrollWidth)||0;
// Eskiden sadece DIKEY tasma bakiyordu - nav'daki 5 sekme + dil/zoom kontrolleri
// dar ekranlarda YATAY tasiyor ama sayfa boyu artmadigindan bu hic yakalanmiyordu.
var vr=(H>0&&SH>H*1.22)?(SH>H*1.7?2:1):0;
var hr=(W>0&&SW>W*1.05)?(SW>W*1.35?2:1):0;
if(vr||hr){__sgset(Math.max(vr,hr));}
}else{__meas();__autofit();__apply();}}
if(window.addEventListener){
window.addEventListener('DOMContentLoaded',__sginit,false);
window.addEventListener('load',function(){__sginit();__sgauto();__hudpos();},false);
window.addEventListener('resize',function(){if(__TRI||!__fc){return;}__meas();
if(!/(?:^|; )fs[xy]=/.test(document.cookie)){TZ.sx=100;TZ.sy=100;__autofit();}
__apply();__hudpos();},false);
}else{window.onload=function(){__sginit();__sgauto();};}
</script>
JS;

    return $preStyle . $css . "\n" . $js . "\n";
}

