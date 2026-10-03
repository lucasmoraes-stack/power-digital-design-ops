(function(){
  /* ---- channel tabs ---- */
  var tabs=[].slice.call(document.querySelectorAll('.hub-tab'));
  function setCh(ch){
    [].forEach.call(document.querySelectorAll('[data-ch]'),function(el){ el.hidden=el.getAttribute('data-ch')!==ch; });
    tabs.forEach(function(t){ t.setAttribute('aria-selected',String(t.getAttribute('data-go')===ch)); });
  }
  tabs.forEach(function(t){ t.addEventListener('click',function(){ setCh(t.getAttribute('data-go')); }); });
  var h=location.hash||'';
  setCh(/^#(post-|p\d|organic)/.test(h)?'organic':'banners');

  /* ---- banner data ---- */
  var COPY={
    h:'Your Whole Wish List, Lease-to-Own.',
    s:'From couches to TVs to tires, lease-to-own the big stuff at thousands of retailers this Cyber Week.',
    c:'Shop Cyber Deals. Lease to Own.'
  };
  var NAMES={sofa:'Armchair',tv:'Monitor',tire:'Tires',fridge:'Refrigerator',mattress:'Bed',laptop:'Laptop',washer:'Dishwasher',console:'Game controller',grill:'Gas grill'};
  var POOL=['sofa','tv','tire','fridge','mattress','laptop','washer','console','grill'];
  /* photos: when a cutout exists, list it here as item:'data:image/png;base64,...' */
  var PHOTOS={};

  var SIZES=[
    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,sb:.3,
      logo:{x:60,y:32,w:200},
      text:{x:60,y:118,w:520,hf:58,sf:24,g1:18,g2:30,cta:{f:26,py:18,px:38}},
      grid:{x:640,y:32,w:500,h:564,c:3,r:3}},
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,sb:.26,flow:{gap:40,bottom:60},
      logo:{x:60,y:60,w:230},
      text:{x:60,y:150,w:1000,hf:84,sf:30,sw:880,g1:22,g2:32,cta:{f:30,py:22,px:46}},
      grid:{x:60,w:1080,c:4,r:2}},
    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,sb:.26,flow:{gap:36,bottom:60},
      logo:{x:48,y:60,w:210},
      text:{x:48,y:146,w:864,hf:76,sf:28,g1:20,g2:30,cta:{f:28,py:20,px:42}},
      grid:{x:48,w:864,c:3,r:2}},
    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,sb:.75,flow:{gap:12,bottom:20},
      logo:{x:16,y:16,w:96},
      text:{x:16,y:50,w:268,hf:29,sf:13,g1:8},
      grid:{x:16,w:268,c:2,r:3},
      ctabox:{x:16,y:540,w:268,f:15,py:10,px:16}},
    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,sb:.75,flow:{gap:16,bottom:16},
      logo:{x:12,y:14,w:84},
      text:{x:12,y:46,w:136,hf:20,g2:12,cta:{f:12,py:8,px:13}},
      grid:{x:12,w:136,c:2,r:3}},
    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,sb:1,
      logo:{x:12,y:12,w:72},
      text:{x:12,y:46,w:150,hf:20.5,g2:12,cta:{f:11.5,py:8,px:13}},
      grid:{x:172,y:10,w:118,h:230,c:2,r:3}},
    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,sb:.6,
      logo:{x:14,cy:45,w:92},
      text:{x:118,y:6,w:250,hb:78,hf:25,center:true},
      grid:{x:352,y:2,w:198,h:86,c:3,r:1},
      ctabox:{x:574,y:6,w:142,hb:78,f:12,py:8,px:12}},
    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,sb:1,
      logo:{x:6,cy:25,w:44},
      text:{x:56,y:3,w:132,hb:44,hf:14,center:true},
      grid:{x:186,y:2,w:46,h:46,c:1,r:1},
      ctabox:{x:242,y:4,w:74,hb:42,f:7,py:4,px:5}}
  ];

  var MH=null;
  function measureHost(){ if(!MH){ MH=el('div','','position:absolute;left:-99999px;top:0;visibility:hidden'); document.body.appendChild(MH); } return MH; }
  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function rot(a,n){ n=n%a.length; return a.slice(n).concat(a.slice(0,n)); }
  function itemsFor(sz,scene){
    var n=sz.grid.c*sz.grid.r;
    var list=scene===1?rot(POOL,5):scene===2?rot(POOL,3):POOL;
    return list.slice(0,n);
  }
  function cta(c){ var b=el('span','kb-cta','font-size:'+c.f+'px;padding:'+c.py+'px '+c.px+'px'); b.textContent=COPY.c; return b; }

  /* scene: 0 = static / end frame, 1 = S01, 2 = S02 */
  function canvas(sz,scene){
    var k=el('div','kb'+(Object.keys(PHOTOS).length?' is-photo':''),'width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    var L=sz.logo, lh=L.w*116/521;
    var logo=document.createElementNS('http://www.w3.org/2000/svg','svg');
    logo.setAttribute('class','kb-logo'); logo.setAttribute('viewBox','0 0 521 116'); logo.setAttribute('role','img'); logo.setAttribute('aria-label','Katapult');
    logo.style.cssText='position:absolute;left:'+L.x+'px;top:'+(L.cy!=null?L.cy-lh/2:L.y)+'px;width:'+L.w+'px';
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); logo.appendChild(u);
    k.appendChild(logo);

    var T=sz.text, showText=scene!==1, full=scene===0;
    var t=el('div','kb-text'+(T.center?' is-center':''),'left:'+T.x+'px;top:'+T.y+'px;width:'+T.w+'px;'+(T.hb?'height:'+T.hb+'px;':''));
    var hd=el('p','kb-h','font-size:'+T.hf+'px'); hd.textContent=COPY.h; t.appendChild(hd);
    if(T.sf){ var s=el('p','kb-s'+(full?'':' kb-hide'),'font-size:'+T.sf+'px;margin-top:'+(T.g1||0)+'px;'+(T.sw?'max-width:'+T.sw+'px':'')); s.textContent=COPY.s; t.appendChild(s); }
    if(T.cta){ var w=el('div',full?'':'kb-hide','margin-top:'+(T.g2||0)+'px'); w.appendChild(cta(T.cta)); t.appendChild(w); }
    if(!showText) t.classList.add('kb-hide');
    k.appendChild(t);

    var cb=null;
    if(sz.ctabox){
      var C=sz.ctabox; cb=el('div','kb-ctabox'+(full?'':' kb-hide'),'left:'+C.x+'px;top:'+C.y+'px;width:'+C.w+'px;'+(C.hb?'height:'+C.hb+'px;':''));
      var p=cta(C); p.style.width='100%'; cb.appendChild(p); k.appendChild(cb);
    }

    var G=sz.grid, flow=!!sz.flow;
    var cw=flow?G.w/G.c:G.w/G.c, ch=flow?G.w/G.c*.8:G.h/G.r, m=Math.min(cw,ch);
    var g=flow
      ? el('div','kb-grid kb-grid-flex','margin-top:'+sz.flow.gap+'px;grid-template-columns:repeat('+G.c+',minmax(0,1fr));grid-template-rows:repeat('+G.r+',minmax(0,1fr))')
      : el('div','kb-grid','left:'+G.x+'px;top:'+G.y+'px;width:'+G.w+'px;height:'+G.h+'px;grid-template-columns:repeat('+G.c+','+cw+'px);grid-template-rows:repeat('+G.r+','+ch+'px)');
    itemsFor(sz,scene).forEach(function(id,i){
      var col=i%G.c, edge=G.c>1&&G.r>1, c=el('div','kb-cell'+(edge&&col===0?' is-first':'')+(edge&&col===G.c-1?' is-last':'')); c.title=NAMES[id];
      c.appendChild(el('span','kb-foot','border-radius:'+Math.round(m*.08)+'px'));
      if(PHOTOS[id]){ var im=el('img'); im.src=PHOTOS[id]; im.alt=NAMES[id]; c.appendChild(im); }
      else{
        var lab=m>=110, isz=Math.round(m*(lab?.58:.7));
        var ic=document.createElementNS('http://www.w3.org/2000/svg','svg'); ic.setAttribute('viewBox','0 0 64 64'); ic.setAttribute('width',isz); ic.setAttribute('height',isz); ic.setAttribute('aria-hidden','true');
        var iu=document.createElementNS('http://www.w3.org/2000/svg','use'); iu.setAttribute('href','#kb-i-'+id); ic.appendChild(iu); c.appendChild(ic);
        if(lab){ var lb=el('span','kb-lab','font-size:'+Math.max(9,Math.round(m*.075))+'px'); lb.textContent=NAMES[id]; c.appendChild(lb); }
      }
      g.appendChild(c);
    });
    k.appendChild(g);

    if(flow){ /* vertical sizes: logo, copy, grid, CTA stacked in one column, so items can never ride over the copy */
      var col=el('div','kb-col','left:'+T.x+'px;top:'+L.y+'px;width:'+T.w+'px;bottom:'+sz.flow.bottom+'px');
      logo.style.cssText='width:'+L.w+'px'; col.appendChild(logo);
      t.style.cssText='position:static;width:100%;margin-top:'+Math.max(0,Math.round(T.y-L.y-lh))+'px'; col.appendChild(t);
      col.appendChild(g);
      if(cb){ cb.style.cssText='position:static;width:100%;margin-top:'+sz.flow.gap+'px'; col.appendChild(cb); }
      k.appendChild(col);
    }
    return k;
  }

  function frameName(sz,v,scene){
    return 'KAT26019-TopItems-'+sz.w+'x'+sz.h+'-'+(v===1?'Static':'Animated')+'-'+sz.plat+'-V'+v+(scene?'-S0'+scene:'');
  }
  function figure(sz,v,scene,scale,cap){
    var f=el('figure','kb-fig');
    var sc=el('div','kb-scroll'), fr=el('div','kb-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=scale;
    var c=canvas(sz,v===1?0:(scene===3?0:scene)); fr.appendChild(c); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'); var b=el('b'); b.textContent=cap; var mo=el('span','mono'); mo.textContent=frameName(sz,v,scene);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }
  function label(sz){ return sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }

  function render(){
  var v1=document.getElementById('kb-v1-rows'), v2=document.getElementById('kb-v2-rows');
  v1.replaceChildren(); v2.replaceChildren();
  ['PMAX','Programmatic'].forEach(function(pl){
    var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; v1.appendChild(hd);
    var row=el('div','kb-row');
    SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){ row.appendChild(figure(sz,1,0,sz.show,label(sz))); });
    v1.appendChild(row);
  });
  var SCN=['S01 · Logo and grid','S02 · Items swap, headline lands','S03 · End frame = V1'];
  SIZES.forEach(function(sz){
    var b=el('div','kb-sb'); var t=el('b'); t.textContent=label(sz)+' · '+(sz.plat==='PMAX'?'PMAX':'Programmatic'); b.appendChild(t);
    var r=el('div','kb-sb-scenes');
    [1,2,3].forEach(function(n){ r.appendChild(figure(sz,2,n,sz.sb,SCN[n-1])); });
    b.appendChild(r); v2.appendChild(b);
  });

  applyScale();
  }
  /* ---- scale + safe zones ---- */
  var full=document.getElementById('kb-full'), safe=document.getElementById('kb-safe'), root=document.querySelector('.hub-ch-banners');
  function applyScale(){
    [].forEach.call(document.querySelectorAll('.kb-frame'),function(fr){
      var s=full.checked?1:+fr.dataset.s;
      fr.style.width=(fr.dataset.w*s)+'px'; fr.style.height=(fr.dataset.h*s)+'px';
      fr.firstChild.style.transform='scale('+s+')';
    });
  }
  full.addEventListener('change',applyScale);
  var fl=document.fonts?Promise.all(['300','500','700'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(render);
  function applySafe(){ root.classList.toggle('kb-safe-on',safe.checked); }
  safe.addEventListener('change',applySafe); applySafe();
})();
