(function(){
  /* ---- banner data ---- */
  var COPY={
    h:"Don't take our word for it.",
    s:"Real people, real reviews. There's a reason why thousands rate Katapult 5 stars.",
    c:'See Why Shoppers Love Katapult.'
  };
  /* every line-break variant used anywhere below must still join back to COPY.h / COPY.s
     exactly -- copy is verbatim law, line breaks are a formatting choice only. */
  var H_SETS={
    two:["Don't take","our word for it."],
    one:["Don't take our word for it."],
    four:["Don't","take our","word for","it."]
  };
  var S_SETS={
    two:["Real people, real reviews. There's a reason","why thousands rate Katapult 5 stars."],
    three:["Real people, real reviews.","There's a reason why thousands","rate Katapult 5 stars."],
    five:["Real people,","real reviews. There's","a reason why","thousands rate Katapult","5 stars."],
    seven:["Real","people, real","reviews. There's","a reason why","thousands rate","Katapult 5","stars."],
    row:["Real people, real reviews.","There's a reason why thousands rate Katapult 5 stars."]
  };
  Object.keys(H_SETS).forEach(function(k){ if(H_SETS[k].join(' ')!==COPY.h) console.error('KAT26022: headline set "'+k+'" does not match the copy'); });
  Object.keys(S_SETS).forEach(function(k){ if(S_SETS[k].join(' ')!==COPY.s) console.error('KAT26022: subhead set "'+k+'" does not match the copy'); });

  /* ================================================================
     SEVENTH PASS (2026-10-05): scope goes from the 1200x1200 approval pair to
     8 sizes x 2 options = 16 deliverables.

     Reference = the two 1200x1200 frames the account lead adjusted in Figma and
     that pass 6 synced into the hub 1:1 (Progressive Global - LAB, page "kat"):
       Option A "Centered badge"       node 383:14304
       Option B "Photo and seam badge" node 387:14518
     Their 1200x1200 numbers below are the published ones, untouched. The only
     change on those two frames: Option B's shopper photo is now an honest
     placeholder (this brand's Q4 kit convention: Light Blue fill, dashed Dark
     Blue outline, "PHOTO PLACEHOLDER"), on purpose, until the real photo is
     swapped in by another route. Same box: 1200x600, 54px bottom corners.

     The other 7 sizes of each option carry the same language:
       A: copy centered at the top, a #282B60 circle rising behind the badge,
          the badge inside a halo of blurred star-only cards, logo bottom-right.
       B: photo band, the badge card bridging the photo's edge on the right,
          copy stacked left on the Dark Blue panel, logo bottom-right on the
          panel (never on the photo).
     728x90 and 320x50 collapse to one row (logo, copy, trust element, CTA).

     Type floors, both options, every size (never under these): the higher of
     this brand's two approved banner jobs at that size, KAT26019 kb.js and
     KAT26021 k21.js.
       1200x628: logo200, hf58, sf26, cta 28/19/42
       960x1200: logo220, hf76, sf34, cta 34/24/50
       300x600:  logo100, hf29, sf15, cta 17/11/18
       160x600:  logo88,  hf24, sf12, cta 13/8/12
       300x250:  logo76,  hf20.5, sf10, cta 12/8/14
       728x90:   logo96,  hf25, cta 13/9/12
       320x50:   logo46,  hf14, cta 8/4/5
     The subhead at 728x90 / 320x50 has no floor in either precedent (both jobs
     drop it there); here it stays because this brief puts it on every size.

     Verified by rendering in headless Chrome with the real Aktiv Grotesk loaded,
     reading back getBoundingClientRect frame-relative at 1:1 (see the pass 7
     note in k22.html for the numbers). */
  var FLOOR={
    '1200x1200':{logo:230,hf:84,sf:36,cf:36},
    '1200x628':{logo:200,hf:58,sf:26,cf:28},
    '960x1200':{logo:220,hf:76,sf:34,cf:34},
    '300x600':{logo:100,hf:29,sf:15,cf:17},
    '160x600':{logo:88,hf:24,sf:12,cf:13},
    '300x250':{logo:76,hf:20.5,sf:10,cf:12},
    '728x90':{logo:96,hf:25,sf:0,cf:13},
    '320x50':{logo:46,hf:14,sf:0,cf:8}
  };

  /* the badge, as Figma draws it at 1200x1200; every other size scales these */
  var TP={
    A:{w:499,h:230,gap:22,word:42,stars:62,sls:9,rad:32,plate:20},
    B:{w:433.4,h:200.5,gap:16,word:36.48,stars:62,sls:7.82,rad:27.8,plate:17.4,trim:true}
  };
  /* Option A's five decorative cards, Figma 383:14304, frame-relative around the
     badge centre (600,852). Figma layer blur / 4 = CSS blur; Figma rotation is
     counter-clockwise, so CSS rotate = -rot. */
  var DECO=[
    {x:316.6,y:729.1,w:194.6,h:71.8,r:-17.9,f:21.95,ls:2.93,blur:1.9,sh:14.6,oy:5.9,rad:16.1},
    {x:990.5,y:707.0,w:266,h:98,r:8,f:30,ls:4,blur:8.3,sh:20,oy:8,rad:22},
    {x:166.4,y:959.6,w:266,h:98,r:6,f:30,ls:4,blur:0,sh:20,oy:8,rad:22},
    {x:1095.5,y:983.2,w:196.2,h:73.2,r:23.9,f:22.13,ls:2.95,blur:6.1,sh:14.8,oy:5.9,rad:16.2},
    {x:586,y:1072.9,w:204.6,h:76.3,r:-17.4,f:23.07,ls:3.08,blur:6.4,sh:15.4,oy:6.2,rad:16.9}
  ];

  var SIZES=[
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      /* published Figma sync, 1:1 */
      A:{kind:'square',cx:600,
        arc:{x:-182,y:572,d:1563},
        tp:{cx:600,cy:852,s:1},
        deco:{cx:600,cy:852,s:1,spx:1,spy:1},
        logo:{w:230,right:77,bottom:60},
        hFont:109.67,hTop:77.4,
        sFont:42.18,sTop:324.5,
        cta:{f:42.18,w:779.3,h:108.1,top:464.5}},
      B:{kind:'square',
        photo:{x:0,y:0,w:1200,h:600,rad:'0 0 54px 54px'},
        tp:{cx:876.8,cy:573.25,s:1},
        logo:{w:230,right:77,bottom:60},
        x:78,
        hFont:100.77,hTop:662.2,
        sFont:38.76,sTop:894,
        cta:{f:38.76,w:715.4,h:99.3,top:1029.6}}},

    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      A:{kind:'stack',
        col:{x0:60,x1:620,vcenter:true},
        hSet:'two',hFont:72,
        sSet:'three',sFont:28,
        cta:{f:28,py:19,px:42},
        g:{hs:20,sc:28},
        tp:{cx:925,cy:300,s:.6},
        arc:{d:700,up:150},
        deco:{s:.6,spx:1,spy:1.1,pick:[0,1,2,3,4]},
        logo:{w:200,right:60,bottom:32}},
      B:{kind:'stack',
        photo:{x:0,y:0,w:470,h:628,rad:'0 40px 40px 0'},
        col:{x0:540,x1:1140,top:204,left:true},
        hSet:'two',hFont:64,
        sSet:'three',sFont:28,
        cta:{f:28,py:19,px:42},
        g:{hs:18,sc:26},
        tp:{cx:470,cy:118,s:.6},
        logo:{w:200,right:60,bottom:32}}},

    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      A:{kind:'square',cx:480,
        arc:{x:-301.5,y:572,d:1563},
        tp:{cx:480,cy:852,s:1},
        deco:{cx:480,cy:852,s:1,spx:.78,spy:1},
        logo:{w:220,right:60,bottom:60},
        hFont:109.67,hTop:77.4,
        sFont:42.18,sTop:324.5,
        cta:{f:42.18,w:779.3,h:108.1,top:464.5}},
      B:{kind:'stack',
        photo:{x:0,y:0,w:960,h:540,rad:'0 0 48px 48px'},
        col:{x0:64,x1:912,top:668,left:true},
        hSet:'two',hFont:92,
        sSet:'two',sFont:36,
        cta:{f:34,py:24,px:50},
        g:{hs:22,sc:26},
        tp:{cx:680,cy:540,s:.92},
        logo:{w:220,right:48,bottom:60}}},

    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,
      A:{kind:'stack',
        col:{x0:12,x1:288,top:20},
        hSet:'two',hFit:{floor:29,max:42},
        sSet:'five',sFit:{floor:15,max:17},
        cta:{f:17,py:11,px:18,wrap:true},
        g:{hs:12,sc:18},
        tp:{s:.46},region:{gapTop:30,gapBottom:30},
        arc:{d:520,up:90},
        deco:{s:.46,spx:.46,spy:.85,pick:[0,1,2,3,4]},
        logo:{w:100,right:12,bottom:12}},
      B:{kind:'stack',
        photo:{x:0,y:0,w:300,h:230,rad:'0 0 22px 22px'},
        col:{x0:12,x1:288,top:282,left:true},
        hSet:'two',hFit:{floor:29,max:40},
        sSet:'five',sFit:{floor:15,max:17},
        cta:{f:17,py:11,px:18,wrap:true},
        g:{hs:10,sc:16},
        tp:{cx:188,cy:230,s:.4},
        logo:{w:100,right:12,bottom:12}}},

    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,
      A:{kind:'stack',
        col:{x0:8,x1:152,top:16},
        hSet:'four',hFit:{floor:24,max:32},
        sSet:'seven',sFit:{floor:12,max:14},
        cta:{f:13,py:8,px:12,wrap:true},
        g:{hs:10,sc:14},
        tp:{s:.25},region:{gapTop:34,gapBottom:28},
        arc:{d:300,up:44},
        deco:{s:.25,spx:.3,spy:1.1,pick:[0,1,2,3,4]},
        logo:{w:88,right:8,bottom:8}},
      B:{kind:'stack',
        photo:{x:0,y:0,w:160,h:180,rad:'0 0 16px 16px'},
        col:{x0:8,x1:152,top:222,left:true},
        hSet:'four',hFit:{floor:24,max:30},
        sSet:'seven',sFit:{floor:12,max:13},
        cta:{f:13,py:8,px:12,wrap:true},
        g:{hs:8,sc:12},
        tp:{cx:90,cy:180,s:.26},
        logo:{w:88,right:8,bottom:8}}},

    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,
      A:{kind:'stack',
        col:{x0:8,x1:292,top:10},
        hSet:'two',hFont:22,
        sSet:'two',sFont:10.5,
        cta:{f:12,py:8,px:14},
        g:{hs:6,sc:9},
        tp:{s:.22},region:{gapTop:16,gapBottom:6},
        arc:{d:300,up:40},
        deco:{s:.22,spx:.9,spy:.55,pick:[0,1,2,3]},
        logo:{w:76,right:8,bottom:8}},
      B:{kind:'stack',
        photo:{x:0,y:0,w:300,h:84,rad:'0 0 12px 12px'},
        col:{x0:12,x1:292,top:104,left:true},
        hSet:'two',hFont:21,
        sSet:'two',sFont:10,
        cta:{f:12,py:8,px:14},
        g:{hs:5,sc:9},
        tp:{cx:224,cy:84,s:.21},
        logo:{w:76,right:8,bottom:8}}},

    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,
      A:{kind:'row',
        logo:{x:14,w:96},
        text:{x:124,w:344},
        hSet:'one',hFont:25,sSet:'row',sFont:11,gap:3,
        tp:{cx:521,cy:45,s:.16,fs:.2},
        arc:{d:110,up:20},
        deco:{s:.16,spx:.8,spy:.75,pick:[0,2,4]},
        cta:{x:578,w:138,f:13,py:9,px:12,wrap:true}},
      B:{kind:'row',
        logo:{x:14,w:96},
        text:{x:124,w:344},
        hSet:'one',hFont:25,sSet:'row',sFont:11,gap:3,
        photo:{x:482,y:0,w:80,h:58,rad:'0 0 9px 9px'},
        tp:{cx:522,cy:60,s:.15,fs:.19},
        cta:{x:578,w:138,f:13,py:9,px:12,wrap:true}}},

    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,
      A:{kind:'row',
        logo:{x:6,w:46,y:34.5},
        text:{x:60,w:184},
        hSet:'one',hFont:14,sSet:'row',sFont:6,gap:2,
        tp:{cx:29,cy:17,s:.092,fs:.12},
        cta:{x:250,w:66,f:8,py:4,px:5,wrap:true}},
      B:{kind:'row',
        logo:{x:6,w:46,y:34.5},
        text:{x:60,w:184},
        hSet:'one',hFont:14,sSet:'row',sFont:6,gap:2,
        photo:{x:6,y:0,w:46,h:20,rad:'0 0 5px 5px'},
        tp:{cx:29,cy:20,s:.095,fs:.115},
        cta:{x:250,w:66,f:8,py:4,px:5,wrap:true}}}
  ];

  /* ---- helpers ---- */
  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function mark(e,name){ e.dataset.el=name; return e; }
  var MH=null;
  function host(){ if(!MH){ MH=el('div','','position:absolute;left:-99999px;top:0;visibility:hidden;width:4000px;height:4000px'); document.body.appendChild(MH); } return MH; }
  /* size of a node as it will render on the canvas (absolute, shrink-to-fit) */
  function measure(node,maxW){
    var c=node.cloneNode(true); c.style.position='absolute'; c.style.left='0'; c.style.top='0'; c.style.transform='none';
    if(maxW) c.style.maxWidth=maxW+'px';
    host().appendChild(c); var r={w:c.offsetWidth,h:c.offsetHeight}; host().removeChild(c); return r;
  }
  /* largest half-pixel font size that fits the box, clamped to [floor,max] */
  function fit(node,w,h,o){
    var c=node.cloneNode(true); c.style.fontSize='100px';
    var m=measure(c), f=Math.floor(100*Math.min(w/m.w,h/m.h)*.98*2)/2;
    if(o.max) f=Math.min(f,o.max);
    return Math.max(f,o.floor||0);
  }
  function lines(cls,arr,fontPx,left){
    var p=el('p',cls+(left?' k22-left':''), fontPx?('font-size:'+fontPx+'px'):'');
    arr.forEach(function(t){ var s=el('span'); s.textContent=t; p.appendChild(s); });
    return p;
  }
  function logoSvg(w){
    var s=document.createElementNS('http://www.w3.org/2000/svg','svg');
    s.setAttribute('class','k22-logo'); s.setAttribute('viewBox','0 0 521 116'); s.setAttribute('role','img'); s.setAttribute('aria-label','Katapult');
    s.style.width=w+'px'; s.dataset.el='logo';
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); s.appendChild(u);
    return s;
  }
  function logoH(w){ return w*116/521; }
  /* the one trust element: wordmark + stars on a white card with the brand's flat cream
     plate, no quote, no invented TrustScore or review count. s scales the box, fs the
     type (the two smallest sizes keep the type a little larger than pure scale) */
  function badge(cx,cy,s,v,fs){
    var P=TP[v], t=fs||s, w=P.w*s, h=P.h*s;
    var b=el('div','k22-tp','left:'+cx+'px;top:'+cy+'px;width:'+w+'px;height:'+h+'px;padding:0;gap:'+(P.gap*t)+'px;border-radius:'+(P.rad*s)+'px;box-shadow:'+(P.plate*s)+'px '+(P.plate*s)+'px 0 #D4A574;transform:translate(-50%,-50%)');
    mark(b,'badge'); b.dataset.plate=P.plate*s;
    var wd=el('span','k22-tp-word','font-size:'+(P.word*t)+'px'); wd.textContent='Trustpilot';
    var st=el('span','k22-tp-stars','font-size:'+(P.stars*t)+'px;letter-spacing:'+(P.sls*t)+'px'+(P.trim?';margin-right:-'+(P.sls*t)+'px':'')); st.textContent='★★★★★';
    b.appendChild(wd); b.appendChild(st);
    return b;
  }
  /* decorative-only: white card + mini star row, no quote text, blurred, so it never
     reads as a legible (and therefore fabricated) testimonial */
  function decoCard(d){
    var b=el('div','k22-deco','left:'+d.x+'px;top:'+d.y+'px;width:'+d.w+'px;height:'+d.h+'px;padding:0;border-radius:'+d.rad+'px;box-shadow:0 '+d.oy+'px '+d.sh+'px rgba(0,0,0,.18);filter:'+(d.blur?'blur('+d.blur+'px)':'none')+';transform:translate(-50%,-50%) rotate('+d.r+'deg)');
    mark(b,'deco');
    var st=el('span','k22-deco-stars','font-size:'+d.f+'px;letter-spacing:'+d.ls+'px'); st.textContent='★★★★★';
    b.appendChild(st);
    return b;
  }
  /* Figma's halo, re-centred on (cx,cy), scaled by s, spread by spx/spy */
  function halo(k,cx,cy,o){
    var s=o.s, pick=o.pick||[0,1,2,3,4];
    pick.forEach(function(i){
      var d=DECO[i];
      k.appendChild(decoCard({x:cx+(d.x-600)*s*o.spx,y:cy+(d.y-852)*s*o.spy,w:d.w*s,h:d.h*s,r:d.r,f:d.f*s,ls:d.ls*s,
        blur:d.blur?Math.max(.6,d.blur*s):0,sh:d.sh*s,oy:d.oy*s,rad:d.rad*s}));
    });
  }
  function arc(k,x,y,d){ k.appendChild(mark(el('div','k22-arc','left:'+x+'px;top:'+y+'px;width:'+d+'px;height:'+d+'px'),'arc')); }
  function cta(c){
    var b=el('span','k22-cta'+(c.wrap?' wrap':''),'font-size:'+c.f+'px;'+(c.w&&c.h?'width:'+c.w+'px;height:'+c.h+'px;padding:0;box-sizing:border-box':'padding:'+c.py+'px '+c.px+'px'));
    mark(b,'cta'); b.textContent=COPY.c; return b;
  }
  /* photo placeholder: this brand's own Q4 kit convention (kp-ph), so Option B never
     reads as a real or stock photo pending the real asset */
  function photo(k,p,label){
    var u=Math.min(1,Math.max(p.w,p.h)/1200);
    var b=el('div','k22-ph','left:'+p.x+'px;top:'+p.y+'px;width:'+p.w+'px;height:'+p.h+'px;border-radius:'+p.rad+
      ';outline-width:'+Math.max(1,Math.round(4*u))+'px;outline-offset:-'+Math.max(2,Math.round(14*u))+'px;font-size:'+Math.max(9,Math.round(18*u))+'px');
    b.setAttribute('role','img'); b.setAttribute('aria-label','Photo placeholder: real shopper photo to come');
    mark(b,'photo');
    if(label){ var sp=el('span'); sp.textContent='Photo placeholder'; b.appendChild(sp); }
    k.appendChild(b);
  }
  function put(k,node,x,y){ node.style.left=x+'px'; node.style.top=y+'px'; k.appendChild(node); return node; }
  function canvasEl(sz){ return el('div','k22','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px'); }

  /* ---- square-ish PMAX, explicit Figma geometry (A: 1200 and 960, B: 1200) ---- */
  function squareA(k,sz,A){
    arc(k,A.arc.x,A.arc.y,A.arc.d);
    halo(k,A.deco.cx,A.deco.cy,A.deco);
    k.appendChild(badge(A.tp.cx,A.tp.cy,A.tp.s,'A'));
    var hd=mark(lines('k22-h',H_SETS.two,A.hFont),'headline'); hd.style.cssText+=';left:'+A.cx+'px;top:'+A.hTop+'px;transform:translateX(-50%)'; k.appendChild(hd);
    var sb=mark(lines('k22-s2',S_SETS.two,A.sFont),'subhead'); sb.style.cssText+=';left:'+A.cx+'px;top:'+A.sTop+'px;transform:translateX(-50%)'; k.appendChild(sb);
    var cb=cta(A.cta); cb.style.cssText+=';left:'+A.cx+'px;top:'+A.cta.top+'px;transform:translateX(-50%)'; k.appendChild(cb);
    var lg=logoSvg(A.logo.w); lg.style.cssText+=';right:'+A.logo.right+'px;bottom:'+A.logo.bottom+'px'; k.appendChild(lg);
  }
  function squareB(k,sz,B){
    photo(k,B.photo,true);
    k.appendChild(badge(B.tp.cx,B.tp.cy,B.tp.s,'B'));
    put(k,mark(lines('k22-h',H_SETS.two,B.hFont,true),'headline'),B.x,B.hTop);
    put(k,mark(lines('k22-s2',S_SETS.two,B.sFont,true),'subhead'),B.x,B.sTop);
    put(k,cta(B.cta),B.x,B.cta.top);
    var lg=logoSvg(B.logo.w); lg.style.cssText+=';right:'+B.logo.right+'px;bottom:'+B.logo.bottom+'px'; k.appendChild(lg);
  }

  /* ---- measured stack: headline / subhead / cta as one column, everything else from it ---- */
  function stack(k,sz,C,v){
    var left=!!C.col.left, cw=C.col.x1-C.col.x0;
    var hd=mark(lines('k22-h',H_SETS[C.hSet],C.hFont,left),'headline');
    if(C.hFit) hd.style.fontSize=fit(hd,cw,9999,C.hFit)+'px';
    var sb=mark(lines('k22-s2',S_SETS[C.sSet],C.sFont,left),'subhead');
    if(C.sFit) sb.style.fontSize=fit(sb,cw,9999,C.sFit)+'px';
    var cb=cta(C.cta);
    var mh=measure(hd), ms=measure(sb), mc=measure(cb,cw);
    if(C.cta.wrap){ cb.style.maxWidth=cw+'px'; }
    var colH=mh.h+C.g.hs+ms.h+C.g.sc+mc.h;
    var top=C.col.vcenter?Math.round(sz.sy+(sz.h-2*sz.sy-colH)/2):C.col.top;
    var cx=C.col.x0+cw/2;
    function px(m){ return left?C.col.x0:Math.round(cx-m.w/2); }
    var yH=top, yS=yH+mh.h+C.g.hs, yC=yS+ms.h+C.g.sc, colBottom=yC+mc.h;

    var lgTop=sz.h-C.logo.bottom-logoH(C.logo.w);
    if(v==='A'){
      var P=TP.A, bh=P.h*C.tp.s, tcx, tcy;
      if(C.tp.cx!=null){ tcx=C.tp.cx; tcy=C.tp.cy; }
      else { tcx=sz.w/2; var y0=colBottom+C.region.gapTop, y1=lgTop-C.region.gapBottom; tcy=Math.round((y0+y1)/2); }
      arc(k,tcx-C.arc.d/2,tcy-C.arc.up,C.arc.d);
      halo(k,tcx,tcy,C.deco);
      k.appendChild(badge(tcx,tcy,C.tp.s,'A'));
    } else {
      photo(k,C.photo,true);
      k.appendChild(badge(C.tp.cx,C.tp.cy,C.tp.s,'B'));
    }
    put(k,hd,px(mh),yH); put(k,sb,px(ms),yS); put(k,cb,px(mc),yC);
    var lg=logoSvg(C.logo.w); lg.style.cssText+=';right:'+C.logo.right+'px;bottom:'+C.logo.bottom+'px'; k.appendChild(lg);
  }

  /* ---- one-row leaderboards: logo, copy, trust element, cta ---- */
  function row(k,sz,R,v){
    var ih=sz.h-2*sz.sy, lh=logoH(R.logo.w);
    var lg=logoSvg(R.logo.w); put(k,lg,R.logo.x,R.logo.y!=null?R.logo.y:(sz.h-lh)/2);
    var hd=mark(lines('k22-h',H_SETS[R.hSet],R.hFont,true),'headline');
    var sb=mark(lines('k22-s2',S_SETS[R.sSet],R.sFont,true),'subhead');
    var mh=measure(hd), ms=measure(sb), th=mh.h+R.gap+ms.h, ty=Math.round(sz.sy+(ih-th)/2);
    put(k,hd,R.text.x,ty); put(k,sb,R.text.x,ty+mh.h+R.gap);
    if(v==='A'){
      if(R.arc) arc(k,R.tp.cx-R.arc.d/2,R.tp.cy-R.arc.up,R.arc.d);
      if(R.deco) halo(k,R.tp.cx,R.tp.cy,R.deco);
    } else photo(k,R.photo,false);
    k.appendChild(badge(R.tp.cx,R.tp.cy,R.tp.s,v,R.tp.fs));
    var cb=cta(R.cta); cb.style.width=R.cta.w+'px'; cb.style.boxSizing='border-box';
    var mc=measure(cb); put(k,cb,R.cta.x,Math.round((sz.h-mc.h)/2));
  }

  function canvas(sz,v){
    var k=canvasEl(sz), C=sz[v];
    if(C.kind==='square') (v==='A'?squareA:squareB)(k,sz,C);
    else if(C.kind==='stack') stack(k,sz,C,v);
    else row(k,sz,C,v);
    return k;
  }

  var OPT={A:'Centered badge',B:'Photo and seam badge'};
  function frameName(sz,v){ return 'KAT26022-Trusted-'+sz.w+'x'+sz.h+'-Static-'+sz.plat+'-V1-Option'+v; }
  function label(sz,v){ return 'Option '+v+' · '+OPT[v]+' · '+sz.w+' × '+sz.h+(sz.ratio?' · '+sz.ratio:''); }
  function figure(sz,v){
    var f=el('figure','kb-fig'), sc=el('div','kb-scroll'), fr=el('div','k22-frame');
    fr.dataset.w=sz.w; fr.dataset.h=sz.h; fr.dataset.s=sz.show;
    fr.appendChild(canvas(sz,v)); sc.appendChild(fr); f.appendChild(sc);
    var fc=el('figcaption'), b=el('b'), mo=el('span','mono'); b.textContent=label(sz,v); mo.textContent=frameName(sz,v);
    fc.appendChild(b); fc.appendChild(mo); f.appendChild(fc);
    return f;
  }

  /* one row per size, Option A beside Option B, so the two directions compare at a glance */
  function render(){
    var v1=document.getElementById('k22-v1-rows'); v1.replaceChildren();
    ['PMAX','Programmatic'].forEach(function(pl){
      var hd=el('p','kb-plat'); hd.textContent=pl==='PMAX'?'PMAX static':'Google programmatic static'; v1.appendChild(hd);
      SIZES.filter(function(s){return s.plat===pl;}).forEach(function(sz){
        var row=el('div','kb-row'); row.appendChild(figure(sz,'A')); row.appendChild(figure(sz,'B')); v1.appendChild(row);
      });
    });
    applyScale();
  }
  /* ---- scale + safe zones ---- */
  var full=document.getElementById('k22-full'), safe=document.getElementById('k22-safe'), root=document.querySelector('.hub-ch-k22');
  function applyScale(){
    [].forEach.call(document.querySelectorAll('.k22-frame'),function(fr){
      var s=full.checked?1:+fr.dataset.s;
      fr.style.width=(fr.dataset.w*s)+'px'; fr.style.height=(fr.dataset.h*s)+'px';
      fr.firstChild.style.transform='scale('+s+')';
    });
  }
  full.addEventListener('change',applyScale);
  var fl=document.fonts?Promise.all(['400','500','700'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(render);
  function applySafe(){ root.classList.toggle('k22-safe-on',safe.checked); }
  safe.addEventListener('change',applySafe); applySafe();
})();
