import numpy as np, soundfile as sf
SR=44100; rng=np.random.default_rng(7)
def t(d): return np.arange(int(SR*d))/SR
def env(n,a=0.005,r=None):
    e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na)
    if r: nr=int(r*SR); e[-nr:]*=np.linspace(1,0,nr)
    return e
def lp(x,k): # simple one-pole lowpass
    y=np.zeros_like(x); a=k
    for i in range(1,len(x)): y[i]=y[i-1]+a*(x[i]-y[i-1])
    return y
def norm(x,p=0.9): return x/(np.abs(x).max()+1e-9)*p
def save(n,x): sf.write(f"audio/{n}.wav",np.stack([x,x],1).astype(np.float32),SR)
def noise(d): return rng.standard_normal(int(SR*d))
# whoosh: filtered noise swell
def whoosh(d=0.45,bright=0.25):
    n=noise(d); x=lp(n,bright)-lp(n,0.02); tt=t(d)
    e=np.sin(np.pi*np.clip(tt/d,0,1))**2
    return norm(x*e,0.8)
save("whoosh",whoosh(0.45)); save("swish",whoosh(0.25,0.4))
# hit/thump
tt=t(0.5); f=55+90*np.exp(-tt*25); hit=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7)+0.3*lp(noise(0.5),0.3)*np.exp(-tt*40)
save("hit",norm(hit,0.95))
# boom (reveal)
tt=t(1.4); f=42+60*np.exp(-tt*12); boom=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.8)
shim=sum(np.sin(2*np.pi*fr*tt)*np.exp(-tt*(2.5+i)) for i,fr in enumerate([1568,2093,2637,3136]))*0.12
save("boom",norm(boom+shim+0.2*lp(noise(1.4),0.2)*np.exp(-tt*9),0.95))
# pop
tt=t(0.12); f=900-500*tt/0.12; pop=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*35); save("pop",norm(pop,0.8))
# tick / click
tt=t(0.03); save("tick",norm(np.sin(2*np.pi*2400*tt)*np.exp(-tt*200),0.7))
tt=t(0.06); save("click",norm((np.sin(2*np.pi*1800*tt)+0.5*noise(0.06))*np.exp(-tt*120),0.8))
# chime
tt=t(1.2); ch=np.zeros(len(tt))
for i,fr in enumerate([1318.5,1568,2093]):
    d=int(i*0.07*SR); s=np.sin(2*np.pi*fr*tt[:len(tt)-d])*np.exp(-tt[:len(tt)-d]*3.5); ch[d:]+=s
save("chime",norm(ch,0.6))
# error buzz (serba tak kena)
tt=t(0.35); bz=np.sign(np.sin(2*np.pi*140*tt))*0.5+np.sin(2*np.pi*147*tt)*0.5; bz=lp(bz,0.15)*env(len(tt),0.005,0.08)
save("buzz",norm(bz,0.6))
# riser
d=0.6; tt=t(d); f=300+1500*(tt/d)**2; rs=np.sin(2*np.pi*np.cumsum(f)/SR)*(tt/d)**2*0.4+lp(noise(d),0.3)*(tt/d)**3*0.6
save("riser",norm(rs,0.6))
# ---- music: warm lo-fi, 96 bpm, Fmaj7 Em7 Dm7 Cmaj7
BPM=96; B=60/BPM; DUR=17.8; N=int(SR*DUR); m=np.zeros(N); T=np.arange(N)/SR
def mid(n): return 440*2**((n-69)/12)
# shimmer (premium sparkle)
tt=t(0.9); sh=sum(np.sin(2*np.pi*fr*tt)*np.exp(-tt*(4+i)) for i,fr in enumerate([2637,3136,3520,4186]))
save("shimmer",norm(sh*env(len(tt),0.01),0.5))
# ---- music: airy travel pop, 112 bpm, Am F C G with plucks + sub
import sys, json as _j
TOTAL=float(sys.argv[1]); json_P=_j.loads(sys.argv[2])
BPM=112; B=60/BPM; N=int(SR*(TOTAL+0.2)); m=np.zeros(N)
def mid(n): return 440*2**((n-69)/12)
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]
bar=4*B
for k in range(int(TOTAL/bar)+2):
    c=chords[k%4]; s0=int(k*bar*SR)
    if s0>=N: break
    n=min(int(bar*SR),N-s0); tt=np.arange(n)/SR
    for p in c:  # soft pad
        fr=mid(p); m[s0:s0+n]+=np.sin(2*np.pi*fr*tt+0.3*np.sin(2*np.pi*0.5*tt))*0.035*np.minimum(1,tt/0.25)
    fr=mid(c[0]-24); m[s0:s0+n]+=np.sin(2*np.pi*fr*tt)*0.13*np.exp(-tt*0.5)
    for e in range(8):  # pluck arp on 8ths
        s1=s0+int(e*B/2*SR); n1=min(int(0.3*SR),N-s1)
        if n1<=0: continue
        tt1=np.arange(n1)/SR; fr=mid(c[[0,2,1,3,2,1,3,2][e]]+12)
        m[s1:s1+n1]+=(np.sin(2*np.pi*fr*tt1)+0.3*np.sin(4*np.pi*fr*tt1))*np.exp(-tt1*14)*0.05
for b in range(int(TOTAL/B)+2):
    s0=int(b*B*SR)
    if s0>=N: break
    n=min(int(0.3*SR),N-s0); tt=np.arange(n)/SR; f=48+80*np.exp(-tt*32)
    m[s0:s0+n]+=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*10)*0.33
    if b%2==1:
        n=min(int(0.18*SR),N-s0); tt=np.arange(n)/SR; nz=rng.standard_normal(n)
        m[s0:s0+n]+=(nz-lp(nz,0.2))*np.exp(-tt*22)*0.10
    for h in (0.5,):
        s1=int((b+h)*B*SR); n=min(int(0.04*SR),N-s1)
        if n>0: nz=rng.standard_normal(n); m[s1:s1+n]+=(nz-lp(nz,0.5))*np.exp(-np.arange(n)/SR*90)*0.06
g=np.ones(N)
# intro filtered feel: lower for cold open
g[:int(1.45*SR)]=0.7
# silence before punchline(s): P list
for P in json_P:
    a_,b_=int((P-0.42)*SR),int((P-0.34)*SR); g[a_:b_]=np.minimum(g[a_:b_],np.linspace(1,0,b_-a_)); g[b_:int(P*SR)]=0
fe=int(0.3*SR); g[int((TOTAL-0.3)*SR):int(TOTAL*SR)]*=np.linspace(1,0,int(TOTAL*SR)-int((TOTAL-0.3)*SR)); g[int(TOTAL*SR):]=0
m=m*g
sf.write("audio/music.wav",np.stack([norm(m,0.8)]*2,1).astype(np.float32),SR)
print("ok")
