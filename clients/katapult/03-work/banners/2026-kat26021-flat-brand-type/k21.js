(function(){
  /* ---- banner data ---- */
  var COPY={
    h1:"The deals won't wait.",
    h2:"And now you don't have to.",
    s:'Lease-to-own on thousands of Cyber Week deals',
    c:'Shop Cyber Deals Now'
  };
  /* L = headline lines, [sentence 1 lines, sentence 2 lines]; joined back they must equal the copy */
  var SIZES=[
    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,type:'col',
      logo:200,L:[["The deals won't wait."],['And now you',"don't have to."]],
      sub:true,cta:{f:28,py:18,px:42},g:{l:24,s:16,c:26}},
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,type:'col',
      logo:240,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']],
      sub:true,cta:{f:34,py:24,px:52},g:{l:40,s:26,c:38}},
    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,type:'col',
      logo:220,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']],
      sub:true,cta:{f:32,py:22,px:48},g:{l:36,s:24,c:34}},
    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,type:'col',
      logo:100,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']],
      sub:true,narrow:true,cta:{f:15,py:11,px:18},g:{l:14,s:10,c:16}},
    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,type:'col',
      logo:88,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']],
      cta:{f:12,py:8,px:12},g:{l:12,c:14}},
    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,type:'col',
      logo:76,L:[['The deals',"won't wait."],['And now you',"don't have to."]],
      cta:{f:12,py:8,px:14},g:{l:8,c:10}},
    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,type:'row',
      logo:{x:14,w:96},head:{x:128,w:412},box:{x:560,w:154,f:13,py:9,px:12},
      L:[["The deals won't wait."],["And now you don't have to."]]},
    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,type:'row',
      logo:{x:6,w:46},head:{x:60,w:172},box:{x:240,w:74,f:8,py:4,px:5},
      L:[["The deals won't wait."],["And now you don't have to."]]}
  ];
  SIZES.forEach(function(sz){
    if(sz.L[0].join(' ')!==COPY.h1||sz.L[1].join(' ')!==COPY.h2) console.error('KAT26021: headline lines do not match the copy at '+sz.w+'x'+sz.h);
  });
  /* a few words break from the sentence's White/Pink into Light Blue, echoing the subhead color for a multicolor feel */
  var ACCENT={deals:1,now:1};
  /* sizes with a subhead get the top-left headline / bottom subhead+CTA layout, the subhead forced to these two lines */
  var SUB_LINES=['Lease-to-own on thousands','of Cyber Week deals'];
  if(SUB_LINES.join(' ')!==COPY.s) console.error('KAT26021: subhead lines do not match the copy');

  var MH=null;
  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function host(){ if(!MH){ MH=el('div','k21','position:absolute;left:-99999px;top:0;visibility:hidden;width:4000px;height:4000px'); document.body.appendChild(MH); } return MH; }
  function heightOf(node,w){ var h=host(); node.style.width=w+'px'; h.appendChild(node); var v=node.offsetHeight; h.removeChild(node); node.style.width=''; return v; }
  function logoSvg(w){
    var s=document.createElementNS('http://www.w3.org/2000/svg','svg');
    s.setAttribute('class','k21-logo'); s.setAttribute('viewBox','0 0 521 116'); s.setAttribute('role','img'); s.setAttribute('aria-label','Katapult');
    s.style.width=w+'px';
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); s.appendChild(u);
    return s;
  }
  function headline(L){
    var p=el('p','k21-h');
    L.forEach(function(lines,i){
      lines.forEach(function(t){
        var s=el('span','t'+(i+1));
        t.split(' ').forEach(function(w,wi){
          if(wi) s.appendChild(document.createTextNode(' '));
          var key=w.toLowerCase().replace(/[^a-z']/g,'');
          if(ACCENT[key]){ var a=el('span','ta'); a.textContent=w; s.appendChild(a); }
          else s.appendChild(document.createTextNode(w));
        });
        p.appendChild(s);
      });
    });
    return p;
  }
  /* largest font size at which the stack fits w x h */
  /* headline block sized down proportionally across every frame */
  var FIT_SCALE=.85;
  /* subhead trimmed to 2/3 of its width-fit size, per feedback on the enlarged 2-line subhead */
  var SUB_SCALE=2/3;
  function fit(p,w,h){
    var m=host(); p.style.cssText='position:absolute;font-size:100px'; m.appendChild(p);
    var W=p.offsetWidth, H=p.offsetHeight; m.removeChild(p); p.style.cssText='';
    return Math.floor(100*Math.min(w/W,h/H)*FIT_SCALE*2)/2;
  }
  function cta(c){ var b=el('span','k21-cta','font-size:'+c.f+'px;padding:'+c.py+'px '+c.px+'px'); b.textContent=COPY.c; return b; }

  function canvas(sz){
    var k=el('div','k21','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    var hd=headline(sz.L);
    if(sz.type==='row'){
      var lg=logoSvg(sz.logo.w), lh=sz.logo.w*116/521;
      lg.style.cssText+=';position:absolute;left:'+sz.logo.x+'px;top:'+((sz.h-lh)/2)+'px';
      k.appendChild(lg);
      var ih=sz.h-2*sz.sy;
      var hb=el('div','k21-box','left:'+sz.head.x+'px;top:'+sz.sy+'px;width:'+sz.head.w+'px;height:'+ih+'px');
      hd.style.fontSize=fit(hd,sz.head.w,ih)+'px'; hb.appendChild(hd); k.appendChild(hb);
      var B=sz.box, cb=el('div','k21-box','left:'+B.x+'px;top:'+sz.sy+'px;width:'+B.w+'px;height:'+ih+'px');
      var p=cta(B); p.style.width='100%'; cb.appendChild(p); k.appendChild(cb);
      return k;
    }
    var iw=sz.w-2*sz.sx, ihc=sz.h-2*sz.sy, G=sz.g;
    var col=el('div','k21-col','left:'+sz.sx+'px;top:'+sz.sy+'px;width:'+iw+'px;height:'+ihc+'px');

    if(sz.sub){
      /* headline pinned top-left; subhead (bigger, forced 2 lines) sits right above the CTA at the bottom;
         logo moves to the bottom-right corner, or below the CTA only on frames too narrow for a side-by-side logo */
      var vertical=!!sz.narrow;
      var sub=el('p','k21-s2');
      SUB_LINES.forEach(function(l){ var ln=el('span'); ln.textContent=l; sub.appendChild(ln); });
      sub.style.fontSize=(fit(sub,iw,9999)*SUB_SCALE)+'px';
      sub.style.marginTop=G.s+'px';
      var used=heightOf(sub,iw)+G.s;
      var cw=el('div','','margin-top:'+G.c+'px'); cw.appendChild(cta(sz.cta)); used+=heightOf(cw,iw)+G.c;
      var logoBelow=null;
      if(vertical){ logoBelow=el('div','','margin-top:'+G.l+'px'); logoBelow.appendChild(logoSvg(sz.logo)); used+=heightOf(logoBelow,iw)+G.l; }
      hd.style.fontSize=fit(hd,iw,ihc-used)+'px';
      col.appendChild(hd);
      col.appendChild(el('div','k21-gap'));
      col.appendChild(sub);
      col.appendChild(cw);
      if(logoBelow) col.appendChild(logoBelow);
      k.appendChild(col);
      if(!vertical){
        var corner=logoSvg(sz.logo);
        corner.style.cssText+=';position:absolute;right:'+sz.sx+'px;bottom:'+sz.sy+'px';
        k.appendChild(corner);
      }
      return k;
    }

    /* no subhead on this size: logo on top, headline fills the rest, CTA anchored to the bottom */
    col.appendChild(logoSvg(sz.logo));
    col.appendChild(el('div','k21-gap'));
    var used=sz.logo*116/521+G.l;
    var cw=el('div','','margin-top:'+G.c+'px'); cw.appendChild(cta(sz.cta)); used+=heightOf(cw,iw)+G.c;
    hd.style.fontSize=fit(hd,iw,ihc-used)+'px';
    col.appendChild(hd); col.appendChild(cw);
    k.appendChild(col);
    return k;
  }

  function frameName(sz){ return 'KAT26021-FlatBrandType-'+sz.w+'x'+sz.h+'-Static-'+sz.plat+'-V1'; }
  function label(sz){ return sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }
  function figure(sz){
    var f=el('figure','kb-fig'), sc=el('div','kb-scroll'), fr=el('div','k21-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=sz.show;
    fr.appendChild(canvas(sz)); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'), b=el('b'), mo=el('span','mono'); b.textContent=label(sz); mo.textContent=frameName(sz);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }

  function render(){
    var v1=document.getElementById('k21-v1-rows'); v1.replaceChildren();
    ['PMAX','Programmatic'].forEach(function(pl){
      var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; v1.appendChild(hd);
      var row=el('div','kb-row');
      SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){ row.appendChild(figure(sz)); });
      v1.appendChild(row);
    });
    applyScale();
  }
  /* ---- scale + safe zones ---- */
  var full=document.getElementById('k21-full'), safe=document.getElementById('k21-safe'), root=document.querySelector('.hub-ch-k21');
  function applyScale(){
    [].forEach.call(document.querySelectorAll('.k21-frame'),function(fr){
      var s=full.checked?1:+fr.dataset.s;
      fr.style.width=(fr.dataset.w*s)+'px'; fr.style.height=(fr.dataset.h*s)+'px';
      fr.firstChild.style.transform='scale('+s+')';
    });
  }
  full.addEventListener('change',applyScale);
  var fl=document.fonts?Promise.all(['500','700'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(render);
  function applySafe(){ root.classList.toggle('k21-safe-on',safe.checked); }
  safe.addEventListener('change',applySafe); applySafe();
})();
