// 07 Katapult at checkout (15 s). Beats in T; anim.py builds the elements.
const T = {
  wipe1: [2.5, 3.05], phoneIn: [2.8, 3.45], x12: [5.35, 5.85], x23: [9.0, 9.5], wipe2: [12.0, 12.55], end: 15,
};
const TAP = { opt: 4.2, contA: 5.1, field: 6.15, contB: 8.75, chk: 10.0, place: 10.5 };
const MOBILE = { a: 6.35, dt: .085 }, CODE = { a: 7.5, dt: .08 }, VERIFIED = 8.1;
// touch path (stage px): screen origin is (288, 618)
const KF = [
  [3.55, 760, 1560], [4.1, 700, 1372], [4.5, 700, 1372], [4.95, 560, 1520], [5.45, 560, 1520], [6.05, 560, 1014],
  [7.3, 560, 1014], [7.7, 700, 1200], [8.3, 700, 1200], [8.68, 560, 1520], [9.55, 560, 1520], [9.95, 342, 1332],
  [10.08, 342, 1332], [10.45, 560, 1520],
];
const TAPS = Object.values(TAP);

function swapX(t, x, aId, bId) {           // screen a slides out left, b slides in from right
  const p = io(lin(t, x[0], x[1]));
  if (aId) { set(aId, 1, `translateX(${-504 * p}px)`); $(aId).style.visibility = p < 1 ? "visible" : "hidden"; }
  if (bId) { set(bId, 1, `translateX(${504 * (1 - p)}px)`); $(bId).style.visibility = p > 0 ? "visible" : "hidden"; }
}

function cluster(p, t, a) {                // shapes pop, cutouts rise onto them
  for (let i = 0; i < 3; i++) {
    const q = lin(t, a + i * .1, a + .5 + i * .1);
    set(p + "s" + i, clamp(q * 3), `rotate(${i === 0 ? -5 : 0}deg) scale(${mix(.5, 1, back(q))})`);
    const r = out(lin(t, a + .17 + i * .1, a + .67 + i * .1));
    set(p + "p" + i, r, `translateY(${(1 - r) * 90}px)`);
  }
}

function seek(t) {
  // ---- cover (Dark Blue panel, wipes up)
  const w1 = io(lin(t, ...T.wipe1));
  $("dk1").style.transform = `translateY(${-1920 * w1}px)`;
  $("dk1").style.visibility = w1 < 1 ? "visible" : "hidden";
  rise("lg1", t, .1, .5, 40);
  rise("ch0", t, .25, .55, 70); rise("ch1", t, .38, .55, 70); rise("ch2", t, .51, .55, 70);
  rise("csub", t, .8, .5, 40);
  cluster("c", t, .95);
  accent("acc1", t, 1.05, .8);

  // ---- step stage
  const ph = out(lin(t, ...T.phoneIn));
  $("phone").style.transform = `translateY(${(1 - ph) * 300}px)`;
  accent("acc2", t, 3.05, .8);
  pop("sn", t, 2.95, .45, .5);
  $("sn").style.overflow = "hidden";
  const step = t < (T.x12[0] + T.x12[1]) / 2 ? 0 : t < (T.x23[0] + T.x23[1]) / 2 ? 1 : 2;
  for (let i = 0; i < 3; i++) {
    // numeral in the disc: old slides up, new slides in from below
    const xin = i === 1 ? T.x12 : i === 2 ? T.x23 : null, xout = i === 0 ? T.x12 : i === 1 ? T.x23 : null;
    let o = i === 0 ? 1 : 0, dy = 0;
    if (xin) { const p = io(lin(t, xin[0] + .1, xin[0] + .45)); o = p; dy = (1 - p) * 76; }
    if (xout && t > xout[0] + .1) { const p = io(lin(t, xout[0] + .1, xout[0] + .45)); o = 1 - p; dy = -p * 76; }
    set("sn" + i, o, `translateY(${dy}px)`);
    // headline
    let ho = 0, hy = 0;
    if (i === 0) { const p = out(lin(t, 3.0, 3.55)); ho = p; hy = (1 - p) * 60; }
    if (xin) { const p = out(lin(t, xin[0] + .22, xin[0] + .72)); ho = p; hy = (1 - p) * 60; }
    if (xout && t > xout[0]) { const p = io(lin(t, xout[0], xout[0] + .28)); ho *= 1 - p; hy -= p * 40; }
    set("sh" + i, ho, `translateY(${hy}px)`);
  }

  // screens
  if (t < T.x12[0]) { swapX(t, T.x12, "scrA", "scrB"); $("scrC").style.visibility = "hidden"; }
  else if (t < T.x23[0]) { swapX(t, T.x12, "scrA", "scrB"); $("scrC").style.visibility = "hidden"; }
  else { $("scrA").style.visibility = "hidden"; swapX(t, T.x23, "scrB", "scrC"); }

  // A: pick Katapult, Continue
  const sel = t >= TAP.opt;
  $("o2").className = "opt" + (sel ? " sel" : "");
  $("o2r").style.transform = `scale(${sel ? back(lin(t, TAP.opt, TAP.opt + .3)) : 0})`;
  $("o2").style.transform = `scale(${press(t, TAP.opt)})`;
  $("bA").className = "btn" + (t >= TAP.opt + .2 ? " on" : "");
  $("bA").style.transform = `scale(${press(t, TAP.contA)})`;

  // B: mobile number (masked), code autofill, verified
  const fFocus = t >= TAP.field && t < CODE.a;
  $("fM").className = "fld" + (fFocus ? " focus" : "");
  let last = -1;
  for (let i = 0; i < 10; i++) {
    const a = MOBILE.a + i * MOBILE.dt, d = $("md" + i);
    d.style.visibility = t >= a ? "visible" : "hidden";
    d.style.transform = `scale(${back(lin(t, a, a + .15))})`;
    if (t >= a) last = i;
  }
  const cM = $("cM");
  cM.style.left = (last < 0 ? 28 : 28 + $("md" + last).offsetLeft + 26) + "px";
  const sinceKey = t - (last < 0 ? TAP.field : MOBILE.a + last * MOBILE.dt);
  cM.style.opacity = fFocus && (sinceKey < .45 || Math.floor(sinceKey * 2.4) % 2 === 0) ? 1 : 0;
  for (let i = 0; i < 6; i++) {
    const a = CODE.a + i * CODE.dt;
    $("cb" + i).className = "box" + (t >= a - CODE.dt && t < a ? " focus" : "");
    $("cd" + i).style.transform = `scale(${back(lin(t, a, a + .15))})`;
  }
  pop("vok", t, VERIFIED, .4, .3);
  $("bB").className = "btn" + (t >= VERIFIED + .1 ? " on" : "");
  $("bB").style.transform = `scale(${press(t, TAP.contB)})`;

  // C: review, agree, Place order, success
  for (let i = 0; i < 6; i++) {
    const a = T.x23[0] + .35 + i * .06;
    $("sq" + i).className = "sq" + (i < 2 && t >= a + .1 ? " p" : "");
    $("sq" + i).style.transform = `scale(${mix(.6, 1, back(lin(t, a, a + .3)))})`;
  }
  $("chk").className = "chk" + (t >= TAP.chk ? " on" : "");
  $("chk").style.transform = `scale(${press(t, TAP.chk)})`;
  $("chk").firstElementChild.style.transform = `scale(${back(lin(t, TAP.chk, TAP.chk + .3))})`;
  $("bC").className = "btn" + (t >= TAP.chk + .1 ? " on" : "");
  $("bC").style.transform = `scale(${press(t, TAP.place)})`;
  const ck = lin(t, TAP.place + .05, TAP.place + .2);
  set("bCt", 1 - ck);
  set("bCk", clamp(lin(t, TAP.place + .1, TAP.place + .2)), `scale(${back(lin(t, TAP.place + .1, TAP.place + .4))})`);
  const ok = lin(t, 10.95, 11.2);
  $("okv").style.opacity = ok; $("okv").style.visibility = ok > 0 ? "visible" : "hidden";
  pop("okd", t, 11.0, .5, .4);
  rise("okb1", t, 11.25, .4, 24); rise("okb2", t, 11.35, .4, 24);

  // touch indicator
  const vis = lin(t, 3.6, 3.8) * (1 - lin(t, 10.75, 10.95));
  touch(t, KF, TAPS, t < 3.5 || t > 11 ? 0 : vis);

  // ---- end card (Dark Blue panel, wipes up from the bottom)
  const w2 = io(lin(t, ...T.wipe2));
  $("dk2").style.transform = `translateY(${1920 * (1 - w2)}px)`;
  $("dk2").style.visibility = w2 > 0 ? "visible" : "hidden";
  rise("eh0", t, 12.45, .55, 80); rise("eh1", t, 12.6, .55, 80); rise("eh2", t, 12.75, .55, 80);
  accent("acc3", t, 12.65, .75);
  cluster("e", t, 12.9);
  rise("lg3", t, 13.45, .5, 40);
}

boot(seek);
