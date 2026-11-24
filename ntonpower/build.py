"""Builds index.html (HyperFrames composition) for the NTONPOWER Travel Extension Lead UGC ad."""
import json, os

W = json.load(open("words.json"))
VID_END = 16.62           # last spoken frame of footage
TOTAL = 17.82             # + 1.2 s end card
HAS_CUT = os.path.exists("cut_hook.webm")

# palette (from product + packaging)
LIGHT, PINK, APRICOT, BLUE, INK = "#fcf2f5", "#ec6f8e", "#f6a55c", "#0071bc", "#2a1a20"

CHUNKS = [3, 3, 4, 3, 3, 4, 2, 2, 3, 3, 2, 2, 2, 2, 4]
KEY = {"socket", "penyelamat", "2", "plug,", "3", "USB.", "sekaligus.", "1.5", "meter",
       "gulung", "luggage.", "berebut.", "bawa", "ni."}
assert sum(CHUNKS) == len(W), (sum(CHUNKS), len(W))

caps_html, caps_js, groups, i = [], [], [], 0
for n in CHUNKS:
    groups.append(W[i:i + n]); i += n
for gi, g in enumerate(groups):
    s = g[0]["s"]
    nxt = groups[gi + 1][0]["s"] if gi + 1 < len(groups) else VID_END
    e = min(nxt, g[-1]["e"] + 0.3)
    keyidx = [wi for wi, w in enumerate(g) if w["w"] in KEY and not (w["w"] in ("bawa", "ni.") and gi < 10)]
    spans = []
    for wi, w in enumerate(g):
        cls = "w key" if wi in keyidx else "w"
        spans.append(f'<span id="c{gi}w{wi}" class="{cls}">{w["w"]}</span>')
    caps_html.append(f'<div id="cap{gi}" class="cap f-plus-jakarta-sans">{"".join(spans)}</div>')
    caps_js.append({"id": f"cap{gi}", "s": round(s, 2), "e": round(e, 2),
                    "w": [[f"c{gi}w{wi}", w["s"], wi in keyidx] for wi, w in enumerate(g)]})

SFX = [  # file, start, volume
    ("whoosh", 0.0, 0.5), ("hit", 0.02, 0.55), ("pop", 1.34, 0.4), ("pop", 1.58, 0.4), ("hit", 1.88, 0.35),
    ("swish", 2.14, 0.4), ("pop", 2.38, 0.4), ("riser", 2.57, 0.35), ("buzz", 2.81, 0.3),
    ("boom", 3.2, 0.6), ("chime", 3.21, 0.3), ("pop", 4.48, 0.4),
    ("swish", 4.98, 0.4), ("tick", 5.04, 0.5), ("tick", 5.19, 0.45), ("tick", 5.64, 0.5), ("tick", 5.79, 0.45),
    ("tick", 5.93, 0.45), ("whoosh", 6.46, 0.35), ("pop", 6.58, 0.4), ("pop", 7.02, 0.4), ("pop", 7.64, 0.4),
    ("chime", 7.89, 0.25), ("swish", 8.56, 0.4), ("tick", 9.1, 0.45), ("tick", 9.27, 0.45), ("tick", 9.43, 0.45),
    ("tick", 9.6, 0.45), ("tick", 9.77, 0.5), ("swish", 11.7, 0.4), ("pop", 11.81, 0.4), ("pop", 11.88, 0.4),
    ("pop", 12.86, 0.4), ("whoosh", 13.38, 0.35), ("whoosh", 14.72, 0.4),
    ("click", 15.82, 0.55), ("whoosh", 16.52, 0.45), ("chime", 16.76, 0.35),
]
sfx_html = "\n".join(
    f'  <audio id="sfx{k}" class="clip" src="audio/{f}.wav" data-start="{t}" data-duration="{min(1.4, round(TOTAL - t, 2))}" data-volume="{v}"></audio>'
    for k, (f, t, v) in enumerate(SFX))

ICON = {
 "phone": '<svg viewBox="0 0 48 48" width="64" height="64"><rect x="14" y="4" width="20" height="40" rx="4" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="24" cy="38" r="2.4" fill="currentColor"/></svg>',
 "buds": '<svg viewBox="0 0 48 48" width="64" height="64"><path d="M14 8a7 7 0 0 1 7 7v4a7 7 0 0 1-4 6.3V40h-6V15a7 7 0 0 1 3-7z" fill="currentColor"/><path d="M34 8a7 7 0 0 0-7 7v4a7 7 0 0 0 4 6.3V40h6V15a7 7 0 0 0-3-7z" fill="currentColor"/></svg>',
 "laptop": '<svg viewBox="0 0 48 48" width="64" height="64"><rect x="9" y="10" width="30" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="4"/><path d="M4 36h40l-3 4H7z" fill="currentColor"/></svg>',
 "check": '<svg viewBox="0 0 48 48" width="40" height="40"><path d="M10 25l9 9 19-20" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "down": '<svg viewBox="0 0 48 48" width="46" height="46"><path d="M24 8v28M12 26l12 12 12-12" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "hand": '<svg viewBox="0 0 64 80" width="96" height="120"><path d="M24 6a6 6 0 0 1 12 0v30l3-1a6 6 0 0 1 6 2l3-1a6 6 0 0 1 7 4l2-.5a6 6 0 0 1 7 6V60c0 10-8 18-18 18H34c-6 0-11-3-14-8L6 48a6 6 0 0 1 9-8l9 8z" fill="#fff" stroke="#2a1a20" stroke-width="4" stroke-linejoin="round"/></svg>',
}

cut_tag = ('<video id="cut" class="clip" src="cut_hook.webm" muted data-start="0" data-duration="3.2"></video>'
           if HAS_CUT else "")
bt_layer = "behind" if HAS_CUT else "front"

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/fonts.css">
<script src="vendor/gsap.min.js"></script>
<style>
:root{{--light:{LIGHT};--pink:{PINK};--apricot:{APRICOT};--blue:{BLUE};--ink:{INK}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F Plus Jakarta Sans",sans-serif}}
#ground{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 40%,#4a2a33,#140b0e)}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
#stage{{position:absolute;inset:0;overflow:hidden}}
#stage video{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}
#broll{{position:absolute;inset:0;overflow:hidden;opacity:0}}
#broll img{{position:absolute;left:0;top:0;width:1080px;height:1935px;transform-origin:62% 62%}}
#tint{{position:absolute;inset:0;background:#1b2a3a;mix-blend-mode:soft-light;opacity:0}}
#light{{position:absolute;inset:0;mix-blend-mode:soft-light;opacity:.6;
  background:radial-gradient(520px 620px at var(--lx,540px) var(--ly,700px),rgba(255,236,220,.8),rgba(255,236,220,0) 70%)}}
#glow{{position:absolute;inset:0;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(900px 760px at 30% 52%,rgba(255,170,150,.55),rgba(255,170,150,0) 70%)}}
#vig{{position:absolute;inset:0;background:radial-gradient(130% 95% at 50% 45%,rgba(0,0,0,0) 56%,rgba(18,6,10,.42) 100%)}}
/* hook kinetic words */
.bt{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;white-space:nowrap;opacity:0;line-height:.9;
  color:#fff;text-shadow:0 12px 44px rgba(60,10,25,.35)}}
#bt1{{top:150px;font-size:340px;color:var(--light)}}
#bt2{{top:860px;font-size:290px;color:#fff}}
#bt3{{top:1035px;left:auto;right:95px;margin:0;font-size:150px;color:#fff;background:var(--pink);padding:0 34px 8px;border-radius:30px;text-shadow:none;line-height:1.05}}
#pov{{position:absolute;left:60px;top:230px;opacity:0;font-size:44px;color:var(--ink);background:#fff;padding:8px 26px;border-radius:40px;
  box-shadow:0 14px 34px rgba(0,0,0,.3)}}
/* captions */
#captions{{position:absolute;left:0;right:0;top:1250px;height:200px}}
.cap{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;max-width:960px;text-align:center;opacity:0;
  font-size:72px;line-height:1.15;color:#fff;letter-spacing:-1px;
  text-shadow:0 4px 0 rgba(0,0,0,.3),0 0 24px rgba(0,0,0,.45),0 2px 3px rgba(0,0,0,.6)}}
.w{{display:inline-block;margin:0 9px;color:rgba(255,255,255,.55)}}
.w.key{{background:rgba(236,111,142,.0);padding:0 16px 6px;border-radius:18px;text-shadow:0 3px 10px rgba(0,0,0,.35)}}
/* problem chips */
.chip{{position:absolute;left:60px;height:96px;padding:0 36px 0 20px;border-radius:48px;display:flex;align-items:center;gap:18px;
  background:rgba(255,255,255,.94);color:var(--ink);font-size:42px;opacity:0;box-shadow:0 18px 40px rgba(10,10,25,.35)}}
.chip .x{{flex:0 0 58px;height:58px;border-radius:50%;background:#e0383e;color:#fff;font-size:34px;display:flex;align-items:center;justify-content:center}}
.chip .strike{{position:absolute;left:96px;right:28px;top:45px;height:7px;background:#e0383e;border-radius:4px;transform-origin:0 50%}}
#chip1{{top:930px}} #chip2{{top:1050px}}
/* reveal label */
#label{{position:absolute;left:56px;top:240px;opacity:0;text-align:left}}
#label .b{{display:inline-block;font-size:40px;letter-spacing:3px;color:#fff;background:var(--blue);padding:8px 24px;border-radius:30px}}
#label .n{{font-size:92px;color:#fff;line-height:.95;margin-top:10px;text-shadow:0 8px 30px rgba(0,0,0,.45)}}
#label .n span{{color:var(--pink)}}
/* counters (ports) */
.cnt{{position:absolute;top:250px;width:330px;text-align:center;opacity:0}}
.cnt .num{{font-size:250px;line-height:.85;color:#fff;text-shadow:0 10px 40px rgba(0,0,0,.45)}}
.cnt .lbl{{display:inline-block;margin-top:10px;font-size:40px;color:var(--ink);background:var(--light);padding:8px 26px;border-radius:30px}}
#cntA{{right:120px}} #cntB{{left:120px}}
#cntA .num{{color:var(--light)}} #cntB .num{{color:var(--pink)}}
.ring{{position:absolute;width:150px;height:150px;border-radius:50%;border:7px solid var(--apricot);opacity:0;
  box-shadow:0 0 34px rgba(246,165,92,.85),inset 0 0 24px rgba(246,165,92,.5)}}
.arrow{{position:absolute;height:7px;background:var(--apricot);border-radius:4px;transform-origin:0 50%;opacity:0;box-shadow:0 0 18px rgba(246,165,92,.7)}}
/* device icons */
#icons{{position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center;gap:34px}}
.ic{{flex:0 0 200px;height:200px;border-radius:44px;background:rgba(255,255,255,.95);color:var(--ink);opacity:0;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;font-size:30px;box-shadow:0 18px 40px rgba(0,0,0,.3)}}
.ic svg{{flex:0 0 64px}}
#all{{position:absolute;left:0;right:0;margin:0 auto;top:490px;width:fit-content;opacity:0;font-size:46px;color:#fff;background:var(--pink);
  padding:10px 30px 10px 20px;border-radius:40px;display:flex;align-items:center;gap:12px;box-shadow:0 14px 34px rgba(236,111,142,.5)}}
#all svg{{flex:0 0 40px}}
/* cord ruler */
#ruler{{position:absolute;left:70px;right:70px;top:240px;height:330px;opacity:0}}
#ruler .num{{font-size:230px;line-height:.85;color:#fff;text-shadow:0 10px 40px rgba(0,0,0,.45)}}
#ruler .num small{{font-size:120px;color:var(--pink)}}
#ruler .track{{position:absolute;left:0;right:0;top:230px;height:18px;border-radius:9px;background:rgba(255,255,255,.3)}}
#ruler .fill{{position:absolute;left:0;right:0;top:230px;height:18px;border-radius:9px;background:var(--apricot);transform-origin:0 50%}}
#ruler .ticks{{position:absolute;left:0;right:0;top:256px;height:30px;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.8) 0 4px,transparent 4px 93.5px)}}
#ruler .lbl{{position:absolute;right:0;top:20px;font-size:40px;color:var(--ink);background:var(--light);padding:8px 26px;border-radius:30px}}
/* pack steps */
#steps{{position:absolute;left:60px;top:250px;display:flex;flex-direction:column;gap:20px}}
.st{{display:flex;align-items:center;gap:16px;height:92px;padding:0 34px 0 16px;border-radius:46px;background:rgba(255,255,255,.95);
  color:var(--ink);font-size:44px;opacity:0;width:fit-content;box-shadow:0 16px 36px rgba(0,0,0,.3)}}
.st .d{{flex:0 0 62px;height:62px;border-radius:50%;background:var(--pink);color:#fff;display:flex;align-items:center;justify-content:center}}
#size{{position:absolute;right:60px;top:250px;width:300px;height:300px;opacity:0;text-align:center}}
#size svg{{position:absolute;inset:0}}
#size .v{{position:absolute;left:0;right:0;top:92px;font-size:120px;color:#fff;line-height:1;text-shadow:0 6px 24px rgba(0,0,0,.4)}}
#size .u{{position:absolute;left:0;right:0;top:206px;font-size:30px;color:#fff;letter-spacing:2px}}
/* payoff */
#pay{{position:absolute;right:70px;top:250px;opacity:0;text-align:right}}
#pay .a{{font-size:250px;color:#fff;line-height:1;text-shadow:0 10px 44px rgba(90,20,40,.5)}}
.spark{{position:absolute;width:34px;height:34px;opacity:0;
  background:radial-gradient(circle,#fff 0 18%,rgba(255,214,190,.95) 30%,rgba(255,214,190,0) 70%)}}
/* CTA card */
#cta{{position:absolute;left:60px;right:60px;top:200px;height:270px;border-radius:40px;background:rgba(252,242,245,.97);opacity:0;
  display:flex;align-items:center;gap:26px;padding:0 28px;box-shadow:0 30px 70px rgba(30,5,15,.45)}}
#cta img{{flex:0 0 210px;width:210px;height:210px;object-fit:contain;border-radius:26px;background:#fff}}
#cta .info{{flex:1 1 auto}}
#cta .brand{{font-size:30px;color:var(--blue);letter-spacing:3px}}
#cta .name{{font-size:42px;color:var(--ink);line-height:1.05;margin:4px 0 6px}}
#cta .tag{{font-size:52px;color:var(--pink);line-height:1;margin-bottom:12px}}
#btn{{display:inline-flex;align-items:center;gap:10px;background:var(--blue);color:#fff;font-size:38px;padding:10px 28px 10px 18px;border-radius:40px;
  box-shadow:0 10px 24px rgba(0,113,188,.45)}}
#btn svg{{flex:0 0 46px}}
#tap{{position:absolute;left:585px;top:414px;width:96px;height:120px;opacity:0}}
#tapring{{position:absolute;left:565px;top:358px;width:130px;height:130px;border-radius:50%;border:7px solid var(--apricot);opacity:0}}
/* watermark */
#wm{{position:absolute;left:0;right:0;margin:0 auto;top:790px;width:fit-content;font-size:64px;letter-spacing:4px;color:#fff;opacity:.3}}
/* end card */
#end{{position:absolute;inset:0;background:var(--light);opacity:0;overflow:hidden}}
#end .halo{{position:absolute;left:90px;top:420px;width:900px;height:900px;border-radius:50%;
  background:radial-gradient(circle,rgba(236,111,142,.28),rgba(236,111,142,0) 68%)}}
#end img.hero{{position:absolute;left:115px;top:520px;width:850px;height:707px;object-fit:contain}}
#end .logo{{position:absolute;left:0;right:0;margin:0 auto;top:250px;width:fit-content;font-size:44px;letter-spacing:6px;color:var(--blue);
  border:5px solid var(--blue);border-radius:50px;padding:6px 34px}}
#end .name{{position:absolute;left:0;right:0;margin:0 auto;top:350px;width:fit-content;font-size:46px;color:var(--ink)}}
#end .q{{position:absolute;left:0;right:0;margin:0 auto;top:1250px;width:fit-content;white-space:nowrap;font-size:120px;color:var(--pink);line-height:1}}
#end .s{{position:absolute;left:0;right:0;margin:0 auto;top:1395px;width:fit-content;font-size:44px;color:#fff;display:flex;align-items:center;gap:12px;
  background:var(--blue);padding:12px 34px 12px 22px;border-radius:44px}}
#end .s svg{{flex:0 0 46px}}
#end .by{{position:absolute;left:0;right:0;margin:0 auto;top:1500px;width:fit-content;font-size:34px;color:rgba(42,26,32,.6)}}
#disc{{position:absolute;left:0;right:0;margin:0 auto;top:1466px;width:fit-content;max-width:900px;text-align:center;font-size:25px;line-height:1.3;color:rgba(255,255,255,.85);
  text-shadow:0 1px 3px rgba(0,0,0,.8),0 0 10px rgba(0,0,0,.5)}}
#end .disc{{position:absolute;left:0;right:0;margin:0 auto;top:1580px;width:fit-content;max-width:900px;text-align:center;font-size:25px;line-height:1.3;color:rgba(42,26,32,.6)}}
.actual{{position:absolute;font-size:28px;letter-spacing:2px;color:#fff;background:rgba(42,26,32,.75);padding:6px 18px;border-radius:24px}}
#actB{{left:60px;top:1150px;opacity:0}}
#end .actual{{left:0;right:0;margin:0 auto;width:fit-content;top:470px;background:var(--pink)}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0}}
#bar{{position:absolute;left:0;bottom:0;height:8px;width:1080px;background:var(--apricot);transform-origin:0 50%}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="ground" class="clip" data-start="0" data-duration="{TOTAL}"></div>
  <div id="cam">
    <div id="stage">
      <video id="vid" class="clip" src="footage.mp4" data-start="0" data-duration="{VID_END}" data-has-audio="true"></video>
      <div id="broll"><img id="bimg" src="img/ports.jpg"></div>
      <div id="tint"></div>
      <div id="bt1" class="bt f-anton">SATU</div>
      {cut_tag}
      <div id="bt2" class="bt f-anton">SOCKET</div>
      <div id="bt3" class="bt f-anton">JE?!</div>
      <div id="light"></div>
      <div id="glow"></div>
    </div>
  </div>
  <div id="vig"></div>
  <div id="wm" class="f-plus-jakarta-sans">Wanderlogika</div>

  <div id="pov" class="f-plus-jakarta-sans">POV: hotel room</div>
  <div id="chip1" class="chip f-plus-jakarta-sans"><span class="x">✕</span>1 SOCKET JE<span class="strike"></span></div>
  <div id="chip2" class="chip f-plus-jakarta-sans"><span class="x">✕</span>BELAKANG KATIL<span class="strike"></span></div>

  <div id="label"><div class="b f-plus-jakarta-sans">NTONPOWER</div><div class="n f-anton">TRAVEL<br><span>EXTENSION</span><br>LEAD</div></div>

  <div id="cntA" class="cnt"><div class="num f-anton"><span id="nA">0</span></div><div class="lbl f-plus-jakarta-sans">UK PLUG</div></div>
  <div id="cntB" class="cnt"><div class="num f-anton"><span id="nB">0</span></div><div class="lbl f-plus-jakarta-sans">USB-A + C</div></div>
  <div id="arA" class="arrow" style="left:795px;top:610px;width:350px"></div>
  <div id="arB" class="arrow" style="left:285px;top:610px;width:530px"></div>
  <div id="rgA" class="ring" style="left:870px;top:925px"></div>
  <div id="rgB" class="ring" style="left:615px;top:975px"></div>

  <div id="icons">
    <div id="ic0" class="ic f-plus-jakarta-sans">{ICON['phone']}Phone</div>
    <div id="ic1" class="ic f-plus-jakarta-sans">{ICON['buds']}Earbuds</div>
    <div id="ic2" class="ic f-plus-jakarta-sans">{ICON['laptop']}Laptop</div>
  </div>
  <div id="all" class="f-plus-jakarta-sans">{ICON['check']}5-in-1, sekaligus</div>

  <div id="ruler"><div class="num f-anton"><span id="nM">0.0</span><small> M</small></div><div class="lbl f-plus-jakarta-sans">WAYAR</div>
    <div class="track"></div><div class="fill"></div><div class="ticks"></div></div>

  <div id="steps">
    <div id="st1" class="st f-plus-jakarta-sans"><span class="d">{ICON['check']}</span>Gulung</div>
    <div id="st2" class="st f-plus-jakarta-sans"><span class="d">{ICON['check']}</span>Masuk luggage</div>
  </div>
  <div id="size"><svg viewBox="0 0 300 300"><circle cx="150" cy="150" r="132" fill="rgba(42,26,32,.35)" stroke="rgba(255,255,255,.3)" stroke-width="10"/>
    <circle id="sarc" cx="150" cy="150" r="132" fill="none" stroke="{APRICOT}" stroke-width="12" stroke-linecap="round"
      stroke-dasharray="829" stroke-dashoffset="829" transform="rotate(-90 150 150)"/></svg>
    <div class="v f-anton"><span id="nS">0</span></div><div class="u f-plus-jakarta-sans">MM · COMPACT</div></div>


  <div id="cta"><img src="img/product.png"><div class="info"><div class="brand f-plus-jakarta-sans">NTONPOWER</div>
    <div class="name f-plus-jakarta-sans">Travel Extension Lead</div><div class="tag f-instrument-serif">Travel must have!</div>
    <div id="btn" class="f-plus-jakarta-sans">{ICON['down']}link below!</div></div></div>
  <div id="tapring"></div><div id="tap">{ICON['hand']}</div>

  <div id="actB" class="actual f-plus-jakarta-sans">ACTUAL PRODUCT PHOTO</div>
  <div id="disc" class="f-plus-jakarta-sans">Visuals for illustration only. Actual product may differ — please refer to the actual product photo &amp; description.</div>
  <div id="captions">
    {"".join(caps_html)}
  </div>

  <div id="end">
    <div class="halo"></div>
    <div class="logo f-plus-jakarta-sans">NTONPOWER</div>
    <div class="name f-plus-jakarta-sans">Travel Extension Lead</div>
    <img class="hero" src="img/product_end.png">
    <div class="q f-instrument-serif">Travel must have!</div>
    <div class="s f-plus-jakarta-sans">{ICON['down']}link below!</div>
    <div class="actual f-plus-jakarta-sans">ACTUAL PRODUCT</div>
    <div class="by f-plus-jakarta-sans">by @Wanderlogika</div>
    <div class="disc f-plus-jakarta-sans">Actual product may differ from visuals shown. Please refer to the actual product photo &amp; description.</div>
  </div>
  <div id="flash"></div>
  <div id="bar"></div>
{sfx_html}
</div>
<script>
const FPS = 30, F = n => n / FPS;
const E = {{ land:"power3.out", soft:"power2.out", snap:"expo.out", settle:"back.out(1.15)", exit:"power2.in", throw:"power4.in", move:"power2.inOut" }};
const tl = gsap.timeline({{ paused: true }});
const CAPS = {json.dumps(caps_js)};
const count = (id, from, to, t, d, dec) => {{
  const o = {{ v: from }};
  tl.to(o, {{ v: to, duration: d, ease: E.move, onUpdate: () => {{ const el = document.getElementById(id); if (el) el.textContent = o.v.toFixed(dec); }} }}, t);
}};

// ---------- camera: per-shot origin + key light that follows the face ----------
const SHOTS = [ // t, origin, light x, light y
  [0.0, "52% 34%", 560, 640], [3.2, "45% 40%", 520, 600], [4.98, "62% 55%", 760, 1050],
  [6.48, "55% 55%", 600, 950], [8.58, "50% 45%", 560, 860], [11.72, "50% 50%", 560, 980], [13.4, "35% 35%", 420, 720] ];
SHOTS.forEach(([t,o,lx,ly]) => {{
  tl.set("#cam", {{ transformOrigin:o, scale:1, x:0 }}, t);
  tl.set("#light", {{ "--lx": lx+"px", "--ly": ly+"px" }}, t);
}});
tl.fromTo("#cam", {{ scale:1.15 }}, {{ scale:1.0, duration:F(10), ease:E.snap, immediateRender:false }}, 0.0);
const PUNCH = [[1.58,1.06],[4.48,1.06],[7.82,1.06],[9.1,1.08],[11.88,1.06],[14.1,1.05],[15.82,1.1]];
PUNCH.forEach(([t,s]) => tl.to("#cam", {{ scale:s, duration:F(7), ease:E.snap }}, t));
tl.fromTo("#cam", {{ scale:1.1 }}, {{ scale:1.0, duration:F(9), ease:E.snap, immediateRender:false }}, 3.2);

// ---------- hook: flash + giant words ({bt_layer} the speaker) ----------
tl.fromTo("#flash", {{ opacity:1 }}, {{ opacity:0, duration:F(7), ease:E.exit }}, 0.0);
tl.fromTo("#pov", {{ opacity:0, x:-200 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 0.12);
tl.to("#pov", {{ opacity:0, x:-160, duration:F(6), ease:E.exit }}, 1.94);
tl.fromTo("#bt1", {{ opacity:0, scale:2.2 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 1.32);
tl.fromTo("#bt2", {{ opacity:0, x:-500 }}, {{ opacity:1, x:0, duration:F(8), ease:E.snap }}, 1.55);
tl.fromTo("#bt3", {{ opacity:0, scale:1.8, rotation:-6 }}, {{ opacity:1, scale:1, rotation:-4, duration:F(7), ease:E.snap }}, 1.86);
tl.to(["#bt1","#bt2","#bt3"], {{ opacity:0, y:-80, duration:F(6), ease:E.throw, stagger:F(2) }}, 2.1);

// ---------- problem: cooler mood + chips ----------
tl.to("#tint", {{ opacity:.6, duration:F(8), ease:E.soft }}, 2.08);
tl.to("#stage", {{ filter:"saturate(0.72) brightness(0.95)", duration:F(8), ease:E.soft }}, 2.08);
[["#chip1",2.14],["#chip2",2.35]].forEach(([id,t]) =>
  tl.fromTo(id, {{ opacity:0, x:-420 }}, {{ opacity:1, x:0, duration:F(9), ease:E.land }}, t));
tl.fromTo(".chip .strike", {{ scaleX:0 }}, {{ scaleX:1, duration:F(6), ease:E.snap, stagger:F(3) }}, 2.75);
tl.to(["#chip1","#chip2"], {{ x:(i)=>[-14,12][i], duration:F(2), ease:"none", yoyo:true, repeat:3 }}, 2.86);
tl.to("#cam", {{ x:9, duration:F(2), ease:"none", yoyo:true, repeat:3 }}, 2.86);
tl.to(["#chip1","#chip2"], {{ opacity:0, x:-500, duration:F(5), ease:E.throw, stagger:F(2) }}, 3.04);

// ---------- reveal: flash, warm glow, colour back ----------
tl.fromTo("#flash", {{ opacity:.85 }}, {{ opacity:0, duration:F(6), ease:E.exit, immediateRender:false }}, 3.2);
tl.set("#tint", {{ opacity:0 }}, 3.2);
tl.set("#stage", {{ filter:"saturate(1.06) brightness(1.02)" }}, 3.2);
tl.fromTo("#glow", {{ opacity:.55 }}, {{ opacity:.25, duration:1.2, ease:E.soft, immediateRender:false }}, 3.2);
tl.fromTo("#label", {{ opacity:0, x:-380 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 3.59);
tl.to("#label", {{ opacity:0, x:-300, duration:F(6), ease:E.throw }}, 4.8);
tl.to("#glow", {{ opacity:0, duration:F(6), ease:E.exit }}, 4.84);
tl.to("#stage", {{ filter:"saturate(1) brightness(1)", duration:F(6), ease:E.exit }}, 4.84);

// ---------- feature 1: 2 plug, 3 USB (real product photo) ----------
tl.set("#broll", {{ opacity:1 }}, 4.98);
tl.set("#broll", {{ opacity:0 }}, 6.48);
tl.fromTo("#actB", {{ opacity:0, x:-200 }}, {{ opacity:1, x:0, duration:F(8), ease:E.land }}, 5.02);
tl.set("#actB", {{ opacity:0 }}, 6.48);
// bed shots: product sits at the bottom, so lift the disclaimer above the captions
tl.set("#disc", {{ y:-300 }}, 13.40);
tl.fromTo("#bimg", {{ scale:1.28, y:-120 }}, {{ scale:1.12, y:-210, duration:1.5, ease:"none" }}, 4.98);
tl.fromTo("#cntA", {{ opacity:0, y:-160 }}, {{ opacity:1, y:0, duration:F(8), ease:E.snap }}, 5.02);
count("nA", 0, 2, 5.04, 0.18, 0);
tl.fromTo("#cntB", {{ opacity:0, y:-160 }}, {{ opacity:1, y:0, duration:F(8), ease:E.snap }}, 5.58);
count("nB", 0, 3, 5.64, 0.3, 0);
tl.fromTo("#arA", {{ opacity:0, scaleX:0.05, rotation:69 }}, {{ opacity:1, scaleX:1, rotation:69, duration:F(10), ease:E.soft }}, 5.21);
tl.fromTo("#arB", {{ opacity:0, scaleX:0.05, rotation:48 }}, {{ opacity:1, scaleX:1, rotation:48, duration:F(10), ease:E.soft }}, 5.83);
tl.fromTo("#rgA", {{ opacity:0, scale:1.8 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 5.4);
tl.fromTo("#rgB", {{ opacity:0, scale:1.8 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 5.99);
tl.to(["#rgA","#rgB"], {{ scale:1.12, duration:F(7), ease:E.move, yoyo:true, repeat:1 }}, 6.17);
tl.to(["#cntA","#cntB","#arA","#arB","#rgA","#rgB"], {{ opacity:0, y:-120, duration:F(6), ease:E.throw }}, 6.29);

// ---------- feature 2: phone, earbuds, laptop ----------
[["#ic0",6.57],["#ic1",7.0],["#ic2",7.62]].forEach(([id,t]) =>
  tl.fromTo(id, {{ opacity:0, y:-220 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, t));
tl.fromTo("#all", {{ opacity:0, scale:1.7 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 7.84);
tl.to(["#ic0","#ic1","#ic2","#all"], {{ opacity:0, y:-160, duration:F(6), ease:E.throw, stagger:F(1) }}, 8.36);

// ---------- feature 3: 1.5 m cord ----------
tl.fromTo("#ruler", {{ opacity:0, x:-300 }}, {{ opacity:1, x:0, duration:F(10), ease:E.land }}, 8.6);
tl.fromTo("#ruler .fill", {{ scaleX:0.02 }}, {{ scaleX:1, duration:0.8, ease:E.move }}, 9.06);
count("nM", 0, 1.5, 9.06, 0.8, 1);
tl.to("#ruler", {{ opacity:0, x:300, duration:F(6), ease:E.throw }}, 11.5);

// ---------- feature 4: guna, gulung, masuk luggage + compact size ----------
[["#st1",11.86],["#st2",12.48]].forEach(([id,t]) =>
  tl.fromTo(id, {{ opacity:0, x:-420 }}, {{ opacity:1, x:0, duration:F(9), ease:E.land }}, t));
tl.fromTo("#size", {{ opacity:0, scale:1.6 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 11.88);
tl.to("#sarc", {{ attr:{{ "stroke-dashoffset":0 }}, duration:0.9, ease:E.move }}, 11.93);
tl.to("#size svg", {{ rotation:360, duration:1.3, ease:E.move }}, 11.9);
count("nS", 0, 120, 11.93, 0.9, 0);
tl.to(["#st1","#st2","#size"], {{ opacity:0, y:-140, duration:F(6), ease:E.throw, stagger:F(1) }}, 13.21);

// ---------- payoff: big serif word + sparkles ----------
tl.fromTo("#glow", {{ opacity:0 }}, {{ opacity:.35, duration:F(14), ease:E.soft, immediateRender:false }}, 13.4);

// ---------- CTA: product card + tap ----------
tl.fromTo("#cta", {{ opacity:0, y:-260 }}, {{ opacity:1, y:0, duration:F(12), ease:E.land }}, 14.76);
tl.fromTo("#tap", {{ opacity:0, x:240, y:260 }}, {{ opacity:1, x:0, y:0, duration:F(11), ease:E.land }}, 15.26);
tl.to("#tap", {{ scale:.84, duration:F(3), ease:E.exit }}, 15.74);
tl.to("#tap", {{ scale:1, duration:F(5), ease:E.land }}, 15.88);
tl.set("#tapring", {{ opacity:1, scale:.5 }}, 15.82);
tl.to("#tapring", {{ opacity:0, scale:2.3, duration:F(14), ease:E.soft }}, 15.82);
tl.fromTo("#btn", {{ scale:1.16 }}, {{ scale:1, duration:F(9), ease:E.snap, immediateRender:false }}, 15.82);
tl.to("#glow", {{ opacity:0, duration:F(8), ease:E.exit }}, 15.48);

// ---------- end card (loops into the white flash of the hook) ----------
tl.fromTo("#end", {{ opacity:1, y:1920 }}, {{ opacity:1, y:0, duration:F(8), ease:E.land }}, {VID_END - 0.08});
tl.fromTo("#end img.hero", {{ scale:1.14, rotation:-3 }}, {{ scale:1.0, rotation:0, duration:1.2, ease:E.soft }}, {VID_END - 0.08});
tl.fromTo("#end .q", {{ opacity:0, y:70 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END + 0.12});
tl.fromTo("#end .s", {{ opacity:0, y:70 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END + 0.24});
tl.fromTo("#end .by", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END + 0.34});
tl.to("#end .s", {{ scale:1.06, duration:F(8), ease:E.move, yoyo:true, repeat:1 }}, {VID_END + 0.6});
tl.set(["#cta","#tap","#captions","#wm","#disc"], {{ opacity:0 }}, {VID_END});
tl.to("#end", {{ backgroundColor:"#ffffff", duration:F(6), ease:"none" }}, {TOTAL - 0.2});

// ---------- watermark: 1.0 -> 1.12 -> 1.0, twice every 5 s ----------
tl.fromTo("#wm", {{ scale:1 }}, {{ scale:1.12, duration:1.25, ease:"sine.inOut", yoyo:true, repeat:{int(VID_END / 1.25)} }}, 0);

// ---------- captions (karaoke) ----------
CAPS.forEach(c => {{
  tl.fromTo("#"+c.id, {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:F(6), ease:E.land }}, c.s);
  c.w.forEach(([id, t, key]) => {{
    if (key) tl.to("#"+id, {{ color:"#ffffff", backgroundColor:"{PINK}", duration:F(2), ease:"none" }}, t);
    else tl.to("#"+id, {{ color:"#ffffff", duration:F(2), ease:"none" }}, t);
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
print("index.html written,", len(groups), "caption chunks, cutout:", HAS_CUT)
