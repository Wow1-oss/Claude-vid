"""Builds index.html (HyperFrames composition) for the Cymbo Cleansing Oil UGC ad.
Style: Premium UGC Ad (same system as edit/build.py SimHome), new font set:
Bricolage Grotesque 800 (UI/captions) + Instrument Serif italic (emotion) + Anton (hook/CTA)."""
import json

W = json.load(open("words.json"))
VID_END = 8.875          # cut footage length
TOTAL = 10.075           # + 1.2s end card
CHUNKS = [2, 1, 2, 3, 2, 3, 3, 2, 2, 2, 2]
EMPH = {"tebal?", "Relaks!", "Cymbo", "makeup", "kotoran.", "Vitamin", "E,", "serai", "fresh.", "double", "cleansing."}
assert sum(CHUNKS) == len(W), (sum(CHUNKS), len(W))

# ---------- captions ----------
caps_html, caps_js, groups, i = [], [], [], 0
for n in CHUNKS:
    groups.append(W[i:i + n]); i += n
for gi, g in enumerate(groups):
    s = g[0]["s"]
    nxt = groups[gi + 1][0]["s"] if gi + 1 < len(groups) else VID_END
    e = min(nxt, g[-1]["e"] + 0.3)
    spans = [f'<span id="c{gi}w{wi}" class="{"w emph" if w["w"] in EMPH else "w"}">{w["w"]}</span>' for wi, w in enumerate(g)]
    low = ' style="top:215px"' if gi in (2, 3) else ''  # bottle shot: keep label clear
    caps_html.append(f'<div id="cap{gi}" class="cap f-bricolage-grotesque"{low}>{"".join(spans)}</div>')
    caps_js.append({"id": f"cap{gi}", "s": round(max(0, s - 0.04), 2), "e": round(e, 2),
                    "w": [[f"c{gi}w{wi}", w["s"], w["w"] in EMPH] for wi, w in enumerate(g)]})

SFX = [  # file, start, volume
    ("whoosh", 0.00, 0.55), ("hit", 0.08, 0.55), ("boom", 0.46, 0.6), ("swish", 1.04, 0.45),
    ("sparkle", 1.08, 0.35), ("whoosh", 1.56, 0.4), ("sparkle", 1.99, 0.45), ("swish", 2.95, 0.4),
    ("drip", 3.10, 0.5), ("tick", 3.98, 0.55), ("tick", 4.55, 0.55), ("swish", 4.79, 0.35),
    ("pop", 5.26, 0.5), ("pop", 6.12, 0.45), ("swish", 6.33, 0.35), ("chime", 7.00, 0.4),
    ("whoosh", 7.31, 0.4), ("hit", 8.02, 0.45), ("whoosh", 8.80, 0.5), ("click", 9.45, 0.6), ("chime", 9.48, 0.35),
]
sfx_html = "\n".join(
    f'  <audio id="sfx{k}" class="clip" src="audio/{f}.wav" data-start="{t}" data-duration="{min(1.2, round(TOTAL - t, 2))}" data-volume="{v}"></audio>'
    for k, (f, t, v) in enumerate(SFX))

TICK = ('<svg viewBox="0 0 40 40" width="46" height="46"><circle cx="20" cy="20" r="19" fill="#c9db3f"/>'
        '<path class="tk" d="M11 20.5l6 6 12-13" fill="none" stroke="#1f2610" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" '
        'stroke-dasharray="30" stroke-dashoffset="30"/></svg>')
DROP = ('<svg viewBox="0 0 40 52" width="44" height="58"><path d="M20 3C14 14 6 23 6 33a14 14 0 0 0 28 0C34 23 26 14 20 3z" fill="#f3dc6b"/>'
        '<path d="M13 34a7 7 0 0 0 7 7" stroke="#fffaf0" stroke-width="3.5" fill="none" stroke-linecap="round"/></svg>')
LEAF = ('<svg viewBox="0 0 60 90" width="56" height="84"><path class="lf" d="M30 86C30 60 22 30 8 6M30 86C31 58 40 34 54 12M30 86V20" '
        'fill="none" stroke="#9fbf2a" stroke-width="5" stroke-linecap="round" stroke-dasharray="120" stroke-dashoffset="120"/></svg>')
ARROW = ('<svg viewBox="0 0 40 40" width="44" height="44"><path d="M20 6v24M9 20l11 11 11-11" fill="none" stroke="#1f2610" '
         'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
STAR = ('<svg viewBox="0 0 40 40"><path d="M20 0C21 13 27 19 40 20 27 21 21 27 20 40 19 27 13 21 0 20 13 19 19 13 20 0z" fill="#fffbe8"/></svg>')

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/fonts.css">
<script src="vendor/gsap.min.js"></script>
<style>
:root{{--cream:#fbf7ee;--ink:#1f2610;--olive:#3c4a1c;--lime:#c9db3f;--oil:#f3dc6b;--blush:#f2c6bd}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F Bricolage Grotesque",sans-serif}}
#ground{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 40%,#efe6d2,#cbbd9f)}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
#stage{{position:absolute;inset:0;overflow:hidden}}
#stage video{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}
#tint{{position:absolute;inset:0;background:#2b3a44;mix-blend-mode:soft-light;opacity:0}}
#light{{position:absolute;inset:0;mix-blend-mode:soft-light;opacity:.5;
  background:radial-gradient(520px 620px at var(--lx,560px) var(--ly,760px),rgba(255,240,222,.8),rgba(255,240,222,0) 70%)}}
#glow{{position:absolute;inset:0;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(900px 760px at 82% 8%,rgba(255,226,160,.55),rgba(255,226,160,0) 70%)}}
#fresh{{position:absolute;inset:0;mix-blend-mode:soft-light;opacity:0;
  background:radial-gradient(1000px 900px at 30% 30%,rgba(214,236,120,.7),rgba(214,236,120,0) 70%)}}
#vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(130% 95% at 50% 45%,rgba(0,0,0,0) 58%,rgba(30,22,10,.38) 100%)}}
#grain{{position:absolute;inset:-50%;opacity:.05;mix-blend-mode:overlay;
  background-image:repeating-radial-gradient(circle at 17% 32%,#fff 0 1px,transparent 1px 3px),repeating-radial-gradient(circle at 73% 61%,#000 0 1px,transparent 1px 4px)}}
/* hook headline (pre-hook, over hands) */
#hk{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:250px;font-size:250px;line-height:.9;color:#fff;opacity:0;
  letter-spacing:4px;text-shadow:0 12px 50px rgba(40,25,10,.45)}}
/* text behind body */
.bt{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;color:var(--cream);opacity:0;white-space:nowrap;
  text-shadow:0 10px 40px rgba(70,50,20,.35)}}
#bt1{{top:150px;font-size:360px;line-height:1;letter-spacing:6px}}
#bt2{{top:150px;font-size:300px;line-height:1;color:#fff6dc}}
#bt3{{top:330px;font-size:300px;line-height:1;letter-spacing:6px}}
#bt4{{top:190px;font-size:150px;line-height:1;color:#fff6dc}}
/* captions */
#captions{{position:absolute;left:0;right:0;top:1230px;height:200px}}
.cap{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;max-width:980px;text-align:center;opacity:0;
  font-size:74px;line-height:1.1;color:#fff;letter-spacing:-1px;
  text-shadow:0 4px 0 rgba(0,0,0,.3),0 0 24px rgba(0,0,0,.42),0 2px 3px rgba(0,0,0,.55)}}
.w{{display:inline-block;margin:0 9px;color:rgba(255,255,255,.62)}}
.w.emph{{background:var(--lime);color:var(--ink);padding:2px 16px 6px;border-radius:14px;text-shadow:none;
  box-shadow:0 10px 30px rgba(40,50,10,.35)}}
/* brand wordmark on bottle reveal */
#wm{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:205px;text-align:center;opacity:0}}
#wm .shop{{font-size:40px;color:var(--olive);letter-spacing:1px;opacity:.9}}
#wm .nm{{font-size:200px;line-height:.95;color:var(--ink);letter-spacing:-6px}}
#wm .sub{{display:inline-block;margin-top:6px;font-size:66px;color:var(--olive);background:rgba(251,247,238,.82);padding:2px 28px 8px;border-radius:40px}}
.star{{position:absolute;width:64px;height:64px;opacity:0}}
.star svg{{width:100%;height:100%;filter:drop-shadow(0 0 12px rgba(255,240,180,.9))}}
/* checklist pills */
.pill{{position:absolute;left:60px;height:104px;padding:0 40px 0 24px;border-radius:52px;display:flex;align-items:center;gap:18px;
  background:rgba(251,247,238,.94);color:var(--ink);font-size:56px;opacity:0;box-shadow:0 18px 40px rgba(40,30,10,.25)}}
.pill svg{{flex:0 0 46px}}
#pl1{{top:300px}} #pl2{{top:430px}}
/* ingredient badges */
.ing{{position:absolute;left:60px;display:flex;align-items:center;gap:22px;opacity:0;padding:18px 40px 18px 26px;border-radius:30px;
  background:rgba(251,247,238,.94);box-shadow:0 18px 40px rgba(40,30,10,.25)}}
.ing svg{{flex:0 0 auto}}
.ing .t1{{font-size:62px;color:var(--ink);line-height:1}}
.ing .t2{{font-size:40px;color:var(--olive);line-height:1.1}}
#ing1{{top:290px}} #ing2{{top:470px}}
/* fresh word */
#fw{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:640px;font-size:300px;line-height:1;color:#fffbe8;opacity:0;
  text-shadow:0 10px 50px rgba(120,140,20,.45)}}
.sp{{position:absolute;width:30px;height:30px;opacity:0;background:radial-gradient(circle,#fff 0 20%,rgba(240,250,190,.9) 30%,rgba(240,250,190,0) 70%)}}
/* end card */
#end{{position:absolute;inset:0;background:var(--cream);opacity:0;overflow:hidden}}
#end .bg{{position:absolute;inset:0;background:radial-gradient(90% 60% at 50% 40%,#fffdf6,#efe8d4)}}
#end img.hero{{position:absolute;left:150px;top:300px;width:780px;height:910px;object-fit:cover;border-radius:44px;box-shadow:0 40px 90px rgba(60,50,20,.25)}}
#end .logo{{position:absolute;left:0;right:0;margin:0 auto;top:195px;width:fit-content;font-size:46px;color:var(--olive);letter-spacing:1px}}
#end .q{{position:absolute;left:0;right:0;margin:0 auto;top:1250px;width:fit-content;white-space:nowrap;font-size:96px;color:var(--ink)}}
#end .s{{position:absolute;left:0;right:0;margin:0 auto;top:1385px;width:fit-content;font-size:50px;color:var(--ink);display:flex;align-items:center;gap:14px;
  background:var(--lime);padding:16px 38px 16px 28px;border-radius:50px;box-shadow:0 14px 30px rgba(120,140,20,.35)}}
#end .s svg{{flex:0 0 44px}}
#tap{{position:absolute;left:870px;top:1440px;width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.85);border:5px solid var(--ink);opacity:0}}
#tapring{{position:absolute;left:845px;top:1415px;width:120px;height:120px;border-radius:50%;border:6px solid var(--lime);opacity:0}}
#flash{{position:absolute;inset:0;background:#fffaf0;opacity:0}}
#bar{{position:absolute;left:0;bottom:0;height:8px;width:1080px;background:var(--lime);transform-origin:0 50%;opacity:.9}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="ground" class="clip" data-start="0" data-duration="{TOTAL}"></div>
  <div id="cam">
    <div id="stage">
      <video id="vid" class="clip" src="footage.mp4" data-start="0" data-duration="{VID_END}" data-has-audio="true"></video>
      <div id="tint"></div>
      <div id="bt1" class="bt f-anton">TEBAL?</div>
      <div id="bt2" class="bt f-instrument-serif">relaks.</div>
      <video id="cut" class="clip" src="cut_hook.webm" muted data-start="0.4583" data-duration="1.125"></video>
      <div id="bt3" class="bt f-anton">DOUBLE</div>
      <div id="bt4" class="bt f-instrument-serif">cleansing</div>
      <video id="cut2" class="clip" src="cut_end.webm" muted data-start="7.3333" data-duration="1.5417"></video>
      <div id="light"></div>
      <div id="glow"></div>
      <div id="fresh"></div>
    </div>
  </div>
  <div id="vig"></div>
  <div id="grain"></div>

  <div id="hk" class="f-anton">MAKEUP</div>

  <div id="wm"><div class="shop f-instrument-serif">the pastels shop</div><div class="nm f-bricolage-grotesque">Cymbo</div>
    <div class="sub f-instrument-serif">Cleansing Oil</div></div>
  <div id="st0" class="star" style="left:300px;top:760px">{STAR}</div>
  <div id="st1" class="star" style="left:700px;top:900px;width:44px;height:44px">{STAR}</div>
  <div id="st2" class="star" style="left:380px;top:1080px;width:36px;height:36px">{STAR}</div>

  <div id="pl1" class="pill f-bricolage-grotesque">{TICK}Angkat makeup</div>
  <div id="pl2" class="pill f-bricolage-grotesque">{TICK}Buang kotoran</div>

  <div id="ing1" class="ing">{DROP}<div><div class="t1 f-bricolage-grotesque">Vitamin E</div><div class="t2 f-instrument-serif">nourish &amp; protect</div></div></div>
  <div id="ing2" class="ing">{LEAF}<div><div class="t1 f-bricolage-grotesque">Serai</div><div class="t2 f-instrument-serif">lemongrass oil, fresh</div></div></div>

  <div id="fw" class="f-instrument-serif">fresh</div>
  <div id="sp0" class="sp" style="left:240px;top:660px"></div><div id="sp1" class="sp" style="left:830px;top:650px"></div>
  <div id="sp2" class="sp" style="left:300px;top:900px"></div><div id="sp3" class="sp" style="left:780px;top:920px"></div>

  <div id="captions">
    {"".join(caps_html)}
  </div>

  <div id="end">
    <div class="bg"></div>
    <div class="logo f-instrument-serif">the pastels shop</div>
    <img class="hero" src="img/hero_end.jpg">
    <div class="q"><span class="f-anton">MAKEUP TEBAL?</span> <span class="f-instrument-serif">Relaks.</span></div>
    <div class="s f-bricolage-grotesque">Dapatkan kat link di bawah{ARROW}</div>
    <div id="tapring"></div><div id="tap"></div>
  </div>
  <div id="flash"></div>
  <div id="bar"></div>

  <audio id="music" class="clip" src="audio/music.wav" data-start="0" data-duration="{TOTAL}" data-volume="0.2"></audio>
{sfx_html}
</div>
<script>
const FPS = 30, F = n => n / FPS;
const E = {{ land:"power3.out", soft:"power2.out", snap:"expo.out", settle:"back.out(1.15)", exit:"power2.in", throw:"power4.in", move:"power2.inOut" }};
const tl = gsap.timeline({{ paused: true }});
const CAPS = {json.dumps(caps_js)};

// ---------- camera: per-shot origin + key light; punch-in on every cut ----------
const SHOTS = [ // t, origin, light x/y, scale-from
  [0.000, "50% 55%", 560, 900, 1.16], [0.458, "52% 36%", 570, 720, 1.12], [1.583, "50% 45%", 520, 800, 1.10],
  [2.958, "50% 60%", 540, 1200, 1.08], [4.792, "55% 55%", 640, 1000, 1.08], [6.333, "45% 55%", 480, 1000, 1.08],
  [7.333, "50% 38%", 540, 760, 1.10] ];
SHOTS.forEach(([t,o,lx,ly,s]) => {{
  tl.set("#cam", {{ transformOrigin:o, x:0, y:0 }}, t);
  tl.set("#light", {{ "--lx": lx+"px", "--ly": ly+"px" }}, t);
  tl.fromTo("#cam", {{ scale:s }}, {{ scale:1.0, duration:F(10), ease:E.snap, immediateRender:false }}, t);
}});
// slow push on bottle + closing
tl.to("#cam", {{ scale:1.06, duration:1.0, ease:"none" }}, 1.92);
tl.to("#cam", {{ scale:1.04, duration:0.38, ease:"none" }}, 7.62);

// ---------- 0.00 pre-hook: hands + MAKEUP ----------
tl.fromTo("#flash", {{ opacity:.95 }}, {{ opacity:0, duration:F(6), ease:E.exit }}, 0);
tl.fromTo("#hk", {{ opacity:0, scale:2.2 }}, {{ opacity:1, scale:1, duration:F(7), ease:E.snap }}, 0.06);
tl.to("#hk", {{ opacity:0, y:-80, duration:F(4), ease:E.throw }}, 0.40);

// ---------- 0.46 face: TEBAL? behind head + shake ----------
tl.fromTo("#flash", {{ opacity:.5 }}, {{ opacity:0, duration:F(4), ease:E.exit, immediateRender:false }}, 0.458);
tl.to("#tint", {{ opacity:.5, duration:F(6), ease:E.soft }}, 0.458);
tl.to("#stage", {{ filter:"saturate(0.85) brightness(0.97)", duration:F(6), ease:E.soft }}, 0.458);
tl.fromTo("#bt1", {{ opacity:0, scale:1.9, y:-30 }}, {{ opacity:1, scale:1, y:0, duration:F(7), ease:E.snap }}, 0.46);
tl.to("#cam", {{ x:12, duration:F(2), ease:"none", yoyo:true, repeat:5 }}, 0.62);
tl.to("#bt1", {{ opacity:0, y:-70, duration:F(5), ease:E.throw }}, 0.86);

// ---------- 1.04 Relaks! : mood lifts warm, serif behind head ----------
tl.to("#tint", {{ opacity:0, duration:F(5), ease:E.exit }}, 1.0);
tl.to("#stage", {{ filter:"saturate(1.04) brightness(1.03)", duration:F(6), ease:E.soft }}, 1.0);
tl.to("#glow", {{ opacity:.45, duration:F(12), ease:E.soft }}, 1.04);
tl.fromTo("#bt2", {{ opacity:0, x:-180 }}, {{ opacity:1, x:0, duration:F(11), ease:E.land }}, 1.04);
tl.to("#cam", {{ scale:1.07, duration:F(7), ease:E.snap }}, 1.04);
tl.to("#bt2", {{ opacity:0, x:140, duration:F(6), ease:E.throw }}, 1.40);
tl.to("#glow", {{ opacity:.2, duration:F(8), ease:E.exit }}, 1.50);

// ---------- 1.58 bottle reveal: wordmark + glints ----------
tl.fromTo("#flash", {{ opacity:.55 }}, {{ opacity:0, duration:F(5), ease:E.exit, immediateRender:false }}, 1.583);
tl.fromTo("#wm .shop", {{ opacity:0, y:30 }}, {{ opacity:.9, y:0, duration:F(10), ease:E.land }}, 1.70);
tl.fromTo("#wm", {{ opacity:0, y:-160 }}, {{ opacity:1, y:0, duration:F(11), ease:E.land }}, 1.68);
tl.fromTo("#wm .nm", {{ scale:1.5 }}, {{ scale:1, duration:F(8), ease:E.snap, immediateRender:false }}, 1.99);
tl.fromTo("#wm .sub", {{ opacity:0, x:-120 }}, {{ opacity:1, x:0, duration:F(9), ease:E.land }}, 2.36);
[0,1,2].forEach(k => {{
  const t = 2.0 + k*F(4);
  tl.set("#st"+k, {{ opacity:1, scale:.4, rotation:0 }}, t);
  tl.to("#st"+k, {{ opacity:0, scale:1.4, rotation:90, duration:F(16), ease:E.soft }}, t);
}});
tl.to("#wm", {{ opacity:0, y:-140, duration:F(6), ease:E.throw }}, 2.80);

// ---------- 2.96 pour: checklist pills ----------
[["#pl1",3.98],["#pl2",4.55]].forEach(([id,t]) => {{
  tl.fromTo(id, {{ opacity:0, x:-320 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, t - 0.12);
  tl.to(id + " .tk", {{ attr:{{ "stroke-dashoffset":0 }}, duration:F(7), ease:E.snap }}, t);
  tl.fromTo(id, {{ scale:1.12 }}, {{ scale:1, duration:F(7), ease:E.snap, immediateRender:false }}, t);
}});
tl.to(["#pl1","#pl2"], {{ opacity:0, x:-300, duration:F(6), ease:E.throw, stagger:F(2) }}, 4.95);

// ---------- 4.79 rub: Vitamin E, 6.10 serai ----------
tl.fromTo("#ing1", {{ opacity:0, x:-340 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 5.16);
tl.fromTo("#ing1 svg", {{ y:-60 }}, {{ y:0, duration:F(9), ease:E.snap }}, 5.26);
tl.fromTo("#ing2", {{ opacity:0, x:-340 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 6.08);
tl.to("#ing2 .lf", {{ attr:{{ "stroke-dashoffset":0 }}, duration:F(14), ease:E.soft }}, 6.15);
tl.to(["#ing1","#ing2"], {{ opacity:0, x:-320, duration:F(6), ease:E.throw, stagger:F(2) }}, 6.80);

// ---------- 6.33 pad wipe: fresh ----------
tl.to("#fresh", {{ opacity:.6, duration:F(14), ease:E.soft }}, 6.40);
tl.fromTo("#fw", {{ opacity:0, y:90, scale:1.3 }}, {{ opacity:1, y:0, scale:1, duration:F(12), ease:E.settle }}, 6.92);
[0,1,2,3].forEach(k => {{
  const t = 7.0 + k*F(3);
  tl.set("#sp"+k, {{ opacity:1, scale:.6 }}, t);
  tl.to("#sp"+k, {{ opacity:0, scale:2.2, y:-60, duration:F(12), ease:E.soft }}, t);
}});
tl.to("#fw", {{ opacity:0, y:-90, duration:F(5), ease:E.throw }}, 7.20);
tl.to("#fresh", {{ opacity:0, duration:F(8), ease:E.exit }}, 7.25);

// ---------- 7.33 closing: DOUBLE cleansing behind head ----------
tl.fromTo("#flash", {{ opacity:.45 }}, {{ opacity:0, duration:F(5), ease:E.exit, immediateRender:false }}, 7.333);
tl.to("#glow", {{ opacity:.35, duration:F(14), ease:E.soft }}, 7.40);
tl.fromTo("#bt3", {{ opacity:0, scale:1.8 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 8.02);
tl.fromTo("#bt4", {{ opacity:0, x:-200 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 8.30);
tl.to("#cam", {{ scale:1.1, duration:F(7), ease:E.snap }}, 8.02);

// ---------- 8.875 end card (loops back to hook) ----------
tl.fromTo("#end", {{ opacity:1, y:1920 }}, {{ opacity:1, y:0, duration:F(8), ease:E.land }}, {VID_END - 0.07});
tl.fromTo("#end img.hero", {{ scale:1.12 }}, {{ scale:1.0, duration:1.2, ease:E.soft }}, {VID_END - 0.07});
tl.fromTo("#end .q", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END + 0.12});
tl.fromTo("#end .s", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END + 0.25});
tl.fromTo("#tap", {{ opacity:0, x:200, y:160 }}, {{ opacity:1, x:0, y:0, duration:F(10), ease:E.land }}, 9.10);
tl.to("#tap", {{ scale:.78, duration:F(3), ease:E.exit }}, 9.42);
tl.to("#tap", {{ scale:1, duration:F(5), ease:E.land }}, 9.52);
tl.set("#tapring", {{ opacity:1, scale:.5 }}, 9.45);
tl.to("#tapring", {{ opacity:0, scale:2.2, duration:F(14), ease:E.soft }}, 9.45);
tl.fromTo("#end .s", {{ scale:1.12 }}, {{ scale:1, duration:F(8), ease:E.snap, immediateRender:false }}, 9.45);
tl.to("#end .s svg", {{ y:8, duration:F(6), ease:E.move, yoyo:true, repeat:3 }}, 9.55);
tl.set(["#captions","#bt3","#bt4"], {{ opacity:0 }}, {VID_END + 0.2});

// ---------- captions (karaoke) ----------
CAPS.forEach(c => {{
  tl.fromTo("#"+c.id, {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:F(6), ease:E.land }}, c.s);
  c.w.forEach(([id, t, em]) => {{
    tl.to("#"+id, {{ color: em ? "#1f2610" : "#ffffff", duration:F(2), ease:"none" }}, t);
    tl.fromTo("#"+id, {{ scale:1.25 }}, {{ scale:1, duration:F(6), ease:E.snap, immediateRender:false }}, t);
  }});
  tl.to("#"+c.id, {{ opacity:0, y:-20, duration:F(4), ease:E.exit }}, Math.max(c.s + 0.2, c.e - F(4)));
}});

// ---------- progress ----------
tl.fromTo("#bar", {{ scaleX:0 }}, {{ scaleX:1, duration:{TOTAL}, ease:"none" }}, 0);

window.__timelines = window.__timelines || {{}};
window.__timelines['main'] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
print("index.html written,", len(groups), "caption chunks")
