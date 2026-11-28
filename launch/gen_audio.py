import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=44100; DUR=15.0; N=int(SR*DUR); rng=np.random.default_rng(11)
BPM=120; B=60/BPM
def T(d): return np.arange(int(SR*d))/SR
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
def lpf(x,f): return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def hpf(x,f): return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
def add(buf,x,t,g=1.0):
    s=int(t*SR); n=min(len(x),len(buf)-s)
    if n>0: buf[s:s+n]+=x[:n]*g
def mid(n): return 440*2**((n-69)/12)
def norm(x,p): return x/(np.abs(x).max()+1e-9)*p
# ---------- instruments
def kick():
    t=T(0.35); f=50+110*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
def clap():
    t=T(0.25); n=rng.standard_normal(len(t)); e=np.exp(-t*22)
    for d in (0.0,0.012,0.024): e+=np.exp(-np.clip(t-d,0,None)*120)*(t>=d)*0.5
    return bp(n,900,5000)*e*0.5
def shaker():
    t=T(0.07); return hpf(rng.standard_normal(len(t)),6000)*np.exp(-t*60)*0.25
def pluck(f,d=0.35):  # bright retro organ/pluck
    t=T(d); x=np.sign(np.sin(2*np.pi*f*t))*0.35+np.sin(2*np.pi*f*t)*0.65
    return lpf(x,3200)*np.exp(-t*7)
def bass(f,d):
    t=T(d); x=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)
    e=np.minimum(1,t/0.005)*np.exp(-t*3.5); return x*e
def glock(f,d=0.6):
    t=T(d); return (np.sin(2*np.pi*f*t)+0.25*np.sin(2*np.pi*4.01*f*t)*np.exp(-t*12))*np.exp(-t*5)
drums=np.zeros(N); keys=np.zeros(N); bs=np.zeros(N); mel=np.zeros(N)
# D  Bm  G  A   (bar = 2s)
prog=[(62,[62,66,69]),(59,[59,62,66]),(55,[55,59,62]),(57,[57,61,64])]
END=14.0
nb=int(END/B)
for b in range(nb):
    t=b*B
    if b%2==0: add(drums,kick(),t,0.9)
    else: add(drums,clap(),t,0.55)
    if b%4==3: add(drums,kick(),t+B/2,0.5)
for k in range(int(END/(B/2))):
    add(drums,shaker(),k*B/2+(0.012 if k%2 else 0),0.8 if k%2 else 0.5)
for bar in range(int(END/2)):
    root,ch=prog[bar%4]; t0=bar*2
    for j in range(4):  # offbeat stabs
        for p in ch: add(keys,pluck(mid(p+12),0.3),t0+j*B+B/2,0.11)
    for j,iv in enumerate([0,0,7,0,12,7,0,7]):  # bouncy bass 8ths
        add(bs,bass(mid(root-24+iv),B/2*0.9),t0+j*B/2,0.32)
# glock hook (D major pentatonic), plays bars 1-6
hook=[(0,74),(0.5,76),(1.0,78),(1.5,81),(2.25,78),(3.0,76),(3.5,74)]
for rep in (2,6,10):
    for dt,n in hook: add(mel,glock(mid(n+12)),rep+dt,0.16)
# final chord at 14.0 (button hit already earlier); ring to end
for p in [50,62,66,69,74]:
    add(keys,pluck(mid(p+12),1.0)*0+glock(mid(p+12),1.0)*0.6,END,0.12)
add(bs,bass(mid(38),1.0),END,0.4); add(drums,kick(),END,1.0)
music=drums*0.9+keys+bs+mel
# duck before reveal (silence before punch): 4.6-5.0
g=np.ones(N); t=np.arange(N)/SR
g[(t>4.6)&(t<5.0)]=0.15; g=np.convolve(g,np.ones(800)/800,'same')
fade=np.clip((DUR-t)/0.4,0,1); music*=g*fade
# ---------- SFX
def noise(d): return rng.standard_normal(int(SR*d))
def whoosh(d=0.4,lo=400,hi=4000):
    x=bp(noise(d),lo,hi); tt=T(d); return x*np.sin(np.pi*tt/d)**2
def rip(d=0.42):  # paper tear: crackly bursts through bandpass
    tt=T(d); n=noise(d); cr=(rng.random(len(tt))<0.02).astype(float)
    cr=np.convolve(cr,np.exp(-np.arange(200)/40),'same')
    x=bp(n,1200,7000)*(0.4+cr)*np.minimum(1,tt/0.02)*np.exp(-tt*4)
    return norm(x,0.8)
def thud():
    tt=T(0.4); f=70+80*np.exp(-tt*35); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*10)
    return norm(x+0.25*bp(noise(0.4),200,2000)*np.exp(-tt*50),0.9)
def stamp():
    tt=T(0.3); x=thud()[:len(tt)]+0.5*bp(noise(0.3),1500,6000)*np.exp(-tt*60); return norm(x,0.9)
def pop():
    tt=T(0.1); f=700+600*tt/0.1; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*40)*0.7
def tick(): tt=T(0.04); return np.sin(2*np.pi*2600*tt)*np.exp(-tt*150)*0.5
def riser(d=0.6):
    tt=T(d); f=300+1800*(tt/d)**2; return norm(np.sin(2*np.pi*np.cumsum(f)/SR)*(tt/d)**2*0.5+bp(noise(d),2000,8000)*(tt/d)**3,0.5)
def boom():
    tt=T(1.2); f=40+70*np.exp(-tt*12); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*3)
    sh=sum(np.sin(2*np.pi*fr*tt)*np.exp(-tt*(3+i)) for i,fr in enumerate([1568,2093,2637]))*0.12
    return norm(x+sh,0.9)
def ding():
    tt=T(1.0); return norm(sum(np.sin(2*np.pi*fr*tt)*np.exp(-tt*4)*a for fr,a in [(1975,1),(2637,.6),(3951,.25)]),0.55)
S=np.zeros(N)
ev=[(0.0,thud(),.7),(0.5,whoosh(0.3,800,6000),.35),(1.0,pop(),.5),(0.25,whoosh(1.2,300,2500),.18),
    (2.28,rip(),.6),(2.55,whoosh(0.3,600,5000),.35),(3.0,whoosh(0.3,600,5000),.35)]
ev+=[(3.25+i*0.15,tick(),.55) for i in range(5)]
ev+=[(4.05,whoosh(0.25,1000,7000),.25),(4.4,riser(),.55),(4.78,rip(),.6),(5.0,boom(),.75),(5.05,stamp(),.7),
     (5.35,whoosh(0.3,800,6000),.3),(5.6,thud(),.55),(6.0,whoosh(0.45,300,3000),.3),(6.45,tick(),.4),(6.75,stamp(),.75),
     (7.78,rip(),.6),(8.05,thud(),.65),(8.35,whoosh(0.3,600,5000),.35),(8.75,pop(),.45),(9.1,pop(),.45),
     (9.3,whoosh(1.0,300,2500),.18),(10.28,rip(),.6),(10.55,thud(),.65),(10.8,thud(),.55),(11.05,pop(),.5),
     (11.3,stamp(),.6),(11.3,ding(),.6),(11.45,whoosh(0.25,1000,6000),.25)]
ev+=[(11.65+i*0.15,tick(),.45) for i in range(3)]
ev+=[(12.6,whoosh(1.1,300,2500),.15)]
for t0,x,gn in ev: add(S,x,t0,gn)
mix=music*0.55+S*0.6
mix=np.tanh(mix*1.2)/1.2
sf.write("audio/premix.wav",np.stack([mix,mix],1).astype(np.float32),SR)
