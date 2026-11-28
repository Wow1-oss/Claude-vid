"""Build index.html for the Wanderlogika launch video (HyperFrames + GSAP)."""
import json, random
R = json.load(open("regions.json"))
DUR = 15.0
rnd = random.Random(42)

def torn(w, h, amp=9, step=26, top=True, bottom=True):
    """clip-path polygon (px) with torn top/bottom edges."""
    pts = []
    x = 0
    if top:
        while x < w:
            pts.append((x, rnd.uniform(0, amp))); x += rnd.uniform(step * .6, step * 1.4)
        pts.append((w, rnd.uniform(0, amp)))
    else:
        pts += [(0, 0), (w, 0)]
    x = w; bt = []
    if bottom:
        while x > 0:
            bt.append((x, h - rnd.uniform(0, amp))); x -= rnd.uniform(step * .6, step * 1.4)
        bt.append((0, h - rnd.uniform(0, amp)))
    else:
        bt += [(w, h), (0, h)]
    return "polygon(" + ",".join(f"{a:.0f}px {b:.0f}px" for a, b in pts + bt) + ")"

SCENES = [  # id, image, top, card height
    ("s1", "hook", 285, 1350), ("s2", "problem", 285, 1350), ("s3", "reveal", 285, 1350),
    ("s4", "bundle", 285, 1350), ("s5", "cta", 150, 1170)]
LIFTS = {"s1": ["h1", "h2", "h3"], "s2": ["p1", "p2", "p3", "n1", "n2", "n3", "n4", "n5"],
         "s3": ["r1", "r2", "r3", "r4", "cov"], "s4": ["b1", "b2", "c1", "c2"], "s5": ["t1", "t2", "pr", "btn"]}

def lift(k):
    _, x, y, w, h = R[k]
    return f'<img id="L{k}" class="lift" src="img/L_{k}.png" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'

PLANE = '''<svg viewBox="0 0 100 100" width="{s}" height="{s}"><path fill="{c}" d="M95 46c0-4-4-6-8-6H62L38 6h-9l13 34H20l-8-10H5l5 18-5 18h7l8-10h22L29 94h9l24-34h25c4 0 8-2 8-6z"/></svg>'''
PIN = '<svg viewBox="0 0 40 52" width="{s}" height="{h}"><path fill="#F83C92" d="M20 0C9 0 0 9 0 20c0 15 20 32 20 32s20-17 20-32C40 9 31 0 20 0z"/><circle cx="20" cy="19" r="8" fill="#F7F0DF"/></svg>'

scene_html = []
for sid, img, top, ch in SCENES:
    deco = ""
    if sid == "s3":
        cx, cy, cw, chh = R["cov"][1:]
        deco = f'''<div id="gleamBox" style="left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px"><div id="gleam"></div></div>
<div id="stamp" style="left:828px;top:116px">
 <svg viewBox="0 0 240 240" width="240" height="240"><defs><path id="ring" d="M120 120m-86 0a86 86 0 1 1 172 0a86 86 0 1 1 -172 0"/></defs>
 <circle cx="120" cy="120" r="112" fill="none" stroke="#F83C92" stroke-width="7"/>
 <circle cx="120" cy="120" r="66" fill="none" stroke="#F83C92" stroke-width="4"/>
 <text font-family="F Anton" font-size="25" fill="#F83C92" letter-spacing="3.2"><textPath href="#ring">JUST LAUNCHED &#183; WANDERLOGIKA &#183;</textPath></text>
 <text x="120" y="138" text-anchor="middle" font-family="F Anton" font-size="56" fill="#F83C92">NEW</text></svg></div>'''
    if sid == "s4":
        deco = '''<div id="pstamp" style="left:842px;top:1222px"><svg viewBox="0 0 200 150" width="200" height="150">
 <rect x="4" y="4" width="192" height="142" rx="4" fill="#F7F0DF" stroke="#FFD326" stroke-width="8" stroke-dasharray="2 9" stroke-linecap="round"/>
 <rect x="20" y="20" width="160" height="110" fill="#085BE5"/>
 <circle cx="140" cy="48" r="16" fill="#FFD326"/>
 <path d="M20 130 L70 80 L100 105 L130 75 L180 125 L180 130Z" fill="#F83C92"/>
 <g transform="translate(46 34) rotate(-18) scale(.5)"><path fill="#F7F0DF" d="M95 46c0-4-4-6-8-6H62L38 6h-9l13 34H20l-8-10H5l5 18-5 18h7l8-10h22L29 94h9l24-34h25c4 0 8-2 8-6z"/></g></svg></div>'''
    lifts = "\n".join(lift(k) for k in LIFTS[sid])
    if sid == "s3":  # cover lift wrapper for wipe
        lifts = lifts.replace('id="Lcov" class="lift"', 'id="Lcov" class="lift cov"')
    scene_html.append(f'''<div id="{sid}" class="scene" style="top:{top}px;height:{ch}px">
 <div class="cardwrap"><div class="card" style="height:{ch}px;clip-path:{torn(1080, ch)}">
  <img class="plate" src="img/{img}_plate.jpg">
  {lifts}
  {deco}
 </div></div>
 <div class="tape t1"></div><div class="tape t2"></div>
</div>''')

# rip sheets
RIPS = [("rp1", "#085BE5", 2.25), ("rp2", "#F83C92", 4.75), ("rp3", "#FFD326", 7.75), ("rp4", "#085BE5", 10.25)]
rip_html = "\n".join(f'''<div id="{i}" class="rip"><div class="fiber" style="clip-path:{torn(1080, 3200, 26, 34)}"></div>
<div class="sheet" style="background-color:{c};clip-path:{torn(1080, 3160, 22, 30)}"></div></div>''' for i, c, _ in RIPS)

# plane path keyframes (top band) — quadratic bezier
def bez(p0, p1, p2, n):
    out = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
        dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        import math
        out.append((round(x), round(y), round(math.degrees(math.atan2(dy, dx)))))
    return out
TOP = ((-60, 230), (520, -10), (1140, 170))
BOT = ((-60, 1830), (560, 1650), (1140, 1790))
kt = json.dumps(bez(*TOP, 12)); kb = json.dumps(bez(*BOT, 12))
pathTop = f"M{TOP[0][0]} {TOP[0][1]} Q{TOP[1][0]} {TOP[1][1]} {TOP[2][0]} {TOP[2][1]}"
pathBot = f"M{BOT[0][0]} {BOT[0][1]} Q{BOT[1][0]} {BOT[1][1]} {BOT[2][0]} {BOT[2][1]}"

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/fonts.css">
<script src="vendor/gsap.min.js"></script>
<style>
:root{{--cream:#F7F0DF;--blue:#085BE5;--yellow:#FFD326;--pink:#F83C92;--ink:#171717}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--cream)}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"F Dm Sans",sans-serif}}
#ground{{position:absolute;inset:0;background:url(img/paper.jpg) center/cover}}
.band{{position:absolute;left:0;width:1080px}}
#bandTop{{top:0;height:330px}}
#bandBot{{top:1560px;height:360px}}
.strip{{position:absolute;left:-40px;width:1160px}}
#cam{{position:absolute;inset:0;transform-origin:50% 40%}}
.scene{{position:absolute;left:0;width:1080px;opacity:0}}
.cardwrap{{position:absolute;inset:0;filter:drop-shadow(0 18px 22px rgba(23,23,23,.28))}}
.card{{position:absolute;left:0;top:0;width:1080px;overflow:hidden;background:var(--cream)}}
.plate{{position:absolute;left:0;top:0;width:1080px;height:1350px}}
.lift{{position:absolute;display:block}}
#Lc1,#Lc2,#Lbtn{{filter:drop-shadow(0 0 0 rgba(0,0,0,0))}}
.tape{{position:absolute;width:190px;height:52px;opacity:.82;background:repeating-linear-gradient(90deg,rgba(255,255,255,.18) 0 6px,transparent 6px 12px)}}
.tape.t1{{left:-30px;top:-16px;background-color:var(--yellow);rotate:-14deg}}
.tape.t2{{right:-30px;top:-14px;background-color:var(--pink);rotate:12deg}}
#s5 .tape{{display:none}}
#gleamBox{{position:absolute;overflow:hidden;pointer-events:none}}
#gleam{{position:absolute;top:-10%;left:-60%;width:40%;height:120%;opacity:0;
  background:linear-gradient(100deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.55) 50%,rgba(255,255,255,0) 100%)}}
#stamp{{position:absolute;width:240px;height:240px;opacity:0;mix-blend-mode:multiply}}
#pstamp{{position:absolute;width:200px;height:150px;opacity:0;filter:drop-shadow(0 6px 8px rgba(0,0,0,.25))}}
.rip{{position:absolute;left:0;top:0;width:1080px;height:3200px}}
.rip .fiber{{position:absolute;left:0;top:0;width:1080px;height:3200px;background:#fffaf0}}
.rip .sheet{{position:absolute;left:0;top:20px;width:1080px;height:3160px;
  background-image:url(img/paper.jpg);background-size:1080px 1920px;background-blend-mode:multiply}}
#ctaPanel{{position:absolute;left:100px;top:1338px;width:840px;text-align:center}}
#url{{display:inline-block;font-size:30px;color:var(--blue);background:#fff;padding:10px 22px;border-radius:40px;
  border:3px solid var(--blue);opacity:0;letter-spacing:-.2px}}
#tag{{margin-top:18px;font-size:56px;line-height:1.08;color:var(--ink);text-transform:uppercase}}
.tw{{display:inline-block;margin:0 8px;opacity:0}}
#shine{{position:absolute;left:0;top:0;width:120px;height:105px;opacity:0;mix-blend-mode:screen;
  background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.7),rgba(255,255,255,0))}}
#btnBox{{position:absolute;overflow:hidden;border-radius:16px;pointer-events:none}}
.pl{{position:absolute;left:0;top:0;width:92px;height:92px}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
 <div id="ground" class="clip" data-start="0" data-duration="{DUR}"></div>
 <div id="bandTop" class="band">
  <svg width="1080" height="330" style="position:absolute;left:0;top:0;overflow:visible">
   <defs><mask id="mTop"><path id="mTopP" d="{pathTop}" stroke="#fff" stroke-width="16" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></mask></defs>
   <path d="{pathTop}" stroke="#085BE5" stroke-width="5" fill="none" stroke-dasharray="4 14" stroke-linecap="round" mask="url(#mTop)"/>
  </svg>
  <div id="pinTop" style="position:absolute;left:968px;top:40px;opacity:0">{PIN.format(s=56, h=73)}</div>
  <div id="planeTop" class="pl" style="opacity:0">{PLANE.format(s=92, c="#085BE5")}</div>
 </div>
 <div id="bandBot" class="band">
  <div class="strip" style="top:150px;height:240px;background:#085BE5;clip-path:{torn(1160, 240, 16, 30, True, False)};rotate:-2.5deg"></div>
  <div class="strip" style="top:120px;left:560px;width:620px;height:120px;background:#F83C92;clip-path:{torn(620, 120, 12, 26)};rotate:4deg"></div>
  <div class="strip" style="top:96px;left:-30px;width:300px;height:58px;background:#FFD326;opacity:.9;rotate:-6deg"></div>
 </div>
 <svg id="botPath" width="1080" height="1920" style="position:absolute;left:0;top:0;overflow:visible">
  <defs><mask id="mBot"><path id="mBotP" d="{pathBot}" stroke="#fff" stroke-width="16" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></mask></defs>
  <path d="{pathBot}" stroke="#F7F0DF" stroke-width="5" fill="none" stroke-dasharray="4 14" stroke-linecap="round" mask="url(#mBot)"/>
 </svg>
 <div id="planeBot" class="pl" style="opacity:0">{PLANE.format(s=92, c="#F7F0DF")}</div>
 <div id="cam">
  {"".join(scene_html)}
  <div id="btnBox" style="left:{R['btn'][1]}px;top:{150 + R['btn'][2]}px;width:{R['btn'][3]}px;height:{R['btn'][4]}px"><div id="shine"></div></div>
 </div>
 <div id="ctaPanel">
  <div id="url" class="f-dm-sans">wanderlog.gumroad.com/l/passport-plans-besties</div>
  <div id="tag" class="f-anton"><span class="tw">Explore more.</span><span class="tw" style="color:#085BE5">Plan smarter.</span><br><span class="tw" style="color:#F83C92">Travel confidently.</span></div>
 </div>
 {rip_html}
 <audio id="mix" class="clip" src="audio/mix.wav" data-start="0" data-duration="{DUR}" data-volume="1"></audio>
</div>
<script>
const FPS = 30, F = n => n / FPS;
const E = {{ land:"power3.out", soft:"power2.out", snap:"expo.out", settle:"back.out(1.15)", exit:"power2.in", throw:"power4.in", move:"power2.inOut" }};
const tl = gsap.timeline({{paused:true}});
const $ = s => document.querySelector(s);
// ---------- initial states
gsap.set(["#Lh1","#Lh2","#Lh3","#Lp1","#Lp2","#Lp3","#Lr1","#Lr2","#Lr3","#Lr4","#Lb1","#Lb2","#Lt1","#Lt2","#Lpr"],{{opacity:0}});
gsap.set("#s1",{{opacity:1}});
gsap.set("#cam",{{scale:1.16,transformOrigin:"12% 30%"}});
// rip sheets parked below
gsap.set(["#rp1","#rp2","#rp3","#rp4"],{{y:1960}});
// ---------- helpers
function slam(el,t,from=1.45){{ tl.fromTo(el,{{scale:from,opacity:0}},{{scale:1,opacity:1,duration:F(8),ease:E.snap}},t); }}
function slideX(el,t,dx){{ tl.fromTo(el,{{x:dx,opacity:0}},{{x:0,opacity:1,duration:F(10),ease:E.land}},t); }}
function slideY(el,t,dy=40){{ tl.fromTo(el,{{y:dy,opacity:0}},{{y:0,opacity:1,duration:F(10),ease:E.land}},t); }}
function wipe(el,t,d=F(9)){{ tl.fromTo(el,{{clipPath:"inset(0% 100% 0% 0%)",opacity:1}},{{clipPath:"inset(0% 0% 0% 0%)",opacity:1,duration:d,ease:E.land}},t); }}
function rip(r,t,from,to){{ tl.fromTo(r,{{y:1960}},{{y:-3300,duration:0.62,ease:E.move}},t);
  tl.set(from,{{opacity:0}},t+0.31); tl.set(to,{{opacity:1}},t+0.31); }}
function fly(el,t,d,keys){{ tl.set(el,{{opacity:1,x:keys[0][0]-46,y:keys[0][1]-46,rotation:keys[0][2]}},t);
  const step=d/(keys.length-1);
  keys.slice(1).forEach((k,i)=>tl.to(el,{{x:k[0]-46,y:k[1]-46,rotation:k[2],duration:step,ease:"none"}},t+step*i));
  tl.set(el,{{opacity:0}},t+d); }}
const KT={kt}, KB={kb};
// ===== S1 HOOK 0.00-2.50
slam("#Lh1",0.0,1.5);
wipe("#Lh2",0.5);
slideY("#Lh3",1.0);
tl.to("#cam",{{scale:1.0,duration:2.2,ease:E.move}},0.1);
tl.fromTo("#bandTop",{{y:-26}},{{y:0,duration:2.4,ease:E.move}},0);
tl.fromTo("#bandBot",{{y:30}},{{y:0,duration:2.4,ease:E.move}},0);
tl.fromTo("#mTopP",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:2.0,ease:E.soft}},0.2);
fly("#planeTop",0.2,2.0,KT);
tl.fromTo("#pinTop",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:F(8),ease:E.snap}},2.15);
// ===== S2 PROBLEM 2.50-5.00
rip("#rp1",2.25,"#s1","#s2");
tl.set("#cam",{{scale:1.0,transformOrigin:"50% 55%"}},2.56);
slideX("#Lp1",2.55,-760);
slideX("#Lp2",3.0,860);
["#Ln1","#Ln2","#Ln3","#Ln4","#Ln5"].forEach((n,i)=>{{
  tl.to(n,{{scale:1.22,rotation:[-6,5,-4,6,-5][i],duration:F(5),ease:E.snap}},3.25+i*0.15);
  tl.to(n,{{scale:1,rotation:0,duration:F(9),ease:E.land}},3.25+i*0.15+F(5)); }});
wipe("#Lp3",4.05,F(10));
tl.to("#cam",{{scale:1.07,duration:2.4,ease:E.move}},2.56);
tl.to("#bandTop",{{y:18,duration:2.4,ease:E.move}},2.56);
tl.to("#bandBot",{{y:-22,duration:2.4,ease:E.move}},2.56);
// ===== S3 REVEAL 5.00-8.00
rip("#rp2",4.75,"#s2","#s3");
tl.set("#cam",{{scale:1.0,transformOrigin:"78% 45%"}},5.06);
gsap.set("#Lcov",{{clipPath:"inset(100% 0% 0% 0%)"}});
slam("#Lr1",5.05,2.2);
wipe("#Lr2",5.35);
slam("#Lr3",5.6,1.5);
slideY("#Lr4",5.75,30);
tl.to("#Lcov",{{clipPath:"inset(0% 0% 0% 0%)",duration:F(12),ease:E.soft}},5.85);
tl.set("#gleam",{{opacity:1}},6.4);
tl.fromTo("#gleam",{{x:0}},{{x:1100,duration:F(16),ease:E.move}},6.4);
tl.set("#gleam",{{opacity:0}},6.4+F(16));
tl.fromTo("#stamp",{{scale:2.0,rotation:-4,opacity:0}},{{scale:1,rotation:-12,opacity:.92,duration:F(7),ease:E.snap}},6.75);
tl.to("#cam",{{scale:1.09,duration:1.65,ease:E.move}},6.3);
tl.to("#bandTop",{{y:-10,duration:2.9,ease:E.move}},5.06);
tl.to("#bandBot",{{y:16,duration:2.9,ease:E.move}},5.06);
// ===== S4 BUNDLE 8.00-10.50
rip("#rp3",7.75,"#s3","#s4");
tl.set("#cam",{{scale:1.07,transformOrigin:"50% 45%"}},8.06);
slam("#Lb1",8.05,1.5);
slideX("#Lb2",8.35,-1000);
[["#Lc1",8.75,-1.5],["#Lc2",9.1,1.5]].forEach(([c,t,r])=>{{
  tl.to(c,{{scale:1.045,y:-14,rotation:r,filter:"drop-shadow(0 24px 24px rgba(0,0,0,.32))",duration:F(8),ease:E.snap}},t);
  tl.to(c,{{scale:1,y:0,rotation:0,filter:"drop-shadow(0 0px 0px rgba(0,0,0,0))",duration:F(12),ease:E.land}},t+0.7); }});
tl.fromTo("#pstamp",{{scale:1.8,rotation:0,opacity:0}},{{scale:1,rotation:8,opacity:1,duration:F(7),ease:E.snap}},9.3);
tl.to("#cam",{{scale:1.0,duration:2.4,ease:E.move}},8.06);
tl.fromTo("#mBotP",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:1.0,ease:E.soft}},9.3);
fly("#planeBot",9.3,1.0,KB);
tl.to("#bandBot",{{y:0,duration:2.4,ease:E.move}},8.06);
// ===== S5 CTA 10.50-15.00
rip("#rp4",10.25,"#s4","#s5");
tl.set("#botPath",{{opacity:0}},10.56);
tl.set("#cam",{{scale:1.0,transformOrigin:"50% 40%"}},10.56);
slam("#Lt1",10.55,1.4);
slam("#Lt2",10.8,1.6);
tl.fromTo("#Lpr",{{scale:1.3,opacity:0}},{{scale:1,opacity:1,duration:F(8),ease:E.snap}},11.05);
tl.to("#Lbtn",{{scale:1.06,duration:F(6),ease:E.snap}},11.3);
tl.to("#Lbtn",{{scale:1.03,duration:F(14),ease:E.settle}},11.3+F(6));
slideY("#url",11.45,36);
document.querySelectorAll(".tw").forEach((w,i)=>slideY(w,11.65+i*0.15,40));
tl.set("#shine",{{opacity:1}},13.2);
tl.fromTo("#shine",{{x:-140}},{{x:900,duration:0.6,ease:E.move}},13.2);
tl.set("#shine",{{opacity:0}},13.8);
tl.to("#cam",{{scale:1.035,duration:4.3,ease:"none"}},10.6);
tl.to("#root",{{opacity:1,duration:0.01}},{DUR - 0.01});
window.__timelines = window.__timelines || {{}};
window.__timelines['main'] = tl;
</script>
</body>
</html>
'''
open("index.html", "w").write(html)
print("ok")
