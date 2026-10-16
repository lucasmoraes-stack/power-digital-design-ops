(function(){
  /* photos injected by build.py: {kitchen:{src,w,h}, livingroom:{src,w,h}} */
  var K20_PHOTOS={};

  /* ---- copy (client, verbatim). The test variable is the imagery: V1 kitchen, V2 living room ---- */
  var V={
    V1:{img:'kitchen', theme:'Kitchen', h1:"The turkey's fine.", h2:"The oven isn't.", c:'Shop Appliances. Lease to Own.'},
    V2:{img:'livingroom', theme:'Living room', h1:'Cyber deals are here.', h2:'Let Katapult help.', c:'Lease new furniture before family arrives', u:'before'}
  };
  /* disclaimer: one line, as in the Figma PMAX frames */
  var DISC="Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.";

  /* Round 4: rebuilt from Lucas's Figma frames (D8FpNuKI3uPGjCPqonIn3C, page 547:1720).
     Every value below is the Figma value for that frame, per version (the two versions are
     cropped and sized independently in Figma, so they are not forced to match).
     img   = [left, top, width, flip] of the photo in frame px (height follows the photo's ratio)
     scrim = black layers over the photo: {a} flat, or {g:css angle, a:alpha at p0, p0, p1 (alpha 0)}
     logo  = [x, y, width, color]
     head  = highlight bars: y (top of the stack), f (size), pad [[top,bottom] per sentence], px,
             x (left-aligned at x; omitted = centered on the frame), L = lines per sentence
     cta   = pink pill: y (top), h, f, lh, px, w (fixed width, else padding), L (lines), trim (cap trim)
             cx (center x, default frame center) or x (left)
     disc  = cy (center y), f, lh */
  var W='#FFFFFF', P='#ED5370';
  var DARK_TR=function(g){ return {g:g,a:.39,p0:10.791,p1:79.599}; };
  /* 728x90 V1: Figma's photo fill there is stretched (278x273 for a 0.806 photo, ~24% squashed).
     Kept at the photo's true ratio, same width and left edge, turkey at the same height in frame. */
  var SIZES=[
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      V1:{img:[0,-185.16,1200], scrim:[DARK_TR(214.576)], logo:[898.32,69.49,220,W],
        head:{y:700.49,f:119.299,pad:[[12,13.783],[6.998,13.783]],px:23.86,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{y:1017.49,h:90.3,w:772.76,f:44,lh:47.441,trim:1}, disc:{cy:1166.78,f:17.185,lh:20.622}},
      V2:{img:[0,-289.68,1200], scrim:[{g:-3.697,a:.44,p0:3.459,p1:23.301}], logo:[898.01,69.5,220,W],
        head:{y:754.15,f:96.742,pad:[[5.675,11.177],[5.675,11.177]],px:19.348,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{y:1017.49,h:90.3,w:948.76,f:44,lh:50.6}, disc:{cy:1166.78,f:17.185,lh:20.622}}},
    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      V1:{img:[0,-495.43,1200], scrim:[{g:-2.349,a:.44,p0:.213,p1:31.334},DARK_TR(199.835)], logo:[968,37,150,W],
        head:{y:265.28,f:88,lh:91.754,pad:[[7.2,8.69],[12,8.69]],px:18.351,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{y:505,h:64.24,f:31.341,lh:33.792,px:44.076,trim:1}, disc:{cy:604,f:15,lh:14.4}},
      V2:{img:[0,-623.6,1200], scrim:[{a:.1}], logo:[968,37,150,W],
        head:{y:314.28,f:74.38,pad:[[4.217,8.669],[4.217,8.669]],px:14.876,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{y:510,h:64.24,w:675.08,f:31.341,lh:36.042}, disc:{cy:604,f:15,lh:14.4}}},
    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      V1:{img:[0,0,966.62], scrim:[{a:.1}], logo:[695.02,69.5,200,W],
        head:{y:764.91,f:95.452,pad:[[5.34,11.161],[5.34,11.161]],px:19.09,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{y:1037,h:93.57,f:45.591,lh:49.156,px:64.117,trim:1}, disc:{cy:1166.72,f:14.041,lh:16.849}},
      V2:{img:[-243.65,-294.84,1204.03], scrim:[{g:.308,a:.4,p0:3.67,p1:22.675},{a:.1}], logo:[695.02,69.5,200,W],
        head:{y:751.65,f:77.419,pad:[[4.331,9.052],[4.331,9.052]],px:15.484,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{y:981.34,h:150.06,w:558.23,f:45.591,lh:52.43,L:['Lease new furniture','before family arrives']}, disc:{cy:1166.72,f:14.041,lh:16.849}}},
    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,
      V1:{img:[-80.22,-281.64,821.67], scrim:[{a:.1}], logo:[102,535,96,W],
        head:{y:254,f:33.437,pad:[[4.62,2.67],[5.62,3.671]],px:6.687,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{y:353,h:51.3,w:270,f:19.092,lh:21.956,trim:1,L:['Shop Appliances.','Lease to Own.']}},
      V2:{img:[-338.76,-392.04,821.67], scrim:[{a:.1}], logo:[102,535,96,W],
        head:{y:254,f:27.091,pad:[[2.31,2],[4.31,2.974]],px:5.418,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{y:338.31,h:51.3,w:270,f:19.092,lh:21.956,trim:1,L:['Lease new furniture','before family arrives']}}},
    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,
      V1:{img:[-163.74,-297.3,870], scrim:[{a:.1}], logo:[38.32,25.49,84,W],
        head:{y:338.95,f:31.405,pad:[[2.198,3.455],[2.198,3.455]],px:6.281,L:[["The","turkey's","fine."],['The oven',"isn't."]]},
        cta:{y:534.24,h:45.91,w:143.5,f:11.938,lh:13.728,L:['Shop Appliances.','Lease to Own.']}},
      /* V2: the Figma crop (top -426.66) put the white logo on the lampshade and tinsel. Photo raised
         to -260 so the logo sits on the plain wood panel above the tree, plus a soft top scrim */
      V2:{img:[-437.5,-260,870], scrim:[{g:180,a:.4,p0:0,p1:16},{a:.1}], logo:[38.32,25.49,84,W],
        head:{y:299.78,f:31.661,pad:[[2.216,3.483],[2.216,3.483]],px:6.332,L:[['Cyber','deals are','here.'],['Let','Katapult','help.']]},
        cta:{y:533.95,h:46.02,w:143.87,f:12.014,lh:13.816,L:['Lease new furniture','before family arrives']}}},
    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,
      V1:{img:[0,-155.75,384.03], scrim:[DARK_TR(209.872),{a:.1}], logo:[231.02,10,58,W],
        head:{y:120.3,f:29.622,pad:[[4.44,2.25],[4.44,2.25]],px:5.924,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{y:207.18,h:28.82,w:205.85,f:12.075,lh:13.8}},
      V2:{img:[-82,-186.73,390], scrim:[{g:206.839,a:.39,p0:2.959,p1:81.11}], logo:[231.02,10,58,W],
        head:{y:136.66,f:23.959,pad:[[3.16,2],[4.16,2.63]],px:4.792,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{y:207.18,h:28.82,w:254.15,f:12.075,lh:13.8}}},
    /* leaderboards: Dark Blue ground, logo in Pink at the left, headline left-aligned, photo as a
       hard-edged block on the right (V1 mirrored so the oven faces in), CTA pill over the photo edge */
    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,row:1,
      V1:{img:[450.41,-124.2,278.02,1], scrim:[], logo:[13.65,34.0,97.84,P],
        head:{x:131,y:11.86,f:32.429,pad:[[1.573,3.56],[1.573,3.56]],px:6.486,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{cx:510.62,y:17.48,h:52.95,w:197.68,f:18.2,lh:19.217,trim:1,L:['Shop Appliances.','Lease to Own.']}},
      V2:{img:[404.33,-175.18,323.67], scrim:[], logo:[13.6,34,97.8,P],
        head:{x:131,y:9.49,f:32.43,pad:[[5.57,1.56],[5.57,2.56]],px:6.486,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{x:473.65,y:16.06,h:57.88,w:210.94,f:18.2,lh:20.938,L:['Lease new furniture','before family arrives']}}},
    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,row:1,
      V1:{img:[197.98,-51.07,122.21,1], scrim:[], logo:[6,19.71,43,P],
        head:{x:56,y:10.49,f:14.254,pad:[[.691,1.565],[.691,1.565]],px:2.851,L:[["The turkey's fine."],["The oven isn't."]]},
        cta:{cx:224.45,y:12.96,h:23.28,w:86.89,f:8,lh:8.447,trim:1,L:['Shop Appliances.','Lease to Own.']}},
      V2:{img:[223.74,-62.82,129.18], scrim:[], logo:[6,19.7,43,P],
        head:{x:56,y:8.73,f:14.25,pad:[[3,1],[3,0]],px:2.85,L:[['Cyber deals are here.'],['Let Katapult help.']]},
        cta:{x:209,y:12.86,h:24.29,f:8,lh:9.143,px:8.45,L:['Lease new furniture','before family arrives']}}}
  ];
  SIZES.forEach(function(sz){
    ['V1','V2'].forEach(function(v){
      var s=sz[v], L=s.head.L;
      if(L[0].join(' ')!==V[v].h1||L[1].join(' ')!==V[v].h2) console.error('KAT26020: headline lines do not match the copy at '+sz.w+'x'+sz.h+' '+v);
      if(s.cta.L&&s.cta.L.join(' ')!==V[v].c) console.error('KAT26020: CTA lines do not match the copy at '+sz.w+'x'+sz.h+' '+v);
    });
  });

  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function svg(tag,attrs){ var e=document.createElementNS('http://www.w3.org/2000/svg',tag); for(var k in attrs) e.setAttribute(k,attrs[k]); return e; }
  function logo(spec){
    var s=svg('svg',{'class':'k20-logo',viewBox:'0 0 521 116',role:'img','aria-label':'Katapult'});
    s.style.cssText='left:'+spec[0]+'px;top:'+spec[1]+'px;width:'+spec[2]+'px;color:'+spec[3];
    s.appendChild(svg('use',{href:'#k-logo'})); return s;
  }
  function headline(sz,H){
    var p=el('div','k20-h'+(H.x==null?' k20-center':''),'top:'+H.y+'px;font-size:'+H.f+'px;'+(H.x==null?'left:0;width:'+sz.w+'px':'left:'+H.x+'px'));
    H.L.forEach(function(lines,i){ lines.forEach(function(t){
      var s=el('span','t'+(i+1),'padding:'+H.pad[i][0]+'px '+H.px+'px '+H.pad[i][1]+'px'+(H.lh?';line-height:'+H.lh+'px':''));
      s.textContent=t; p.appendChild(s);
    }); });
    return p;
  }
  function cta(sz,C,v){
    var pos=C.x!=null?'left:'+C.x+'px':'left:'+(C.cx!=null?C.cx:sz.w/2)+'px;transform:translateX(-50%)';
    var b=el('div','k20-cta',pos+';top:'+C.y+'px;height:'+C.h+'px;font-size:'+C.f+'px;line-height:'+C.lh+'px;'+(C.w?'width:'+C.w+'px':'padding:0 '+C.px+'px'));
    var t=el('span',C.trim?'trim':'');
    /* u: the word the client wants underlined in the CTA (round 5: V2 "before") */
    var U=V[v].u;
    (C.L||[V[v].c]).forEach(function(line,i){
      if(i) t.appendChild(el('br'));
      var k=U?line.indexOf(U):-1;
      if(k<0){ t.appendChild(document.createTextNode(line)); return; }
      var u=el('u'); u.textContent=U;
      t.appendChild(document.createTextNode(line.slice(0,k))); t.appendChild(u); t.appendChild(document.createTextNode(line.slice(k+U.length)));
    });
    b.appendChild(t); return b;
  }
  function disc(sz,D){ var p=el('p','k20-disc','left:'+sz.w/2+'px;top:'+D.cy+'px;font-size:'+D.f+'px;line-height:'+D.lh+'px'); p.textContent=DISC; return p; }

  /* the photo rect from Figma, clipped to the frame: the box is what's visible */
  function picGeom(sz,v){
    var s=sz[v], I=K20_PHOTOS[V[v].img]||{w:1412,h:1753}, l=s.img[0], t=s.img[1], iw=s.img[2], k=iw/I.w, ih=I.h*k;
    var bx=Math.max(0,l), by=Math.max(0,t), bx1=Math.min(sz.w,l+iw), by1=Math.min(sz.h,t+ih);
    var flip=!!s.img[3], sx0=(bx-l)/k, sx1=(bx1-l)/k;
    if(flip){ var a=I.w-sx1; sx1=I.w-sx0; sx0=a; }
    return {bx:bx,by:by,bw:bx1-bx,bh:by1-by,k:k,iw:iw,ih:ih,ox:l-bx,oy:t-by,flip:flip,src:[sx0,(by-t)/k,sx1-sx0,(by1-by)/k]};
  }
  function scrimCss(layers){
    return layers.map(function(L){
      return L.g==null ? 'linear-gradient(rgba(0,0,0,'+L.a+'),rgba(0,0,0,'+L.a+'))'
        : 'linear-gradient('+L.g+'deg,rgba(0,0,0,'+L.a+') '+L.p0+'%,rgba(0,0,0,0) '+L.p1+'%)';
    }).join(',');
  }
  function photo(sz,v){
    var g=picGeom(sz,v), P=K20_PHOTOS[V[v].img], sc=sz[v].scrim;
    var wrap=el('div','k20-pic','left:'+g.bx+'px;top:'+g.by+'px;width:'+g.bw+'px;height:'+g.bh+'px');
    if(P){
      var im=el('img','','left:'+g.ox+'px;top:'+g.oy+'px;width:'+g.iw+'px;height:'+g.ih+'px'+(g.flip?';transform:scaleX(-1)':''));
      im.src=P.src; im.alt=''; im.setAttribute('width',Math.round(g.iw)); im.setAttribute('height',Math.round(g.ih));
      /* export.py bakes this crop (+ scrim) into one image: name, source rect x,y,w,h, box w,h, flip */
      im.dataset.crop=[V[v].img].concat(g.src,[g.bw,g.bh,g.flip?1:0]).join(',');
      im.dataset.scrim=JSON.stringify(sc);
      wrap.appendChild(im);
    }
    if(sc.length) wrap.appendChild(el('div','k20-fade','left:0;top:0;width:100%;height:100%;position:absolute;background:'+scrimCss(sc)));
    return wrap;
  }

  function canvas(sz,v){
    var s=sz[v];
    var k=el('div','k20','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    k.dataset.v=v;
    k.appendChild(photo(sz,v));
    k.appendChild(logo(s.logo));
    k.appendChild(headline(sz,s.head));
    k.appendChild(cta(sz,s.cta,v));
    if(s.disc) k.appendChild(disc(sz,s.disc));
    return k;
  }

  function frameName(sz,v){ return 'KAT26020-HolidayDisaster-'+sz.w+'x'+sz.h+'-Static-'+sz.plat+'-'+v; }
  function label(sz){ return sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }
  function figure(sz,v){
    var f=el('figure','kb-fig'), sc=el('div','kb-scroll'), fr=el('div','k20-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=sz.show;
    fr.appendChild(canvas(sz,v)); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'), b=el('b'), mo=el('span','mono'); b.textContent=label(sz)+' · '+v+' '+V[v].theme; mo.textContent=frameName(sz,v);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }

  /* layout check: logo, headline and CTA inside the safe zone; the disclaimer only has to sit inside
     the frame (it lives in the bottom margin, as in Figma); no two blocks overlapping.
     Results land on data-k20-issues for export.py. */
  function check(){
    var issues=[];
    [].forEach.call(document.querySelectorAll('.hub-ch-k20 .k20'),function(k){
      var fr=k.parentNode, W=+fr.dataset.w, H=+fr.dataset.h, sz=SIZES.filter(function(z){return z.w===W&&z.h===H;})[0];
      var v=k.dataset.v, name=frameName(sz,v), kr=k.getBoundingClientRect(), sc=kr.width/W, rects=[];
      [].forEach.call(k.querySelectorAll('.k20-logo,.k20-h > span,.k20-cta,.k20-disc'),function(n){
        var r=n.getBoundingClientRect(), x0=(r.left-kr.left)/sc, y0=(r.top-kr.top)/sc, x1=(r.right-kr.left)/sc, y1=(r.bottom-kr.top)/sc;
        var cls=n.className.baseVal!=null?'logo':n.className;
        var tag=cls+':'+(n.textContent||'').slice(0,16), m=sz.row&&cls==='t2'?{x:0,y:0}:cls==='k20-disc'?{x:2,y:2}:{x:sz.sx,y:sz.sy};
        if(x0<m.x-.5||y0<m.y-.5||x1>W-m.x+.5||y1>H-m.y+.5) issues.push(name+' SAFE '+tag);
        rects.push({t:tag,c:cls,r:[x0,y0,x1,y1]});
      });
      for(var i=0;i<rects.length;i++) for(var j=i+1;j<rects.length;j++){
        var a=rects[i].r, b=rects[j].r;
        if(/^t[12]/.test(rects[i].c)&&/^t[12]/.test(rects[j].c)) continue;
        if(a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3]) issues.push(name+' OVERLAP '+rects[i].t+' / '+rects[j].t);
      }
    });
    var root=document.querySelector('.hub-ch-k20'); if(root) root.dataset.k20Issues=JSON.stringify(issues);
    if(issues.length) console.warn('KAT26020 layout issues:\n'+issues.join('\n'));
  }

  function render(){
    var rows=document.getElementById('k20-rows'); if(!rows) return; rows.replaceChildren();
    ['PMAX','Programmatic'].forEach(function(pl){
      var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; rows.appendChild(hd);
      SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){
        var pr=el('div','kb-row k20-pair');
        ['V1','V2'].forEach(function(v){ pr.appendChild(figure(sz,v)); });
        rows.appendChild(pr);
      });
    });
    applyScale();
  }
  /* ---- scale + safe zones ---- */
  var full=document.getElementById('k20-full'), safe=document.getElementById('k20-safe'), root=document.querySelector('.hub-ch-k20');
  function applyScale(){
    [].forEach.call(document.querySelectorAll('.k20-frame'),function(fr){
      var s=full&&full.checked?1:+fr.dataset.s;
      fr.style.width=(fr.dataset.w*s)+'px'; fr.style.height=(fr.dataset.h*s)+'px';
      fr.firstChild.style.transform='scale('+s+')';
    });
  }
  if(full) full.addEventListener('change',applyScale);
  var fl=document.fonts?Promise.all(['500','700'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(function(){ render(); setTimeout(check,50); });
  window.k20Check=check;
  function applySafe(){ if(root) root.classList.toggle('k20-safe-on',safe.checked); }
  if(safe){ safe.addEventListener('change',applySafe); applySafe(); }
})();
