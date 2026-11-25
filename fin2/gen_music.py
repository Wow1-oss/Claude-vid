import numpy as np, soundfile as sf
SR=44100; rng=np.random.default_rng(11)
def lp(x,a):
    y=np.zeros_like(x)
    for i in range(1,len(x)): y[i]=y[i-1]+a*(x[i]-y[i-1])
    return y
DUR=8.63; B=DUR/16; N=int(SR*DUR); m=np.zeros(N)
def mid(n): return 440*2**((n-69)/12)
chords=[[57,60,64,67],[53,57,60,64],[60,64,67,71],[55,59,62,67]]  # Cmaj7 G Am F G7
for k in range(4):
    c=chords[k]; s0=int(k*4*B*SR); n=min(int(4*B*SR),N-s0); tt=np.arange(n)/SR
    for st in range(8):  # plucky 8th-note stabs
        a=int(st*B/2*SR); seg=tt[:n-a]
        if len(seg)<=0: continue
        for p in c:
            fr=mid(p+12); m[s0+a:s0+n]+= (np.sin(2*np.pi*fr*seg)+0.3*np.sin(4*np.pi*fr*seg))*np.exp(-seg*9)*0.035*(1 if st%2==0 else 0.6)
    for p in c[:3]:  # soft pad
        fr=mid(p); m[s0:s0+n]+=np.sin(2*np.pi*fr*tt)*0.025*(1-np.exp(-tt*4))
    fr=mid(c[0]-24)
    for st in range(4):
        a=int(st*B*SR); seg=tt[:n-a]; m[s0+a:s0+n]+=np.sin(2*np.pi*fr*seg)*np.exp(-seg*4)*0.14
for b in range(16):
    s0=int(b*B*SR); n=min(int(0.3*SR),N-s0); tt=np.arange(n)/SR
    f=50+80*np.exp(-tt*32); m[s0:s0+n]+=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*10)*0.4
    if b%2==1:
        n2=min(int(0.18*SR),N-s0); nz=rng.standard_normal(n2); m[s0:s0+n2]+=(nz-lp(nz,0.2))*np.exp(-np.arange(n2)/SR*22)*0.16
    for h in (0.5,):
        s1=int((b+h)*B*SR); n3=min(int(0.05*SR),N-s1)
        if n3>0: nz=rng.standard_normal(n3); m[s1:s1+n3]+=(nz-lp(nz,0.5))*np.exp(-np.arange(n3)/SR*80)*0.07
g=np.ones(N); a,b_=int(6.80*SR),int(6.88*SR); g[a:b_]=np.linspace(1,0,b_-a); g[b_:int(7.20*SR)]=0
fi=int(0.25*SR); g[:fi]*=np.linspace(0.3,1,fi); fe=int(0.25*SR); g[-fe:]*=np.linspace(1,0,fe)
m*=g; m=m/np.abs(m).max()*0.8
sf.write("audio/music.wav",np.stack([m,m],1).astype(np.float32),SR); print("ok")
