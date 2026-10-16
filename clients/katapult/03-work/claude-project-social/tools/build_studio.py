"""Build studio/katapult-social-studio.html, the "Katapult Social Studio" artifact.

Usage: python tools/build_studio.py [--local]

  --local   asset paths stay relative (assets/...), for a test served from studio/ on localhost
  default   asset paths come from studio/asset-map.json (rel path -> artifact asset url, written after upload_asset)

The page: Make PNG (drop a post file from the Claude Project, every frame renders from the kit with its slots
filled, checks run, PNG or .zip download), Layouts (every template and banner pattern with its slots),
Photos and products (every id a post may use), How it works.
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
STUDIO = HERE / "studio"
OUT = STUDIO / "katapult-social-studio.html"
LINKS = {
    "ds": "https://claude.ai/code/artifact/ee8bd24b-c2e4-4f39-b14b-4523c87c4704",
    "hub": "https://claude.ai/code/artifact/2abbbef7-4ac3-4e9c-a431-7c37b8e05dcf",
    "lib": "https://claude.ai/code/artifact/bc252c47-7c82-4376-ba50-383a10c1a576",
    "pd": "https://claude.ai/code/artifact/91b3a212-4b8f-4cb4-ade3-0ae3b6122be6",
}

EXAMPLE = """<!DOCTYPE html>
<!--
  Katapult post file
  Job: Example, home upgrade (shows how the Studio reads a file)
  Frames: T06-4x5, T04-1x1, P3A-300x600
  Copy: example copy from the approved templates
  Open: none
-->
<html lang="en"><head><meta charset="utf-8"><title>Example, home upgrade</title></head><body>
<section data-use="T06-4x5" data-file="2026-10-13-example-home-upgrade-4x5">
  <div data-slot="headline">Time for the home<br>upgrade you want.</div>
  <div data-slot="sub">No credit score needed. Just fair, straightforward terms.</div>
  <div data-slot="cta">Leap Forward</div>
  <div data-slot="photo" data-img="library:unboxing-woman-unboxing-sofa-02" data-pos="50% 35%"></div>
</section>
<section data-use="T04-1x1" data-file="2026-10-13-example-kitchen-1x1">
  <div data-slot="headline">The kitchen upgrade<br>starts today.</div>
  <div data-slot="sub">No credit required. Just the appliances you actually need.</div>
  <div data-slot="cta">Leap Forward</div>
  <div data-slot="product1" data-img="product:fridge"></div>
  <div data-slot="product2" data-img="product:washer"></div>
  <div data-slot="product3" data-img="product:tv"></div>
</section>
<section data-use="P3A-300x600" data-file="KAT26000-Example-300x600-Static-Programmatic-V1">
  <div data-slot="headline"><span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span></div>
  <div data-slot="sub"><span>Lease-to-own</span><span>on thousands</span><span>of Cyber Week deals.</span></div>
  <div data-slot="cta"><span>Shop Cyber Deals Now</span></div>
</section>
</body></html>
"""

CSS = r"""
/* Layout: the Katapult family masthead (Dark Blue band shared with the DS, Deliverables Hub and Image Library),
   then a tab bar; Make PNG is a drop zone over a contact sheet of rendered frames. Tokens follow the Katapult DS. */
:root{
  --k-pink:#ED5370; --k-dark-blue:#131540; --k-blue:#365488; --k-light-blue:#9EB5C0; --k-cream:#D4A574;
  --k-white:#FFFFFF; --k-grey-light:#D8D8D8;
  --font-brand:"Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif;
  --font-mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --bg:#F5F5F3; --panel:#FFFFFF; --panel-2:#F0F0F0; --ink:#131540; --ink-2:#4D4D4D; --rule:#D8D8D8; --rule-strong:#A4A4A4;
  --accent:#ED5370; --focus:#131540; --stage:#E4E5EA;
  --ok-bg:#E3EEE6; --ok-ink:#1E4D2B; --warn-bg:#F7DDE2; --warn-ink:#7A1F31;
  --gutter:clamp(16px,4vw,48px);
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0D0E2C; --panel:#131540; --panel-2:#171A4A; --ink:#F0F0F0; --ink-2:#C8C9CF; --rule:#2B2E62; --rule-strong:#4A4E86;
    --focus:#ED5370; --stage:#0A0B24; --ok-bg:#16382A; --ok-ink:#BFE5CB; --warn-bg:#43182A; --warn-ink:#F7C4CF;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#0D0E2C; --panel:#131540; --panel-2:#171A4A; --ink:#F0F0F0; --ink-2:#C8C9CF; --rule:#2B2E62; --rule-strong:#4A4E86;
  --focus:#ED5370; --stage:#0A0B24; --ok-bg:#16382A; --ok-ink:#BFE5CB; --warn-bg:#43182A; --warn-ink:#F7C4CF;
}
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:300 16px/1.55 var(--font-brand);-webkit-font-smoothing:antialiased}
h1,h2,h3{font-weight:500;margin:0;text-wrap:balance;line-height:1.1}
p{margin:0}
button,input,textarea,select{font:inherit}
code{font-family:var(--font-mono);font-size:.84em;background:var(--panel-2);border-radius:3px;padding:1px 5px}
:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:2px}
.wrap{max-width:1240px;margin-inline:auto;padding-inline:var(--gutter)}
.label{font-size:12px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2)}
.masthead{background:var(--k-dark-blue);color:var(--k-white)}
.masthead .wrap{padding-block:28px 36px;display:grid;gap:18px}
.family{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px}
.family img{height:26px;width:auto;display:block}
.family nav{display:flex;flex-wrap:wrap;gap:6px}
.family a,.family button{font:500 13px/1 var(--font-brand);color:var(--k-grey-light);text-decoration:none;border:1px solid rgba(158,181,192,.35);border-radius:999px;padding:7px 13px;background:transparent;cursor:pointer}
.family a:hover,.family button:hover{border-color:var(--k-pink);color:var(--k-white)}
.family a[aria-current="page"]{background:var(--k-pink);border-color:var(--k-pink);color:var(--k-dark-blue);font-weight:700}
.masthead .eyebrow{color:var(--k-light-blue)}
.masthead h1{font-size:clamp(40px,6vw,72px);font-weight:400;letter-spacing:-.03em;line-height:.95}
.masthead h1 span{color:var(--k-pink)}
.lede{max-width:68ch;color:var(--k-grey-light);font-size:17px}
.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--rule)}
.tabs .wrap{display:flex;gap:4px;overflow-x:auto}
.tabs button{border:0;background:none;color:var(--ink-2);font-weight:500;font-size:15px;padding:16px 14px 14px;border-bottom:3px solid transparent;cursor:pointer;white-space:nowrap}
.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}
main .wrap{padding-block:32px 64px;display:grid;gap:28px}
.sec-h{display:grid;gap:8px;max-width:72ch}
.sec-h h2{font-size:32px;font-weight:400;letter-spacing:-.02em}
.sec-h p{color:var(--ink-2)}
.steps{list-style:none;counter-reset:k;padding:0;margin:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.steps li{counter-increment:k;display:grid;gap:6px;align-content:start;border-top:2px solid var(--rule);padding-top:14px}
.steps li::before{content:counter(k);display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--k-pink);color:var(--k-dark-blue);font-weight:700;font-size:14px}
.steps b{font-weight:500;font-size:17px}
.steps span{color:var(--ink-2);font-size:14px}
@media (max-width:760px){.steps{grid-template-columns:minmax(0,1fr)}}
.make{background:var(--panel);border:1px solid var(--rule);border-radius:20px;padding:clamp(18px,3vw,32px);display:grid;gap:16px}
.drop{position:relative;display:grid;place-items:center;gap:6px;text-align:center;min-height:170px;border:2px dashed var(--rule-strong);border-radius:16px;padding:24px;cursor:pointer;background:var(--panel-2)}
.drop.over{border-color:var(--k-pink)}
.drop b{font-size:20px;font-weight:500}
.drop span{color:var(--ink-2);font-size:14px;max-width:56ch}
.drop input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.pill{font-weight:500;font-size:15px;min-height:44px;padding:0 22px;border-radius:999px;border:0;background:var(--k-pink);color:var(--k-dark-blue);cursor:pointer}
.pill.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--rule-strong)}
.pill:disabled{opacity:.45;cursor:default}
details.paste summary{cursor:pointer;font-weight:500;font-size:14px;min-height:32px}
details.paste textarea{width:100%;min-height:150px;margin-top:10px;font:13px/1.4 var(--font-mono);border-radius:12px;border:1px solid var(--rule);padding:12px;background:var(--panel-2);color:var(--ink)}
.msg{font-size:14px;color:var(--ink-2)}
.msg:empty{display:none}
.uploads{font-size:13px;color:var(--ink-2)}
.uploads:empty{display:none}
.pv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:28px}
.pv{display:grid;gap:10px;align-content:start}
.pv-box{position:relative;overflow:hidden;border-radius:8px;background:var(--stage);max-width:100%}
.pv-in{position:absolute;left:0;top:0;transform-origin:0 0}
.pv-bar{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:13px;color:var(--ink-2)}
.pv-bar b{color:var(--ink);font-weight:500;font-family:var(--font-mono);font-size:12px;word-break:break-all}
.pv-bar button{font-weight:500;font-size:13px;min-height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--rule-strong);background:var(--panel);color:var(--ink);cursor:pointer;white-space:nowrap}
.chk{list-style:none;margin:0;padding:10px 12px;border-radius:10px;font-size:13px;display:grid;gap:4px}
.chk.ok{background:var(--ok-bg);color:var(--ok-ink)}
.chk.warn{background:var(--warn-bg);color:var(--warn-ink)}
.chk li::before{content:"\2022  "}
.chk.ok li::before{content:"\2713  "}
.filters{display:flex;flex-wrap:wrap;gap:8px}
.filters button{border:1px solid var(--rule-strong);background:var(--panel);color:var(--ink);border-radius:999px;padding:8px 14px;font-size:14px;cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--k-dark-blue);border-color:var(--k-dark-blue);color:var(--k-white)}
:root[data-theme="dark"] .filters button[aria-pressed="true"]{background:var(--k-pink);color:var(--k-dark-blue);border-color:var(--k-pink)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .filters button[aria-pressed="true"]{background:var(--k-pink);color:var(--k-dark-blue);border-color:var(--k-pink)}}
.fam{display:grid;gap:14px;padding-top:18px;border-top:1px solid var(--rule)}
.fam-h{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline}
.fam-h h3{font-size:22px;font-weight:500}
.fam-h code{font-size:13px}
.fam-h p{color:var(--ink-2);font-size:14px;flex-basis:100%}
.lay-grid{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end}
.lay{display:grid;gap:6px}
.lay .pv-box{background:var(--stage)}
.lay span{font-size:12px;color:var(--ink-2);font-family:var(--font-mono)}
.slots{font-size:13px;color:var(--ink-2)}
.ph-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px}
.ph{display:grid;gap:6px;align-content:start;font-size:13px}
.ph img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;background:var(--stage);display:block}
.ph.prod img{object-fit:contain;padding:10px}
.ph code{justify-self:start;word-break:break-all}
.ph small{color:var(--ink-2)}
.tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:2px 8px;background:var(--panel-2);color:var(--ink-2)}
.tag.care{background:var(--warn-bg);color:var(--warn-ink)}
.prose{display:grid;gap:14px;max-width:72ch}
.prose h3{font-size:20px;margin-top:10px}
.prose ul{margin:0;padding-left:20px;display:grid;gap:6px}
.prose pre{overflow-x:auto;background:var(--panel-2);border-radius:10px;padding:14px;font:12.5px/1.5 var(--font-mono);margin:0}
.foot{border-top:1px solid var(--rule);padding-block:20px 40px;color:var(--ink-2);font-size:13px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
/* the frames themselves: fixed brand colors, never theme */
.kframe{position:relative;overflow:hidden;flex:none;color-scheme:light}
.art{position:relative;overflow:hidden;--kfont:"Aktiv Grotesk","Helvetica Neue",Arial,sans-serif;font-family:var(--kfont)}
.art p{margin:0}
"""

JS = r"""
(function(){
var KIT=window.__KIT__,MAP=window.__ASSETS__,UP={},post=null,frames=[],dl=null;
var $=function(id){return document.getElementById(id);};
var esc=function(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');};
if(window.claude&&claude.use)claude.use('downloads').then(function(d){dl=d;refresh();});
// theme switch
$('theme-btn').onclick=function(){var r=document.documentElement,cur=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');r.setAttribute('data-theme',cur==='dark'?'light':'dark');};
// tabs
var tabs=[].slice.call(document.querySelectorAll('.tabs button'));
function show(id,user){tabs.forEach(function(b){var on=b.dataset.tab===id;b.setAttribute('aria-selected',on);$(b.dataset.tab).hidden=!on;});
 if(id==='sec-layouts')renderLayouts();if(id==='sec-photos')renderPhotos();if(user){try{history.replaceState(null,'','#'+id.slice(4));}catch(e){}}}
tabs.forEach(function(b){b.onclick=function(){show(b.dataset.tab,true);};});

function asset(rel){if(rel.indexOf('svg:')===0)return KIT.svg[rel.slice(4)]||'';return MAP[rel]||rel;}
function frameHTML(code){var L=KIT.layouts[code];return L.html.replace(/src="([^"]+)"/g,function(m,s){return 'src="'+esc(asset(s))+'"';});}
function makeFrame(code){var L=KIT.layouts[code],f=document.createElement('div');f.className='kframe';f.style.width=L.w+'px';f.style.height=L.h+'px';f.innerHTML=frameHTML(code);
 var first=f.firstElementChild;if(first){first.style.width=L.w+'px';first.style.height=L.h+'px';}return f;}
function fitButtons(root){root.querySelectorAll('[data-name="Button"]').forEach(function(b){
 if(b.dataset.t===undefined){b.dataset.t=b.style.top||'';b.dataset.l=b.style.left||'';}
 b.style.zoom=1;var z=446/b.offsetWidth;if(!isFinite(z)||z<=0)return;b.style.zoom=z;
 if(b.style.position==='absolute'){['t','l'].forEach(function(k){var v=b.dataset[k],p=k==='t'?'top':'left';if(/^-?[\d.]+px$/.test(v))b.style[p]=(parseFloat(v)/z)+'px';});}});}

// ---- reading a post file
var ALLOWED_CLASS=/^(t1|t2|ta|trim)$/;
function clean(node,mode,issues,where){var out='';node.childNodes.forEach(function(n){
 if(n.nodeType===3){out+=esc(n.nodeValue.replace(/\s+/g,' '));return;}
 if(n.nodeType!==1)return;var tag=n.tagName.toLowerCase();
 if(tag==='br'){out+='<br>';return;}
 if(tag==='em'||tag==='i'){out+=(mode==='accent'?'<em>':'')+clean(n,mode,issues,where)+(mode==='accent'?'</em>':'');if(mode!=='accent')issues.push(where+': this layout has no accent colour, the <em> was ignored');return;}
 if(tag==='span'&&mode==='markup'){var c=(n.getAttribute('class')||'').split(/\s+/).filter(function(x){return ALLOWED_CLASS.test(x);}).join(' ');
  out+='<span'+(c?' class="'+c+'"':'')+'>'+clean(n,mode,issues,where)+'</span>';return;}
 out+=clean(n,mode,issues,where);});return out;}
function trimHTML(s){return s.replace(/^\s+|\s+$/g,'').replace(/\s*<br>\s*/g,'<br>');}
function scaleNode(el,f){['fontSize','letterSpacing','lineHeight'].forEach(function(p){var v=el.style[p];if(/^-?[\d.]+px$/.test(v))el.style[p]=(parseFloat(v)*f)+'px';});
 if(el.style.padding){el.style.padding=el.style.padding.replace(/([\d.]+)px/g,function(m,x){return (parseFloat(x)*f)+'px';});}}
function applyText(tgt,v,spec,name,issues){
 var html=trimHTML(clean(v,spec.mode,issues,name));
 if(/[–—]/.test(v.textContent))issues.push(name+': has a long dash. Katapult copy never uses one');
 if(!v.textContent.trim()){issues.push(name+': empty');}
 if(spec.mode==='lines'){var ps=tgt.querySelectorAll(':scope > p'),first=ps[0],last=ps[ps.length-1],lines=html.split('<br>');tgt.innerHTML='';
  lines.forEach(function(l,i){var p=(i===lines.length-1?last:first).cloneNode(false);p.innerHTML=l;tgt.appendChild(p);});}
 else if(spec.mode==='accent'){var sp=tgt.querySelectorAll(':scope > span'),nor=sp[0],acc=sp[sp.length-1];tgt.innerHTML='';
  html.split(/(<em>.*?<\/em>|<br>)/).forEach(function(part){if(!part)return;if(part==='<br>'){tgt.appendChild(document.createElement('br'));return;}
   var em=/^<em>(.*)<\/em>$/.exec(part),s=(em?acc:nor).cloneNode(false);s.innerHTML=em?em[1]:part;tgt.appendChild(s);});}
 else tgt.innerHTML=html;
 var size=parseFloat(v.getAttribute('data-size'));
 if(size&&spec.size){var f=size/spec.size;if(f<0.7)issues.push(name+': data-size '+size+' is under 70% of the layout size ('+Math.round(spec.size)+'). Shorten the copy instead');
  var host=tgt.style.fontSize?tgt:(tgt.parentElement&&tgt.parentElement.style.fontSize?tgt.parentElement:tgt);
  [host].concat([].slice.call(host.querySelectorAll('*'))).forEach(function(el){scaleNode(el,f);});}
 tgt.setAttribute('data-filled','1');}
function imgHit(ref){var m=/^(library|product):(.+)$/.exec(ref||'');if(!m)return null;return (m[1]==='library'?KIT.library:KIT.products).filter(function(x){return x.id===m[2];})[0]||null;}
function imgSrc(ref,issues,name){var m=/^(library|product|upload):(.+)$/.exec(ref||'');
 if(!m){issues.push(name+': data-img must be library:ID, product:ID or upload:FILE');return null;}
 if(m[1]==='upload'){if(UP[m[2]])return UP[m[2]];issues.push(name+': drop the image "'+m[2]+'" here with the post file');return null;}
 var list=m[1]==='library'?KIT.library:KIT.products,hit=list.filter(function(x){return x.id===m[2];})[0];
 if(!hit){issues.push(name+': "'+m[2]+'" is not a '+(m[1]==='library'?'Library photo':'product')+' id');return null;}
 if(hit.fit==='no people')issues.push(name+': '+hit.id+' has no people; the guideline keeps it out of the main image');
 return asset(hit.path);}
function applyImage(tgt,v,spec,name,issues){var src=imgSrc(v.getAttribute('data-img'),issues,name);if(!src)return;
 tgt.src=src;tgt.style.objectFit=spec.fit;var hit=imgHit(v.getAttribute('data-img')),pos=v.getAttribute('data-pos')||(spec.fit==='contain'?'50% 100%':(hit&&hit.face)||'50% 50%');
 if(!/^-?[\d.]+% -?[\d.]+%$/.test(pos)){issues.push(name+': data-pos must look like "50% 30%"');pos='50% 50%';}
 if(spec.fit==='contain'){
  // a cutout fills the visible box of its slot (the named Figma node), not the placeholder's crop
  var box=tgt.parentElement;while(box&&!box.hasAttribute('data-name')&&!box.classList.contains('kframe'))box=box.parentElement;
  for(var n=tgt.parentElement;n&&n!==box;n=n.parentElement){n.style.cssText+=';position:absolute;left:0;top:0;right:0;bottom:0;width:auto;height:auto;inset:0;overflow:visible;transform:none';}
  var sc=parseFloat(v.getAttribute('data-scale'))||1;if(sc<0.4||sc>1){issues.push(name+': data-scale goes from 0.4 to 1');sc=Math.min(1,Math.max(0.4,sc));}
  tgt.style.cssText+=';position:absolute;max-width:none;left:'+((1-sc)*50)+'%;top:'+((1-sc)*100)+'%;width:'+(sc*100)+'%;height:'+(sc*100)+'%;right:auto;bottom:auto;transform:none';
  if(box&&box.style.overflow==='hidden')box.style.overflow='visible';}
 tgt.style.objectPosition=pos;tgt.setAttribute('data-filled','1');}
function build(sec,i){var code=sec.getAttribute('data-use'),L=KIT.layouts[code],issues=[];
 if(!L)return {error:'Frame '+(i+1)+': "'+esc(code||'')+'" is not a layout code. Check the Layouts tab.'};
 var f=makeFrame(code),given={};
 sec.querySelectorAll('[data-slot]').forEach(function(el){given[el.getAttribute('data-slot')]=el;});
 Object.keys(L.slots).forEach(function(n){var spec=L.slots[n],tgt=f.querySelector('[data-slot="'+n+'"]'),v=given[n];
  if(!tgt)return;if(!v){if(n!=='phone')issues.push(n+': not filled, still the template sample');return;}
  if(spec.kind==='image')applyImage(tgt,v,spec,n,issues);else applyText(tgt,v,spec,n,issues);});
 Object.keys(given).forEach(function(n){if(!L.slots[n])issues.push('"'+n+'" is not a slot of '+code+' (slots: '+Object.keys(L.slots).join(', ')+')');});
 var name=sec.getAttribute('data-file');if(!name||/[{}\s]/.test(name))name=(post||'post')+'-'+String(i+1).padStart(2,'0');
 return {code:code,L:L,f:f,issues:issues,name:name.replace(/[^\w.-]+/g,'-')};}

function textRects(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,out=[];while((n=w.nextNode())){if(!n.nodeValue.trim())continue;var r=document.createRange();r.selectNodeContents(n);out=out.concat([].slice.call(r.getClientRects()));}return out;}
function ink(el,f,s){var b=f.getBoundingClientRect(),x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
 textRects(el).forEach(function(c){if(c.width<1||c.height<1)return;x0=Math.min(x0,c.left);y0=Math.min(y0,c.top);x1=Math.max(x1,c.right);y1=Math.max(y1,c.bottom);});
 if(x0>x1)return null;return {x:(x0-b.left)/s,y:(y0-b.top)/s,w:(x1-x0)/s,h:(y1-y0)/s};}
function lineCount(el){var tops={};textRects(el).forEach(function(c){if(c.width>1)tops[Math.round(c.top)]=1;});return Object.keys(tops).length;}
var DEFH={};
function defaultHeight(code){if(DEFH[code]!==undefined)return DEFH[code];var hold=document.createElement('div');hold.style.cssText='position:absolute;left:-99999px;top:0';
 var f=makeFrame(code);hold.appendChild(f);document.body.appendChild(hold);var h=f.querySelector('[data-slot="headline"]');DEFH[code]=h?h.offsetHeight:0;hold.remove();return DEFH[code];}
function anchor(it){if(it.L.family!=='P2'||it.anchored)return;var h=it.f.querySelector('[data-slot="headline"]');if(!h)return;
 var d=h.offsetHeight-defaultHeight(it.code),t=h.style.top;if(Math.abs(d)>0.5&&/^-?[\d.]+px$/.test(t))h.style.top=(parseFloat(t)-d)+'px';it.anchored=true;}
function boxOf(el,f,s,banner){if(!banner)return ink(el,f,s);var host=el.closest('[class$="-cta"]')||el,kids=host.matches('[class$="-cta"]')?[host]:[].slice.call(host.children).filter(function(k){return k.tagName==='SPAN';});
 if(!kids.length)kids=[host];var b=f.getBoundingClientRect(),x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;kids.forEach(function(k){var c=k.getBoundingClientRect();x0=Math.min(x0,c.left);y0=Math.min(y0,c.top);x1=Math.max(x1,c.right);y1=Math.max(y1,c.bottom);});
 return {x:(x0-b.left)/s,y:(y0-b.top)/s,w:(x1-x0)/s,h:(y1-y0)/s};}
function check(it,s){var f=it.f,L=it.L,out=[],banner=L.group==='banner';
 f.querySelectorAll('[data-slot][data-filled]').forEach(function(el){if(el.tagName==='IMG')return;var r=ink(el,f,s),n=el.getAttribute('data-slot');
  if(r&&(r.x<-1||r.y<-1||r.x+r.w>L.w+1||r.y+r.h>L.h+1))out.push(n+': runs off the frame');
  if(el.querySelector(':scope > p'))[].slice.call(el.querySelectorAll(':scope > p')).forEach(function(p,k){if(lineCount(p)>1)out.push(n+': line '+(k+1)+' wraps. Shorten it or move the break');});
 });
 var boxes=[].slice.call(f.querySelectorAll('[data-slot][data-filled]:not(img),[data-lock]')).map(function(el){return {n:el.getAttribute('data-slot')||'legal line',r:boxOf(el,f,s,banner&&!el.hasAttribute('data-lock'))};}).filter(function(b){return b.r;});
 var tol=banner?1:6;
 for(var a=0;a<boxes.length;a++)for(var b=a+1;b<boxes.length;b++){var p=boxes[a].r,q=boxes[b].r;
  if(p.x<q.x+q.w-tol&&q.x<p.x+p.w-tol&&p.y<q.y+q.h-tol&&q.y<p.y+p.h-tol)out.push(boxes[a].n+' overlaps '+boxes[b].n);}
 return out;}

function say(h){$('mk-msg').innerHTML=h;}
function refresh(){var b=$('mk-all');b.disabled=!frames.length||!dl;b.textContent=frames.length>1?'Download all ('+frames.length+' PNG in a .zip)':'Download PNG';$('mk-clear').hidden=!frames.length;
 $('mk-dl-note').hidden=!!dl||!frames.length;}
function scaleBox(box,inner,w,h){var bw=box.clientWidth,s=bw/w;inner.style.transform='scale('+s+')';box.style.height=(h*s)+'px';return s;}
function load(text,name){
 var doc=new DOMParser().parseFromString(text,'text/html'),secs=[].slice.call(doc.querySelectorAll('section[data-use]'));
 if(!secs.length){say('<ul class="chk warn"><li>No frames in this file. Use the post file the Katapult Social Studio project hands over: every frame is a &lt;section data-use="..."&gt;.</li></ul>');return;}
 post=(name||'post').replace(/\.html?$/i,'');$('pv-grid').innerHTML='';frames=[];var errs=[];
 secs.forEach(function(sec,i){var it=build(sec,i);if(it.error){errs.push(it.error);return;}
  var box=document.createElement('div');box.className='pv';
  box.innerHTML='<div class="pv-box" style="aspect-ratio:'+it.L.w+'/'+it.L.h+'"><div class="pv-in"></div></div><div class="pv-bar"><b>'+esc(it.name)+'</b><button type="button">PNG</button></div><ul class="chk"></ul>';
  box.querySelector('.pv-in').appendChild(it.f);$('pv-grid').appendChild(box);it.box=box;frames.push(it);
  box.querySelector('button').onclick=function(){one(it);};});
 document.fonts.ready.then(function(){frames.forEach(function(it){fitButtons(it.f);anchor(it);});setTimeout(report,60);});
 window.__report=report;
 function report(){var bad=0;frames.forEach(function(it){var s=scaleBox(it.box.querySelector('.pv-box'),it.box.querySelector('.pv-in'),it.L.w,it.L.h),
   list=it.issues.concat(check(it,s)),ul=it.box.querySelector('.chk');it.ok=!list.length;if(list.length)bad++;
   ul.className='chk '+(list.length?'warn':'ok');ul.innerHTML=(list.length?list:['Slots filled, nothing off the frame or overlapping']).map(function(x){return '<li>'+esc(x)+'</li>';}).join('');});
  say('<b>'+frames.length+' frame'+(frames.length>1?'s':'')+'</b> from '+esc(post)+'. '+(bad?bad+' need a fix in the project before they go to review.':'Every check passed. Look at each frame, then download.')+
   (errs.length?'<ul class="chk warn">'+errs.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>':''));refresh();}
 refresh();}
addEventListener('resize',function(){frames.forEach(function(it){scaleBox(it.box.querySelector('.pv-box'),it.box.querySelector('.pv-in'),it.L.w,it.L.h);});});
var FONTCSS=window.__FONTCSS__;
async function png(it){await document.fonts.ready;
 return htmlToImage.toBlob(it.f,{width:it.L.w,height:it.L.h,pixelRatio:1,fontEmbedCSS:FONTCSS,cacheBust:false});}
window.__png=png;window.__frames=function(){return frames;};
async function save(filename,data){if(!dl){say('Downloads are not available in this view. Open Katapult Social Studio in claude.ai to download.');return;}
 try{await dl.save({filename:filename,data:data});}catch(e){if(!e||e.code!=='declined')say('The download did not go through ('+esc(e&&e.code||'error')+'). Try again.');}}
async function one(it){var b=it.box.querySelector('button'),t=b.textContent;b.disabled=true;b.textContent='Making...';
 try{await save(it.name+'.png',await png(it));}catch(e){say('This frame could not be turned into a PNG. Reload the page and try again.');}finally{b.disabled=false;b.textContent=t;}}
$('mk-all').onclick=async function(){if(frames.length===1)return one(frames[0]);var b=this,t=b.textContent;b.disabled=true;b.textContent='Making '+frames.length+' PNG...';
 try{var z=new JSZip();for(var i=0;i<frames.length;i++)z.file(frames[i].name+'.png',await png(frames[i]));await save(post+'.zip',await z.generateAsync({type:'blob'}));}
 catch(e){say('The frames could not be turned into PNG. Reload the page and try again.');}finally{b.textContent=t;refresh();}};
$('mk-clear').onclick=function(){$('pv-grid').innerHTML='';frames=[];say('');refresh();};
var lastText=null,lastName=null;
function readFiles(list){var files=[].slice.call(list||[]),htmlF=null;
 files.forEach(function(f){if(/\.html?$/i.test(f.name))htmlF=f;else if(/^image\//.test(f.type)){if(UP[f.name])URL.revokeObjectURL(UP[f.name]);UP[f.name]=URL.createObjectURL(f);}});
 var names=Object.keys(UP);$('mk-up').textContent=names.length?'Images added for upload: slots: '+names.join(', '):'';
 if(htmlF){var r=new FileReader();r.onload=function(){lastText=String(r.result);lastName=htmlF.name;load(lastText,lastName);};r.readAsText(htmlF);}
 else if(lastText)load(lastText,lastName);}
$('mk-file').onchange=function(){readFiles(this.files);this.value='';};
var drop=$('drop');
drop.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();$('mk-file').click();}});
['dragenter','dragover'].forEach(function(t){drop.addEventListener(t,function(ev){ev.preventDefault();drop.classList.add('over');});});
['dragleave','drop'].forEach(function(t){drop.addEventListener(t,function(ev){ev.preventDefault();drop.classList.remove('over');});});
drop.addEventListener('drop',function(ev){readFiles(ev.dataTransfer.files);});
$('mk-go').onclick=function(){var v=$('mk-paste').value;if(v.trim()){lastText=v;lastName='pasted-post';load(v,'pasted-post');}};
$('mk-ex').onclick=function(){lastText=window.__EXAMPLE__;lastName='2026-10-13-example-home-upgrade.html';load(lastText,lastName);};

// ---- layouts tab
var laysDone=false,famFilter='all';
function renderLayouts(){if(laysDone)return;laysDone=true;var host=$('lay-list'),fams={};
 Object.keys(KIT.layouts).forEach(function(c){var L=KIT.layouts[c];(fams[L.family]=fams[L.family]||{name:L.name,group:L.group,codes:[]}).codes.push(c);});
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var c=e.target.dataset.code,L=KIT.layouts[c],f=makeFrame(c),inn=e.target.querySelector('.pv-in');
  inn.appendChild(f);inn.style.transform='scale('+(e.target.querySelector('.pv-box').clientWidth/L.w)+')';document.fonts.ready.then(function(){fitButtons(f);});});},{rootMargin:'300px'});
 Object.keys(fams).forEach(function(k){var F=fams[k],first=KIT.layouts[F.codes[0]],sec=document.createElement('section');sec.className='fam';sec.dataset.group=F.group;
  var slots=Object.keys(first.slots).map(function(n){var s=first.slots[n];return n+(s.kind==='image'?' (image)':'');}).join(' · ');
  sec.innerHTML='<div class="fam-h"><h3>'+esc(F.name)+'</h3><code>'+esc(k)+'</code><p>Slots: '+esc(slots)+'</p></div><div class="lay-grid"></div>';
  var grid=sec.querySelector('.lay-grid');
  F.codes.forEach(function(c){var L=KIT.layouts[c],w=Math.max(60,Math.min(260,L.w*(F.group==='banner'?(L.w<400?.6:.2):.17))),d=document.createElement('div');d.className='lay';d.dataset.code=c;
   d.innerHTML='<div class="pv-box" style="width:'+w+'px;aspect-ratio:'+L.w+'/'+L.h+'"><div class="pv-in"></div></div><span>'+esc(c)+'</span>';grid.appendChild(d);io.observe(d);});
  host.appendChild(sec);});
 applyFilter();}
function applyFilter(){document.querySelectorAll('#lay-filters button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.g===famFilter);});
 document.querySelectorAll('#lay-list .fam').forEach(function(s){s.hidden=famFilter!=='all'&&s.dataset.group!==famFilter;});}
document.querySelectorAll('#lay-filters button').forEach(function(b){b.onclick=function(){famFilter=b.dataset.g;applyFilter();};});

// ---- photos tab
var phDone=false;
function renderPhotos(){if(phDone)return;phDone=true;
 $('ph-lib').innerHTML=KIT.library.map(function(p){return '<figure class="ph" style="margin:0"><img loading="lazy" src="'+esc(asset(p.path))+'" alt="'+esc(p.subject)+'"><code>library:'+esc(p.id)+'</code><span>'+esc(p.subject)+'</span><small>Copy space: '+esc(p.text_space)+'</small>'+
  '<span><span class="tag'+(p.fit==='on-brand'?'':' care')+'">'+esc(p.fit)+'</span></span></figure>';}).join('');
 $('ph-prod').innerHTML=KIT.products.map(function(p){return '<figure class="ph prod" style="margin:0"><img loading="lazy" src="'+esc(asset(p.path))+'" alt="'+esc(p.label)+'"><code>product:'+esc(p.id)+'</code><span>'+esc(p.label)+'</span><small>'+esc(p.view)+' view</small></figure>';}).join('');}

var start=(location.hash||'#make').slice(1);show('sec-'+(['make','layouts','photos','how'].indexOf(start)>=0?start:'make'));
refresh();
})();
"""


def body(kit):
    n_t = sum(1 for v in kit["layouts"].values() if v["group"] == "template")
    n_b = len(kit["layouts"]) - n_t
    logo = kit["logos"]["white"]
    return f"""
<header class="masthead">
  <div class="wrap">
    <div class="family">
      <img src="{logo}" alt="Katapult">
      <nav aria-label="Katapult pages">
        <a href="{LINKS['ds']}" target="_blank" rel="noopener">Design System</a>
        <a href="{LINKS['hub']}" target="_blank" rel="noopener">Deliverables Hub</a>
        <a href="{LINKS['lib']}" target="_blank" rel="noopener">Image Library</a>
        <a href="#" aria-current="page">Social Studio</a>
        <a href="{LINKS['pd']}" target="_blank" rel="noopener">Power Digital Hub</a>
        <button id="theme-btn" type="button">Switch theme</button>
      </nav>
    </div>
    <span class="label eyebrow">Katapult · Meta, Instagram, PMAX and programmatic</span>
    <h1>Katapult <span>Social Studio</span></h1>
    <p class="lede">Where a post file from the Katapult Social Studio project becomes the PNGs that go to review. Every frame is built from the approved layouts: {n_t // 4} social templates in four ratios and 4 banner patterns (6 variants) in eight sizes. The file only changes the copy, the photo and the products.</p>
  </div>
</header>
<nav class="tabs" aria-label="Sections"><div class="wrap" role="tablist">
  <button type="button" role="tab" data-tab="sec-make" aria-selected="true">Make PNG</button>
  <button type="button" role="tab" data-tab="sec-layouts" aria-selected="false">Layouts</button>
  <button type="button" role="tab" data-tab="sec-photos" aria-selected="false">Photos and products</button>
  <button type="button" role="tab" data-tab="sec-how" aria-selected="false">How it works</button>
</div></nav>
<main>
<section class="wrap" id="sec-make">
  <div class="sec-h"><h2>Make PNG</h2><p>The last step of every job. The project writes the copy, picks the layouts and photos, and hands over one .html file. Drop it here to see every frame with the real fonts, photos and products, read the checks, and download.</p></div>
  <ol class="steps">
    <li><b>Ask the project</b><span>In the Katapult Social Studio project, attach the brief PDF or describe the post. When the plan and copy are approved, Claude hands over a file named like KAT26023-BackToSchool.html.</span></li>
    <li><b>Drop it here</b><span>Add any image the file asks for (upload:...) in the same drop. Each frame shows its checks: slots filled, nothing off the frame, nothing overlapping.</span></li>
    <li><b>Download</b><span>One PNG per frame, or every frame in a .zip, named for the job. Those go to the Deliverables Hub review.</span></li>
  </ol>
  <div class="make">
    <label class="drop" id="drop" tabindex="0"><b>Drop the post file here</b><span>or click to choose it. Drop images in the same go when the file uses upload:FILE for a new photo or product.</span><input type="file" id="mk-file" multiple accept=".html,.htm,text/html,image/*"></label>
    <details class="paste"><summary>Or paste the code</summary><textarea id="mk-paste" spellcheck="false" aria-label="Post file code"></textarea><div class="row" style="margin-top:10px"><button class="pill ghost" type="button" id="mk-go">Show frames</button></div></details>
    <div class="row"><button class="pill ghost" type="button" id="mk-ex">Try the example file</button><button class="pill" type="button" id="mk-all" disabled>Download PNG</button><button class="pill ghost" type="button" id="mk-clear" hidden>Clear</button></div>
    <p class="msg" id="mk-dl-note" hidden>Downloads work when this page is open in claude.ai.</p>
    <p class="uploads" id="mk-up"></p>
    <div class="msg" id="mk-msg" aria-live="polite"></div>
    <div class="pv-grid" id="pv-grid"></div>
  </div>
</section>
<section class="wrap" id="sec-layouts" hidden>
  <div class="sec-h"><h2>Layouts</h2><p>Every layout a post file can use, with its code and its slots. A frame is <code>data-use="CODE"</code>. Templates: T01 to T10 in 1x1 (1200), 4x5 (1080x1350), 16x9 (1920x1080) and 9x16 (1080x1920). Banner patterns: P1 to P4 in the eight PMAX and programmatic sizes. Samples show the copy they were approved with.</p></div>
  <div class="filters" id="lay-filters"><button type="button" data-g="all">All</button><button type="button" data-g="template">Social templates</button><button type="button" data-g="banner">Banner patterns</button></div>
  <div id="lay-list" style="display:grid;gap:26px"></div>
</section>
<section class="wrap" id="sec-photos" hidden>
  <div class="sec-h"><h2>Photos and products</h2><p>The ids a post file may use. Photos come from the <a href="{LINKS['lib']}" target="_blank" rel="noopener">Image Library</a>; anything else (a client photo, a new product cutout) goes in as <code>upload:FILE</code> and is dropped here with the file.</p></div>
  <h3 class="label">Library photos</h3>
  <div class="ph-grid" id="ph-lib"></div>
  <h3 class="label">Product cutouts</h3>
  <div class="ph-grid" id="ph-prod"></div>
</section>
<section class="wrap" id="sec-how" hidden>
  <div class="prose">
    <div class="sec-h"><h2>How it works</h2></div>
    <p>Three pieces work together. The <b>Katapult Social Studio</b> Claude Project is where you work: it reads the brief, plans the frames, writes or places the copy and builds the post file. This page turns that file into PNGs. The <a href="{LINKS['ds']}" target="_blank" rel="noopener">Design System</a> and the <a href="{LINKS['lib']}" target="_blank" rel="noopener">Image Library</a> are the references both use.</p>
    <h3>A frame in the post file</h3>
<pre>&lt;section data-use="T06-4x5" data-file="2026-10-20-home-upgrade-4x5"&gt;
  &lt;div data-slot="headline"&gt;Time for the home&lt;br&gt;upgrade you want.&lt;/div&gt;
  &lt;div data-slot="sub"&gt;No credit score needed. Just fair, straightforward terms.&lt;/div&gt;
  &lt;div data-slot="cta"&gt;Leap Forward&lt;/div&gt;
  &lt;div data-slot="photo" data-img="library:unboxing-woman-unboxing-sofa-02" data-pos="50% 35%"&gt;&lt;/div&gt;
&lt;/section&gt;</pre>
    <ul>
      <li>Only slots change. Positions, sizes, the logo, the pill and the legal line come from the layout.</li>
      <li><code>&lt;br&gt;</code> sets a line break. T09 marks its pink words with <code>&lt;em&gt;</code>. Banner patterns use their own spans (<code>t1</code>, <code>t2</code>, <code>ta</code>), listed in the project.</li>
      <li><code>data-pos</code> moves the crop of a photo. <code>data-size</code> steps a text down when rebreaking is not enough, never under 70%.</li>
      <li>Images: <code>library:ID</code>, <code>product:ID</code> or <code>upload:FILE</code>.</li>
    </ul>
    <h3>When a check fails</h3>
    <p>Paste the check into the project ("line 2 wraps on T06-4x5") and ask for the fix. It hands the whole file back; drop it again.</p>
  </div>
</section>
</main>
<footer class="wrap foot">Katapult Social Studio · Power Digital. Layouts from Figma "Progressive Global - LAB" (social templates node 547:1042, banner patterns node 547:1720). Built {kit.get('built', '')}.</footer>
"""


TEST = r"""<script>
if(location.search.indexOf('dump=1')>=0){window.addEventListener('load',function(){document.fonts.ready.then(function(){var out={};
 Object.keys(window.__KIT__.layouts).forEach(function(c){var L=window.__KIT__.layouts[c],hold=document.createElement('div');hold.style.cssText='position:absolute;left:0;top:0';
  hold.innerHTML=L.html;document.body.appendChild(hold);var f=hold.firstElementChild;f.style.width=L.w+'px';f.style.height=L.h+'px';var fb=f.getBoundingClientRect();
  f.querySelectorAll('img[data-slot]').forEach(function(im){var box=im.closest('[class$="-pic"]')||im.parentElement;while(box&&box!==f&&!box.hasAttribute('data-name')&&!/-pic$/.test(box.className))box=box.parentElement;
   var r=(box||im).getBoundingClientRect(),x0=Math.max(r.left,fb.left),y0=Math.max(r.top,fb.top),x1=Math.min(r.right,fb.right),y1=Math.min(r.bottom,fb.bottom);
   (out[c]=out[c]||{})[im.getAttribute('data-slot')]={w:Math.round(x1-x0),h:Math.round(y1-y0),x:Math.round(x0-fb.left),y:Math.round(y0-fb.top)};});
  hold.remove();});
 var pre=document.createElement('pre');pre.id='autotest-out';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);});});}
else if(location.search.indexOf('autotest')>=0){window.addEventListener('load',function(){
 var src=localStorage.getItem('autotest')||null;
 fetch(new URLSearchParams(location.search).get('post')||'example').then(function(r){return r.ok?r.text():window.__EXAMPLE__;}).catch(function(){return window.__EXAMPLE__;}).then(function(t){
  document.getElementById('mk-paste').value=t;document.getElementById('mk-go').click();
  setTimeout(async function(){var out=[];var fr=window.__frames();for(var i=0;i<fr.length;i++){var b=await window.__png(fr[i]);
   var u=await new Promise(function(res){var r=new FileReader();r.onload=function(){res(r.result);};r.readAsDataURL(b);});
   out.push({name:fr[i].name,checks:[].slice.call(fr[i].box.querySelectorAll('.chk li')).map(function(l){return l.textContent;}),png:u});}
   var pre=document.createElement('pre');pre.id='autotest-out';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);},window.__WAIT__||2500);});});}
</script>"""


def main():
    local = "--local" in sys.argv
    kit = json.loads((STUDIO / "kit.json").read_text(encoding="utf-8"))
    amap = {}
    if not local and "--bootstrap" not in sys.argv:
        mp = STUDIO / "asset-map.json"
        if not mp.is_file():
            sys.exit("studio/asset-map.json missing: upload the assets first, or build with --local")
        amap = json.loads(mp.read_text(encoding="utf-8"))
        served = json.loads((STUDIO / "served.json").read_text(encoding="utf-8"))
        missing = [p for p in served if p not in amap]
        shas = json.loads((STUDIO / "asset-map-sha.json").read_text(encoding="utf-8"))
        stale = [p for p in served if p in shas and shas[p]["sha"] != served[p]]
        if missing or stale:
            sys.exit(f"upload first: {len(missing)} new, {len(stale)} changed since upload, e.g. {(missing + stale)[:3]}")
    fontcss = "".join(f'@font-face{{font-family:"Aktiv Grotesk";font-weight:{w};font-style:normal;font-display:block;src:url({u}) format("woff")}}'
                      for w, u in kit["fonts"].items())
    framecss = "\n".join(kit["css"].values())
    page_kit = {k: kit[k] for k in ("layouts", "svg", "library", "products")}
    data = (f"<script>window.__KIT__={json.dumps(page_kit, ensure_ascii=False, separators=(',', ':'))};"
            f"window.__ASSETS__={json.dumps(amap, separators=(',', ':'))};"
            f"window.__FONTCSS__={json.dumps(fontcss)};window.__EXAMPLE__={json.dumps(EXAMPLE)};</script>")
    doc = (('<meta charset="utf-8">\n' if local else "") + "<title>Katapult Social Studio</title>\n"
           f"<style>{fontcss}\n{CSS}\n/* banner pattern css, from the approved jobs */\n{framecss}</style>\n"
           + body(kit) + "\n"
           '<script src="https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js"></script>\n'
           '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>\n'
           + data.replace("</", "<\\/").replace("<!--", "<\\!--").replace("<\\/script>", "</script>") + "\n"
           f"<script>{JS}</script>\n" + (TEST if local else ""))
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT.name} ({OUT.stat().st_size / 1e6:.2f} MB){' LOCAL' if local else ''}")


if __name__ == "__main__":
    main()
