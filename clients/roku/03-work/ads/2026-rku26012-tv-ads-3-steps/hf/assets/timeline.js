// RKU26012 timeline: seek(t) sets every element for time t (s). Pure function of t, so frames
// can be rendered in any order. Layout numbers come from CFG (anim.py SIZES).
const $ = id => document.getElementById(id);
const C = CFG, K = C.k, W = C.W, H = C.H;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const io = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const out = p => 1 - Math.pow(1 - p, 3);
const back = p => { const c = 1.7; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
const mix = (a, b, p) => a + (b - a) * p;
const set = (el, o, tf) => { el.style.opacity = o; if (tf !== undefined) el.style.transform = tf; };

// beats
const T = {
  introOut: [2.05, 2.45], stepIn: [2.4, 2.95], cardIn: [2.5, 3.1],
  x01: [5.75, 6.25], x12: [10.55, 11.05], exit: [14.55, 14.95],
  tv: [15.0, 17.75], cta: 17.4, end: 20,
};
const CARD_H = [560, 830, 790];
const BUDGET = { keys: [3.95, 4.1, 4.25, 4.4], v: ["5", "50", "500", "5,000"], focus: [3.68, 5.45] };
const ZIP = { keys: [9.1, 9.23, 9.36, 9.49, 9.62], v: ["9", "90", "902", "9021", "90210"], focus: [8.92, 10.38] };
const MENU = { open: [7.0, 7.18], close: [7.66, 7.75], pick: 7.62 };
const AGE = 8.32, UP = 11.68, PROG = [11.8, 13.2], LAUNCH = 13.9, CTA_CLICK = 18.85;
const PRESS = { "b-next0": 5.45, "b-next1": 10.38, "b-up": UP, "b-launch": LAUNCH };

function step(t) { return t < T.x01[1] ? 0 : t < T.x12[1] ? 1 : 2; }
function cardH(t) {
  const a = io(lin(t, ...T.x01)), b = io(lin(t, ...T.x12));
  return mix(mix(CARD_H[0], CARD_H[1], a), CARD_H[2], b);
}
function cardBox(t) {
  const h = cardH(t) * K;
  let y = C.anchor === "center" ? C.cy - h / 2 : C.top;
  if (C.anchor === "group") {                 // copy + card centred in the safe area, copy rides on the card
    const G = C.top - C.pillY, mid = (C.safe[0] + H - C.safe[1]) / 2;
    y = Math.max(C.minTop, mid - (G + h) / 2) + G;
  }
  return { x: C.cardX, y, h };
}

// cursor keyframes: [t, kind, a, b]. card = card px; stage = stage px; el = element centre; hold = stay
const KF = [
  [3.0, "stage", W * .96, H * 1.04], [3.6, "card", 470, 334], [4.7, "hold"], [5.35, "card", 702, 477],
  [6.35, "hold"], [6.95, "card", 470, 304], [7.18, "hold"], [7.55, "card", 300, 456], [7.8, "hold"],
  [8.25, "card", 430, 470], [8.4, "hold"], [8.85, "card", 470, 626], [9.75, "hold"], [10.3, "card", 702, 751],
  [11.1, "hold"], [11.6, "card", 380, 413], [13.25, "hold"], [13.8, "card", 642, 707], [20, "hold"],
];
const KF2 = [[18.05, "stage", W * .9, H * 1.06], [18.75, "el", "ctab"], [20, "hold"]];
const CLICKS = [3.68, 5.45, 7.0, MENU.pick, AGE, 8.92, 10.38, UP, LAUNCH, CTA_CLICK];

function resolve(list) {
  const pts = [];
  for (const k of list) {
    if (k[1] === "hold") { pts.push([k[0], ...pts[pts.length - 1].slice(1)]); continue; }
    if (k[1] === "stage") { pts.push([k[0], k[2], k[3]]); continue; }
    if (k[1] === "card") { const b = cardBox(k[0]); pts.push([k[0], b.x + k[2] * K, b.y + k[3] * K]); continue; }
    pts.push([k[0], null, null, k[2]]);
  }
  return pts;
}
let P1 = null, P2 = null;
function elCenter(id) {
  const r = $(id).getBoundingClientRect(), s = $("st").getBoundingClientRect();
  return [r.left - s.left + r.width * .62, r.top - s.top + r.height * .62];
}
function cursorAt(pts, t) {
  if (t <= pts[0][0]) return pts[0].slice(1, 3);
  for (let i = 1; i < pts.length; i++) {
    if (t <= pts[i][0]) {
      const [t0, x0, y0] = pts[i - 1], [t1, x1, y1] = pts[i];
      const p = io(lin(t, t0, t1)), arc = Math.sin(Math.PI * p) * Math.hypot(x1 - x0, y1 - y0) * .1;
      return [mix(x0, x1, p) + arc * .6, mix(y0, y1, p) - arc];
    }
  }
  return pts[pts.length - 1].slice(1, 3);
}

function typed(spec, t) { let v = ""; spec.keys.forEach((k, i) => { if (t >= k) v = spec.v[i]; }); return v; }
function caret(spec, t) {
  if (t < spec.focus[0] || t >= spec.focus[1]) return 0;
  const last = Math.max(spec.focus[0], ...spec.keys.filter(k => k <= t));
  return (t - last < .5 || Math.floor((t - last) * 2.4) % 2 === 0) ? 1 : 0;
}
function press(t, c) { const p = lin(t, c, c + .26); return p <= 0 || p >= 1 ? 1 : 1 - .07 * Math.sin(Math.PI * p); }

function seek(t) {
  // background drift
  $("city").style.transform = `translateX(${-(C.cw - W) * lin(t, 0, T.end)}px)`;
  $("glow").style.transform = `translate(${W * mix(.45, .62, lin(t, 0, 20)) - parseFloat(getComputedStyle($("glow")).width) / 2}px,${H * -.25}px)`;
  // Roku City blimp: slow drift across its lane, gentle bob and pitch
  const B = C.blimp, bp = lin(t, 0, T.end);
  $("blimp").style.transform = `translate(${mix(B[0], B[1], bp)}px,${B[2] + Math.sin(t * .9) * 7}px) rotate(${Math.sin(t * .6) * 1.4}deg)`;
  $("glow2").style.transform = `translate(${W * mix(-.25, -.12, lin(t, 0, 20))}px,${H * .45}px)`;

  // intro
  const io_ = lin(t, ...T.introOut);
  $("intro").style.opacity = t < T.introOut[1] ? 1 : 0;
  const rise = (el, a, d = .5, dist = 40) => { const p = out(lin(t, a, a + d)); set($(el), p * (1 - io_), `translateY(${(1 - p) * dist - io_ * 40}px)`); };
  rise("ilk", .1); rise("ih0", .25, .55, 60); rise("ih1", .45, .55, 60);
  [1.0, 1.18, 1.36].forEach((a, i) => { const p = back(lin(t, a, a + .42)); set($("chip" + i), clamp(lin(t, a, a + .2)) * (1 - io_), `scale(${mix(.8, 1, p)})`); });

  // steps
  const showSteps = t >= T.stepIn[0] && t < T.tv[0];
  $("steps").style.opacity = showSteps ? 1 : 0;
  const ex = lin(t, ...T.exit);
  const sIn = out(lin(t, ...T.stepIn));
  set($("slk"), sIn * (1 - ex));
  const s = step(t);
  for (let i = 0; i < 3; i++) {
    let o = 0, dy = 0;
    const xin = i === 1 ? T.x01 : i === 2 ? T.x12 : null, xout = i === 0 ? T.x01 : i === 1 ? T.x12 : null;
    if (i === 0) { o = sIn; dy = (1 - sIn) * 40; }
    if (xin) { const p = out(lin(t, (xin[0] + xin[1]) / 2, xin[1] + .1)); o = p; dy = (1 - p) * 40; }
    if (xout && t > xout[0]) { const p = io(lin(t, xout[0], (xout[0] + xout[1]) / 2)); o = 1 - p; dy = -p * 40; }
    o *= 1 - ex;
    const off = cardBox(t).y - C.top;
    set($("pill" + i), o, `translateY(${dy + off}px)`);
    set($("hl" + i), o, `translateY(${dy * 1.4 + off}px)`);
  }

  // card
  const b = cardBox(t), ci = out(lin(t, ...T.cardIn));
  const card = $("card");
  card.style.height = cardH(t) + "px";
  card.style.opacity = ci * (1 - ex);
  card.style.transform = `translate(${b.x}px,${b.y + (1 - ci) * 70 * K}px) scale(${K * mix(.94, 1, ci) * mix(1, 1.05, io(ex))})`;
  for (let i = 0; i < 3; i++) {
    const pn = $("pane" + i);
    let o = 0, dx = 0;
    if (i === 0) o = 1;
    const xin = i === 1 ? T.x01 : i === 2 ? T.x12 : null, xout = i === 0 ? T.x01 : i === 1 ? T.x12 : null;
    if (xin) { const p = out(lin(t, (xin[0] + xin[1]) / 2 - .05, xin[1])); o = p; dx = (1 - p) * 70; }
    if (xout && t > xout[0]) { const p = io(lin(t, xout[0], (xout[0] + xout[1]) / 2)); o = 1 - p; dx = -p * 70; }
    set(pn, o, `translateX(${dx}px)`);
    pn.style.visibility = o > 0 ? "visible" : "hidden";
    const st = $("si" + i), n = $("sn" + i);
    st.className = "it" + (i === s ? " on" : i < s ? " done" : "");
    n.innerHTML = i < s ? '<svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>' : String(i + 1);
  }
  const fill = mix(mix(1, 2, io(lin(t, ...T.x01))), 3, io(lin(t, ...T.x12))) / 3;
  $("sfi").style.width = 764 * mix(fill, 1, out(lin(t, PROG[1], PROG[1] + .4))) * (fill < 1 ? 1 : 1) + "px";

  // step 1: budget
  const bv = typed(BUDGET, t);
  $("v-budget").innerHTML = bv || '<span class="ph">0</span>';
  $("c-budget").style.opacity = caret(BUDGET, t);
  $("f-budget").className = "fld" + (t >= BUDGET.focus[0] && t < BUDGET.focus[1] ? " focus" : "");

  // step 2: audience
  const mOpen = out(lin(t, ...MENU.open)) * (1 - lin(t, ...MENU.close));
  const menu = $("menu");
  set(menu, t < MENU.close[0] ? mOpen : mOpen * mOpen, `scaleY(${mix(t < MENU.close[0] ? .85 : .4, 1, mOpen)})`);
  menu.style.visibility = mOpen > 0 ? "visible" : "hidden";
  $("int-chev").style.transform = `rotate(${180 * mOpen}deg)`;
  $("f-int").className = "fld" + (mOpen > 0 ? " focus" : "");
  $("v-int").innerHTML = t >= MENU.pick ? "Home &amp; Garden" : '<span class="ph">Select interests</span>';
  const cur = P1 ? cursorAt(P1, t) : [0, 0];
  const cy = (cur[1] - b.y) / K, hov = Math.floor((cy - 364) / 62);
  for (let i = 0; i < 5; i++) $("mo" + i).className = "o" + (i === hov && t > 7.25 && t < MENU.close[0] ? " hov" : "");
  for (let i = 0; i < 3; i++) {
    const sel = i === 1 && t >= AGE;
    $("age" + i).className = "p" + (sel ? " sel" : "");
    $("age" + i).style.transform = sel ? `scale(${mix(1.08, 1, out(lin(t, AGE, AGE + .25)))})` : "";
  }
  $("v-zip").innerHTML = typed(ZIP, t) || '<span class="ph" style="font-weight:500">00000</span>';
  $("c-zip").style.opacity = caret(ZIP, t);
  $("f-zip").className = "fld" + (t >= ZIP.focus[0] && t < ZIP.focus[1] ? " focus" : "");

  // step 3: upload
  const fr = out(lin(t, UP + .07, UP + .35));
  set($("frow"), fr, `translateY(${(1 - fr) * 16}px)`); set($("bar"), fr);
  const pr = io(lin(t, ...PROG));
  $("bar-i").style.width = pr * 100 + "%";
  $("v-pc").textContent = Math.round(pr * 100) + "%";
  const ok = back(lin(t, PROG[1], PROG[1] + .35));
  set($("okc"), clamp(lin(t, PROG[1], PROG[1] + .1)), `scale(${ok})`);
  $("v-pc").style.display = t >= PROG[1] ? "inline" : "inline";
  for (const [id, c] of Object.entries(PRESS)) $(id).style.transform = `scale(${press(t, c)})`;
  const lg = lin(t, LAUNCH, LAUNCH + .3);
  $("b-launch").style.filter = `brightness(${1 + .25 * lg})`;

  // tv
  const tvOn = t >= T.tv[0] && t < T.end + 1;
  const tvFade = 1 - lin(t, T.cta, T.cta + .35);
  $("tv").style.opacity = tvOn ? tvFade : 0;
  if (tvOn) {
    const R = C.room, [x0, y0, x1, y1] = R.screen, s0 = Math.max(W, H) / R.size;
    const z0 = W * 1.02 / ((x1 - x0) * s0);
    const z = mix(z0, 1, io(lin(t, T.tv[0] + .35, T.cta + .1)));
    const sc = s0 * z, vw = W / sc, vh = H / sc;
    const fx = clamp((x0 + x1) / 2 - vw / 2, 0, R.size - vw), fy = clamp((y0 + y1) / 2 - vh / 2, 0, R.size - vh);
    $("world").style.transform = `scale(${sc}) translate(${-fx}px,${-fy}px)`;
    $("tvpg").style.width = mix(18, 46, lin(t, T.tv[0], T.cta + .4)) + "%";
  }
  const fl = t < T.tv[0] ? lin(t, T.exit[0] + .15, T.tv[0]) * .92 : (1 - lin(t, T.tv[0], T.tv[0] + .4)) * .92;
  $("flash").style.opacity = fl;

  // cta
  const cOn = t >= T.cta;
  $("cta").style.opacity = cOn ? 1 : 0;
  const rc = (el, a, d = .5, dist = 40) => { const p = out(lin(t, a, a + d)); set($(el), p, `translateY(${(1 - p) * dist}px)`); };
  rc("clk", 17.6); rc("chl", 17.72, .55, 60);
  const cp = back(lin(t, 18.0, 18.4));
  set($("ctab"), clamp(lin(t, 18.0, 18.15)), `scale(${mix(.8, 1, cp) * press(t, CTA_CLICK)})`);

  // cursor
  if (!P1) P1 = resolve(KF);
  if (!P2) P2 = resolve(KF2).map(p => p[3] ? [p[0], ...elCenter(p[3])] : p);
  let pos = null, cv = 0;
  if (t >= 3.0 && t < T.exit[1]) { pos = cursorAt(P1, t); cv = lin(t, 3.0, 3.15) * (1 - lin(t, T.exit[0], T.exit[0] + .2)); }
  if (t >= KF2[0][0] && P2) { pos = cursorAt(P2, t); cv = 1; }
  const curEl = $("cur");
  if (pos) {
    const cl = CLICKS.find(c => t >= c && t < c + .14);
    curEl.style.transform = `translate(${pos[0] - 4}px,${pos[1] - 3}px) scale(${cl ? .86 : 1})`;
  }
  curEl.style.opacity = pos ? cv : 0;
  const ring = $("ring"), lc = CLICKS.filter(c => t >= c && t < c + .45).pop();
  if (lc !== undefined && pos) {
    const p = out(lin(t, lc, lc + .45)), r = 64 * K * p;
    ring.style.left = pos[0] - r + "px"; ring.style.top = pos[1] - r + "px";
    ring.style.width = ring.style.height = 2 * r + "px"; ring.style.opacity = .9 * (1 - p);
  } else ring.style.opacity = 0;
}

window.seek = seek;
window.ready = Promise.all([document.fonts.ready, ...[...document.images].map(i => i.decode().catch(() => 0))]);

// HyperFrames: a paused 20 s GSAP timeline the renderer seeks frame by frame; every render of
// its proxy tween calls seek(t), so the whole frame is still this one pure function of t.
if (window.gsap) {
  const proxy = { t: 0 };
  const tl = gsap.timeline({ paused: true });
  tl.to(proxy, { t: C.dur, duration: C.dur, ease: "none", modifiers: { t: v => { seek(parseFloat(v)); return v; } } }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines[C.comp] = tl;
}
window.addEventListener("hf-seek", e => seek(e.detail.time));
seek(parseFloat(new URLSearchParams(location.search).get("t") || "0"));
