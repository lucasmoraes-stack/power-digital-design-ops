(function(){
  /* photos injected by build.py: {kitchen:{src,w,h}, livingroom:{src,w,h}} */
  var K20_PHOTOS={};

  /* ---- copy (client, verbatim). The test variable is the imagery: V1 kitchen, V2 living room ---- */
  var V={
    V1:{img:'kitchen', theme:'Kitchen', h1:"The turkey's fine.", h2:"The oven isn't.", c:'Shop Appliances. Lease to Own.'},
    V2:{img:'livingroom', theme:'Living room', h1:'Cyber deals are here.', h2:'Let Katapult help.', c:'Lease new furniture before family arrives'}
  };
  /* disclaimer: the text the account lead placed in the Figma 4x5 frames (470:3236 / 470:3241) */
  var DISC=['Lease-purchase service. Total cost exceeds cash price.','Approval required. Not available in MN, NJ, WI, WY. See katapult.com.'];

  /* the mishap in each photo, in source pixels: the point the crop is built around and kept clear of type */
  var FOCUS={kitchen:{x:395,y:785}, livingroom:{x:840,y:960}};

  /* Each size:
     pic  = photo box (defaults to the whole frame), z = zoom over a plain cover fit,
            t = where the mishap lands in the box (fractions), fade = where the photo melts into
            solid Dark Blue: bottom (a = fade starts, b = solid) or left (a = solid, b = fade ends)
     top / bot = stacks anchored to the top or bottom of the safe zone; items run in order
     Both stacks are centered on the frame (round 3): headline, CTA, logo and disclaimer on one axis.
     L = per version, headline lines for [sentence 1, sentence 2]; joined back they must equal the copy.
     The headline gets the largest size that fits hw for BOTH versions, so V1 and V2 match. */
  var SIZES=[
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      pic:{z:1,t:[.5,.47],fade:{dir:'bottom',a:.56,b:.76}},
      top:{x:60,w:1080,hw:900,hmax:150,items:['head']},
      bot:{x:60,w:1080,items:['cta',30,'logo',22,'disc'],cta:{f:32,py:23,px:48},logo:220,disc:12},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      pic:{z:1,t:[.5,.5],fade:{dir:'bottom',a:.54,b:.72}},
      top:{x:60,w:1080,hw:760,hmax:84,items:['head']},
      bot:{x:60,w:1080,items:['cta',14,'logo',12,'disc'],cta:{f:22,py:14,px:30},logo:150,disc:10},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      pic:{z:1,t:[.5,.47],fade:{dir:'bottom',a:.57,b:.76}},
      top:{x:48,w:864,hw:720,hmax:130,items:['head']},
      bot:{x:48,w:864,items:['cta',28,'logo',20,'disc'],cta:{f:30,py:21,px:44},logo:200,disc:12},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,
      pic:{z:1.1,t:[.5,.53],fade:{dir:'bottom',a:.64,b:.8}},
      top:{x:12,w:276,hw:236,hmax:46,items:['head']},
      bot:{x:12,w:276,items:['cta',16,'logo'],cta:{f:15,py:11,px:18,wrap:1},logo:96},
      L:{V1:[["The turkey's","fine."],["The oven","isn't."]],V2:[['Cyber deals','are here.'],['Let Katapult','help.']]}},
    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,
      pic:{z:1.15,t:[.5,.52],fade:{dir:'bottom',a:.66,b:.81}},
      top:{x:8,w:144,hw:124,hmax:34,items:['head']},
      bot:{x:8,w:144,items:['cta',14,'logo'],cta:{f:12,py:9,px:12,wrap:1},logo:84},
      L:{V1:[["The","turkey's","fine."],['The oven',"isn't."]],V2:[['Cyber','deals are','here.'],['Let','Katapult','help.']]}},
    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,
      pic:{z:1.25,t:[.5,.5],fade:{dir:'bottom',a:.56,b:.72}},
      top:{x:8,w:284,hw:240,hmax:30,items:['head']},
      bot:{x:8,w:284,items:['cta',8,'logo'],cta:{f:10.5,py:7,px:12,wrap:1},logo:58},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,row:1,
      pic:{x:500,w:228,z:1,t:[.55,.5],fade:{dir:'left',a:0,b:.38}},
      logo:{x:12,w:88}, head:{x:114,w:236}, box:{x:362,w:140,f:11.5,py:8,px:10},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,row:1,
      pic:{x:236,w:84,z:1,t:[.55,.5],fade:{dir:'left',a:0,b:.4}},
      logo:{x:6,w:42}, head:{x:54,w:100}, box:{x:160,w:84,f:7,py:4,px:5},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}}
  ];
  SIZES.forEach(function(sz){
    ['V1','V2'].forEach(function(v){
      var L=sz.L[v];
      if(L[0].join(' ')!==V[v].h1||L[1].join(' ')!==V[v].h2) console.error('KAT26020: headline lines do not match the copy at '+sz.w+'x'+sz.h+' '+v);
    });
  });

  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function svg(tag,attrs){ var e=document.createElementNS('http://www.w3.org/2000/svg',tag); for(var k in attrs) e.setAttribute(k,attrs[k]); return e; }
  function logo(w){
    var s=svg('svg',{'class':'k20-logo',viewBox:'0 0 521 116',role:'img','aria-label':'Katapult'});
    s.style.width=w+'px'; s.appendChild(svg('use',{href:'#k-logo'})); return s;
  }
  function headline(L,f){
    var p=el('p','k20-h');
    L.forEach(function(lines,i){ lines.forEach(function(t){ var s=el('span','t'+(i+1)); s.textContent=t; p.appendChild(s); }); });
    if(f) p.style.fontSize=f+'px';
    return p;
  }
  /* largest headline size, in half pixels, that fits width w (and height h) for both versions.
     Measured with canvas text metrics, not the DOM: the viewer can run this while the page isn't
     laid out yet (offsetWidth 0), which used to blow every headline up to its cap. The strip box
     is the text plus .2em padding each side; its height is 1em line + .18em padding. */
  var MC=null;
  function lineW(t,f){
    if(!MC) MC=document.createElement('canvas').getContext('2d');
    MC.font='700 '+f+'px "Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif';
    try{ MC.letterSpacing=(-.025*f)+'px'; }catch(e){}
    var w=MC.measureText(t).width;
    if(!('letterSpacing' in MC)) w-=.025*f*t.length;
    return w+.4*f;
  }
  function headSize(sz,w,cap,h){
    var f=cap;
    ['V1','V2'].forEach(function(v){
      var lines=[].concat.apply([],sz.L[v]), mw=0;
      lines.forEach(function(t){ mw=Math.max(mw,lineW(t,100)); });
      var g=mw>0?100*w/mw:cap; if(h) g=Math.min(g,100*h/(lines.length*118));
      f=Math.min(f,g);
    });
    return Math.max(4,Math.floor(f*2)/2);
  }
  function cta(text,c){
    var b=el('span','k20-cta'+(c.wrap?' wrap':''),'font-size:'+c.f+'px;padding:'+c.py+'px '+c.px+'px');
    b.textContent=text; return b;
  }
  function disc(f){ var p=el('p','k20-disc','font-size:'+f+'px'); DISC.forEach(function(t){ var s=el('span'); s.textContent=t; p.appendChild(s); }); return p; }

  /* cover-fit the photo in its box, zoomed by z, with the mishap landing at t (clamped to the edges) */
  function picGeom(sz,v){
    var P=sz.pic, bx=P.x||0, by=P.y||0, bw=P.w||sz.w, bh=P.h||sz.h, I=K20_PHOTOS[V[v].img]||{w:1412,h:1753}, F=FOCUS[V[v].img];
    var k=Math.max(bw/I.w,bh/I.h)*(P.z||1), iw=I.w*k, ih=I.h*k;
    var ox=Math.min(0,Math.max(bw-iw,P.t[0]*bw-F.x*k)), oy=Math.min(0,Math.max(bh-ih,P.t[1]*bh-F.y*k));
    return {bx:bx,by:by,bw:bw,bh:bh,k:k,iw:iw,ih:ih,ox:ox,oy:oy,fx:bx+ox+F.x*k,fy:by+oy+F.y*k};
  }
  function fadeCss(f){
    var c='19,21,64';
    return f.dir==='left'
      ? 'linear-gradient(to right,rgba('+c+',1) '+(f.a*100)+'%,rgba('+c+',0) '+(f.b*100)+'%)'
      : 'linear-gradient(to bottom,rgba('+c+',0) '+(f.a*100)+'%,rgba('+c+',1) '+(f.b*100)+'%)';
  }
  function photo(sz,v){
    var g=picGeom(sz,v), P=K20_PHOTOS[V[v].img];
    var wrap=el('div','k20-pic','left:'+g.bx+'px;top:'+g.by+'px;width:'+g.bw+'px;height:'+g.bh+'px');
    if(P){
      var im=el('img','','left:'+g.ox+'px;top:'+g.oy+'px;width:'+g.iw+'px;height:'+g.ih+'px');
      im.src=P.src; im.alt=''; im.setAttribute('width',Math.round(g.iw)); im.setAttribute('height',Math.round(g.ih));
      /* export.py bakes this crop (+ the fade) into one image: name, source rect x,y,w,h, box w,h, fade */
      var f=sz.pic.fade;
      im.dataset.crop=[V[v].img,-g.ox/g.k,-g.oy/g.k,g.bw/g.k,g.bh/g.k,g.bw,g.bh,f.dir,f.a,f.b].join(',');
      wrap.appendChild(im);
    }
    var fd=el('div','k20-fade','left:0;top:0;width:100%;height:100%;position:absolute;background:'+fadeCss(sz.pic.fade));
    wrap.appendChild(fd);
    return wrap;
  }

  function stack(sz,spec,v,f,anchor){
    var st=el('div','k20-stack k20-center','left:'+spec.x+'px;width:'+spec.w+'px;'+(anchor==='bottom'?'bottom:'+sz.sy+'px':'top:'+sz.sy+'px'));
    var gap=0;
    spec.items.forEach(function(it){
      if(typeof it==='number'){ gap=it; return; }
      var n;
      if(it==='logo') n=logo(spec.logo);
      else if(it==='head') n=headline(sz.L[v],f);
      else if(it==='cta'){ n=cta(V[v].c,spec.cta); if(spec.cta.wrap) n.style.maxWidth=spec.w+'px'; }
      else if(it==='disc') n=disc(spec.disc);
      if(gap) n.style.marginTop=gap+'px';
      gap=0; st.appendChild(n);
    });
    return st;
  }

  function canvas(sz,v){
    var k=el('div','k20','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    k.dataset.v=v;
    k.appendChild(photo(sz,v));
    if(sz.row){
      var ih=sz.h-2*sz.sy;
      var lg=logo(sz.logo.w); lg.style.cssText+=';position:absolute;left:'+sz.logo.x+'px;top:'+((sz.h-sz.logo.w*116/521)/2)+'px'; k.appendChild(lg);
      var hb=el('div','k20-mid','left:'+sz.head.x+'px;top:'+sz.sy+'px;width:'+sz.head.w+'px;height:'+ih+'px');
      hb.appendChild(headline(sz.L[v],headSize(sz,sz.head.w,60,ih))); k.appendChild(hb);
      var B=sz.box, cb=el('div','k20-mid','left:'+B.x+'px;top:'+sz.sy+'px;width:'+B.w+'px;height:'+ih+'px');
      var p=cta(V[v].c,{f:B.f,py:B.py,px:B.px,wrap:1}); p.style.width='100%'; cb.appendChild(p); k.appendChild(cb);
      return k;
    }
    var f=headSize(sz,sz.top.hw,sz.top.hmax);
    k.appendChild(stack(sz,sz.top,v,f,'top'));
    if(sz.bot) k.appendChild(stack(sz,sz.bot,v,f,'bottom'));
    if(sz.logo&&sz.logo.at==='br'){
      var c=logo(sz.logo.w); c.style.cssText+=';position:absolute;right:'+sz.sx+'px;bottom:'+sz.sy+'px'; k.appendChild(c);
    }
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

  /* layout check: every text block and the logo inside the safe zone, no two overlapping, none
     covering the mishap itself, and the logo / CTA / disclaimer on the solid part of the fade.
     Results land on data-k20-issues for export.py. */
  function check(){
    var issues=[];
    [].forEach.call(document.querySelectorAll('.hub-ch-k20 .k20'),function(k){
      var fr=k.parentNode, W=+fr.dataset.w, H=+fr.dataset.h, sz=SIZES.filter(function(z){return z.w===W&&z.h===H;})[0];
      var v=k.dataset.v, name=frameName(sz,v), kr=k.getBoundingClientRect(), sc=kr.width/W, g=picGeom(sz,v);
      var rad=Math.min(W,H)*(sz.row?.18:.09), rects=[];
      [].forEach.call(k.querySelectorAll('.k20-logo,.k20-h > span,.k20-cta,.k20-disc > span'),function(n){
        var r=n.getBoundingClientRect(), x0=(r.left-kr.left)/sc, y0=(r.top-kr.top)/sc, x1=(r.right-kr.left)/sc, y1=(r.bottom-kr.top)/sc;
        var cls=n.className.baseVal!=null?'logo':(n.className||n.parentNode.className);
        var tag=cls+':'+(n.textContent||'').slice(0,16);
        if(x0<sz.sx-.5||y0<sz.sy-.5||x1>W-sz.sx+.5||y1>H-sz.sy+.5) issues.push(name+' SAFE '+tag);
        var nx=Math.max(x0,Math.min(g.fx,x1)), ny=Math.max(y0,Math.min(g.fy,y1));
        if(Math.hypot(nx-g.fx,ny-g.fy)<rad) issues.push(name+' COVERS MISHAP '+tag);
        var F=sz.pic.fade;
        if(!/^t[12]/.test(cls)&&F.dir==='bottom'&&y0<g.by+F.b*g.bh-2) issues.push(name+' NOT ON SOLID '+tag+' (top '+Math.round(y0)+' < '+Math.round(F.b*g.bh)+')');
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
