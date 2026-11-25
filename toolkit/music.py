# Original royalty-free music bed: warm chords + soft beat. Usage: python3 music.py out.wav seconds [bpm] [seed]
import numpy as np, sys, wave
out=sys.argv[1]; dur=float(sys.argv[2]); bpm=float(sys.argv[3]) if len(sys.argv)>3 else 100; seed=int(sys.argv[4]) if len(sys.argv)>4 else 1
sr=44100; n=int(sr*dur); t=np.arange(n)/sr; rng=np.random.default_rng(seed)
beat=60/bpm; bar=beat*4
progs=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]
rng.shuffle(progs)
hz=lambda m:440*2**((m-69)/12)
mix=np.zeros(n)
# pad
for i in range(int(dur/bar)+1):
    s=int(i*bar*sr); e=min(n,int((i+1)*bar*sr)+int(.3*sr))
    if s>=n: break
    tt=t[s:e]-t[s]; env=np.minimum(1,tt/0.6)*np.exp(-tt*0.25)
    for m in progs[i%4]:
        f=hz(m); mix[s:e]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt+0.4)+0.15*np.sin(2*np.pi*f*1.003*tt))
    f=hz(progs[i%4][0]-12); mix[s:e]+=0.10*env*np.sin(2*np.pi*f*tt)
# drums
k=int(0.25*sr); kt=np.arange(k)/sr; kick=np.sin(2*np.pi*(50+90*np.exp(-kt*30))*kt)*np.exp(-kt*9)
h=int(0.05*sr); hat=rng.normal(0,1,h)*np.exp(-np.arange(h)/sr*90); hat=np.diff(hat,prepend=0)
for j in range(int(dur/beat)+1):
    s=int(j*beat*sr)
    if j>=8 or True:
        if j%2==0 and s+k<n: mix[s:s+k]+=0.35*kick
        hs=int((j+0.5)*beat*sr)
        if hs+h<n: mix[hs:hs+h]+=0.05*hat
# arp sparkle
for j in range(int(dur/(beat/2))):
    s=int(j*beat/2*sr); bi=int(j*beat/2/bar)%4; m=progs[bi][j%4]+12
    L=int(0.25*sr)
    if s+L<n: tt=np.arange(L)/sr; mix[s:s+L]+=0.025*np.sin(2*np.pi*hz(m)*tt)*np.exp(-tt*10)
# fades + normalise
fi=int(0.8*sr); fo=int(1.5*sr); mix[:fi]*=np.linspace(0,1,fi); mix[-fo:]*=np.linspace(1,0,fo)
mix=np.tanh(mix*1.2); mix/=np.max(np.abs(mix))*1.12
st=np.stack([mix,np.roll(mix,int(0.012*sr))],1)
with wave.open(out,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype(np.int16).tobytes())
