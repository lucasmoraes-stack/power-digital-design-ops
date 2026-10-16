(function(){
  /* KAT26019 proposal 2, round 2 (2026-10-13): rebuilt one to one from Lucas's Figma pass
     (file D8FpNuKI3uPGjCPqonIn3C, page 547:1720). The flat-lay is no longer a row
     algorithm: every product sits where Lucas placed it, at true relative scale (tall
     fridge, big bed, sofa), packed tight in the lower part of the frame, with three new
     pieces (nightstand, stick vacuum, gold necklace). Headline is set bigger (Figma
     SemiBold; the hub carries Medium and Bold, see HW), explicit line breaks as in Figma.
     Copy is the client's, verbatim. */
  var COPY={
    h:'Your Whole Wish List, Lease-to-Own.',
    s:'From couches to TVs to tires, lease-to-own the big stuff at thousands of retailers this Cyber Week.',
    c:'Shop Cyber Deals. Lease to Own.'
  };
  /* Figma sets the headline in Aktiv Grotesk SemiBold (600). The hub embeds 300/400/500/700;
     600 would fall back to Bold. Side by side with the Figma render, the hub's 500 draws the
     same stroke as Figma's SemiBold, so the headline stays 500. */
  var HW=500;
  var NAMES={couch:'Sofa',tv:'TV',tire:'Tire',fridge:'Refrigerator',bed:'Bed',laptop:'Laptop',washer:'Washing machine',console:'Game console',nightstand:'Nightstand',vacuum:'Vacuum',necklace:'Necklace'};
  /* cutouts, injected by build: id -> {src,w,h,tb}. tb = the trimmed box as fractions of
     the original image (build trims empty alpha), so Figma's image rects still apply. */
  var KN_PHOTOS={};

  /* shadows, as in Figma (offset x, offset y, blur, alpha); they follow each cutout's alpha */
  var SH={couch:[9,3,10,.22],bed:[8,4,13,.25],nk:[2,1,9,.2],nkS:[1,1,3,.2],nkXS:[1,0,2,.14],nkT:[0,0,1,.17],bedT:[5,0,8,.25]};
  /* image rects inside the item box, in % (left, top, width, height), from Figma */
  var C={ns:[-41.67,-46.94,178.47,189.8],ear:[-625.09,-1008.48,1523.44,1305.8]};

  /* items: [id, x, y, w, h, opts], x/y relative to the size's product origin (ox, oy),
     in Figma's stacking order (later = on top).
     opts: r = rotation (deg) of the image box, Figma style: the box keeps w x h, the image
           box is h x w turned by r; c = image rect in %; fit = 'contain'; sh = shadow;
           ear = earring (crop of the necklace, rounded top) */
  var SIZES=[
    {w:1200,h:628,sb:.3,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      logo:{x:52,y:105.42,w:200},
      text:{x:52,y:191.4,h:{f:62,lh:62,ls:-.696,l:['Your Whole Wish','List, Lease-to-Own.']},
        s:{g:18,f:26,lh:32.24,l:['From couches to TVs to tires, lease-to-own','the big stuff at thousands of retailers this','Cyber Week.']},
        c:{g:30,f:28,lh:32.2,ls:-.14,pt:18.5,pb:18.69,px:40,l:[COPY.c]}},
      knoll:{ox:636,oy:32,items:[
        ['laptop',236,196,82,90],['tv',17,294,163,100],['washer',244,19,146,170],['console',200,316,113,73],
        ['tire',393,175,116,116],['fridge',343,297,174,267],['couch',13,399,314,187,{sh:SH.couch}],
        ['nightstand',387,28,128,153,{c:C.ns}],['bed',0,0,268,282,{fit:'contain',sh:SH.bed}],
        ['necklace',320,212,59,59,{sh:SH.nk}],['necklace',341.4,224.97,5.19,5.84,{ear:1,sh:SH.nk}],['necklace',352.42,224.97,5.19,5.84,{ear:1,sh:SH.nk}]]},
      scenes:['','lhs','lhsc|bed nightstand tire couch','*']},
    {w:1200,h:1200,sb:.26,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      logo:{x:60,y:60,w:230},
      text:{x:60,y:149.17,h:{f:95,lh:90,ls:-1.008,l:['Your Whole Wish','List, Lease-to-Own.']},
        s:{g:23.85,f:36,lh:44.64,l:['From couches to TVs to tires, lease-to-own the big stuff at','thousands of retailers this Cyber Week.']},
        c:{g:36,f:36,lh:41.4,ls:-.18,pt:25,pb:26.39,px:54,l:[COPY.c]}},
      knoll:{ox:60,oy:602.42,items:[
        ['couch',254,294.58,466,277,{sh:SH.couch}],['console',372,204,141,91],['tire',236,30.58,141,141],
        ['tv',8,404.58,219,133],['fridge',8,31,239,368],['bed',725,123.58,403,424,{c:[6.51,0,97.95,100],sh:SH.bed}],
        ['washer',525,36.58,215,252],['laptop',249,174,102,115],
        ['vacuum',842,22.58,224,82,{r:-90,c:[-150.51,-42.86,400,146.43]}],['nightstand',378,24,143.08,171,{c:C.ns}],
        ['necklace',744,24.58,91,91,{sh:SH.nk}],['necklace',777,44.58,8,9,{ear:1,sh:SH.nk}],['necklace',794,44.58,8,9,{ear:1,sh:SH.nk}]]},
      scenes:['lh','lhs','lhsc|fridge nightstand couch bed','*']},
    {w:960,h:1200,sb:.26,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      logo:{x:48,y:60,w:210},
      text:{x:48,y:145.01,h:{f:76,lh:79,ls:-.912,l:['Your Whole Wish','List, Lease-to-Own.']},
        s:{g:22,f:34,lh:42.16,l:['From couches to TVs to tires, lease-to-own the big stuff','at thousands of retailers this Cyber Week.']},
        c:{g:34,f:34,lh:39.1,ls:-.17,pt:23,pb:24.09,px:50,l:[COPY.c]}},
      knoll:{ox:48,oy:568.1,items:[
        ['couch',476,13.9,374,223,{sh:SH.couch}],['fridge',618,239.9,232,358],['washer',408,363.9,199,234],
        ['vacuum',285,336.9,88,262,{c:[-150,-30.92,400,134.27]}],['tire',309,31.9,156,153],
        ['laptop',168,17.9,106,94,{r:-90}],['console',168,123.9,131,84],['nightstand',-1,13.9,159,190,{c:C.ns}],
        ['tv',381,218.9,214,129],['bed',-30,213.9,379,398,{fit:'contain',sh:SH.bed}],
        ['necklace',274,228.9,88,88,{sh:SH.nk}],['necklace',305.91,248.24,7.74,8.7,{ear:1,sh:SH.nk}],['necklace',322.35,248.24,7.74,8.7,{ear:1,sh:SH.nk}]]},
      scenes:['','lhs','lhsc|laptop couch bed vacuum fridge','*']},
    {w:300,h:600,sb:.75,plat:'Programmatic',sx:12,sy:12,show:1,
      logo:{x:16,y:27,w:96},
      text:{x:16,y:67.06,h:{f:30,lh:30.16,ls:-.348,l:['Your Whole Wish','List, Lease-to-Own.']},
        s:{g:8,f:15,lh:18.6,l:['From couches to TVs to tires,','lease-to-own the big stuff at thousands','of retailers this Cyber Week.']}},
      cta:{x:16,y:518.91,w:268,f:20,lh:22.5,ls:-.085,pt:10.27,pb:10.82,px:16,l:['Shop Cyber Deals.','Lease to Own.']},
      knoll:{ox:4,oy:190,items:[
        ['laptop',135.88,115.17,37,43],['vacuum',115,166,66,25,{r:-90,c:[-150.68,-47.15,400,151.52]}],
        ['tv',180.88,107.17,77,46],['fridge',186.88,164.17,83,129],['couch',138.88,27.17,131,78,{sh:SH.couch}],
        ['washer',99,200,79,93],['tire',23,239,64,61],['nightstand',20,166,61,73,{c:C.ns}],
        ['necklace',80,167,30,30,{sh:SH.nkS}],['necklace',90.88,173.59,2.64,2.97,{ear:1}],['necklace',96.48,173.59,2.64,2.97,{ear:1}],
        ['bed',11,22,135,142,{c:[6.52,0,94.22,100],sh:SH.bed}]]},
      scenes:['','lhs','lhs|couch laptop vacuum washer nightstand','lhs|couch laptop vacuum washer nightstand fridge bed','*']},
    {w:160,h:600,sb:.75,plat:'Programmatic',sx:8,sy:8,show:1,
      logo:{x:12,y:24,w:84},
      text:{x:12,y:55.42,h:{f:20,lh:23,ls:-.288,l:['Your Whole','Wish List,','Lease-to-Own.']},
        s:{g:10.25,f:12,lh:14.88,l:['From couches to TVs to','tires, lease-to-own the','big stuff at thousands','of retailers this','Cyber Week.']},
        c:{g:15,f:13,lh:14.95,ls:-.065,pt:8,pb:8,px:12.7,l:['Shop Cyber Deals.','Lease to Own.']}},
      knoll:{ox:12,oy:304,items:[
        ['couch',2,219,93,57,{sh:SH.couch}],['fridge',67,-7,69,109],['washer',8,27,57,68],
        ['nightstand',8,122,45,54,{c:C.ns}],['tire',10,173,40,41],
        ['vacuum',-2,5,66.3,17,{r:-90,c:[-150,0,400,102.56]}],['tv',101,214,33,56,{r:-90}],
        ['bed',50,105,89,103,{c:[6.9,4,105.75,96],sh:SH.bed}],
        ['necklace',16.5,100,22,22,{sh:SH.nkXS}],['necklace',24.48,104.84,1.93,2.18,{ear:1}],['necklace',28.59,104.84,1.93,2.18,{ear:1}]]},
      scenes:['lh','lhs|couch washer nightstand vacuum','lhs|couch washer nightstand vacuum fridge bed','*']},
    {w:300,h:250,sb:1,plat:'Programmatic',sx:8,sy:8,show:1,
      logo:{x:12,y:20,w:72},
      text:{x:12,y:50,h:{f:21.5,lh:23.3,ls:-.246,l:['Your Whole','Wish List,','Lease-to-Own.']},
        s:{g:6,f:10,lh:12.4,l:['From couches to TVs to tires,','lease-to-own the big stuff at','thousands of retailers this','Cyber Week.']},
        c:{g:9,f:11.5,lh:13.23,ls:-.057,pt:6.11,pb:7.33,px:20.08,l:['Shop Cyber Deals.','Lease to Own.']}},
      knoll:{ox:145,oy:-12,items:[
        ['couch',23,205,80,50,{sh:SH.couch}],['fridge',86,27,51,79],['washer',28,44,50,59],
        ['nightstand',26,125,37,44,{c:C.ns}],['tire',26,167,35,36],
        ['vacuum',19,25,58.5,15,{r:-90,c:[-150,0,400,102.56]}],['tv',108,199,29,49,{r:-90}],
        ['necklace',32,105,21,21,{sh:SH.nkXS}],['necklace',39.62,109.62,1.85,2.08,{ear:1}],['necklace',43.54,109.62,1.85,2.08,{ear:1}],
        ['bed',62,105,77,89,{c:[6.9,4,105.75,96],sh:SH.bed}]]},
      scenes:['lh','lhs|couch washer nightstand vacuum','lhs|couch washer nightstand vacuum fridge bed','*']},
    {w:728,h:90,sb:.6,plat:'Programmatic',sx:6,sy:6,show:1,
      logo:{x:14,y:36,w:86},
      text:{x:111,y:19,h:{f:25,lh:26,ls:-.3,l:['Your Whole Wish','List, Lease-to-Own.']}},
      cta:{x:574,cy:45,w:142,f:13,lh:14.95,ls:-.065,pt:8,pb:8,px:12,l:['Shop Cyber Deals.','Lease to Own.']},
      knoll:{ox:0,oy:0,items:[
        ['bed',499,10,66,69,{c:[6.52,0,94.22,100],sh:SH.bedT}],
        ['fridge',353,15.42,40.92,65.26],['tv',456.97,14.32,39.82,23.23],['tire',397.24,13.21,23.23,24.33],
        ['nightstand',425,12,27,32,{c:C.ns}],['washer',392.82,38.65,33.18,40.92],
        ['couch',429.32,44.18,63.05,39.82,{sh:SH.couch}],['necklace',433,33,11,11,{sh:SH.nkT}]]},
      scenes:['lh','lh|fridge washer couch','lh|fridge washer couch tire nightstand bed','*']},
    {w:320,h:50,sb:1,plat:'Programmatic',sx:4,sy:4,show:1,
      logo:{x:168,y:30,w:42},
      text:{x:6,y:8.22,h:{f:12.3,lh:14.56,ls:-.168,l:[COPY.h]}},
      cta:{cx:72,cy:34,f:8,lh:8,ls:-.035,pt:3,pb:3,px:5,l:[COPY.c]},
      knoll:{ox:0,oy:0,items:[
        ['tire',220,25,21,22],['nightstand',221,4,19,22,{c:C.ns}],['tv',269,4,29,17],
        ['laptop',300,10,12,12,{r:-90,fit:'contain'}],['couch',269,25,43,25],['fridge',242,4,27,44],
        ['necklace',302,3,7,7,{sh:SH.nkT}]]},
      scenes:['h','h|fridge couch','h|fridge couch tire nightstand tv','*']}
  ];
  /* the copy must stay the client's, word for word: each size only adds line breaks */
  SIZES.forEach(function(sz){
    var T=sz.text, chk=[[T.h,COPY.h],[T.s,COPY.s],[T.c||sz.cta,COPY.c]];
    chk.forEach(function(p){ if(p[0]&&p[0].l.join(' ')!==p[1]) console.error('KN copy drift',sz.w+'x'+sz.h,p[0].l); });
  });

  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function lines(p,arr){ arr.forEach(function(t,i){ if(i) p.appendChild(document.createElement('br')); p.appendChild(document.createTextNode(t)); }); return p; }
  function px(v){ return (+v).toFixed(2).replace(/\.?0+$/,'')+'px'; }
  function cta(c){
    var b=el('span','kn-cta','font-size:'+px(c.f)+';line-height:'+px(c.lh)+';letter-spacing:'+px(c.ls||0)+';padding:'+px(c.pt)+' '+px(c.px)+' '+px(c.pb));
    return lines(b,c.l);
  }

  /* one product. The box is Figma's; the image inside is placed by Figma's rect (c, in %),
     mapped onto the trimmed cutout (tb), or fitted (contain), and turned when r is set */
  function item(it,ox,oy){
    var id=it[0], x=it[1]+ox, y=it[2]+oy, w=it[3], h=it[4], o=it[5]||{}, P=KN_PHOTOS[id];
    var d=el('div','kn-item','left:'+px(x)+';top:'+px(y)+';width:'+px(w)+';height:'+px(h));
    d.title=NAMES[id]; d.dataset.id=id;
    if(o.sh) d.style.filter='drop-shadow('+px(o.sh[0])+' '+px(o.sh[1])+' '+px(o.sh[2]/2)+' rgba(0,0,0,'+o.sh[3]+'))';
    var iw=o.r?h:w, ih=o.r?w:h;
    var box=el('div','kn-clip','left:'+px((w-iw)/2)+';top:'+px((h-ih)/2)+';width:'+px(iw)+';height:'+px(ih)+(o.r?';transform:rotate('+o.r+'deg)':'')+(o.ear?';border-radius:5px 5px 0 0':''));
    var r=o.ear?C.ear:o.c, rx,ry,rw,rh;
    if(r){ rx=r[0]/100*iw; ry=r[1]/100*ih; rw=r[2]/100*iw; rh=r[3]/100*ih; }
    else { rx=0; ry=0; rw=iw; rh=ih; }
    if(P){
      var ar=P.ow/P.oh;
      if(o.fit==='contain'){ var k=Math.min(rw/ar,rh); var nw=k*ar; rx+=(rw-nw)/2; ry+=(rh-k)/2; rw=nw; rh=k; }
      var t=P.tb||[0,0,1,1];
      var im=el('img','', 'left:'+px(rx+t[0]*rw)+';top:'+px(ry+t[1]*rh)+';width:'+px((t[2]-t[0])*rw)+';height:'+px((t[3]-t[1])*rh));
      im.src=P.src; im.alt=o.ear?'':NAMES[id]; box.appendChild(im);
    }
    d.appendChild(box);
    return d;
  }

  /* scene flags: l logo, h headline, s subhead, c CTA; after '|' the products already on
     the ground ('*' = everything = the V1 end frame). Nothing moves between scenes: copy
     and products only appear, in place. */
  function parse(sc){
    if(sc==='*') return {l:1,h:1,s:1,c:1,all:1};
    var p=sc.split('|'), f=p[0], o={l:f.indexOf('l')>-1,h:f.indexOf('h')>-1,s:f.indexOf('s')>-1,c:f.indexOf('c')>-1,ids:{}};
    (p[1]||'').split(' ').forEach(function(i){ if(i) o.ids[i]=1; });
    return o;
  }

  /* scene: index into sz.scenes; null = static V1 (= the last scene) */
  function canvas(sz,scene){
    var S=parse(scene==null?'*':sz.scenes[scene]);
    var k=el('div','kn','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    function hide(n,on){ if(!on) n.classList.add('kn-hide'); return n; }

    var K=sz.knoll;
    K.items.forEach(function(it){ k.appendChild(hide(item(it,K.ox,K.oy),S.all||S.ids[it[0]])); });

    var L=sz.logo;
    var logo=document.createElementNS('http://www.w3.org/2000/svg','svg');
    logo.setAttribute('class','kn-logo'); logo.setAttribute('viewBox','0 0 521 116'); logo.setAttribute('role','img'); logo.setAttribute('aria-label','Katapult');
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); logo.appendChild(u);
    logo.style.cssText='left:'+px(L.x)+';top:'+px(L.y)+';width:'+px(L.w);
    if(!S.l) logo.classList.add('kn-hide');
    k.appendChild(logo);

    var T=sz.text, t=el('div','kn-text','left:'+px(T.x)+';top:'+px(T.y));
    var hd=lines(el('p','kn-h','font-size:'+px(T.h.f)+';line-height:'+px(T.h.lh)+';letter-spacing:'+px(T.h.ls)+';font-weight:'+HW),T.h.l);
    t.appendChild(hide(hd,S.h));
    if(T.s) t.appendChild(hide(lines(el('p','kn-s','font-size:'+px(T.s.f)+';line-height:'+px(T.s.lh)+';margin-top:'+px(T.s.g)),T.s.l),S.s));
    if(T.c){ var cw=el('div','','margin-top:'+px(T.c.g)); cw.appendChild(cta(T.c)); t.appendChild(hide(cw,S.c)); }
    k.appendChild(t);

    var A=sz.cta;
    if(A){
      var b=cta(A);
      if(A.cx!=null) b.style.cssText+=';position:absolute;left:'+px(A.cx)+';top:'+px(A.cy)+';transform:translate(-50%,-50%)';
      else b.style.cssText+=';position:absolute;box-sizing:border-box;left:'+px(A.x)+';width:'+px(A.w)+';'+(A.cy!=null?'top:'+px(A.cy)+';transform:translateY(-50%)':'top:'+px(A.y));
      k.appendChild(hide(b,S.c));
    }
    return k;
  }

  function frameName(sz,v,scene){ return 'KAT26019-TopItems-'+sz.w+'x'+sz.h+'-'+(v===1?'Static':'Animated')+'-'+sz.plat+'-V'+v+(scene!=null?'-S0'+(scene+1):'')+'-Knolling'; }
  function label(sz){ return sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }
  /* scene caption: what is on the frame (the last scene is always the V1 end frame) */
  function caption(sz,i){
    var n='S0'+(i+1)+' · ', sc=sz.scenes[i];
    if(sc==='*') return n+'End frame = V1';
    var S=parse(sc), parts=[];
    if(!S.l&&!S.h&&!S.s&&!S.c&&!Object.keys(S.ids).length) return n+'Ground only';
    if(S.l) parts.push('logo'); if(S.h) parts.push('headline'); if(S.s) parts.push('subhead'); if(S.c) parts.push('CTA');
    var ids=Object.keys(S.ids); if(ids.length) parts.push(ids.length+' product'+(ids.length>1?'s':''));
    var s=parts.join(', '); return n+s.charAt(0).toUpperCase()+s.slice(1);
  }
  function figure(sz,v,scene,scale,cap){
    var f=el('figure','kb-fig'), sc=el('div','kb-scroll'), fr=el('div','kn-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=scale;
    fr.appendChild(canvas(sz,v===1?null:scene)); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'), b=el('b'), mo=el('span','mono'); b.textContent=cap; mo.textContent=frameName(sz,v,v===1?null:scene);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }
  function render(){
    var v=document.getElementById('kn-v1-rows'); v.replaceChildren();
    ['PMAX','Programmatic'].forEach(function(pl){
      var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; v.appendChild(hd);
      /* not .kb-row: the job card thumbnail keeps showing the V1 grid */
      var row=el('div','kn-row');
      SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){ row.appendChild(figure(sz,1,null,sz.show,label(sz))); });
      v.appendChild(row);
    });
    var v2=document.getElementById('kn-v2-rows');
    if(v2){
      v2.replaceChildren();
      SIZES.forEach(function(sz){
        var b=el('div','kb-sb'), t=el('b'); t.textContent=label(sz)+' · '+sz.plat; b.appendChild(t);
        var r=el('div','kb-sb-scenes');
        sz.scenes.forEach(function(_,i){ r.appendChild(figure(sz,2,i,sz.sb,caption(sz,i))); });
        b.appendChild(r); v2.appendChild(b);
      });
    }
    applyScale();
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
  /* every position is fixed now (no measured fit), so the exporter's hook has nothing to
     re-run; kept so export_kn.py works unchanged */
  window.knFitAll=function(){};
  render();
  function applySafe(){ if(root) root.classList.toggle('kn-safe-on',!!(safe&&safe.checked)); }
  if(safe) safe.addEventListener('change',applySafe); applySafe();
})();
