"""SFX + music for Cymbo edit (all synthesized, no downloaded audio)."""
import numpy as np, soundfile as sf, os
os.makedirs("audio", exist_ok=True)
SR=44100; rng=np.random.default_rng(11)
def t(d): return np.arange(int(SR*d))/SR
def lp(x,k):
    y=np.zeros_like(x)
    for i in range(1,len(x)): y[i]=y[i-1]+k*(x[i]-y[i-1])
    return y
def norm(x,p=0.9): return x/(np.abs(x).max()+1e-9)*p
def save(n,x): sf.write(f"audio/{n}.wav",np.stack([x,x],1).astype(np.float32),SR)
def noise(d): return rng.standard_normal(int(SR*d))
def whoosh(d=0.45,bright=0.25):
    n=noise(d); x=lp(n,bright)-lp(n,0.02); tt=t(d); return norm(x*np.sin(np.pi*np.clip(tt/d,0,1))**2,0.8)
save("whoosh",whoosh(0.45)); save("swish",whoosh(0.25,0.45))
tt=t(0.5); f=55+90*np.exp(-tt*25)
save("hit",norm(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7)+0.3*lp(noise(0.5),0.3)*np.exp(-tt*40),0.95))
tt=t(1.2); f=45+55*np.exp(-tt*12)
save("boom",norm(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*3.2)+0.15*lp(noise(1.2),0.2)*np.exp(-tt*10),0.95))
tt=t(0.12); save("pop",norm(np.sin(2*np.pi*np.cumsum(900-500*tt/0.12)/SR)*np.exp(-tt*35),0.8))
tt=t(0.03); save("tick",norm(np.sin(2*np.pi*2400*tt)*np.exp(-tt*200),0.7))
tt=t(0.06); save("click",norm((np.sin(2*np.pi*1800*tt)+0.5*noise(0.06))*np.exp(-tt*120),0.8))
# sparkle: fast ascending bell arpeggio
tt=t(1.0); sp=np.zeros(len(tt))
for i,fr in enumerate([2093,2637,3136,4186,5274]):
    d=int(i*0.045*SR); s=tt[:len(tt)-d]; sp[d:]+=np.sin(2*np.pi*fr*s)*np.exp(-s*6)*(0.8**i)
save("sparkle",norm(sp,0.55))
tt=t(1.2); ch=np.zeros(len(tt))
for i,fr in enumerate([1318.5,1568,2093]):
    d=int(i*0.07*SR); s=tt[:len(tt)-d]; ch[d:]+=np.sin(2*np.pi*fr*s)*np.exp(-s*3.5)
save("chime",norm(ch,0.6))
# drip: water droplet (pitch-up blip)
tt=t(0.18); save("drip",norm(np.sin(2*np.pi*np.cumsum(600+1400*(tt/0.18)**0.5)/SR)*np.exp(-tt*28),0.7))
d=0.5; tt=t(d); rs=np.sin(2*np.pi*np.cumsum(300+1500*(tt/d)**2)/SR)*(tt/d)**2*0.4+lp(noise(d),0.3)*(tt/d)**3*0.6
save("riser",norm(rs,0.6))
# ---- music: airy clean pop, 104 bpm, Dmaj7 Bm7 Gmaj7 A6 (bright, premium skincare)
BPM=104; B=60/BPM; DUR=10.2; N=int(SR*DUR); m=np.zeros(N)
def mid(n): return 440*2**((n-69)/12)
chords=[[62,66,69,73],[59,62,66,69],[55,59,62,66],[57,61,64,66]]
bar=4*B
for k in range(int(DUR/bar)+1):
    c=chords[k%4]; s0=int(k*bar*SR); n=min(int(bar*SR),N-s0)
    if n<=0: break
    tt=np.arange(n)/SR
    for p in c:
        fr=mid(p); m[s0:s0+n]+=(np.sin(2*np.pi*fr*tt)+0.25*np.sin(2*np.pi*2*fr*tt))*(1-np.exp(-tt*8))*np.exp(-tt*0.35)*0.05
    m[s0:s0+n]+=np.sin(2*np.pi*mid(c[0]-24)*tt)*0.13*np.exp(-tt*0.5)
for b in range(int(DUR/B)+1):
    s0=int(b*B*SR)
    if s0>=N: break
    if b%2==0:
        n=min(int(0.3*SR),N-s0); tt=np.arange(n)/SR
        m[s0:s0+n]+=np.sin(2*np.pi*np.cumsum(50+70*np.exp(-tt*30))/SR)*np.exp(-tt*9)*0.32
    else:
        n=min(int(0.18*SR),N-s0); tt=np.arange(n)/SR; nz=rng.standard_normal(n)
        m[s0:s0+n]+=(nz-lp(nz,0.2))*np.exp(-tt*22)*0.12   # clap-ish
    for h in (0,0.5):
        s1=int((b+h)*B*SR); n=min(int(0.035*SR),N-s1)
        if n>0: nz=rng.standard_normal(n); m[s1:s1+n]+=(nz-lp(nz,0.5))*np.exp(-np.arange(n)/SR*100)*0.045
    # pluck arp on 8ths
    for h in (0,0.5):
        s1=int((b+h)*B*SR); n=min(int(0.25*SR),N-s1)
        if n>0:
            c=chords[int((b+h)*B/bar)%4]; fr=mid(c[(b*2+int(h*2))%4]+12); tt=np.arange(n)/SR
            m[s1:s1+n]+=np.sin(2*np.pi*fr*tt)*np.exp(-tt*14)*0.035
# hook: low-passed first 0.40s; silence before "Relaks!" punch (0.72->1.04), drop full at 1.04
filt=lp(m,0.08); x=np.ones(N); x[:int(0.40*SR)]=0
m=filt*(1-x)+m*x
g=np.ones(N); a,b_=int(0.70*SR),int(0.76*SR); g[a:b_]=np.linspace(1,0,b_-a); g[b_:int(1.04*SR)]=0
fe=int(0.3*SR); g[-fe:]*=np.linspace(1,0,fe)
sf.write("audio/music.wav",np.stack([norm(m*g,0.8)]*2,1).astype(np.float32),SR)
print("ok")
