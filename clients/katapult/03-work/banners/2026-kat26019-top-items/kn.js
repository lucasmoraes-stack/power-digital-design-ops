(function(){
  /* KAT26019 proposal 2 (2026-10-07): the client asked to lean into the knolling shot,
     not things floating on white. Every product is shot from straight above, laid flat
     on a neutral matte ground (very light salmon) at right angles, with even gutters
     and one key light, so the frame reads as a real flat-lay. Copy is the client's,
     verbatim. Logo, type and CTA sizes per size are the approved V1 ones (kb.js, round 2);
     only the product area changes. */
  var COPY={
    h:'Your Whole Wish List, Lease-to-Own.',
    s:'From couches to TVs to tires, lease-to-own the big stuff at thousands of retailers this Cyber Week.',
    c:'Shop Cyber Deals. Lease to Own.'
  };
  var NAMES={sofa:'Sofa',tv:'TV',tire:'Tire',fridge:'Refrigerator',mattress:'Bed',laptop:'Laptop',washer:'Washing machine',console:'Game console',grill:'Grill'};
  /* cutouts, injected by build: id -> {src,w,h} (w/h = the cutout's own box, shadow included) */
  var KN_PHOTOS={};
  /* V2: the house storyboard (as V1 of this job). S01 logo + products, S02 the products
     trade places and the headline lands, S03 = the V1 end frame. A product only trades
     places with one of a similar shape (wide, square-ish, tall), so every row keeps its
     proportions and the flat-lay stays orderly from scene to scene; the swap pulls from the
     whole set, so even the 1-slot sizes visibly change. */
  var SHAPES=[['sofa','tv','console'],['tire','laptop','mattress'],['fridge','washer']];
  function rowsFor(K,scene){
    if(!scene) return K.rows;
    return K.rows.map(function(r){ return r.map(function(id){
      for(var i=0;i<SHAPES.length;i++){ var g=SHAPES[i], j=g.indexOf(id); if(j>-1) return g[(j+scene)%g.length]; }
      return id;
    }); });
  }


  /* knoll = the flat-lay. Rows of products; each row is scaled so its items share one
     height and run edge to edge across the area with the gutter between them. If the
     rows don't fit the area's height, they all shrink together and the gutters open up so
     both ends stay flush; spare height centres the block. The subhead's three nouns
     (couch, TV, tire) lead wherever there's room for them.
       flow: the area runs from under the copy (+top) down to bottom, or to the CTA box
       box:  a fixed area {x,y,w,h} */
  var SIZES=[
    {w:1200,h:628,sb:.3,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,vcenter:true,
      logo:{x:60,y:32,w:200},
      text:{x:60,y:118,w:520,hf:58,sf:26,g1:18,g2:30,cta:{f:28,py:19,px:40}},
      knoll:{box:{x:640,y:32,w:500,h:564},gap:28,rows:[['sofa','tv'],['tire','fridge','washer'],['mattress','laptop','console']]}},
    {w:1200,h:1200,sb:.26,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      logo:{x:60,y:60,w:230},
      text:{x:60,y:150,w:1080,hf:84,sf:36,g1:24,g2:36,cta:{f:36,py:26,px:54}},
      knoll:{x:60,w:1080,bottom:1140,top:36,gap:40,rows:[['sofa','tv','tire'],['fridge','mattress','washer','laptop','console']]}},
    {w:960,h:1200,sb:.26,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      logo:{x:48,y:60,w:210},
      text:{x:48,y:146,w:864,hf:76,sf:34,g1:22,g2:34,cta:{f:34,py:24,px:50}},
      knoll:{x:48,w:864,bottom:1140,top:40,gap:36,rows:[['sofa','tv','tire'],['fridge','mattress','washer','laptop','console']]}},
    {w:300,h:600,sb:.75,plat:'Programmatic',sx:12,sy:12,show:1,
      logo:{x:16,y:16,w:96},
      text:{x:16,y:50,w:268,hf:29,sf:15,g1:8},
      ctabox:{x:16,bottom:580,w:268,f:17,py:11,px:16},
      knoll:{x:16,w:268,top:16,gap:14,rows:[['sofa','tv'],['tire','fridge','laptop'],['mattress','washer','console']]}},
    {w:160,h:600,sb:.75,plat:'Programmatic',sx:8,sy:8,show:1,
      logo:{x:12,y:14,w:84},
      text:{x:12,y:46,w:136,hf:24,sf:12,g1:8,g2:12,cta:{f:13,py:8,px:12}},
      knoll:{x:12,w:136,bottom:584,top:16,gap:12,rows:[['sofa'],['tv'],['tire','fridge']]}},
    {w:300,h:250,sb:1,plat:'Programmatic',sx:8,sy:8,show:1,
      logo:{x:12,y:12,w:72},
      text:{x:12,y:44,w:154,hf:20.5,sf:10,g1:6,g2:9,cta:{f:11.5,py:7,px:12}},
      knoll:{box:{x:174,y:12,w:114,h:226},gap:10,rows:[['sofa'],['tv'],['tire','fridge']]}},
    {w:728,h:90,sb:.6,plat:'Programmatic',sx:6,sy:6,show:1,
      logo:{x:14,cy:45,w:92},
      text:{x:118,y:6,w:250,hb:78,hf:25},
      ctabox:{x:574,y:6,w:142,hb:78,f:13,py:8,px:12},
      knoll:{box:{x:378,y:12,w:182,h:66},gap:10,rows:[['sofa','tv','tire']]}},
    {w:320,h:50,sb:1,plat:'Programmatic',sx:4,sy:4,show:1,
      logo:{x:6,cy:25,w:44},
      text:{x:56,y:4,w:132,hb:42,hf:14},
      ctabox:{x:242,y:4,w:74,hb:42,f:7,py:4,px:5},
      knoll:{box:{x:190,y:6,w:46,h:38},gap:0,rows:[['sofa']]}}
  ];

  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  /* the copy, the product area and the CTA are laid out by the browser inside the real
     frame; the products then fill whatever room their area really got. Each area watches
     its own size, so a font that loads late, a hub view that opens after being hidden
     (display:none = size 0), or any other reflow re-fits the products. Nothing is measured
     outside the frame. */
  var RULES=typeof WeakMap!=='undefined'?new WeakMap():null;
  var RO=typeof ResizeObserver!=='undefined'?new ResizeObserver(function(es){ es.forEach(function(e){ fit(e.target); }); }):null;
  function fit(area){
    var K=RULES&&RULES.get(area); if(!K) return;
    var W=area.clientWidth, H=area.clientHeight; if(!W||!H) return;
    if(area.dataset.fit===W+'x'+H) return;
    area.dataset.fit=W+'x'+H; area.replaceChildren(); knoll(area,K);
  }
  function cta(c){ var b=el('span','kn-cta','font-size:'+c.f+'px;padding:'+c.py+'px '+c.px+'px'); b.textContent=COPY.c; return b; }

  /* fill an area (already laid out) with the rows of products, coordinates relative to it */
  function knoll(area,K){
    var W=area.clientWidth, H=area.clientHeight;
    var rows=(K.scRows||K.rows).map(function(r){
      var ar=r.map(function(id){ var p=KN_PHOTOS[id]; return p?p.w/p.h:1; });
      var sum=ar.reduce(function(a,b){return a+b;},0);
      return {ids:r,ar:ar,h:(W-(r.length-1)*K.gap)/sum};
    });
    var rowsH=rows.reduce(function(a,r){return a+r.h;},0), gaps=(rows.length-1)*K.gap;
    var f=Math.max(0,Math.min(1,(H-gaps)/rowsH)), y=(H-(rowsH*f+gaps))/2;
    rows.forEach(function(r){
      var h=r.h*f, ws=r.ar.map(function(a){return a*h;}), sum=ws.reduce(function(a,b){return a+b;},0);
      var n=r.ids.length, g=n>1?(W-sum)/(n-1):0, x=n>1?0:(W-sum)/2;
      r.ids.forEach(function(id,i){
        var it=el('div','kn-item','left:'+x.toFixed(1)+'px;top:'+y.toFixed(1)+'px;width:'+ws[i].toFixed(1)+'px;height:'+h.toFixed(1)+'px');
        it.title=NAMES[id];
        if(KN_PHOTOS[id]){ var im=el('img'); im.src=KN_PHOTOS[id].src; im.alt=NAMES[id]; it.appendChild(im); }
        area.appendChild(it); x+=ws[i]+g;
      });
      y+=h+K.gap;
    });
  }

  /* scene: 0 = static / end frame, 1 = S01 (logo + products), 2 = S02 (+ headline) */
  function canvas(sz,scene){
    scene=scene||0;
    var k=el('div','kn','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    var L=sz.logo, lh=L.w*116/521;
    var logo=document.createElementNS('http://www.w3.org/2000/svg','svg');
    logo.setAttribute('class','kn-logo'); logo.setAttribute('viewBox','0 0 521 116'); logo.setAttribute('role','img'); logo.setAttribute('aria-label','Katapult');
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); logo.appendChild(u);
    logo.style.width=L.w+'px';

    var T=sz.text;
    var t=el('div','kn-text'+(T.hb?' is-center':''));
    var hd=el('p','kn-h','font-size:'+T.hf+'px');
    /* narrow sizes may break Lease-to-Own only after "to-", never after "Lease-" (text unchanged) */
    var hi=COPY.h.indexOf('Lease-to');
    hd.textContent=COPY.h.slice(0,hi); var nb=el('span','','white-space:nowrap'); nb.textContent='Lease-to'; hd.appendChild(nb); hd.appendChild(document.createTextNode(COPY.h.slice(hi+8)));
    t.appendChild(hd);
    /* scenes hide copy with visibility only, so the layout (and the product area) never moves between scenes */
    var full=scene===0;
    if(T.sf){ var s=el('p','kn-s'+(full?'':' kn-hide'),'font-size:'+T.sf+'px;margin-top:'+(T.g1||0)+'px'); s.textContent=COPY.s; t.appendChild(s); }
    if(T.cta){ var cw=el('div',full?'':'kn-hide','margin-top:'+(T.g2||0)+'px'); cw.appendChild(cta(T.cta)); t.appendChild(cw); }
    if(scene===1) hd.classList.add('kn-hide');

    var C=sz.ctabox, cb=null;
    if(C){ cb=el('div','kn-ctabox',C.hb?'height:'+C.hb+'px':''); var p=cta(C); p.style.width='100%'; p.style.boxSizing='border-box'; cb.appendChild(p); }
    if(cb&&!full) p.classList.add('kn-hide');

    var K0=sz.knoll, K={gap:K0.gap,rows:K0.rows,scRows:rowsFor(K0,scene),box:K0.box,top:K0.top,bottom:K0.bottom}, area=el('div','kn-area'), gapLT=T.y-L.y-lh;
    if(K.box){
      /* fixed product area; copy either stacks (logo + text, centred on the frame's height
         when vcenter) or sits at fixed spots (leaderboards) */
      area.style.cssText='left:'+K.box.x+'px;top:'+K.box.y+'px;width:'+K.box.w+'px;height:'+K.box.h+'px';
      if(sz.vcenter){
        var col=el('div','kn-col','left:'+T.x+'px;top:'+sz.sy+'px;bottom:'+sz.sy+'px;width:'+T.w+'px;justify-content:center');
        t.style.marginTop=gapLT+'px'; col.appendChild(logo); col.appendChild(t); k.appendChild(col);
      } else {
        logo.style.cssText+=';position:absolute;left:'+L.x+'px;top:'+(L.cy!=null?L.cy-lh/2:L.y)+'px';
        t.style.cssText+=';position:absolute;left:'+T.x+'px;top:'+T.y+'px;width:'+T.w+'px;'+(T.hb?'height:'+T.hb+'px':'');
        k.appendChild(logo); k.appendChild(t);
      }
      if(cb){ cb.style.cssText+=';position:absolute;left:'+C.x+'px;top:'+C.y+'px;width:'+C.w+'px'; k.appendChild(cb); }
      k.appendChild(area);
    } else {
      /* vertical: logo, copy, product area, CTA in one column; the area takes the rest */
      var bottom=C&&C.bottom!=null?C.bottom:K.bottom;
      var col2=el('div','kn-col','left:'+T.x+'px;top:'+L.y+'px;width:'+T.w+'px;height:'+(bottom-L.y)+'px');
      t.style.marginTop=gapLT+'px'; area.style.marginTop=K.top+'px';
      col2.appendChild(logo); col2.appendChild(t); col2.appendChild(area);
      if(cb){ cb.style.marginTop=K.top+'px'; col2.appendChild(cb); }
      k.appendChild(col2);
    }
    if(RULES) RULES.set(area,K);
    if(RO) RO.observe(area);
    return k;
  }

  function frameName(sz,v,scene){ return 'KAT26019-TopItems-'+sz.w+'x'+sz.h+'-'+(v===1?'Static':'Animated')+'-'+sz.plat+'-V'+v+(scene?'-S0'+scene:'')+'-Knolling'; }
  function label(sz){ return sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }
  function figure(sz,v,scene,scale,cap){
    var f=el('figure','kb-fig'), sc=el('div','kb-scroll'), fr=el('div','kn-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=scale;
    fr.appendChild(canvas(sz,v===1||scene===3?0:scene)); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'), b=el('b'), mo=el('span','mono'); b.textContent=cap; mo.textContent=frameName(sz,v,scene);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }
  function render(){
    if(RO) RO.disconnect();
    var v=document.getElementById('kn-v1-rows'); v.replaceChildren();
    ['PMAX','Programmatic'].forEach(function(pl){
      var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; v.appendChild(hd);
      /* not .kb-row: the job card thumbnail keeps showing the V1 grid */
      var row=el('div','kn-row');
      SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){ row.appendChild(figure(sz,1,0,sz.show,label(sz))); });
      v.appendChild(row);
    });
    var v2=document.getElementById('kn-v2-rows');
    if(v2){
      v2.replaceChildren();
      var SCN=['S01 · Logo and products','S02 · Products swap, headline lands','S03 · End frame = V1'];
      SIZES.forEach(function(sz){
        var b=el('div','kb-sb'), t=el('b'); t.textContent=label(sz)+' · '+sz.plat; b.appendChild(t);
        var r=el('div','kb-sb-scenes');
        [1,2,3].forEach(function(n){ r.appendChild(figure(sz,2,n,sz.sb,SCN[n-1])); });
        b.appendChild(r); v2.appendChild(b);
      });
    }
    applyScale();
    /* first fit right away where the frame is already visible; the observer covers the rest */
    fitAll();
  }
  var full=document.getElementById('kn-full'), safe=document.getElementById('kn-safe'), root=document.querySelector('.kn-part');
  function applyScale(){
    [].forEach.call(document.querySelectorAll('.kn-frame'),function(fr){
      var s=full&&full.checked?1:+fr.dataset.s;
      fr.style.width=(fr.dataset.w*s)+'px'; fr.style.height=(fr.dataset.h*s)+'px';
      fr.firstChild.style.transform='scale('+s+')';
    });
  }
  if(full) full.addEventListener('change',applyScale);
  /* opening the job view (hash change) re-fits right away; the exporter calls knFitAll
     before it snapshots the frames, so no capture ever lands between two layouts */
  function fitAll(){ [].forEach.call(document.querySelectorAll('.kn-area'),fit); }
  window.knFitAll=fitAll;
  window.addEventListener('hashchange',function(){ setTimeout(fitAll,0); setTimeout(fitAll,250); });
  var fl=document.fonts?Promise.all(['400','500'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(render);
  /* any font that finishes loading later (Aktiv Grotesk on a slow connection) re-runs the
     layout, so the product area always matches the copy as it finally renders */
  if(document.fonts){
    var pend=0, again=function(){ if(pend) return; pend=setTimeout(function(){ pend=0; render(); },0); };
    document.fonts.ready.then(again);
    if(document.fonts.addEventListener) document.fonts.addEventListener('loadingdone',again);
  }
  function applySafe(){ if(root) root.classList.toggle('kn-safe-on',!!(safe&&safe.checked)); }
  if(safe) safe.addEventListener('change',applySafe); applySafe();
})();
