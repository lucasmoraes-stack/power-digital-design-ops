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

  /* circle crops, in source pixels: centre fx,fy and side s of the square the circle is cut from.
     wide = the whole mishap with its room around it, tight = the mishap alone, for small circles */
  var CROP={
    kitchen:{wide:{fx:470,fy:770,s:900}, tight:{fx:415,fy:775,s:560}},
    livingroom:{wide:{fx:830,fy:1020,s:1080}, tight:{fx:860,fy:1000,s:720}}
  };

  /* Each size: safe inset, the photo circle (cx,cy,d, may bleed off the frame), and text blocks.
     top / bot = stacks anchored to the top or bottom of the safe zone; items run in order.
     L = per version, the headline lines for [sentence 1, sentence 2]; joined back they must equal the copy.
     The headline gets the largest size that fits hw for BOTH versions, so V1 and V2 differ only by image and copy. */
  var SIZES=[
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      circle:{cx:848,cy:930,d:940,crop:'wide'},
      top:{x:60,w:1080,hw:1080,hmax:120,items:['head',36,'cta'],cta:{f:30,py:22,px:44}},
      bot:{x:60,w:285,items:['logo',28,'disc'],logo:230,disc:12},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      circle:{cx:965,cy:314,d:650,crop:'wide'},
      top:{x:60,w:560,hw:490,hmax:84,items:['logo',34,'head',28,'cta'],logo:190,cta:{f:24,py:17,px:34}},
      bot:{x:60,w:540,items:['disc'],disc:11},
      L:{V1:[["The turkey's","fine."],["The oven isn't."]],V2:[['Cyber deals','are here.'],['Let Katapult help.']]}},
    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      circle:{cx:720,cy:870,d:800,crop:'wide'},
      top:{x:48,w:864,hw:864,hmax:110,items:['head',34,'cta'],cta:{f:28,py:20,px:40}},
      bot:{x:48,w:250,items:['logo',26,'disc'],logo:210,disc:12},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,
      circle:{cx:180,cy:474,d:300,crop:'tight'},
      top:{x:12,w:276,hw:276,hmax:40,items:['logo',22,'head',16,'cta'],logo:104,cta:{f:15,py:11,px:18,wrap:1}},
      L:{V1:[["The turkey's","fine."],["The oven","isn't."]],V2:[['Cyber deals','are here.'],['Let Katapult','help.']]}},
    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,
      circle:{cx:108,cy:478,d:244,crop:'tight'},
      top:{x:8,w:144,hw:144,hmax:30,items:['logo',20,'head',14,'cta'],logo:90,cta:{f:12,py:9,px:12,wrap:1}},
      L:{V1:[["The","turkey's","fine."],['The oven',"isn't."]],V2:[['Cyber','deals are','here.'],['Let','Katapult','help.']]}},
    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,
      circle:{cx:272,cy:112,d:220,crop:'tight'},
      top:{x:8,w:142,hw:142,hmax:26,items:['logo',12,'head',10,'cta'],logo:72,cta:{f:11,py:7,px:11,wrap:1}},
      L:{V1:[["The","turkey's","fine."],['The oven',"isn't."]],V2:[['Cyber deals','are here.'],['Let','Katapult','help.']]}},
    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,row:1,
      circle:{cx:690,cy:45,d:128,crop:'tight'},
      logo:{x:12,w:92}, head:{x:120,w:300}, box:{x:436,w:172,f:12,py:8,px:10},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}},
    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,row:1,
      circle:{cx:313,cy:25,d:64,crop:'tight'},
      logo:{x:6,w:44}, head:{x:58,w:118}, box:{x:182,w:88,f:7.5,py:4,px:5},
      L:{V1:[["The turkey's fine."],["The oven isn't."]],V2:[['Cyber deals are here.'],['Let Katapult help.']]}}
  ];
  SIZES.forEach(function(sz){
    ['V1','V2'].forEach(function(v){
      var L=sz.L[v];
      if(L[0].join(' ')!==V[v].h1||L[1].join(' ')!==V[v].h2) console.error('KAT26020: headline lines do not match the copy at '+sz.w+'x'+sz.h+' '+v);
    });
  });

  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  var MH=null;
  function host(){ if(!MH){ MH=el('div','k20','position:absolute;left:-99999px;top:0;visibility:hidden;width:4000px;height:4000px'); document.body.appendChild(MH); } return MH; }
  function size(node,w){ var h=host(); if(w) node.style.width=w+'px'; h.appendChild(node); var r={w:node.offsetWidth,h:node.offsetHeight}; h.removeChild(node); if(w) node.style.width=''; return r; }
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
  /* largest headline size, in half pixels, that fits width w for both versions */
  function headSize(sz,w,cap,h){
    var f=cap;
    ['V1','V2'].forEach(function(v){
      var p=headline(sz.L[v],100); var r=size(p);
      var g=100*w/r.w; if(h) g=Math.min(g,100*h/r.h);
      f=Math.min(f,g);
    });
    return Math.floor(f*2)/2;
  }
  function cta(text,c,w){
    var b=el('span','k20-cta'+(c.wrap?' wrap':''),'font-size:'+c.f+'px;padding:'+c.py+'px '+c.px+'px'+(w?';width:'+w+'px':''));
    b.textContent=text; return b;
  }
  function disc(f){ var p=el('p','k20-disc','font-size:'+f+'px'); DISC.forEach(function(t){ var s=el('span'); s.textContent=t; p.appendChild(s); }); return p; }

  function photo(sz,v){
    var C=sz.circle, P=K20_PHOTOS[V[v].img], cr=CROP[V[v].img][C.crop], k=C.d/cr.s;
    var wrap=el('div','k20-pic','left:'+(C.cx-C.d/2)+'px;top:'+(C.cy-C.d/2)+'px;width:'+C.d+'px;height:'+C.d+'px');
    if(P){
      var im=el('img','', 'left:'+(-(cr.fx-cr.s/2)*k)+'px;top:'+(-(cr.fy-cr.s/2)*k)+'px;width:'+(P.w*k)+'px;height:'+(P.h*k)+'px');
      im.src=P.src; im.alt=''; im.setAttribute('width',Math.round(P.w*k)); im.setAttribute('height',Math.round(P.h*k));
      im.dataset.crop=[V[v].img,cr.fx,cr.fy,cr.s,C.d].join(',');
      wrap.appendChild(im);
    }
    return wrap;
  }
  /* the Bounce ring: concentric, dotted on the left half, solid on the right half */
  function ring(sz){
    var C=sz.circle, gap=Math.max(3,C.d*.035), sw=Math.max(1.2,C.d*.0075), r=C.d/2+gap, pad=sw*2, S=2*(r+pad);
    var s=svg('svg',{'class':'k20-ring',width:S,height:S,viewBox:'0 0 '+S+' '+S,'aria-hidden':'true'});
    s.style.cssText='left:'+(C.cx-S/2)+'px;top:'+(C.cy-S/2)+'px;width:'+S+'px;height:'+S+'px';
    var c=S/2;
    /* right half solid, from top to bottom through the right */
    s.appendChild(svg('path',{d:'M'+c+' '+(c-r)+' A'+r+' '+r+' 0 0 1 '+c+' '+(c+r),fill:'none',stroke:'#9EB5C0','stroke-width':sw,'stroke-linecap':'round'}));
    /* left half dotted */
    var dots=Math.max(14,Math.round(Math.PI*r/(sw*4.2)));
    s.appendChild(svg('path',{d:'M'+c+' '+(c+r)+' A'+r+' '+r+' 0 0 1 '+c+' '+(c-r),fill:'none',stroke:'#9EB5C0','stroke-width':sw*1.25,'stroke-linecap':'round','stroke-dasharray':'0 '+(Math.PI*r/dots).toFixed(3)}));
    return s;
  }

  function stack(sz,spec,v,f,anchor){
    var st=el('div','k20-stack','left:'+spec.x+'px;width:'+spec.w+'px;'+(anchor==='bottom'?'bottom:'+sz.sy+'px':'top:'+sz.sy+'px'));
    var gap=0;
    spec.items.forEach(function(it){
      if(typeof it==='number'){ gap=it; return; }
      var n;
      if(it==='logo') n=logo(spec.logo);
      else if(it==='head') n=headline(sz.L[v],f);
      else if(it==='cta') n=cta(V[v].c,spec.cta,spec.cta.wrap?null:null);
      else if(it==='disc') n=disc(spec.disc);
      if(it==='cta'&&spec.cta.wrap) n.style.maxWidth=spec.w+'px';
      if(gap) n.style.marginTop=gap+'px';
      gap=0; st.appendChild(n);
    });
    return st;
  }

  function canvas(sz,v){
    var k=el('div','k20','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px');
    k.dataset.v=v;
    k.appendChild(photo(sz,v)); k.appendChild(ring(sz));
    if(sz.row){
      var ih=sz.h-2*sz.sy;
      var lg=logo(sz.logo.w); lg.style.cssText+=';position:absolute;left:'+sz.logo.x+'px;top:'+((sz.h-sz.logo.w*116/521)/2)+'px'; k.appendChild(lg);
      var hb=el('div','k20-mid','left:'+sz.head.x+'px;top:'+sz.sy+'px;width:'+sz.head.w+'px;height:'+ih+'px');
      hb.appendChild(headline(sz.L[v],headSize(sz,sz.head.w,999,ih))); k.appendChild(hb);
      var B=sz.box, cb=el('div','k20-mid','left:'+B.x+'px;top:'+sz.sy+'px;width:'+B.w+'px;height:'+ih+'px');
      var p=cta(V[v].c,{f:B.f,py:B.py,px:B.px,wrap:1}); p.style.width='100%'; cb.appendChild(p); k.appendChild(cb);
      return k;
    }
    var f=headSize(sz,sz.top.hw,sz.top.hmax);
    k.appendChild(stack(sz,sz.top,v,f,'top'));
    if(sz.bot) k.appendChild(stack(sz,sz.bot,v,f,'bottom'));
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

  /* overlap / safe-zone check: every text block and the logo must sit inside the safe zone and
     clear of the photo circle + ring. Results land on data-k20-issues for the build check. */
  function check(){
    var issues=[];
    [].forEach.call(document.querySelectorAll('.hub-ch-k20 .k20'),function(k){
      var fr=k.parentNode, s=fr.style.transform?1:1;
      var W=+fr.dataset.w, H=+fr.dataset.h, sz=SIZES.filter(function(z){return z.w===W&&z.h===H;})[0];
      var kr=k.getBoundingClientRect(), sc=kr.width/W, C=sz.circle, R=C.d/2+Math.max(3,C.d*.035)+Math.max(1.2,C.d*.0075);
      var name=frameName(sz,k.dataset.v);
      [].forEach.call(k.querySelectorAll('.k20-logo,.k20-h > span,.k20-cta,.k20-disc > span'),function(n){
        var r=n.getBoundingClientRect(), x0=(r.left-kr.left)/sc, y0=(r.top-kr.top)/sc, x1=(r.right-kr.left)/sc, y1=(r.bottom-kr.top)/sc;
        var tag=n.className.baseVal!=null?'logo':(n.className||n.parentNode.className)+':'+n.textContent.slice(0,18);
        if(x0<sz.sx-.5||y0<sz.sy-.5||x1>W-sz.sx+.5||y1>H-sz.sy+.5) issues.push(name+' SAFE '+tag+' ['+[x0,y0,x1,y1].map(Math.round)+']');
        var nx=Math.max(x0,Math.min(C.cx,x1)), ny=Math.max(y0,Math.min(C.cy,y1));
        var d=Math.hypot(nx-C.cx,ny-C.cy);
        if(d<R+Math.max(4,sz.sx*.5)) issues.push(name+' CIRCLE '+tag+' clear '+Math.round(d-R)+'px');
      });
      [].forEach.call(k.querySelectorAll('.k20-stack'),function(st){
        if(st.offsetHeight>H) issues.push(name+' STACK too tall');
      });
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
