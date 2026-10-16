// 15 Cyber Monday finds (10.8 s). Full-height layout: headline top, one product big on its own
// 640 px shape in the middle, the cart card docked at the bottom. A big Pink bag disc opens the reel
// and shrinks into the card's corner badge; each product swipes in, its shape swipes off and the
// cutout shrinks into the next slot (left to right). End: check badge, headline to the centre, logo back at the top.
const N = 5, C0 = 1.6, CYC = 1.3;
const CENTER = { x: 540, y: 970 }, S = CFG.slot, BOX = S.box, SLOT_SCALE = S.in / BOX;
const CART_IN = [.45, .95], BAG = [.6, 1.1], BAG_DOCK = [1.25, 1.75], BADGE = { x: 150, y: 1330, d: 80 };
const OK = 8.5, HL_DOWN = [8.55, 9.15], HL_DY = 836 - 364, LOGO2 = 9.0;   // headline block 836-1094, centre ~965
const Ci = i => C0 + i * CYC;                       // product i swipes in
const Fi = i => Ci(i) + .85;                        // shape swipes off, cutout flies to slot i
const FLY = .6;

function shapePose(i, t) {                          // [dx, rot] or null when off stage
  const pin = out(lin(t, Ci(i), Ci(i) + .5)), pout = io(lin(t, Fi(i), Fi(i) + .45));
  if (t < Ci(i) || pout >= 1) return null;
  return [mix(820, 0, pin) - 860 * pout, mix(10, 0, pin) - 16 * pout];
}

function seek(t) {
  // first beat: logo + headline + accent; the logo leaves as product 1 arrives
  // final beat: the logo comes back at the top and the headline moves down to the frame centre
  const lo = lin(t, 1.3, 1.55), p = out(lin(t, .1, .6)), lb = out(lin(t, LOGO2, LOGO2 + .5));
  set("lg1", t < LOGO2 ? p * (1 - lo) : lb, `translateY(${t < LOGO2 ? (1 - p) * 40 - lo * 30 : (1 - lb) * 40}px)`);
  rise("h0", t, .22, .55, 70); rise("h1", t, .36, .55, 70);
  $("hl").style.transform = `translateY(${HL_DY * io(lin(t, ...HL_DOWN))}px)`;

  // cart card (docked at the bottom the whole time)
  const ci = out(lin(t, ...CART_IN));
  set("cart", ci, `translateY(${(1 - ci) * 80}px)`);
  for (let i = 0; i < N; i++) {
    const land = Fi(i) + .05 + FLY, sl = $("sl" + i), on = t >= land - .05;
    sl.className = "slot" + (on ? " on" : "");
    sl.style.transform = `scale(${on ? mix(1.08, 1, out(lin(t, land - .05, land + .25))) : mix(.7, 1, back(lin(t, .6 + i * .05, 1.0 + i * .05)))})`;
  }

  // big bag disc in the middle, then it shrinks into the card's top-left badge
  const bq = lin(t, ...BAG), bd = io(lin(t, ...BAG_DOCK));
  const bx = mix(CENTER.x, BADGE.x, bd), by = mix(CENTER.y, BADGE.y, bd), bs = mix(1, BADGE.d / 360, bd) * mix(.5, 1, back(bq));
  set("bagd", clamp(bq * 3), `translate(${bx - 180}px,${by - 180}px) scale(${bs})`);
  pop("cok", t, OK, .45, .3);

  // products
  for (let i = 0; i < N; i++) {
    const sh = $("ps" + i), el = $("p" + i), pose = shapePose(i, t);
    sh.style.visibility = pose ? "visible" : "hidden";
    if (pose) sh.style.transform = `translateX(${pose[0]}px) rotate(${pose[1]}deg)`;
    if (t < Ci(i)) { el.style.visibility = "hidden"; continue; }
    el.style.visibility = "visible";
    let x = CENTER.x, y = CENTER.y, s = 1, r = 0;
    const f = lin(t, Fi(i) + .05, Fi(i) + .05 + FLY);
    const sx = S.x0 + i * S.dx, sy = S.y;
    if (f <= 0) {
      const ps = pose || [0, 0];
      x += ps[0]; r = ps[1];
    } else {
      const q = io(f), cx = (CENTER.x + sx) / 2 - 60, cy = CENTER.y + 60;
      x = (1 - q) ** 2 * CENTER.x + 2 * (1 - q) * q * cx + q * q * sx;
      y = (1 - q) ** 2 * CENTER.y + 2 * (1 - q) * q * cy + q * q * sy;
      s = mix(1, SLOT_SCALE, out(f));
      r = Math.sin(Math.PI * f) * -6;
    }
    el.style.transform = `translate(${x - BOX / 2}px,${y - BOX / 2}px) rotate(${r}deg) scale(${s})`;
  }
}

boot(seek);
