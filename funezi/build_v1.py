"""FUNEZI Universal Travel Adapter — Premium UGC Ad (SimHome style, new font set).
Builds index.html (HyperFrames composition) from words.json + cutlist.json."""
import json

W = json.load(open("words.json"))
TOTAL = 20.0
VID_END = 18.8333
# captions start after the cold open (words 0-2 are shown as big hook type)
CHUNKS = [2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 1]
CW = W[3:]
assert sum(CHUNKS) == len(CW), (sum(CHUNKS), len(CW))
EMPH = {"gadget", "banyak?", "kena", "4", "USB", "type", "C,", "universal", "soket.",
        "tukar-tukar.", "Kecil", "beg.", "gadget.", "settle."}

caps_html, caps_js, groups, i = [], [], [], 0
for n in CHUNKS:
    groups.append(CW[i:i + n]); i += n
for gi, g in enumerate(groups):
    s = g[0]["s"] - 0.04
    nxt = groups[gi + 1][0]["s"] - 0.04 if gi + 1 < len(groups) else VID_END
    e = min(nxt, g[-1]["e"] + 0.35)
    spans = [f'<span id="c{gi}w{wi}" class="{"w emph" if w["w"] in EMPH else "w"}">{w["w"]}</span>' for wi, w in enumerate(g)]
    caps_html.append(f'<div id="cap{gi}" class="cap">{"".join(spans)}</div>')
    caps_js.append({"id": f"cap{gi}", "s": round(s, 2), "e": round(e, 2),
                    "w": [[f"c{gi}w{wi}", w["s"], w["w"] in EMPH] for wi, w in enumerate(g)]})

SFX = [  # file, start, volume
    ("whoosh", 0.00, 0.55), ("hit", 0.04, 0.6), ("swish", 0.36, 0.4), ("shimmer", 1.00, 0.5),
    ("whoosh", 1.42, 0.5), ("hit", 1.52, 0.45), ("pop", 2.36, 0.45), ("buzz", 2.72, 0.35),
    ("boom", 3.14, 0.7), ("swish", 3.66, 0.4), ("chime", 3.70, 0.3),
    ("whoosh", 4.74, 0.45), ("tick", 6.02, 0.5), ("tick", 6.12, 0.45), ("tick", 6.22, 0.45), ("tick", 6.32, 0.5),
    ("click", 6.62, 0.5), ("swish", 7.34, 0.45), ("pop", 7.76, 0.45),
    ("riser", 8.30, 0.35), ("shimmer", 8.90, 0.45), ("chime", 9.46, 0.3),
    ("whoosh", 9.88, 0.45), ("pop", 10.26, 0.45), ("pop", 10.98, 0.45), ("pop", 11.64, 0.45), ("pop", 12.20, 0.45),
    ("swish", 13.12, 0.45), ("whoosh", 13.72, 0.4), ("tick", 14.20, 0.45), ("click", 15.14, 0.45),
    ("whoosh", 15.80, 0.45), ("pop", 16.72, 0.4), ("swish", 17.30, 0.45),
    ("click", 18.32, 0.6), ("chime", 18.36, 0.4), ("whoosh", 18.74, 0.5), ("shimmer", 18.95, 0.4),
]
sfx_html = "\n".join(
    f'  <audio id="sfx{k}" class="clip" src="audio/{f}.wav" data-start="{t}" data-duration="{min(1.4, round(TOTAL - t, 2))}" data-volume="{v}"></audio>'
    for k, (f, t, v) in enumerate(SFX))

PLANE = ('<svg viewBox="0 0 24 24" width="30" height="30"><path d="M21 15.5v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V8.5l-8 5v2l8-2.5V18l-2 1.5V21l3.5-1 3.5 1v-1.5L13 18v-5z" fill="currentColor"/></svg>')
CART = ('<svg viewBox="0 0 48 48" width="50" height="50"><path d="M6 8h6l5 22h20l5-15H15" fill="none" stroke="#0c1422" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="20" cy="38" r="3.5" fill="#0c1422"/><circle cx="34" cy="38" r="3.5" fill="#0c1422"/></svg>')
SWAP = ('<svg viewBox="0 0 48 48" width="120" height="120"><path d="M10 18h26l-7-7M38 30H12l7 7" fill="none" stroke="#5ab8ff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
DEV = {
 "phone": '<svg viewBox="0 0 48 48" width="64" height="64"><rect x="14" y="5" width="20" height="38" rx="4" fill="none" stroke="#f6f1e8" stroke-width="3.5"/><path d="M21 37h6" stroke="#f6f1e8" stroke-width="3" stroke-linecap="round"/></svg>',
 "laptop": '<svg viewBox="0 0 48 48" width="64" height="64"><rect x="9" y="11" width="30" height="20" rx="2.5" fill="none" stroke="#f6f1e8" stroke-width="3.5"/><path d="M4 37h40" stroke="#f6f1e8" stroke-width="3.5" stroke-linecap="round"/></svg>',
 "buds": '<svg viewBox="0 0 48 48" width="64" height="64"><path d="M15 10a6 6 0 0 1 6 6v6a6 6 0 0 1-4 5.6V38h-4V27.6A6 6 0 0 1 9 22v-6a6 6 0 0 1 6-6zM33 10a6 6 0 0 0-6 6v6a6 6 0 0 0 4 5.6V38h4V27.6a6 6 0 0 0 4-5.6v-6a6 6 0 0 0-6-6z" fill="none" stroke="#f6f1e8" stroke-width="3.2"/></svg>',
 "watch": '<svg viewBox="0 0 48 48" width="64" height="64"><rect x="13" y="12" width="22" height="24" rx="6" fill="none" stroke="#f6f1e8" stroke-width="3.5"/><path d="M18 12l2-7h8l2 7M18 36l2 7h8l2-7" fill="none" stroke="#f6f1e8" stroke-width="3"/></svg>',
 "tablet": '<svg viewBox="0 0 48 48" width="64" height="64"><rect x="8" y="6" width="32" height="36" rx="4" fill="none" stroke="#f6f1e8" stroke-width="3.5"/><circle cx="24" cy="36" r="1.8" fill="#f6f1e8"/></svg>',
}
dev_html = "".join(f'<div class="dev" id="dev{k}">{svg}<div class="bat"><i></i></div></div>' for k, svg in enumerate(DEV.values()))

html = f"""<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/fonts.css">
<script src="vendor/gsap.min.js"></script>
<style>
:root{{--ink:#0c1422;--navy:#14284a;--cream:#f6f1e8;--led:#5ab8ff;--gold:#f3c766;--sand:#e9dcc6}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F Bricolage Grotesque",sans-serif}}
#ground{{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 40%,#1d2d48,#070b13)}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
#stage{{position:absolute;inset:0;overflow:hidden}}
#stage video{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}
#tint{{position:absolute;inset:0;background:#10233d;mix-blend-mode:soft-light;opacity:0}}
#light{{position:absolute;inset:0;mix-blend-mode:soft-light;opacity:.5;
  background:radial-gradient(520px 620px at var(--lx,540px) var(--ly,640px),rgba(255,238,220,.8),rgba(255,238,220,0) 70%)}}
#glow{{position:absolute;inset:0;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(900px 700px at 80% 12%,rgba(255,205,150,.5),rgba(255,205,150,0) 70%)}}
#coolglow{{position:absolute;inset:0;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(800px 600px at 30% 30%,rgba(90,184,255,.45),rgba(90,184,255,0) 70%)}}
#vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(130% 95% at 50% 45%,rgba(0,0,0,0) 55%,rgba(6,10,18,.45) 100%)}}
#grain{{position:absolute;inset:-50%;opacity:.05;mix-blend-mode:overlay;
  background-image:repeating-radial-gradient(circle at 17% 32%,#fff 0 1px,transparent 1px 3px),repeating-radial-gradient(circle at 73% 61%,#000 0 1px,transparent 1px 4px)}}
/* cold open */
#co{{position:absolute;inset:0;overflow:hidden;background:radial-gradient(90% 60% at 50% 48%,#1f3a63 0%,#0c1422 62%,#05080e 100%)}}
#co .halo{{position:absolute;left:140px;top:560px;width:800px;height:800px;border-radius:50%;
  background:radial-gradient(circle,rgba(90,184,255,.42),rgba(90,184,255,0) 65%)}}
#co .ring{{position:absolute;left:190px;top:610px;width:700px;height:700px;border-radius:50%;border:3px solid rgba(246,241,232,.22)}}
#co .ring2{{position:absolute;left:250px;top:670px;width:580px;height:580px;border-radius:50%;border:2px dashed rgba(90,184,255,.5)}}
#co img{{position:absolute;left:215px;top:640px;width:650px;height:auto;filter:drop-shadow(0 50px 60px rgba(0,0,0,.6))}}
#co .t1{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:250px;font-size:200px;line-height:.92;color:var(--cream);text-align:center;letter-spacing:2px}}
#co .t2{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1360px;font-size:210px;color:var(--gold);line-height:1}}
#co .pill{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1610px;font-size:38px;color:var(--cream);opacity:.85}}
/* text behind */
.bt{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;color:var(--cream);opacity:0;white-space:nowrap;text-shadow:0 10px 40px rgba(10,20,40,.35)}}
#bt1{{top:170px;font-size:330px;letter-spacing:4px;line-height:1}}
#bt2{{top:170px;font-size:330px;letter-spacing:4px;line-height:1;color:#dff0ff}}
#bt3{{top:150px;font-size:300px;line-height:1;color:var(--gold)}}
/* captions */
#captions{{position:absolute;left:0;right:0;top:1230px;height:200px}}
.cap{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;max-width:980px;text-align:center;opacity:0;
  font-size:74px;line-height:1.1;color:#fff;letter-spacing:-1px;
  text-shadow:0 4px 0 rgba(0,0,0,.35),0 0 24px rgba(0,0,0,.45),0 2px 3px rgba(0,0,0,.6)}}
.w{{display:inline-block;margin:0 9px;color:rgba(255,255,255,.6)}}
.w.emph{{background:var(--navy);color:var(--cream);padding:2px 18px 8px;border-radius:16px;text-shadow:none;
  box-shadow:0 10px 30px rgba(5,10,25,.45),inset 0 -4px 0 var(--led)}}
/* reveal tag */
#ring{{position:absolute;left:600px;top:640px;width:300px;height:300px;border-radius:50%;border:6px solid var(--led);opacity:0;
  box-shadow:0 0 40px rgba(90,184,255,.85),inset 0 0 30px rgba(90,184,255,.45)}}
#tag{{position:absolute;left:70px;top:990px;opacity:0}}
#tag .b{{font-size:112px;color:var(--cream);line-height:.9;letter-spacing:3px;text-shadow:0 8px 30px rgba(0,0,0,.5)}}
#tag .s{{margin-top:12px;display:inline-block;font-size:34px;color:var(--ink);background:var(--cream);padding:8px 22px;border-radius:30px}}
/* 4 USB */
#usb{{position:absolute;left:70px;top:230px;opacity:0;display:flex;align-items:center;gap:26px}}
#usb .n{{font-size:300px;line-height:.85;color:var(--cream);text-shadow:0 10px 40px rgba(0,0,0,.45)}}
#usb .l{{font-size:64px;line-height:1;color:var(--cream)}}
#usb .dots{{display:flex;gap:14px;margin-top:18px}}
#usb .dots i{{display:block;width:44px;height:44px;border-radius:12px;border:4px solid rgba(246,241,232,.5);background:rgba(246,241,232,.08)}}
#pring{{position:absolute;left:190px;top:660px;width:560px;height:320px;border-radius:40px;border:6px solid var(--led);opacity:0;
  box-shadow:0 0 40px rgba(90,184,255,.8)}}
/* type c pill */
#tc{{position:absolute;right:70px;top:250px;opacity:0;text-align:right}}
#tc .a{{font-size:190px;line-height:.9;color:var(--cream);text-shadow:0 10px 40px rgba(0,0,0,.5)}}
#tc .b{{display:inline-block;margin-top:10px;font-size:36px;color:var(--ink);background:var(--led);padding:8px 22px;border-radius:30px}}
/* universal */
#uni{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:210px;text-align:center;opacity:0}}
#uni .a{{font-size:150px;color:var(--ink);line-height:1}}
#uni .b{{font-size:230px;color:var(--ink);line-height:.9;letter-spacing:4px}}
#globe{{position:absolute;left:0;right:0;margin:0 auto;top:1530px;width:fit-content;opacity:0;display:flex;align-items:center;gap:20px;
  background:var(--ink);color:var(--cream);padding:14px 34px 14px 18px;border-radius:60px;font-size:50px;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
#globe svg{{flex:0 0 70px}}
/* plugs */
.plug{{position:absolute;width:220px;height:120px;border-radius:26px;background:rgba(246,241,232,.94);color:var(--ink);opacity:0;
  display:flex;align-items:center;justify-content:center;font-size:72px;letter-spacing:2px;box-shadow:0 18px 40px rgba(5,10,25,.35)}}
.plug b{{position:absolute;top:-14px;right:-14px;width:44px;height:44px;border-radius:50%;background:var(--led);color:var(--ink);font-size:28px;
  display:flex;align-items:center;justify-content:center}}
#p0{{left:60px;top:230px}} #p1{{left:300px;top:230px}} #p2{{left:540px;top:230px}} #p3{{left:780px;top:230px;width:240px}}
#swap{{position:absolute;left:0;right:0;margin:0 auto;width:120px;top:390px;opacity:0}}
/* size */
.stat{{position:absolute;top:300px;opacity:0;text-align:center;width:280px}}
.stat .v{{font-size:120px;color:var(--cream);line-height:.9;text-shadow:0 8px 30px rgba(0,0,0,.5)}}
.stat .k{{display:inline-block;margin-top:8px;font-size:32px;color:var(--ink);background:var(--gold);padding:6px 18px;border-radius:26px}}
#st0{{left:40px}} #st1{{right:40px}}
#kecil{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:880px;font-size:170px;color:var(--cream);opacity:0;
  text-shadow:0 10px 40px rgba(0,0,0,.5)}}
/* b-roll card */
#card{{position:absolute;left:80px;top:230px;width:920px;height:720px;border-radius:40px;overflow:hidden;opacity:0;
  box-shadow:0 40px 90px rgba(5,10,25,.5);border:6px solid rgba(246,241,232,.9)}}
#card img{{position:absolute;left:0;top:-330px;width:920px;height:auto}}
#devs{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:990px;display:flex;gap:18px;opacity:0}}
.dev{{width:150px;height:150px;border-radius:30px;background:rgba(12,20,34,.82);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;
  box-shadow:0 16px 36px rgba(0,0,0,.35)}}
.dev svg{{flex:0 0 64px}}
.bat{{width:90px;height:14px;border-radius:7px;background:rgba(246,241,232,.25);overflow:hidden}}
.bat i{{display:block;height:100%;width:100%;background:#58e08a;transform-origin:0 50%}}
#five{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1160px;opacity:0;font-size:44px;color:var(--ink);background:var(--gold);padding:8px 26px;border-radius:30px}}
/* CTA */
#cta{{position:absolute;left:60px;right:60px;top:220px;height:290px;border-radius:38px;background:rgba(246,241,232,.96);opacity:0;
  display:flex;align-items:center;gap:26px;padding:0 30px;box-shadow:0 30px 70px rgba(5,10,25,.45)}}
#cta .ph{{flex:0 0 210px;width:210px;height:210px;border-radius:26px;background:radial-gradient(circle at 50% 40%,#2a456f,#0c1422);display:flex;align-items:center;justify-content:center}}
#cta .ph img{{width:175px;height:auto}}
#cta .info{{flex:1 1 auto}}
#cta .brand{{font-size:34px;color:#3a6ea8}}
#cta .name{{font-size:44px;color:var(--ink);line-height:1.02;margin:2px 0 8px}}
#cta .rate{{font-size:28px;color:#5b6475;margin-bottom:12px}}
#cta .rate b{{color:#e9a400}}
#btn{{display:inline-flex;align-items:center;gap:10px;background:var(--gold);color:var(--ink);font-size:36px;padding:10px 26px 10px 16px;border-radius:40px;
  box-shadow:0 10px 24px rgba(243,199,102,.5)}}
#btn svg{{flex:0 0 50px}}
#tap{{position:absolute;left:560px;top:450px;width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.85);border:5px solid var(--ink);opacity:0}}
#tapring{{position:absolute;left:535px;top:425px;width:120px;height:120px;border-radius:50%;border:6px solid var(--gold);opacity:0}}
/* end card */
#end{{position:absolute;inset:0;background:radial-gradient(90% 60% at 50% 45%,#1f3a63 0%,#0c1422 65%,#05080e 100%);opacity:0;overflow:hidden}}
#end .halo{{position:absolute;left:190px;top:470px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(90,184,255,.4),rgba(90,184,255,0) 65%)}}
#end img{{position:absolute;left:250px;top:520px;width:580px;height:auto;filter:drop-shadow(0 40px 50px rgba(0,0,0,.6))}}
#end .logo{{position:absolute;left:0;right:0;margin:0 auto;top:250px;width:fit-content;font-size:110px;color:var(--cream);letter-spacing:10px}}
#end .sub{{position:absolute;left:0;right:0;margin:0 auto;top:385px;width:fit-content;font-size:38px;color:var(--sand);letter-spacing:2px}}
#end .q{{position:absolute;left:0;right:0;margin:0 auto;top:1180px;width:fit-content;white-space:nowrap;font-size:104px;color:var(--gold)}}
#end .s{{position:absolute;left:0;right:0;margin:0 auto;top:1340px;width:fit-content;font-size:42px;color:var(--ink);display:flex;align-items:center;gap:12px;
  background:var(--gold);padding:12px 34px 12px 20px;border-radius:44px}}
/* watermark */
#wm{{position:absolute;left:56px;top:206px;display:flex;align-items:center;gap:10px;color:var(--cream);opacity:.62;font-size:32px;letter-spacing:1px;
  text-shadow:0 2px 10px rgba(0,0,0,.45)}}
#wm svg{{flex:0 0 30px;transform:rotate(45deg)}}
#flash{{position:absolute;inset:0;background:#f4f9ff;opacity:0}}
#bar{{position:absolute;left:0;bottom:0;height:8px;width:1080px;background:var(--led);transform-origin:0 50%;opacity:.85}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <div id="ground" class="clip" data-start="0" data-duration="{TOTAL}"></div>
  <div id="cam">
    <div id="stage">
      <video id="vid" class="clip" src="footage.mp4" data-start="0" data-duration="{VID_END}" data-has-audio="true"></video>
      <div id="tint"></div>
      <div id="bt1" class="bt f-anton">TRAVEL</div>
      <div id="bt2" class="bt f-anton">GADGET</div>
      <div id="bt3" class="bt f-instrument-serif">banyak?</div>
      <video id="cut" class="clip" src="cut_hook.webm" muted data-start="1.5" data-duration="1.6"></video>
      <div id="light"></div>
      <div id="glow"></div>
      <div id="coolglow"></div>
    </div>
  </div>
  <div id="vig"></div>
  <div id="grain"></div>

  <div id="ring"></div>
  <div id="tag"><div class="b f-anton">FUNEZI</div><div class="s f-bricolage-grotesque">Universal Travel Adapter</div></div>

  <div id="usb"><div class="n f-anton"><span id="unum">0</span></div><div><div class="l f-anton">USB PORT</div>
    <div class="dots"><i id="d0"></i><i id="d1"></i><i id="d2"></i><i id="d3"></i></div></div></div>
  <div id="pring"></div>

  <div id="tc"><div class="a f-anton">2× TYPE-C</div><div class="b f-bricolage-grotesque">+ 2× USB-A · 1 soket</div></div>

  <div id="uni"><div class="a f-instrument-serif">universal</div><div class="b f-anton">SOKET</div></div>
  <div id="globe" class="f-bricolage-grotesque"><svg viewBox="0 0 48 48" width="70" height="70"><circle cx="24" cy="24" r="19" fill="none" stroke="#5ab8ff" stroke-width="3.5"/>
    <ellipse id="mer" cx="24" cy="24" rx="8" ry="19" fill="none" stroke="#5ab8ff" stroke-width="3"/><path d="M5 24h38M8 14h32M8 34h32" stroke="#5ab8ff" stroke-width="2.5"/></svg>
    <span><span id="gnum">0</span>+ negara</span></div>

  <div id="p0" class="plug f-anton">UK<b>✓</b></div><div id="p1" class="plug f-anton">EU<b>✓</b></div>
  <div id="p2" class="plug f-anton">US<b>✓</b></div><div id="p3" class="plug f-anton">AUS<b>✓</b></div>
  <div id="swap">{SWAP}</div>

  <div id="st0" class="stat"><div class="v f-anton">155g</div><div class="k f-bricolage-grotesque">ringan</div></div>
  <div id="st1" class="stat"><div class="v f-anton">6.6cm</div><div class="k f-bricolage-grotesque">muat tapak tangan</div></div>
  <div id="kecil" class="f-instrument-serif">kecil je</div>

  <div id="card"><img src="img/outlet.jpg"></div>
  <div id="devs">{dev_html}</div>
  <div id="five" class="f-bricolage-grotesque">5 device, satu soket</div>

  <div id="cta"><div class="ph"><img src="img/adapter_cta.png"></div><div class="info"><div class="brand f-bricolage-grotesque">FUNEZI</div>
    <div class="name f-bricolage-grotesque">Universal Travel Adapter</div>
    <div class="rate f-bricolage-grotesque"><b>★ 4.9</b> · 1,253 terjual</div>
    <div id="btn" class="f-bricolage-grotesque">{CART}Dapatkan sebelum travel!</div></div></div>
  <div id="tapring"></div><div id="tap"></div>

  <div id="captions">
    {"".join(caps_html)}
  </div>

  <div id="co">
    <div class="halo"></div><div class="ring"></div><div class="ring2"></div>
    <img src="img/adapter.png">
    <div class="t1 f-anton"><span id="co1">SATU</span><br><span id="co2">ADAPTER.</span></div>
    <div class="t2 f-instrument-serif">settle.</div>
    <div class="pill f-bricolage-grotesque">200+ negara · 4 USB · 1 soket</div>
  </div>

  <div id="end">
    <div class="halo"></div>
    <div class="logo f-anton">FUNEZI</div>
    <div class="sub f-bricolage-grotesque">Universal Travel Adapter</div>
    <img src="img/adapter_end.png">
    <div class="q f-instrument-serif">Dapatkan sebelum travel!</div>
    <div class="s f-bricolage-grotesque">{CART}Tekan link / beg kuning</div>
  </div>
  <div id="wm" class="f-bricolage-grotesque">{PLANE}Wanderlogika</div>
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

// ---------- camera: per-shot origin + key light ----------
const SHOTS = [ // t, origin, light x/y, base scale
  [1.50, "50% 35%", 520, 620, 1.0], [3.10, "60% 40%", 480, 560, 1.0], [4.77, "45% 45%", 480, 820, 1.0],
  [7.37, "50% 45%", 560, 700, 1.0], [8.30, "50% 45%", 560, 700, 1.0], [9.90, "40% 45%", 520, 860, 1.0],
  [13.73, "50% 30%", 540, 520, 1.0], [15.33, "45% 35%", 540, 560, 1.0], [17.33, "35% 70%", 420, 1150, 1.0] ];
SHOTS.forEach(([t,o,lx,ly,s]) => {{
  tl.set("#cam", {{ transformOrigin:o, scale:s, x:0, y:0 }}, t);
  tl.set("#light", {{ "--lx": lx+"px", "--ly": ly+"px" }}, t);
}});
const PUNCH = [[1.50,1.14,1.0],[3.16,1.10,1.0],[4.77,1.12,1.0],[6.02,1.06,null],[7.37,1.10,1.0],[8.90,1.06,null],
  [9.90,1.10,1.0],[12.20,1.05,null],[13.73,1.10,1.0],[15.33,1.08,1.0],[17.33,1.10,1.0],[18.32,1.07,null]];
PUNCH.forEach(([t,s,to]) => {{
  if (to !== null) tl.fromTo("#cam", {{ scale:s }}, {{ scale:to, duration:F(12), ease:E.snap, immediateRender:false }}, t);
  else tl.to("#cam", {{ scale:s, duration:F(8), ease:E.snap }}, t);
}});
// slow push on marble beauty shot
tl.to("#cam", {{ scale:1.12, duration:1.5, ease:"none" }}, 8.36);

// ---------- 0.00 cold open ----------
tl.fromTo("#flash", {{ opacity:.95 }}, {{ opacity:0, duration:F(6), ease:E.exit }}, 0);
tl.fromTo("#co img", {{ scale:1.9, rotation:-14, y:120 }}, {{ scale:1, rotation:0, y:0, duration:F(14), ease:E.snap }}, 0);
tl.to("#co img", {{ rotation:4, y:-24, duration:1.0, ease:E.move }}, 0.5);
tl.fromTo("#co .ring2", {{ rotation:0 }}, {{ rotation:120, duration:1.5, ease:"none" }}, 0);
tl.fromTo("#co .halo", {{ scale:.7, opacity:0 }}, {{ scale:1, opacity:1, duration:F(16), ease:E.soft }}, 0);
tl.fromTo("#co1", {{ opacity:0, y:-120 }}, {{ opacity:1, y:0, duration:F(8), ease:E.snap }}, 0.04);
tl.fromTo("#co2", {{ opacity:0, x:-260 }}, {{ opacity:1, x:0, duration:F(8), ease:E.snap }}, 0.36);
tl.fromTo("#co .t2", {{ opacity:0, scale:1.7 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 1.00);
tl.fromTo("#co .pill", {{ opacity:0, y:40 }}, {{ opacity:.85, y:0, duration:F(8), ease:E.land }}, 0.70);
tl.to("#co", {{ opacity:0, scale:1.15, duration:F(4), ease:E.throw }}, 1.42);
tl.set("#co", {{ display:"none" }}, 1.50);
tl.fromTo("#flash", {{ opacity:.85 }}, {{ opacity:0, duration:F(6), ease:E.exit, immediateRender:false }}, 1.50);

// ---------- 1.50 problem hook: text behind body ----------
tl.to("#tint", {{ opacity:.55, duration:F(8), ease:E.soft }}, 1.50);
tl.to("#stage", {{ filter:"saturate(0.82) brightness(0.97)", duration:F(8), ease:E.soft }}, 1.50);
tl.fromTo("#bt1", {{ opacity:0, scale:1.7, y:-40 }}, {{ opacity:1, scale:1, y:0, duration:F(8), ease:E.snap }}, 1.52);
tl.to("#bt1", {{ opacity:0, x:-200, duration:F(5), ease:E.throw }}, 2.28);
tl.fromTo("#bt2", {{ opacity:0, x:260 }}, {{ opacity:1, x:0, duration:F(7), ease:E.snap }}, 2.34);
tl.to("#bt2", {{ opacity:0, y:-80, duration:F(4), ease:E.exit }}, 2.66);
tl.fromTo("#bt3", {{ opacity:0, scale:1.6 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 2.72);
tl.to("#cam", {{ x:10, duration:F(2), ease:"none", yoyo:true, repeat:5 }}, 2.72);
tl.to("#bt3", {{ opacity:0, scale:.92, duration:F(4), ease:E.exit }}, 2.98);

// ---------- 3.10 reveal ----------
tl.fromTo("#flash", {{ opacity:.6 }}, {{ opacity:0, duration:F(5), ease:E.exit, immediateRender:false }}, 3.12);
tl.to("#tint", {{ opacity:0, duration:F(4), ease:E.exit }}, 3.10);
tl.to("#stage", {{ filter:"saturate(1.04) brightness(1.03)", duration:F(4), ease:E.exit }}, 3.10);
tl.to("#glow", {{ opacity:.35, duration:F(16), ease:E.soft }}, 3.12);
tl.fromTo("#ring", {{ opacity:0, scale:1.9 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 3.30);
tl.to("#ring", {{ scale:1.07, duration:F(9), ease:E.move, yoyo:true, repeat:3 }}, 3.62);
tl.fromTo("#tag", {{ opacity:0, x:-320 }}, {{ opacity:1, x:0, duration:F(11), ease:E.land }}, 3.62);
tl.to(["#ring","#tag"], {{ opacity:0, x:-140, duration:F(6), ease:E.throw }}, 4.56);
tl.to("#glow", {{ opacity:.12, duration:F(8), ease:E.exit }}, 4.56);

// ---------- 4.77 4 USB ----------
tl.fromTo("#usb", {{ opacity:0, x:-300 }}, {{ opacity:1, x:0, duration:F(11), ease:E.land }}, 5.00);
const U = {{ v:0 }};
tl.to(U, {{ v:4, duration:F(10), ease:E.move, onUpdate:()=>{{ const el=document.getElementById("unum"); if(el) el.textContent=Math.round(U.v); }} }}, 6.00);
[0,1,2,3].forEach(k => tl.to("#d"+k, {{ background:"#5ab8ff", borderColor:"#5ab8ff", boxShadow:"0 0 24px rgba(90,184,255,.9)", duration:F(3), ease:E.snap }}, 6.02 + k*0.1));
tl.fromTo("#pring", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 6.62);
tl.to(["#usb","#pring"], {{ opacity:0, y:-120, duration:F(6), ease:E.throw }}, 7.20);

// ---------- 7.37 type-C ----------
tl.to("#coolglow", {{ opacity:.35, duration:F(10), ease:E.soft }}, 7.37);
tl.fromTo("#tc", {{ opacity:0, x:300 }}, {{ opacity:1, x:0, duration:F(9), ease:E.snap }}, 7.40);
tl.fromTo("#tc .b", {{ opacity:0, y:30 }}, {{ opacity:1, y:0, duration:F(8), ease:E.land }}, 7.76);
tl.to("#tc", {{ opacity:0, x:260, duration:F(6), ease:E.throw }}, 8.14);

// ---------- 8.30 universal soket ----------
tl.fromTo("#uni .a", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(12), ease:E.land }}, 8.86);
tl.fromTo("#uni", {{ opacity:0 }}, {{ opacity:1, duration:F(6), ease:E.soft }}, 8.86);
tl.fromTo("#uni .b", {{ opacity:0, scale:1.8 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 9.44);
tl.fromTo("#globe", {{ opacity:0, y:120 }}, {{ opacity:1, y:0, duration:F(11), ease:E.land }}, 8.60);
tl.to("#mer", {{ attr:{{ rx:2 }}, duration:.6, ease:E.move, yoyo:true, repeat:1 }}, 8.6);
const G = {{ v:0 }};
tl.to(G, {{ v:200, duration:1.0, ease:E.move, onUpdate:()=>{{ const el=document.getElementById("gnum"); if(el) el.textContent=Math.round(G.v); }} }}, 8.70);
tl.to(["#uni","#globe"], {{ opacity:0, y:-120, duration:F(6), ease:E.throw }}, 9.78);
tl.to("#coolglow", {{ opacity:0, duration:F(8), ease:E.exit }}, 9.78);

// ---------- 9.90 plugs ----------
[[0,10.26],[1,10.98],[2,11.64],[3,12.20]].forEach(([k,t]) => {{
  tl.fromTo("#p"+k, {{ opacity:0, y:-160 }}, {{ opacity:1, y:0, duration:F(9), ease:E.snap }}, t);
  tl.fromTo("#p"+k+" b", {{ scale:1.8 }}, {{ scale:1, duration:F(7), ease:E.snap, immediateRender:false }}, t + F(5));
}});
tl.fromTo("#swap", {{ opacity:0, y:80 }}, {{ opacity:1, y:0, duration:F(8), ease:E.land }}, 13.08);
tl.to("#swap svg", {{ rotation:180, duration:F(14), ease:E.move }}, 13.12);
tl.to(["#p0","#p1","#p2","#p3","#swap"], {{ opacity:0, y:-140, duration:F(6), ease:E.throw, stagger:F(1) }}, 13.52);

// ---------- 13.73 kecil ----------
tl.fromTo("#st0", {{ opacity:0, x:-260 }}, {{ opacity:1, x:0, duration:F(11), ease:E.land }}, 13.80);
tl.fromTo("#st1", {{ opacity:0, x:260 }}, {{ opacity:1, x:0, duration:F(11), ease:E.land }}, 14.20);
tl.fromTo("#kecil", {{ opacity:0, scale:1.5 }}, {{ opacity:1, scale:1, duration:F(9), ease:E.snap }}, 13.80);
tl.to("#kecil", {{ opacity:0, y:-60, duration:F(5), ease:E.exit }}, 14.46);
tl.to(["#st0","#st1"], {{ opacity:0, y:-120, duration:F(6), ease:E.throw }}, 15.16);

// ---------- 15.33 gadget b-roll card (J-cut: card lands after the line starts) ----------
tl.to("#stage", {{ filter:"blur(14px) brightness(.8)", duration:F(9), ease:E.soft }}, 15.86);
tl.fromTo("#card", {{ opacity:0, y:-260, rotationX:24, rotation:-3 }}, {{ opacity:1, y:0, rotationX:0, rotation:-2, duration:F(12), ease:E.soft }}, 15.86);
tl.fromTo("#card img", {{ scale:1.0 }}, {{ scale:1.1, duration:1.5, ease:"none" }}, 15.86);
tl.fromTo("#devs", {{ opacity:0, y:120 }}, {{ opacity:1, y:0, duration:F(10), ease:E.land }}, 16.14);
tl.fromTo(".bat i", {{ scaleX:.1 }}, {{ scaleX:1, duration:.7, ease:E.move, stagger:F(3) }}, 16.30);
tl.fromTo("#five", {{ opacity:0, scale:1.4 }}, {{ opacity:1, scale:1, duration:F(8), ease:E.snap }}, 16.72);
tl.to(["#card","#devs","#five"], {{ opacity:0, y:-160, duration:F(6), ease:E.throw, stagger:F(1) }}, 17.18);
tl.to("#stage", {{ filter:"blur(0px) brightness(1.03)", duration:F(6), ease:E.exit }}, 17.22);

// ---------- 17.33 CTA ----------
tl.to("#glow", {{ opacity:.35, duration:F(14), ease:E.soft }}, 17.33);
tl.fromTo("#cta", {{ opacity:0, y:-240 }}, {{ opacity:1, y:0, duration:F(12), ease:E.land }}, 17.36);
tl.fromTo("#tap", {{ opacity:0, x:260, y:240 }}, {{ opacity:1, x:0, y:0, duration:F(12), ease:E.land }}, 17.86);
tl.to("#tap", {{ scale:.78, duration:F(3), ease:E.exit }}, 18.26);
tl.to("#tap", {{ scale:1, duration:F(5), ease:E.land }}, 18.36);
tl.set("#tapring", {{ opacity:1, scale:.5 }}, 18.32);
tl.to("#tapring", {{ opacity:0, scale:2.2, duration:F(14), ease:E.soft }}, 18.32);
tl.fromTo("#btn", {{ scale:1.18 }}, {{ scale:1, duration:F(9), ease:E.snap, immediateRender:false }}, 18.32);

// ---------- end card (loops into cold open) ----------
tl.fromTo("#end", {{ opacity:1, y:1920 }}, {{ opacity:1, y:0, duration:F(9), ease:E.land }}, {VID_END - 0.1});
tl.fromTo("#end img", {{ scale:1.3, rotation:-8 }}, {{ scale:1, rotation:0, duration:1.1, ease:E.soft }}, {VID_END - 0.1});
tl.fromTo("#end .logo", {{ opacity:0, y:-60 }}, {{ opacity:1, y:0, duration:F(10), ease:E.land }}, {VID_END + 0.05});
tl.fromTo("#end .q", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(10), ease:E.land }}, {VID_END + 0.15});
tl.fromTo("#end .s", {{ opacity:0, y:60 }}, {{ opacity:1, y:0, duration:F(10), ease:E.land }}, {VID_END + 0.3});
tl.set(["#cta","#tap","#captions"], {{ opacity:0 }}, {VID_END});

// ---------- captions (karaoke) ----------
CAPS.forEach(c => {{
  tl.fromTo("#"+c.id, {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:F(6), ease:E.land }}, c.s);
  c.w.forEach(([id, t, em]) => {{
    tl.to("#"+id, {{ color: em ? "#f6f1e8" : "#ffffff", duration:F(2), ease:"none" }}, t);
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
