<script>
document.fonts.ready.then(function(){ setTimeout(run, 300); });
function run(){
  var out=[], S=.3, total=0, logoCount=0;
  var COPY='h4.kp-headline,.kp-text,.kp-sub,.kp-cta,.kp-prompt-line,.kp-join,.kp-opt,.kp-tile';
  var ART='.kp-bg > *,.kp-stage *,.kp-ph,.kp-sh,.kp-ico,.kp-cut,.kp-ui,.kp-fan,.kp-print,.kp-cell,.kp-phone,.kp-tri,.kp-grid,.kp-venn .c';
  function r(el,base){ var a=el.getBoundingClientRect(); return {l:(a.left-base.left)/S,t:(a.top-base.top)/S,r:(a.right-base.left)/S,b:(a.bottom-base.top)/S}; }
  function hit(a,b){ return a.l<b.r-1&&a.r>b.l+1&&a.t<b.b-1&&a.b>b.t+1; }
  function solid(el){ var c=getComputedStyle(el).backgroundColor; var m=c.match(/rgba?\(([^)]+)\)/); if(!m) return false; var p=m[1].split(','); return p.length<4||parseFloat(p[3])===1; }
  out.push('font check: '+(document.fonts.check('500 88px "Aktiv Grotesk"')?'Aktiv Grotesk loaded':'FONT NOT LOADED'));
  var bounceDom=0;
  document.querySelectorAll('.q4-strip article.kp-post').forEach(function(art){
    var base=art.getBoundingClientRect(), cs=getComputedStyle(art), W=1080, H=parseFloat(cs.height);
    var st=parseFloat(cs.getPropertyValue('--kp-safe-top')), sb=parseFloat(cs.getPropertyValue('--kp-safe-bottom')), sx=parseFloat(cs.getPropertyValue('--kp-safe-x'));
    var safe={l:sx,t:st,r:W-sx,b:H-sb}, issues=[], minFont=999;
    var copies=[].slice.call(art.querySelectorAll(COPY)).filter(function(e){ return !e.parentElement.closest(COPY); });
    var arts=[].slice.call(art.querySelectorAll(ART));
    // 1 essentials in the safe zone, not clipped
    copies.concat([].slice.call(art.querySelectorAll('.kp-logo'))).forEach(function(el){
      var b=r(el,base), name=(el.className||el.tagName)+' "'+(el.textContent||'').trim().slice(0,26)+'"';
      if(b.l<safe.l-1||b.r>safe.r+1||b.t<safe.t-1||b.b>safe.b+1) issues.push('OUTSIDE SAFE '+name+' '+JSON.stringify([b.l|0,b.t|0,b.r|0,b.b|0]));
      var dx=el.scrollWidth-el.clientWidth, dy=el.scrollHeight-el.clientHeight;
      var ov=getComputedStyle(el).overflow;
      if(dx>2||(ov!=='visible'&&dy>1)) issues.push('CLIPPED '+name+' dx '+dx+' dy '+dy);
      if(dy>14) issues.push('TEXT PAST BOX '+name+' dy '+dy);
      if(!el.classList.contains('kp-logo')) minFont=Math.min(minFont,parseFloat(getComputedStyle(el).fontSize)||999);
    });
    // 2 copy over art: copy on the ground may touch nothing; copy inside a solid .kp-ui only has to clear the card's own contents
    copies.forEach(function(el){
      var b=r(el,base), card=el.closest('.kp-ui'), name='"'+(el.textContent||'').trim().slice(0,26)+'"';
      if(card&&!solid(card)) issues.push('CARD NOT SOLID under '+name);
      arts.forEach(function(a){
        if(a.contains(el)||el.contains(a)) return;
        if(card&&!card.contains(a)) return;
        var cs2=getComputedStyle(a); if(cs2.visibility==='hidden'||cs2.display==='none') return;
        var ab=r(a,base); if(ab.r-ab.l<2||ab.b-ab.t<2) return;
        if(hit(ab,b)) issues.push('COPY OVER ART '+name+' x '+(a.className||a.tagName).toString().slice(0,40));
      });
    });
    // 3 copy vs copy
    for(var i=0;i<copies.length;i++)for(var j=i+1;j<copies.length;j++){ if(hit(r(copies[i],base),r(copies[j],base))) issues.push('COPY OVERLAP '+i+'/'+j); }
    // 4 layout container and stage room
    // copy outside the stage must not run into it (the stage is what the copy leaves; a squeeze shows here)
    art.querySelectorAll('.kp-stage').forEach(function(sg){ var sgb=r(sg,base); copies.forEach(function(el){ if(sg.contains(el)) return; if(hit(sgb,r(el,base))) issues.push('COPY INTO STAGE "'+el.textContent.trim().slice(0,24)+'"'); });
      var bleedB=sg.classList.contains('bl-b'); if(!bleedB&&sgb.b>safe.b+1) issues.push('STAGE PAST SAFE BOTTOM '+Math.round(sgb.b)); if(bleedB&&Math.abs(sgb.b-H)>2) issues.push('BLEED STAGE NOT AT EDGE '+Math.round(sgb.b)); });
    var lastc=copies.concat([].slice.call(art.querySelectorAll('.kp-sticker-zone'))).reduce(function(m,e){return Math.max(m,r(e,base).b);},0); if(lastc>safe.b+1) issues.push('CONTENT PAST SAFE BOTTOM '+Math.round(lastc));
    var stg=[].map.call(art.querySelectorAll('.kp-stage'),function(s){ var b=r(s,base); return Math.round(b.b-b.t); });
    stg.forEach(function(h){ if(h<300) issues.push('STAGE TOO SMALL '+h); });
    // 5 placeholders: icons fully on canvas; the logo never over a photo
    art.querySelectorAll('.kp-ico').forEach(function(e){ var b=r(e,base); if(b.l<-1||b.t<-1||b.r>W+1||b.b>H+1) issues.push('ICON OFF CANVAS '+e.textContent.slice(0,24)); });
    art.querySelectorAll('.kp-logo').forEach(function(lg){ var b=r(lg,base); art.querySelectorAll('.kp-ph').forEach(function(p){ if(hit(r(p,base),b)&&!lg.closest('.kp-ui')) issues.push('LOGO OVER PHOTO'); }); });
    // 5b logo: supplied artwork only, proportions, min size, approved color per ground, x-height clear on every side
    var logoInfo=[];
    art.querySelectorAll('.kp-logo').forEach(function(lg){
      var b=r(lg,base), w=b.r-b.l, hh=b.b-b.t, xh=w*66.51/521, tag='LOGO';
      var u=lg.querySelector('use'); if(lg.tagName.toLowerCase()!=='svg'||!u||u.getAttribute('href')!=='#k-logo'||lg.getAttribute('viewBox')!=='0 0 521 116') issues.push(tag+' NOT THE SUPPLIED SYMBOL');
      if(lg.getAttribute('role')!=='img'||lg.getAttribute('aria-label')!=='Katapult'||(lg.textContent||'').trim()) issues.push(tag+' ROLE/LABEL/TEXT');
      if(Math.abs(w/hh-521/116)>0.02) issues.push(tag+' PROPORTION '+(w/hh).toFixed(3));
      var tf=getComputedStyle(lg).transform; if(tf&&tf!=='none') issues.push(tag+' TRANSFORMED '+tf);
      var anc=lg.parentElement; while(anc&&anc!==art){ var at=getComputedStyle(anc).transform; if(at&&at!=='none'&&!/^matrix\(1, 0, 0, 1,/.test(at)){ issues.push(tag+' IN ROTATED/SCALED PARENT '+(anc.className||'').toString().slice(0,30)); break; } anc=anc.parentElement; }
      if(w<96) issues.push(tag+' UNDER 96PX '+w.toFixed(1));
      // ground: the solid card it sits on, else the post ground
      var card=lg.closest('.kp-ui'), ground=getComputedStyle(card||art).backgroundColor, col=getComputedStyle(lg).color;
      var MAP={'rgb(234, 234, 232)':'rgb(236, 83, 112)','rgb(255, 255, 255)':'rgb(236, 83, 112)','rgb(19, 21, 64)':'rgb(236, 83, 112)','rgb(237, 83, 112)':'rgb(255, 255, 255)','rgb(212, 165, 116)':'rgb(19, 21, 64)','rgb(54, 84, 136)':'rgb(255, 255, 255)','rgb(228, 128, 39)':'rgb(19, 21, 64)'};
      var NAME={'rgb(236, 83, 112)':'Pink','rgb(255, 255, 255)':'White','rgb(19, 21, 64)':'Dark Blue'};
      var GN={'rgb(234, 234, 232)':'surface','rgb(255, 255, 255)':'White','rgb(19, 21, 64)':'Dark Blue','rgb(237, 83, 112)':'Pink','rgb(212, 165, 116)':'Cream','rgb(54, 84, 136)':'Blue','rgb(228, 128, 39)':'Orange'};
      if(!(ground in MAP)) issues.push(tag+' UNKNOWN GROUND '+ground); else if(MAP[ground]!==col) issues.push(tag+' WRONG VERSION '+col+' on '+ground);
      // clear-space box = logo box grown by its x-height on every side
      var cb={l:b.l-xh,t:b.t-xh,r:b.r+xh,b:b.b+xh};
      var box=card?r(card,base):{l:0,t:0,r:W,b:H};
      if(cb.l<box.l-0.5||cb.t<box.t-0.5||cb.r>box.r+0.5||cb.b>box.b+0.5) issues.push(tag+' CLEAR SPACE PAST '+(card?'CARD':'CANVAS')+' EDGE '+JSON.stringify([cb.l|0,cb.t|0,cb.r|0,cb.b|0]));
      var near=Infinity, nearName='';
      art.querySelectorAll(COPY+','+ART+',.kp-track,.kp-track i,.kp-cta,.kp-pill,.kp-ui,.kp-sticker-zone,.kp-a,.kp-sh,.kp-bg > *').forEach(function(o){
        if(o===lg||o.contains(lg)||lg.contains(o)) return;
        var cs3=getComputedStyle(o); if(cs3.visibility==='hidden'||cs3.display==='none') return;
        var ob=r(o,base); if(ob.r-ob.l<2||ob.b-ob.t<2) return;
        var gx=Math.max(ob.l-b.r,b.l-ob.r,0), gy=Math.max(ob.t-b.b,b.t-ob.b,0), g=Math.max(gx,gy);
        if(g<near){ near=g; nearName=(o.className||o.tagName).toString().split(' ')[0]; }
        if(ob.l<cb.r-0.5&&ob.r>cb.l+0.5&&ob.t<cb.b-0.5&&ob.b>cb.t+0.5) issues.push(tag+' CLEAR SPACE HIT '+(o.className||o.tagName).toString().slice(0,34)+' "'+(o.textContent||'').trim().slice(0,18)+'"');
      });
      var edge=Math.min(b.l-box.l,b.t-box.t,box.r-b.r,box.b-b.b);
      logoInfo.push((NAME[col]||col)+' on '+(GN[ground]||ground)+(card?' card':'')+', '+Math.round(w)+'px, x-height '+xh.toFixed(1)+', nearest '+(near===Infinity?'none':Math.round(near)+' ('+nearName+')')+', edge '+Math.round(edge));
      logoCount++;
    });
    var z=art.querySelector('.kp-sticker-zone'); var zinfo='';
    if(z){ var zb=r(z,base); zinfo=' | sticker '+Math.round(zb.b-zb.t)+'px'; if(zb.b>safe.b+1||zb.t<safe.t-1) issues.push('STICKER ZONE OUTSIDE SAFE'); if(zb.b-zb.t<300) issues.push('STICKER ZONE UNDER 300'); }
    // 6 Bounce line graphics in the rendered DOM
    var nb=0;
    art.querySelectorAll('use').forEach(function(u){ if(/k-(support|super|seam|arrow)/.test(u.getAttribute('href')||'')) nb++; });
    art.querySelectorAll('path').forEach(function(pth){ if(/[CcSsQqTtAa]/.test(pth.getAttribute('d')||'')) nb++; if(pth.getAttribute('stroke-dasharray')) nb++; });
    art.querySelectorAll('*').forEach(function(e){ var c=(e.getAttribute('class')||''); if(/\bkp-(bounce|super|seam|swipe|flow)\b/.test(c)) nb++; });
    if(nb) issues.push('BOUNCE LINE PIECES '+nb);
    bounceDom+=nb;
    var h=art.querySelector('h4.kp-headline'); var lines=h?Math.round(h.getBoundingClientRect().height/S/(parseFloat(getComputedStyle(h).lineHeight))):0;
    total+=issues.length;
    out.push(art.id+' | '+(art.className.match(/kp-theme-\w+/)||[''])[0].replace('kp-theme-','')+' | h1 '+lines+' lines | min copy '+minFont+'px | stage '+stg.join('/')+zinfo+(logoInfo.length?'\n   logo: '+logoInfo.join(' | '):'')+(issues.length?'\n   !! '+issues.join('\n   !! '):' | OK'));
  });
  out.push('\nBounce pieces in rendered posts: '+bounceDom);
  out.push('Logos in rendered posts: '+logoCount);
  out.push('TOTAL ISSUES: '+total);
  var pre=document.createElement('pre'); pre.id='layout-report'; pre.textContent=out.join('\n'); document.body.appendChild(pre);
}
</script>
