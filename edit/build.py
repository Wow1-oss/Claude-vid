"""Builds index.html (HyperFrames composition) from words.json."""
import json

W = json.load(open("words.json"))
TOTAL = 17.76
VID_END = 16.56
CHUNKS = [2, 2, 4, 2, 2, 3, 2, 4, 2, 3, 3, 3, 2, 2, 3, 2, 4, 3, 2]
EMPH = {"meja", "makan,", "kerja", "serba", "tak", "kena.", "adjust", "tinggi.",
        "360", "selit", "best", "yellow", "basket."}
assert sum(CHUNKS) == len(W), (sum(CHUNKS), len(W))

# ---------- captions ----------
caps_html, caps_js = [], []
i = 0
groups = []
for n in CHUNKS:
    groups.append(W[i:i + n]); i += n
for gi, g in enumerate(groups):
    s = g[0]["s"]
    nxt = groups[gi + 1][0]["s"] if gi + 1 < len(groups) else VID_END
    e = min(nxt, g[-1]["e"] + 0.35)
    spans = []
    for wi, w in enumerate(g):
        cls = "w emph" if w["w"] in EMPH else "w"
        spans.append(f'<span id="c{gi}w{wi}" class="{cls}">{w["w"]}</span>')
    caps_html.append(f'<div id="cap{gi}" class="cap">{"".join(spans)}</div>')
    caps_js.append({"id": f"cap{gi}", "s": round(s, 2), "e": round(e, 2),
                    "w": [[f"c{gi}w{wi}", w["s"], w["w"] in EMPH] for wi, w in enumerate(g)]})

SFX = [  # id, file, start, volume
    ("whoosh", 0.00, 0.55), ("hit", 0.47, 0.55), ("pop", 1.66, 0.5), ("swish", 2.60, 0.45),
    ("pop", 3.18, 0.45), ("pop", 3.98, 0.45), ("buzz", 5.16, 0.35), ("boom", 6.20, 0.7),
    ("riser", 6.80, 0.35), ("tick", 7.30, 0.5), ("whoosh", 7.90, 0.45), ("swish", 8.35, 0.4),
    ("tick", 9.30, 0.5), ("swish", 9.72, 0.4), ("click", 10.71, 0.5), ("chime", 12.31, 0.35),
    ("swish", 14.10, 0.4), ("pop", 14.40, 0.45), ("click", 15.68, 0.6), ("chime", 15.72, 0.4),
    ("whoosh", 16.40, 0.5), ("chime", 16.60, 0.35),
]
sfx_html = "\n".join(
    f'  <audio id="sfx{k}" class="clip" src="audio/{f}.wav" data-start="{t}" data-duration="{min(1.4, round(TOTAL - t, 2))}" data-volume="{v}"></audio>'
    for k, (f, t, v) in enumerate(SFX))

BASKET = ('<svg viewBox="0 0 48 48" width="54" height="54"><path d="M8 18h32l-3.5 20a3 3 0 0 1-3 2.5h-19a3 3 0 0 1-3-2.5z" '
          'fill="#1b1410"/><path d="M16 18l6-10M32 18l-6-10" stroke="#1b1410" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
          '<path d="M18 26v8M24 26v8M30 26v8" stroke="#ffd23f" stroke-width="3" stroke-linecap="round"/></svg>')

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/fonts.css">
<script src="vendor/gsap.min.js"></script>
<style>
:root{{--cream:#fbf5ec;--walnut:#6b3f24;--navy:#1d2b45;--gold:#f2c14e;--ink:#1b1410;--yellow:#ffd23f}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F Inter Tight",sans-serif}}
#ground{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 40%,#3a2a20,#120c09)}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
#stage{{position:absolute;inset:0;overflow:hidden}}
#stage video{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}
#tint{{position:absolute;inset:0;background:#1a2733;mix-blend-mode:soft-light;opacity:0}}
#light{{position:absolute;inset:0;mix-blend-mode:soft-light;opacity:.55;
  background:radial-gradient(520px 600px at var(--lx,540px) var(--ly,700px),rgba(255,236,214,.75),rgba(255,236,214,0) 70%)}}
#glow{{position:absolute;inset:0;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(900px 700px at 85% 10%,rgba(255,190,120,.55),rgba(255,190,120,0) 70%)}}
#vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(130% 95% at 50% 45%,rgba(0,0,0,0) 55%,rgba(10,6,4,.42) 100%)}}
#grain{{position:absolute;inset:-50%;opacity:.06;mix-blend-mode:overlay;
  background-image:repeating-radial-gradient(circle at 17% 32%,#fff 0 1px,transparent 1px 3px),repeating-radial-gradient(circle at 73% 61%,#000 0 1px,transparent 1px 4px)}}
/* text behind (hook) */
.bt{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;color:var(--cream);opacity:0;white-space:nowrap;
  text-shadow:0 10px 40px rgba(60,30,10,.35)}}
#bt1{{top:150px;font-size:330px;letter-spacing:6px;line-height:1}}
#bt2{{top:170px;font-size:205px;line-height:.95;text-align:center;letter-spacing:4px}}
#bt3{{top:120px;font-size:330px;line-height:1;color:#ffe6c4}}
/* captions */
#captions{{position:absolute;left:0;right:0;top:1215px;height:200px}}
.cap{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;max-width:980px;text-align:center;opacity:0;
  font-size:76px;line-height:1.1;color:#fff;letter-spacing:-1px;
  text-shadow:0 4px 0 rgba(0,0,0,.35),0 0 24px rgba(0,0,0,.45),0 2px 3px rgba(0,0,0,.6)}}
.w{{display:inline-block;margin:0 9px;color:rgba(255,255,255,.62)}}
.w.emph{{background:var(--walnut);color:var(--cream);padding:2px 16px 6px;border-radius:14px;text-shadow:none;
  box-shadow:0 10px 30px rgba(40,20,8,.45)}}
/* problem chips */
.chip{{position:absolute;right:60px;height:96px;padding:0 34px 0 22px;border-radius:48px;display:flex;align-items:center;gap:18px;
  background:rgba(251,245,236,.92);color:var(--ink);font-size:40px;letter-spacing:.5px;opacity:0;
  box-shadow:0 18px 40px rgba(20,10,5,.35)}}
.chip .x{{flex:0 0 56px;height:56px;border-radius:50%;background:#d9493b;color:#fff;font-size:34px;display:flex;align-items:center;justify-content:center}}
.chip .strike{{position:absolute;left:96px;right:28px;top:46px;height:6px;background:#d9493b;border-radius:3px;transform-origin:0 50%}}
#chip1{{top:300px}} #chip2{{top:420px}}
/* height gauge */
#gauge{{position:absolute;right:70px;top:250px;width:250px;height:600px;opacity:0}}
#gauge .track{{position:absolute;left:96px;top:30px;width:16px;height:470px;border-radius:8px;background:rgba(251,245,236,.35)}}
#gauge .fill{{position:absolute;left:96px;bottom:100px;width:16px;height:470px;border-radius:8px;background:var(--gold);transform-origin:50% 100%}}
#gauge .knob{{position:absolute;left:78px;top:470px;width:52px;height:52px;border-radius:50%;background:var(--cream);border:8px solid var(--walnut)}}
#gauge .num{{position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:120px;color:var(--cream);line-height:1;text-shadow:0 6px 30px rgba(0,0,0,.45)}}
#gauge .lbl{{position:absolute;left:0;right:0;top:-60px;text-align:center;font-size:44px;color:var(--cream)}}
/* 360 */
#r360{{position:absolute;left:0;right:0;margin:0 auto;top:230px;width:420px;height:420px;opacity:0}}
#r360 svg{{position:absolute;inset:0}}
#r360 .deg{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:170px;color:var(--cream);
  text-shadow:0 8px 34px rgba(0,0,0,.45)}}
/* base callout */
#call{{position:absolute;left:60px;top:880px;opacity:0}}
#call .t1{{font-size:120px;color:var(--cream);line-height:.9;text-shadow:0 8px 30px rgba(0,0,0,.5)}}
#call .t2{{margin-top:12px;display:inline-block;font-size:34px;color:var(--ink);background:var(--gold);padding:8px 20px;border-radius:30px}}
#ring{{position:absolute;left:470px;top:1500px;width:460px;height:150px;border-radius:50%;border:6px solid var(--gold);opacity:0;
  box-shadow:0 0 40px rgba(242,193,78,.8),inset 0 0 30px rgba(242,193,78,.5)}}
#line{{position:absolute;left:330px;top:1060px;width:6px;height:470px;background:linear-gradient(var(--gold),rgba(242,193,78,.2));transform-origin:50% 0;opacity:0;border-radius:3px}}
/* best */
#best{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:210px;text-align:center;opacity:0}}
#best .a{{font-size:190px;color:#fff3e2;line-height:1;text-shadow:0 10px 40px rgba(80,40,10,.45)}}
.spark{{position:absolute;width:26px;height:26px;opacity:0;background:radial-gradient(circle,#fff 0 20%,rgba(255,220,150,.9) 30%,rgba(255,220,150,0) 70%)}}
/* CTA card */
#cta{{position:absolute;left:60px;right:60px;top:210px;height:250px;border-radius:36px;background:rgba(251,245,236,.95);opacity:0;
  display:flex;align-items:center;gap:28px;padding:0 30px;box-shadow:0 30px 70px rgba(20,10,5,.45)}}
#cta img{{flex:0 0 190px;width:190px;height:190px;object-fit:cover;border-radius:24px}}
#cta .info{{flex:1 1 auto}}
#cta .brand{{font-size:30px;color:var(--walnut)}}
#cta .name{{font-size:46px;color:var(--ink);line-height:1.05;margin:4px 0 14px}}
#btn{{display:inline-flex;align-items:center;gap:12px;background:var(--yellow);color:var(--ink);font-size:38px;padding:10px 26px 10px 16px;border-radius:40px;
  box-shadow:0 10px 24px rgba(255,190,0,.45)}}
#btn svg{{flex:0 0 54px}}
#tap{{position:absolute;left:470px;top:395px;width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.85);border:5px solid var(--ink);opacity:0}}
#tapring{{position:absolute;left:445px;top:370px;width:120px;height:120px;border-radius:50%;border:6px solid var(--yellow);opacity:0}}
/* end card */
#end{{position:absolute;inset:0;background:var(--cream);opacity:0;overflow:hidden}}
#end img.hero{{position:absolute;left:90px;top:330px;width:900px;height:1050px;object-fit:cover;border-radius:44px;box-shadow:0 40px 90px rgba(60,30,10,.3)}}
#end .logo{{position:absolute;left:0;right:0;margin:0 auto;top:190px;width:fit-content;font-size:64px;color:var(--navy);letter-spacing:2px}}
#end .q{{position:absolute;left:0;right:0;margin:0 auto;top:1415px;width:fit-content;white-space:nowrap;font-size:60px;color:var(--walnut)}}
#end .s{{position:absolute;left:0;right:0;margin:0 auto;top:1520px;width:fit-content;font-size:40px;color:var(--ink);display:flex;align-items:center;gap:14px;
  background:var(--yellow);padding:10px 30px 10px 18px;border-radius:40px}}
#flash{{position:absolute;inset:0;background:#fff7ec;opacity:0}}
#bar{{position:absolute;left:0;bottom:0;height:8px;width:1080px;background:var(--gold);transform-origin:0 50%;opacity:.85}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="ground" class="clip" data-start="0" data-duration="{TOTAL}"></div>
  <div id="cam">
    <div id="stage">
      <video id="vid" class="clip" src="footage.mp4" data-start="0" data-duration="{VID_END}" data-has-audio="true"></video>
      <div id="tint"></div>
      <div id="bt1" class="bt f-bebas-neue">KENAPA</div>
      <div id="bt2" class="bt f-bebas-neue">BARU<br>SEKARANG?</div>
      <div id="bt3" class="bt f-playfair-display">meja</div>
      <video id="cut" class="clip" src="cut_hook.webm" muted data-start="0" data-duration="2.62"></video>
      <div id="light"></div>
      <div id="glow"></div>
    </div>
  </div>
  <div id="vig"></div>
  <div id="grain"></div>

  <div id="chip1" class="chip f-inter-tight"><span class="x">✕</span>MAKAN ATAS SOFA<span class="strike"></span></div>
  <div id="chip2" class="chip f-inter-tight"><span class="x">✕</span>KERJA ATAS SOFA<span class="strike"></span></div>

  <div id="gauge"><div class="lbl f-inter-tight">Tinggi</div><div class="track"></div><div class="fill"></div><div class="knob"></div>
    <div class="num f-bebas-neue"><span id="hnum">45</span>CM</div></div>

  <div id="r360"><svg viewBox="0 0 420 420"><circle cx="210" cy="210" r="190" fill="none" stroke="rgba(251,245,236,.25)" stroke-width="10"/>
    <circle id="arc" cx="210" cy="210" r="190" fill="none" stroke="#f2c14e" stroke-width="12" stroke-linecap="round"
      stroke-dasharray="1194" stroke-dashoffset="1194" transform="rotate(-90 210 210)"/></svg>
    <div class="deg f-bebas-neue"><span id="dnum">0</span>°</div></div>

  <div id="line"></div><div id="ring"></div>
  <div id="call"><div class="t1 f-bebas-neue">TAPAK C-SHAPE</div><div class="t2 f-inter-tight">SELIT BAWAH SOFA</div></div>

  <div id="best"><div class="a f-playfair-display">baru best</div></div>
  <div id="sp0" class="spark" style="left:250px;top:250px"></div><div id="sp1" class="spark" style="left:820px;top:230px"></div>
  <div id="sp2" class="spark" style="left:300px;top:420px"></div><div id="sp3" class="spark" style="left:770px;top:420px"></div>

  <div id="cta"><img src="img/hero.jpg"><div class="info"><div class="brand f-inter-tight">SimHome</div>
    <div class="name f-inter-tight">Adjustable Side Table</div><div id="btn" class="f-inter-tight">{BASKET}Yellow Basket</div></div></div>
  <div id="tapring"></div><div id="tap"></div>

  <div id="captions">
    {"".join(caps_html)}
  </div>

  <div id="end">
    <div class="logo f-inter-tight">SimHome</div>
    <img class="hero" src="img/hero_end.jpg">
    <div class="q f-playfair-display">Jangan tunggu “baru sekarang”.</div>
    <div class="s f-inter-tight">{BASKET}Tekan yellow basket</div>
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

// ---------- camera: punch-ins + per-shot key light (face) ----------
const SHOTS = [ // t, origin, light x/y, scale
  [0.00, "50% 38%", 540, 640, 1.0], [2.62, "40% 30%", 440, 600, 1.0], [6.20, "30% 28%", 320, 500, 1.08],
  [6.71, "35% 30%", 380, 500, 1.0], [7.93, "55% 30%", 640, 560, 1.0], [9.73, "60% 55%", 900, 560, 1.0],
  [12.31, "50% 30%", 560, 540, 1.0], [14.12, "50% 30%", 560, 540, 1.08] ];
SHOTS.forEach(([t,o,lx,ly,s]) => {{
  tl.set("#cam", {{ transformOrigin:o, scale:s, x:0, y:0 }}, t);
  tl.set("#light", {{ "--lx": lx+"px", "--ly": ly+"px" }}, t);
}});
tl.fromTo("#cam", {{ scale:1.16 }}, {{ scale:1.0, duration:F(12), ease:E.snap, immediateRender:false }}, 0);
const PUNCH = [[1.66,1.06],[4.48,1.06],[8.35,1.07],[10.71,1.07],[13.06,1.05],[15.68,1.12]];
PUNCH.forEach(([t,s]) => tl.to("#cam", {{ scale:s, duration:F(7), ease:E.snap }}, t));

// ---------- hook: flash + text behind ----------
tl.fromTo("#flash", {{ opacity:.9 }}, {{ opacity:0, duration:F(6), ease:E.exit }}, 0);
tl.fromTo("#bt1", {{ opacity:0, scale:1.8, y:-40 }}, {{ opacity:1, scale:1, y:0, duration:F(8), ease:E.snap }}, 0.47);
tl.to("#bt1", {{ opacity:0, y:-60, duration:F(5), ease:E.exit }}, 0.70);
tl.fromTo("#bt2", {{ opacity:0, scale:1.6 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 0.74);
tl.to("#bt2", {{ opacity:0, scale:.9, duration:F(5), ease:E.exit }}, 1.58);
tl.fromTo("#bt3", {{ opacity:0, x:-160 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 1.66);
tl.to("#bt3", {{ opacity:0, x:120, duration:F(6), ease:E.throw }}, 2.44);

// ---------- problem: cooler mood + chips ----------
tl.to("#tint", {{ opacity:.55, duration:F(10), ease:E.soft }}, 2.62);
tl.to("#stage", {{ filter:"saturate(0.8) brightness(0.96)", duration:F(10), ease:E.soft }}, 2.62);
[["#chip1",3.18],["#chip2",3.98]].forEach(([id,t]) =>
  tl.fromTo(id, {{ opacity:0, x:260 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, t));
tl.fromTo(".chip .strike", {{ scaleX:0 }}, {{ scaleX:1, duration:F(7), ease:E.snap, stagger:F(3) }}, 5.16);
tl.to(["#chip1","#chip2"], {{ x:(i)=>[-14,12][i], duration:F(2), ease:"none", yoyo:true, repeat:5 }}, 5.16);
tl.to("#cam", {{ x:10, duration:F(2), ease:"none", yoyo:true, repeat:5 }}, 5.16);
tl.to(["#chip1","#chip2"], {{ opacity:0, x:300, duration:F(6), ease:E.throw, stagger:F(2) }}, 5.95);

// ---------- reveal ----------
tl.fromTo("#flash", {{ opacity:.6 }}, {{ opacity:0, duration:F(5), ease:E.exit, immediateRender:false }}, 6.20);
tl.to("#tint", {{ opacity:0, duration:F(4), ease:E.exit }}, 6.20);
tl.to("#stage", {{ filter:"saturate(1) brightness(1)", duration:F(4), ease:E.exit }}, 6.20);
tl.to("#glow", {{ opacity:.3, duration:F(16), ease:E.soft }}, 6.20);
tl.fromTo("#gauge", {{ opacity:0, y:120 }}, {{ opacity:1, y:0, duration:F(11), ease:E.land }}, 6.76);
tl.fromTo("#gauge .fill", {{ scaleY:0.05 }}, {{ scaleY:1, duration:1.0, ease:E.move }}, 6.90);
tl.fromTo("#gauge .knob", {{ y:0 }}, {{ y:-440, duration:1.0, ease:E.move }}, 6.90);
const H = {{ v:45 }};
tl.to(H, {{ v:80, duration:1.0, ease:E.move, onUpdate:()=>{{ const el=document.getElementById("hnum"); if(el) el.textContent=Math.round(H.v); }} }}, 6.90);
tl.to("#gauge", {{ opacity:0, x:200, duration:F(6), ease:E.throw }}, 7.84);
tl.to("#glow", {{ opacity:0, duration:F(8), ease:E.exit }}, 7.84);

// ---------- 360 ----------
tl.fromTo("#r360", {{ opacity:0, scale:1.6 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 8.10);
tl.to("#arc", {{ attr:{{ "stroke-dashoffset":0 }}, duration:1.0, ease:E.move }}, 8.35);
tl.to("#r360 svg", {{ rotation:360, duration:1.3, ease:E.move }}, 8.30);
const D = {{ v:0 }};
tl.to(D, {{ v:360, duration:1.0, ease:E.move, onUpdate:()=>{{ const el=document.getElementById("dnum"); if(el) el.textContent=Math.round(D.v); }} }}, 8.35);
tl.to("#r360", {{ opacity:0, y:-160, duration:F(7), ease:E.throw }}, 9.55);

// ---------- base callout ----------
tl.fromTo("#call", {{ opacity:0, x:-300 }}, {{ opacity:1, x:0, duration:F(11), ease:E.land }}, 10.10);
tl.fromTo("#line", {{ opacity:0, scaleY:0.05 }}, {{ opacity:1, scaleY:1, duration:F(12), ease:E.soft }}, 10.40);
tl.fromTo("#ring", {{ opacity:0, scale:1.8 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 10.71);
tl.to("#ring", {{ scale:1.06, duration:F(9), ease:E.move, yoyo:true, repeat:3 }}, 11.05);
tl.to(["#call","#line","#ring"], {{ opacity:0, x:-120, duration:F(7), ease:E.throw }}, 12.10);

// ---------- "baru best" ----------
tl.to("#glow", {{ opacity:.4, duration:F(14), ease:E.soft }}, 12.31);
tl.fromTo("#best", {{ opacity:0, y:80, scale:1.3 }}, {{ opacity:1, y:0, scale:1, duration:F(12), ease:E.settle }}, 12.70);
[0,1,2,3].forEach(k => {{
  const t = 13.06 + k*F(3);
  tl.set("#sp"+k, {{ opacity:1, scale:0.6 }}, t);
  tl.to("#sp"+k, {{ opacity:0, scale:2.2, y:-60, duration:F(14), ease:E.soft }}, t);
}});
tl.to("#best", {{ opacity:0, y:-90, duration:F(7), ease:E.throw }}, 14.00);
tl.to("#glow", {{ opacity:.2, duration:F(10), ease:E.exit }}, 14.00);

// ---------- CTA ----------
tl.fromTo("#cta", {{ opacity:0, y:-220 }}, {{ opacity:1, y:0, duration:F(12), ease:E.land }}, 14.40);
tl.fromTo("#tap", {{ opacity:0, x:260, y:220 }}, {{ opacity:1, x:0, y:0, duration:F(12), ease:E.land }}, 15.20);
tl.to("#tap", {{ scale:.78, duration:F(3), ease:E.exit }}, 15.64);
tl.to("#tap", {{ scale:1, duration:F(5), ease:E.land }}, 15.74);
tl.set("#tapring", {{ opacity:1, scale:.5 }}, 15.68);
tl.to("#tapring", {{ opacity:0, scale:2.2, duration:F(14), ease:E.soft }}, 15.68);
tl.fromTo("#btn", {{ scale:1.18 }}, {{ scale:1, duration:F(9), ease:E.snap, immediateRender:false }}, 15.68);

// ---------- end card (loop back to hook) ----------
tl.fromTo("#end", {{ opacity:1, y:1920 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END - 0.1});
tl.fromTo("#end img.hero", {{ scale:1.12 }}, {{ scale:1.0, duration:1.3, ease:E.soft }}, {VID_END - 0.1});
tl.fromTo("#end .q", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(10), ease:E.land }}, {VID_END + 0.15});
tl.fromTo("#end .s", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(10), ease:E.land }}, {VID_END + 0.3});
tl.set(["#cta","#tap","#captions"], {{ opacity:0 }}, {VID_END});

// ---------- captions (karaoke) ----------
CAPS.forEach(c => {{
  tl.fromTo("#"+c.id, {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:F(6), ease:E.land }}, c.s);
  c.w.forEach(([id, t, em]) => {{
    tl.to("#"+id, {{ color: em ? "#fbf5ec" : "#ffffff", duration:F(2), ease:"none" }}, t);
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
