// Katapult November reels: shared timeline helpers. Every frame is a pure function of t (s),
// so HyperFrames can render frames in any order. Pattern from RKU26012 (roku/03-work/ads).
const $ = id => document.getElementById(id);
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const io = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const out = p => 1 - Math.pow(1 - p, 3);
const out5 = p => 1 - Math.pow(1 - p, 5);
const inq = p => p * p * p;
const back = (p, c = 1.6) => p <= 0 ? 0 : p >= 1 ? 1 : 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2);
const mix = (a, b, p) => a + (b - a) * p;
const set = (el, o, tf) => { if (typeof el === "string") el = $(el); el.style.opacity = o; if (tf !== undefined) el.style.transform = tf; };

// rise in: opacity + translateY from dist to 0 over d seconds starting at a
function rise(id, t, a, d = .5, dist = 50, k = 1) {
  const p = out(lin(t, a, a + d));
  set(id, p * k, `translateY(${(1 - p) * dist}px)`);
  return p;
}
// pop in with a little overshoot
function pop(id, t, a, d = .45, s0 = .6) {
  const p = lin(t, a, a + d);
  set(id, clamp(p * 3), `scale(${mix(s0, 1, back(p))})`);
  return p;
}
// button press dip
function press(t, c, d = .24) { const p = lin(t, c, c + d); return p <= 0 || p >= 1 ? 1 : 1 - .07 * Math.sin(Math.PI * p); }

// Pink line accent: solid stroke drawn on from the frame edge, then the dots pop in one by one.
// Element ids: <id>-l (path), <id>-d0..n (dots). Built in anim.py accent().
function accent(id, t, a, d = .7, k = 1) {
  const l = $(id + "-l"), len = parseFloat(l.dataset.len), p = io(lin(t, a, a + d));
  l.style.strokeDashoffset = len * (1 - p);
  l.style.opacity = k;
  const n = parseInt(l.dataset.n);
  for (let i = 0; i < n; i++) {
    const q = out(lin(t, a + d * .85 + i * .05, a + d * .85 + i * .05 + .22));
    const dot = $(id + "-d" + i);
    dot.setAttribute("r", (dot.dataset.r * q).toFixed(2));
    dot.style.opacity = k;
  }
}

// touch indicator on a path of keyframes [t, x, y]; arcs a little like a finger
function touchAt(kf, t) {
  if (t <= kf[0][0]) return [kf[0][1], kf[0][2]];
  for (let i = 1; i < kf.length; i++) {
    if (t <= kf[i][0]) {
      const [t0, x0, y0] = kf[i - 1], [t1, x1, y1] = kf[i];
      const p = io(lin(t, t0, t1)), arc = Math.sin(Math.PI * p) * Math.hypot(x1 - x0, y1 - y0) * .12;
      return [mix(x0, x1, p) + arc * .5, mix(y0, y1, p) - arc];
    }
  }
  const k = kf[kf.length - 1];
  return [k[1], k[2]];
}
function touch(t, kf, taps, vis) {
  const el = $("touch"), ring = $("ring");
  if (vis <= 0) { el.style.opacity = 0; ring.style.opacity = 0; return; }
  const [x, y] = touchAt(kf, t);
  const tap = taps.find(c => t >= c - .06 && t < c + .16);
  el.style.opacity = vis;
  el.style.transform = `translate(${x - 34}px,${y - 34}px) scale(${tap !== undefined ? .82 : 1})`;
  const lc = taps.filter(c => t >= c && t < c + .5).pop();
  if (lc !== undefined) {
    const p = out(lin(t, lc, lc + .5)), r = 34 + 60 * p;
    ring.style.transform = `translate(${x - r}px,${y - r}px)`;
    ring.style.width = ring.style.height = 2 * r + "px";
    ring.style.opacity = vis * (1 - p);
  } else ring.style.opacity = 0;
}

function boot(seek) {
  window.seek = seek;
  window.ready = Promise.all([document.fonts.ready, ...[...document.images].map(i => i.decode().catch(() => 0))]);
  // HyperFrames: a paused GSAP timeline the renderer seeks frame by frame; its proxy tween calls seek(t).
  if (window.gsap) {
    const proxy = { t: 0 };
    const tl = gsap.timeline({ paused: true });
    tl.to(proxy, { t: CFG.dur, duration: CFG.dur, ease: "none", modifiers: { t: v => { seek(parseFloat(v)); return v; } } }, 0);
    window.__timelines = window.__timelines || {};
    window.__timelines[CFG.comp] = tl;
  }
  window.addEventListener("hf-seek", e => seek(e.detail.time));
  seek(parseFloat(new URLSearchParams(location.search).get("t") || "0"));
}
