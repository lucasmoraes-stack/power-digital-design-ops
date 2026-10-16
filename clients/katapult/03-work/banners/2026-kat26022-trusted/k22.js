(function(){
  /* ---- banner data ---- */
  var COPY={
    h:"Don't take our word for it.",
    s:"Real people, real reviews. There's a reason why thousands rate Katapult 5 stars.",
    c:'See Why Shoppers Love Katapult'
  };
  /* every line-break variant used below must still join back to the copy exactly:
     copy is verbatim law, line breaks are a formatting choice only. */
  var H={
    two:["Don't take","our word for it."],
    one:["Don't take our word for it."],
    row:["Don't take our","word for it."],
    three:["Don't take","our word","for it."],
    threeN:["Don't","take our","word for it."]
  };
  var S={
    two:["Real people, real reviews. There's a reason","why thousands rate Katapult 5 stars."],
    three:["Real people, real reviews.","There's a reason why","thousands rate Katapult 5 stars."],
    four:["Real people, real","reviews. There's a","reason why thousands","rate Katapult 5 stars."]
  };
  var C={ one:[COPY.c], two:["See Why Shoppers","Love Katapult"] };
  [[H,COPY.h],[S,COPY.s],[C,COPY.c]].forEach(function(p){
    Object.keys(p[0]).forEach(function(k){ if(p[0][k].join(' ')!==p[1]) console.error('KAT26022: line set "'+k+'" does not match the copy'); });
  });

  /* the shopper photo (library: laptop-woman-window-desk-06, Adobe Stock 410115591),
     filled in by build.py as a WebP data URI */
  var K22_PHOTO={};

  /* ================================================================
     EIGHTH PASS (2026-10-13): synced 1:1 from the account lead's Figma rework,
     Progressive Global - LAB, page 547:1720.
       Option A  PMAX 547:3269 (1x1 547:3270, 1.91:1 547:3305, 4x5 547:3343)
                 Programmatic 547:3380 (300x250 547:3381, 728x90 547:3412,
                 320x50 547:3438, 300x600 547:3464, 160x600 547:3498)
       Option B  PMAX 547:3106 (1x1 547:3107, 1.91:1 547:3127, 4x5 547:3148)
                 Programmatic 547:3170 (300x250 547:3171, 728x90 547:3191,
                 320x50 547:3209, 300x600 547:3227, 160x600 547:3248)
     Every number below is frame-relative px read from get_design_context.
     Text y = the top of the Figma text node. Nodes marked trim:1 use Figma's
     cap-to-baseline trim, so their y is the cap top; the renderer offsets the
     line box by the real font metrics (see capTop) so the cap lands there.
     The hidden "disclaimer" layers on both 4x5 frames stay out.

     Element types:
       arc   circle {x,y,d}
       photo {x,y,w,h,r:border-radius, img:{l,t,w,h} inside the box}
       h/s   headline / subhead {x,y,w?,c:center,f,lh,ls,trim,l:lines,wt}
       cta   pink pill {x,y,w,h,f,lh,ls,l:lines}
       logo  {x,y,w}
       deco  decorative star-only card {x,y,w,h,r,f,ls,oy,sb}, one blur per frame
       tp    Trustpilot card {x,y,w,h,r,p:plate,g:gap,wf,wp:[top,bottom],sf,sls,sw}
     Drawn in Figma's layer order. */
  var FRAMES=[
    {w:1200,h:1200,plat:'PMAX',ratio:'1:1',sx:60,sy:60,show:.4,
      A:{blur:3,els:[
        ['arc',{x:-182,y:543,d:1563}],
        ['h',{x:148,y:96.72,w:903,c:1,f:123.7,lh:121.23,ls:-1.645,l:H.two}],
        ['s',{x:195.4,y:363.81,w:802,c:1,f:42.2,lh:50.62,l:S.two}],
        ['cta',{x:210.35,y:504.5,w:779.3,h:108.09,f:42.2,lh:48.51,ls:-.211,l:C.one}],
        ['logo',{x:893,y:1088.8,w:230}],
        ['deco',{x:161,y:764,w:194.59,h:71.8,r:16.9,f:22,ls:2.93,oy:6.2,sb:7.7}],
        ['deco',{x:882.53,y:702.03,w:266,h:98,r:16.9,f:30,ls:4,oy:6.2,sb:7.7}],
        ['deco',{x:41,y:934,w:266,h:98,r:16.9,f:30,ls:4,oy:6.2,sb:7.7}],
        ['deco',{x:997.4,y:946.59,w:196.19,h:73.19,r:16.9,f:22.1,ls:2.95,oy:6.2,sb:7.7}],
        ['deco',{x:483.71,y:1034.74,w:204.59,h:76.3,r:16.9,f:23.1,ls:3.08,oy:6.2,sb:7.7}],
        ['tp',{x:331,y:737,w:499,h:230,r:32,p:20,g:12,wf:42,wp:[4,4],sf:62,sls:9,sw:355}]]},
      B:{els:[
        ['photo',{x:0,y:0,w:1200,h:600,r:'0 0 54px 54px',img:{l:0,t:-100,w:1200,h:800}}],
        ['h',{x:78,y:651,f:110,lh:105.8,ls:-1.512,l:H.two}],
        ['s',{x:78,y:897,f:38.8,lh:46.51,l:S.two}],
        ['cta',{x:78,y:1029.59,w:715.39,h:99.3,f:38.8,lh:44.57,ls:-.194,l:C.one}],
        ['logo',{x:893,y:1088.8,w:230}],
        ['tp',{x:660.1,y:473,w:433.39,h:200.5,r:27.8,p:17.4,g:16,wf:36.5,wp:[3,4],sf:62,sls:7.82,sw:341.29}]]}},

    {w:1200,h:628,plat:'PMAX',ratio:'1.91:1',sx:60,sy:32,show:.4,
      A:{blur:1.8,els:[
        ['arc',{x:646,y:-166,d:960}],
        ['logo',{x:55,y:96.05,w:186}],
        ['h',{x:55,y:173.45,f:76,lh:72,ls:-1.08,trim:1,l:H.two}],
        ['s',{x:55,y:335.45,f:28,lh:33.6,trim:1,l:S.three}],
        ['cta',{x:55,y:468.45,w:471,h:63.69,f:25.362,lh:29.166,ls:-.1268,l:C.one}],
        ['deco',{x:696.58,y:197.34,w:116.75,h:43.08,r:9.66,f:13.2,ls:1.758,oy:3.54,sb:4.38}],
        ['deco',{x:1079.5,y:174.9,w:159.59,h:58.8,r:13.2,f:18,ls:2.4,oy:4.8,sb:6}],
        ['deco',{x:585.03,y:341.62,w:159.59,h:58.8,r:13.2,f:18,ls:2.4,oy:4.8,sb:6}],
        ['deco',{x:1163.44,y:364.62,w:117.72,h:43.91,r:9.72,f:13.3,ls:1.77,oy:3.54,sb:4.44}],
        ['deco',{x:855.22,y:422.9,w:122.75,h:45.77,r:10.14,f:13.8,ls:1.848,oy:3.72,sb:4.62}],
        ['deco',{x:1051.13,y:433.4,w:76.475,h:28.515,r:6.317,f:8.598,ls:1.1513,oy:2.318,sb:2.878}],
        ['tp',{x:775.3,y:231,w:299.39,h:138,r:19.2,p:12,g:13.18,wf:25.2,wp:[2,3],sf:37.2,sls:5.4,sw:212.94}]]},
      B:{els:[
        ['photo',{x:656,y:0,w:544,h:628,r:'40px 0 0 40px',img:{l:-235.9,t:0,w:941.9,h:628}}],
        ['tp',{x:707,y:50,w:260.03,h:120.3,r:16.68,p:10.44,g:9.6,wf:21.9,wp:[2,2],sf:37.2,sls:4.692,sw:204.718}],
        ['h',{x:40,y:50,f:82.57,lh:81.566,ls:-1.2235,trim:1,l:H.two}],
        ['s',{x:40,y:231,f:28,lh:33.6,trim:1,l:S.two}],
        ['cta',{x:40,y:325,w:534,h:70.19,f:28,lh:32.2,ls:-.14,l:C.one}],
        ['logo',{x:40,y:543,w:200}]]}},

    {w:960,h:1200,plat:'PMAX',ratio:'4:5',sx:48,sy:60,show:.4,
      A:{blur:3,els:[
        ['arc',{x:-301.5,y:533,d:1563}],
        ['h',{x:119.94,y:89.72,w:761,c:1,f:112,lh:109.67,ls:-1.645,l:H.two}],
        ['s',{x:75.4,y:336.81,w:802,c:1,f:42.2,lh:50.62,l:S.two}],
        ['cta',{x:86.75,y:487.81,w:779.3,h:108.09,f:42.2,lh:48.51,ls:-.211,l:C.one}],
        ['logo',{x:680,y:1091.03,w:220}],
        ['deco',{x:67.32,y:694.17,w:194.59,h:71.8,r:16.1,f:22,ls:2.93,oy:5.9,sb:7.3}],
        ['deco',{x:666.53,y:680.03,w:266,h:98,r:22,f:30,ls:4,oy:8,sb:10}],
        ['deco',{x:8.78,y:923.62,w:266,h:98,r:22,f:30,ls:4,oy:8,sb:10}],
        ['deco',{x:777.41,y:949.6,w:196.19,h:73.19,r:16.2,f:22.1,ls:2.95,oy:5.9,sb:7.4}],
        ['deco',{x:366.78,y:1047.77,w:204.59,h:76.3,r:16.9,f:23.1,ls:3.08,oy:6.2,sb:7.7}],
        ['tp',{x:231,y:763,w:499,h:204,r:32,p:20,g:22,wf:42,wp:[4,4],sf:62,sls:9,sw:355}]]},
      B:{els:[
        ['photo',{x:0,y:-22,w:960,h:582,r:'0 0 43.2px 43.2px',img:{l:0,t:21.94,w:960,h:640.1}}],
        ['h',{x:64,y:648,f:95,lh:92,ls:-1.38,trim:1,l:H.two}],
        ['s',{x:64,y:848,f:36,lh:43.2,trim:1,l:S.two}],
        ['cta',{x:64,y:957,w:621,h:87.09,f:34,lh:39.1,ls:-.17,l:C.one}],
        ['logo',{x:64,y:1084.09,w:220}],
        ['tp',{x:550.29,y:447.77,w:329.07,h:152.23,r:21.112,p:13.212,g:12.149,wf:27.731,wp:[2.476,3.301],sf:47.043,sls:5.9374,sw:259.106}]]}},

    {w:300,h:600,plat:'Programmatic',sx:12,sy:12,show:1,
      A:{blur:1.4,els:[
        ['arc',{x:-110,y:306,d:520}],
        ['h',{x:10,y:43,w:279,c:1,f:53,lh:47.17,ls:-.615,trim:1,l:H.three}],
        ['s',{x:26.5,y:199,w:246,c:1,f:17,lh:20.4,trim:1,l:S.three}],
        ['cta',{x:26.5,y:276,w:246,h:61.09,f:17,lh:19.55,ls:-.085,l:C.two}],
        ['logo',{x:188,y:565.75,w:100}],
        ['deco',{x:12.91,y:367.96,w:89.52,h:33.02,r:7.41,f:10.1,ls:1.348,oy:2.714,sb:3.358}],
        ['deco',{x:190.17,y:378.08,w:104.405,h:38.465,r:10.12,f:13.8,ls:1.84,oy:3.68,sb:4.6}],
        ['deco',{x:-17.98,y:485.27,w:122.36,h:45.08,r:10.12,f:13.8,ls:1.84,oy:3.68,sb:4.6}],
        ['deco',{x:189.95,y:500.84,w:90.25,h:33.67,r:7.45,f:10.2,ls:1.357,oy:2.714,sb:3.404}],
        ['deco',{x:70.09,y:550.27,w:94.11,h:35.09,r:7.77,f:10.6,ls:1.417,oy:2.852,sb:3.542}],
        ['tp',{x:46,y:407,w:208,h:92,r:14.72,p:9.2,g:6.11,wf:19.3,wp:[2,2],sf:28.5,sls:4.14}]]},
      B:{els:[
        ['photo',{x:0,y:0,w:300,h:230,r:'0 0 22px 22px',img:{l:-22.5,t:0,w:345,h:230}}],
        ['h',{x:19,y:314,f:40,lh:40,ls:-.6,trim:1,l:H.two}],
        ['s',{x:19,y:407,f:17,lh:20.4,trim:1,l:S.three}],
        ['cta',{x:19,y:484,w:217.17,h:45.88,f:12.801,lh:14.721,ls:-.064,l:C.two}],
        ['logo',{x:19,y:553.88,w:100}],
        ['tp',{x:101.32,y:189.91,w:173.36,h:80.19,r:11.12,p:6.96,g:6.39,wf:14.6,wp:[1,2],sf:24.8,sls:3.128,sw:136.502}]]}},

    {w:160,h:600,plat:'Programmatic',sx:8,sy:8,show:1,
      A:{blur:.75,els:[
        ['arc',{x:-143,y:297,d:446}],
        ['h',{x:6,y:48,w:148,c:1,f:27.667,lh:27.667,ls:-.415,l:H.threeN}],
        ['s',{x:6,y:147,w:148,c:1,f:14,lh:16.8,trim:1,l:S.four}],
        ['cta',{x:6,y:223,w:148,h:44.31,f:12.442,lh:14.308,ls:-.0622,l:C.two}],
        ['logo',{x:36,y:520,w:88}],
        ['deco',{x:-3.42,y:332.04,w:48.64,h:17.94,r:4.03,f:5.5,ls:.733,oy:1.475,sb:1.825}],
        ['deco',{x:99.38,y:305.51,w:66.5,h:24.5,r:5.5,f:7.5,ls:1,oy:2,sb:2.5}],
        ['deco',{x:-11.9,y:434.41,w:66.5,h:24.5,r:5.5,f:7.5,ls:1,oy:2,sb:2.5}],
        ['deco',{x:104.6,y:429.15,w:49.05,h:18.3,r:4.05,f:5.5,ls:.738,oy:1.475,sb:1.85}],
        ['deco',{x:71.68,y:478.21,w:51.14,h:19.06,r:4.22,f:5.8,ls:.77,oy:1.55,sb:1.925}],
        ['tp',{x:12,y:357,w:135.6,h:62.5,r:8.696,p:5.435,g:5.978,wf:11.413,wp:[1.087,1.087],sf:16.848,sls:2.4457}]]},
      B:{els:[
        ['photo',{x:0,y:-11,w:160,h:232,r:'0 0 16px 16px',img:{l:-94,t:0,w:348,h:232}}],
        ['h',{x:6,y:280,w:146,c:1,f:30,lh:30,ls:-.45,trim:1,l:H.three}],
        ['s',{x:6,y:385,w:146,c:1,f:13,lh:15.6,l:S.four}],
        ['cta',{x:6,y:472,w:146,h:42.68,f:11.931,lh:13.72,ls:-.0597,l:C.two}],
        ['logo',{x:35,y:538.68,w:88}],
        ['tp',{x:33.66,y:194.94,w:112.67,h:52.13,r:7.23,p:4.524,g:4.16,wf:9.5,wp:[1,1],sf:16.1,sls:2.033,sw:88.687}]]}},

    {w:300,h:250,plat:'Programmatic',sx:8,sy:8,show:1,
      A:{blur:.65,els:[
        ['arc',{x:-24,y:125,d:348}],
        ['h',{x:8,y:24,w:283,c:1,f:23,lh:22,ls:-.33,trim:1,l:H.one}],
        ['s',{x:49.5,y:52,w:200,c:1,f:10.5,lh:12.6,trim:1,l:S.two}],
        ['cta',{x:43.5,y:84,w:212,h:30,f:12,lh:13.8,ls:-.06,l:C.one}],
        ['logo',{x:216,y:225.09,w:76}],
        ['deco',{x:55.39,y:146.2,w:42.8,h:15.78,r:3.54,f:4.8,ls:.645,oy:1.298,sb:1.606}],
        ['deco',{x:240.21,y:155.97,w:58.52,h:21.55,r:4.84,f:6.6,ls:.88,oy:1.76,sb:2.2}],
        ['deco',{x:3.97,y:185,w:58.52,h:21.55,r:4.84,f:6.6,ls:.88,oy:1.76,sb:2.2}],
        ['deco',{x:155.41,y:225.05,w:43.16,h:16.09,r:3.56,f:4.9,ls:.649,oy:1.298,sb:1.628}],
        ['tp',{x:95.12,y:154.7,w:109.77,h:50.59,r:7.04,p:4.4,g:3.82,wf:9.2,wp:[1,1],sf:13.6,sls:1.98}]]},
      B:{els:[
        ['photo',{x:0,y:-8,w:300,h:111,r:'0 0 12px 12px',img:{l:0,t:-44.5,w:300,h:200}}],
        ['h',{x:18,y:125,w:263,c:1,f:21,lh:21,ls:-.315,trim:1,l:H.one}],
        ['s',{x:18,y:152,w:263,c:1,f:10,lh:12,trim:1,l:S.two}],
        ['cta',{x:54.5,y:183,w:190,h:25.84,f:10.381,lh:11.939,ls:-.0519,l:C.one}],
        ['logo',{x:115.5,y:220.84,w:68}],
        ['tp',{x:185,y:67,w:91,h:42.09,r:5.84,p:3.654,g:3.36,wf:7.7,wp:[1,1],sf:13,sls:1.642,sw:71.658}]]}},

    {w:728,h:90,plat:'Programmatic',sx:6,sy:6,show:1,
      A:{blur:.5,els:[
        ['arc',{x:360,y:12,d:181}],
        ['logo',{x:18,y:36,w:78}],
        ['h',{x:115,y:17.35,f:35.156,lh:30.508,ls:-.5273,trim:1,l:H.row}],
        ['tp',{x:410.43,y:18.51,w:99.57,h:46.05,r:6.388,p:3.998,g:4.657,wf:10.57,wp:[0,1.532],sf:13.589,sls:1.7113,sw:74.606}],
        ['cta',{x:563,y:23,w:146,h:42.68,f:11.931,lh:13.72,ls:-.0597,l:C.two}],
        ['deco',{x:372.01,y:29.51,w:31.13,h:11.48,r:2.58,f:3.5,ls:.469,oy:.944,sb:1.168}],
        ['deco',{x:358.7,y:64.18,w:42.55,h:15.67,r:3.52,f:4.8,ls:.64,oy:1.28,sb:1.6}],
        ['deco',{x:516.08,y:69.61,w:32.73,h:12.2,r:2.7,f:3.7,ls:.493,oy:.992,sb:1.232}]]},
      B:{els:[
        ['logo',{x:18,y:36,w:78}],
        ['h',{x:115,y:16,f:36.875,lh:32,ls:-.5531,trim:1,l:H.row}],
        ['photo',{x:373,y:-53,w:180,h:130.5,r:'0 0 20.25px 20.25px',img:{l:0,t:16.63,w:180,h:120.02}}],
        ['tp',{x:351,y:51,w:65,h:30.06,r:4.17,p:2.61,g:3.04,wf:6.9,wp:[0,1],sf:8.871,sls:1.1172,sw:48.704}],
        ['cta',{x:563,y:23,w:146,h:42.68,f:11.931,lh:13.72,ls:-.0597,l:C.two}]]}},

    {w:320,h:50,plat:'Programmatic',sx:4,sy:4,show:1,
      A:{blur:.2,els:[
        ['arc',{x:158.24,y:10.27,d:79.56}],
        ['logo',{x:7.91,y:20.82,w:34.286}],
        ['h',{x:50.55,y:12.63,f:15.453,lh:13.41,ls:-.2318,trim:1,l:H.row}],
        ['tp',{x:180.41,y:13.13,w:43.77,h:20.24,r:2.808,p:1.757,g:2.047,wf:4.646,wp:[0,.673],sf:5.973,sls:.7522,sw:32.794}],
        ['cta',{x:247.47,y:15.11,w:64.18,h:19.45,f:5.244,lh:6.031,ls:-.0262,l:C.two}],
        ['deco',{x:163.52,y:17.97,w:13.684,h:5.046,r:1.134,f:1.538,ls:.2062,oy:.415,sb:.513}],
        ['deco',{x:157.67,y:33.21,w:18.703,h:6.888,r:1.547,f:2.11,ls:.2813,oy:.563,sb:.703}],
        ['deco',{x:226.85,y:35.6,w:14.387,h:5.363,r:1.187,f:1.626,ls:.2167,oy:.436,sb:.542}]]},
      B:{els:[
        ['logo',{x:7.91,y:20.82,w:34.286}],
        ['h',{x:50.55,y:12.03,f:16.209,lh:14.066,ls:-.2431,trim:1,l:H.row}],
        ['photo',{x:163.96,y:-18.3,w:79.12,h:57.36,r:'0 0 8.9px 8.9px',img:{l:.13,t:3.33,w:89.97,h:59.98}}],
        ['tp',{x:156,y:20.78,w:42.92,h:19.85,r:2.754,p:1.723,g:2.007,wf:4.556,wp:[0,.66],sf:5.858,sls:.7377,sw:32.161}],
        ['cta',{x:247.47,y:15.11,w:64.18,h:19.45,f:5.244,lh:6.031,ls:-.0262,l:C.two}]]}}
  ];

  /* ---- helpers ---- */
  function el(tag,cls,css){ var e=document.createElement(tag); if(cls) e.className=cls; if(css) e.style.cssText=css; return e; }
  function mark(e,name){ e.dataset.el=name; return e; }
  function px(n){ return (+n.toFixed(3))+'px'; }
  /* Figma's cap-to-baseline trim: distance from the top of a CSS line box to the cap
     top of its first line, from the loaded font's real metrics */
  var CV=document.createElement('canvas').getContext('2d');
  function capTop(f,lh,wt){
    CV.font=(wt||400)+' 100px "Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif';
    var m=CV.measureText('H'), A=m.fontBoundingBoxAscent/100, D=m.fontBoundingBoxDescent/100, cap=m.actualBoundingBoxAscent/100;
    return (lh-(A+D)*f)/2+(A-cap)*f;
  }
  /* Figma draws the star row with a ★ glyph 0.932em wide (every star text node:
     width = 5 x (0.932em + tracking)); Chrome falls back to a narrower system ★, so the
     star size is scaled until one glyph has Figma's advance */
  function starPx(f){
    CV.font='300 100px "Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif';
    var adv=CV.measureText('★').width/100;
    return adv>0?f*.932/adv:f;
  }
  function lines(cls,o,wt){
    var p=el('p',cls+(o.c?'':' k22-left'),'font-size:'+px(o.f)+';line-height:'+px(o.lh)+(o.ls?';letter-spacing:'+px(o.ls):'')+
      ';left:'+px(o.x)+';top:'+px(o.trim?o.y-capTop(o.f,o.lh,wt):o.y)+(o.w?';width:'+px(o.w):''));
    o.l.forEach(function(t){ var s=el('span'); s.textContent=t; p.appendChild(s); });
    return p;
  }
  function logo(o){
    var s=document.createElementNS('http://www.w3.org/2000/svg','svg');
    s.setAttribute('class','k22-logo'); s.setAttribute('viewBox','0 0 521 116'); s.setAttribute('role','img'); s.setAttribute('aria-label','Katapult');
    s.style.cssText='left:'+px(o.x)+';top:'+px(o.y)+';width:'+px(o.w);
    var u=document.createElementNS('http://www.w3.org/2000/svg','use'); u.setAttribute('href','#k-logo'); s.appendChild(u);
    return mark(s,'logo');
  }
  function cta(o){
    var b=el('span','k22-cta','left:'+px(o.x)+';top:'+px(o.y)+';width:'+px(o.w)+';height:'+px(o.h)+';font-size:'+px(o.f)+';line-height:'+px(o.lh)+';letter-spacing:'+px(o.ls));
    o.l.forEach(function(t){ var s=el('span'); s.textContent=t; b.appendChild(s); });
    return mark(b,'cta');
  }
  /* the one trust element: wordmark + stars on a white card with the brand's flat cream
     plate, no quote, no invented TrustScore or review count */
  function badge(o){
    var b=el('div','k22-tp','left:'+px(o.x)+';top:'+px(o.y)+';width:'+px(o.w)+';height:'+px(o.h)+';gap:'+px(o.g)+';border-radius:'+px(o.r)+';box-shadow:'+px(o.p)+' '+px(o.p)+' 0 #D4A574');
    var wd=el('span','k22-tp-word','font-size:'+px(o.wf)+';padding:'+px(o.wp[0])+' 0 '+px(o.wp[1])); wd.textContent='Trustpilot';
    var st=el('span','k22-tp-stars','font-size:'+px(starPx(o.sf))+';line-height:'+px(o.sf)+';letter-spacing:'+px(o.sls)+(o.sw?';min-width:'+px(o.sw):'')); st.textContent='★★★★★';
    b.appendChild(wd); b.appendChild(st);
    return mark(b,'badge');
  }
  /* decorative only: a straight white card with a mini star row and no quote text, under
     the same light frame-wide blur Figma gives all of them, so none reads as a legible
     (and therefore fabricated) testimonial */
  function deco(o,blur){
    var b=el('div','k22-deco','left:'+px(o.x)+';top:'+px(o.y)+';width:'+px(o.w)+';height:'+px(o.h)+';border-radius:'+px(o.r)+
      ';filter:blur('+px(blur)+') drop-shadow(0 '+px(o.oy)+' '+px(o.sb)+' rgba(0,0,0,.18))');
    var st=el('span','k22-deco-stars','font-size:'+px(starPx(o.f))+';line-height:'+px(o.f)+';letter-spacing:'+px(o.ls)); st.textContent='★★★★★';
    b.appendChild(st);
    return mark(b,'deco');
  }
  function photo(o){
    var b=el('div','k22-pic','left:'+px(o.x)+';top:'+px(o.y)+';width:'+px(o.w)+';height:'+px(o.h)+';border-radius:'+o.r);
    var i=el('img','','left:'+px(o.img.l)+';top:'+px(o.img.t)+';width:'+px(o.img.w)+';height:'+px(o.img.h));
    i.alt='Smiling woman writing at a desk with her laptop by a bright window';
    if(K22_PHOTO.src) i.src=K22_PHOTO.src;
    b.appendChild(i);
    return mark(b,'photo');
  }

  function canvas(sz,v){
    var k=el('div','k22','width:'+sz.w+'px;height:'+sz.h+'px;--sx:'+sz.sx+'px;--sy:'+sz.sy+'px;--ow:'+Math.max(1,Math.round(sz.w/400))+'px'), F=sz[v];
    F.els.forEach(function(e){
      var t=e[0], o=e[1], n;
      if(t==='arc') n=mark(el('div','k22-arc','left:'+px(o.x)+';top:'+px(o.y)+';width:'+px(o.d)+';height:'+px(o.d)),'arc');
      else if(t==='h') n=mark(lines('k22-h',o,500),'headline');
      else if(t==='s') n=mark(lines('k22-s2',o,400),'subhead');
      else if(t==='cta') n=cta(o);
      else if(t==='logo') n=logo(o);
      else if(t==='deco') n=deco(o,F.blur);
      else if(t==='tp') n=badge(o);
      else if(t==='photo') n=photo(o);
      k.appendChild(n);
    });
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
      FRAMES.filter(function(s){return s.plat===pl;}).forEach(function(sz){
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
  /* re-render once the brand fonts are in, so the cap-trim offsets use real metrics */
  var fl=document.fonts?Promise.all(['400','500','700'].map(function(w){return document.fonts.load(w+' 20px "Aktiv Grotesk"');})).catch(function(){}):Promise.resolve();
  render(); fl.then(render);
  function applySafe(){ root.classList.toggle('k22-safe-on',safe.checked); }
  safe.addEventListener('change',applySafe); applySafe();
})();
