(function(){
  /* ---- banner data ---- */
  var COPY={
    h1:"The deals won't wait.",
    h2:"And now you don't have to.",
    s:'Lease-to-own on thousands of Cyber Week deals.',
    c:'Shop Cyber Deals Now'
  };
  /* Every size is placed from Lucas's Figma frames (file D8FpNuKI3uPGjCPqonIn3C, page 547:1720):
     PMAX V1 547:2851 / V2 547:2904, Programmatic V1 547:2957 / V2 547:3031.
     All numbers are canvas px. Text blocks: x = left edge or cx = center (centered stacks), y = top of the first line box,
     f = font size, lh = line pitch, L = lines. Headline L = [sentence 1 lines, sentence 2 lines]; joined they must equal the copy.
     logo: w = width, x/cx/r = left/center/right edge, y/b = top/bottom edge. cta: pill padding pt/pb/px, or a fixed w x h pill.
     v2 = what the Cream version changes on that size (Figma nudged a few positions and sizes per version).
     Headline y values are tuned against Figma renders (ink compared row by row), not copied from the node tree:
     Figma's V1 PMAX paragraphs carry padding that does not show in the render, and Chrome sets glyphs a few px lower. */
  var SIZES=[
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      head:{x:60,y:68,f:151,lh:138.9,L:[['The deals',"won't wait."],['And now you',"don't have to."]]},
      sub:{x:60,y:861.73,f:63,lh:71.13,L:['Lease-to-own on thousands','of Cyber Week deals.']},
      cta:{x:60,y:1042.91,f:45,lh:39.1,pt:23,pb:24.09,px:52},
      logo:{w:270,r:52,b:63},
      v2:{head:{y:69}}},
    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      head:{x:60,y:39,f:99.5,lh:91.5,L:[["The deals won't wait."],['And now you',"don't have to."]]},
      sub:{x:60,y:378.97,f:48.3,lh:55.58,L:['Lease-to-own on thousands','of Cyber Week deals.']},
      cta:{x:60,y:516.81,f:42,lh:32.2,pt:17.5,pb:17.69,px:42},
      logo:{w:200,r:60,b:43},
      v2:{head:{y:45},sub:{y:374.97},cta:{y:512.81},logo:{b:47}}},
    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      head:{x:48,y:49,f:156.5,lh:144,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']]},
      sub:{x:48,y:908,f:50.99,lh:58.59,L:['Lease-to-own on thousands','of Cyber Week deals.']},
      cta:{x:48,y:1059.2,f:43,lh:36.8,pt:22,pb:22,px:48},
      logo:{w:220,r:48,b:60},
      v2:{head:{y:62},sub:{f:55}}},
    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,
      head:{cx:149.68,y:36.38,f:50,lh:46,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']]},
      sub:{cx:149.68,y:382.59,f:21.86,lh:25.2,L:['Lease-to-own','on thousands','of Cyber Week deals.']},
      cta:{cx:150.18,y:481.38,f:18,lh:17.25,pt:10.5,pb:10.75,px:18},
      logo:{w:109,cx:150.49,y:551.38}},
    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,
      head:{cx:80,y:129,f:28.96,lh:27,L:[['The deals',"won't wait."],['And now',"you don't",'have to.']]},
      sub:{cx:80,y:291,f:16.26,lh:18.75,L:['Lease-to-own','on thousands of','Cyber Week deals.']},
      cta:{cx:80,y:372,f:16,lh:16.8,pt:8,pb:8,px:24,L:['Shop Cyber','Deals Now']},
      logo:{w:99,cx:80,y:446}},
    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,
      logo:{w:76,x:16,y:17.7},
      head:{x:16,y:43.6,f:39,lh:35.9,L:[['The deals',"won't wait."],['And now you',"don't have to."]]},
      cta:{x:16,y:202.3,f:13,lh:13.8,pt:8,pb:8,px:14,h:30},
      v2:{cta:{f:15}}},
    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,
      logo:{w:96,x:14,y:34.31},
      head:{x:137.68,y:11.31,f:33.26,lh:30.62,L:[["The deals won't wait."],["And now you don't have to."]]},
      cta:{x:560,y:20,w:154,h:50,f:16,lh:15.9,L:['Shop Cyber','Deals Now']}},
    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,
      logo:{w:46,x:6,y:19.88},
      head:{x:63.68,y:12.06,f:13.74,lh:11.89,L:[["The deals won't wait."],["And now you don't have to."]]},
      cta:{x:240,y:9.81,w:74,h:30.38,f:10,lh:11.2,wt:400,L:['Shop Cyber','Deals Now']}}
  ];
  var VERSIONS=['V1','V2'];
  SIZES.forEach(function(sz){
    var L=sz.head.L;
    if(L[0].join(' ')!==COPY.h1||L[1].join(' ')!==COPY.h2) console.error('KAT26021: headline lines do not match the copy at '+sz.w+'x'+sz.h);
    if(sz.sub&&sz.sub.L.join(' ')!==COPY.s) console.error('KAT26021: subhead lines do not match the copy at '+sz.w+'x'+sz.h);
    if(sz.cta.L&&sz.cta.L.join(' ')!==COPY.c) console.error('KAT26021: CTA lines do not match the copy at '+sz.w+'x'+sz.h);
  });
  /* "deals" and "now" break from their sentence color into the accent (Lavender on V1, Dark Blue on V2) */
  var ACCENT={deals:1,now:1};

  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function merge(a,b){ var o={},k; for(k in a) o[k]=a[k]; if(b) for(k in b) o[k]=b[k]; return o; }
  function spec(sz,v){
    var o=v==='V2'&&sz.v2?sz.v2:{};
    return {head:merge(sz.head,o.head),sub:sz.sub&&merge(sz.sub,o.sub),cta:merge(sz.cta,o.cta),logo:merge(sz.logo,o.logo)};
  }
  function place(e,b){
    var s=e.style;
    if(b.cx!=null){ s.left=b.cx+'px'; e.classList.add('k21-c'); } else if(b.r!=null) s.right=b.r+'px'; else s.left=b.x+'px';
    if(b.b!=null) s.bottom=b.b+'px'; else s.top=b.y+'px';
  }
  function text(cls,b){ var p=el('p',cls,'font-size:'+b.f+'px;line-height:'+b.lh+'px'); place(p,b); return p; }
  function logoSvg(b){
    var s=document.createElementNS('http://www.w3.org/2000/svg','svg');
    s.setAttribute('class','k21-logo'); s.setAttribute('viewBox','0 0 521 116'); s.setAttribute('role','img'); s.setAttribute('aria-label','Katapult');
    s.style.position='absolute'; s.style.width=b.w+'px'; place(s,b);
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); s.appendChild(u);
    return s;
  }
  function headline(b){
    var p=text('k21-h',b);
    b.L.forEach(function(lines,i){
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
  function subhead(b){ var p=text('k21-s2',b); b.L.forEach(function(l){ var s=el('span'); s.textContent=l; p.appendChild(s); }); return p; }
  function cta(b){
    var c=el('span','k21-cta','font-size:'+b.f+'px;line-height:'+b.lh+'px;letter-spacing:-.004em');
    if(b.w){ c.style.width=b.w+'px'; c.style.height=b.h+'px'; }
    else { c.style.padding=b.pt+'px '+b.px+'px '+b.pb+'px'; if(b.h) c.style.height=b.h+'px'; }
    if(b.wt) c.style.fontWeight=b.wt;
    (b.L||[COPY.c]).forEach(function(l){ var s=el('span'); s.textContent=l; c.appendChild(s); });
    place(c,b); return c;
  }

  function canvas(sz,v){
    var S=spec(sz,v);
    var k=el('div','k21 k21-'+v.toLowerCase(),'width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    k.appendChild(headline(S.head));
    if(S.sub) k.appendChild(subhead(S.sub));
    k.appendChild(cta(S.cta));
    k.appendChild(logoSvg(S.logo));
    return k;
  }

  function frameName(sz,v){ return 'KAT26021-FlatBrandType-'+sz.w+'x'+sz.h+'-Static-'+sz.plat+'-'+v; }
  function label(sz){ return sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }
  function figure(sz,v){
    var f=el('figure','kb-fig'), sc=el('div','kb-scroll'), fr=el('div','k21-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=sz.show;
    fr.appendChild(canvas(sz,v)); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'), b=el('b'), mo=el('span','mono'); b.textContent=label(sz); mo.textContent=frameName(sz,v);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }

  function render(){
    VERSIONS.forEach(function(v){
      var box=document.getElementById('k21-'+v.toLowerCase()+'-rows'); if(!box) return; box.replaceChildren();
      ['PMAX','Programmatic'].forEach(function(pl){
        var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; box.appendChild(hd);
        var row=el('div','kb-row');
        SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){ row.appendChild(figure(sz,v)); });
        box.appendChild(row);
      });
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
  var fl=document.fonts?Promise.all(['400','500','700'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(render);
  function applySafe(){ root.classList.toggle('k21-safe-on',safe.checked); }
  safe.addEventListener('change',applySafe); applySafe();
})();
