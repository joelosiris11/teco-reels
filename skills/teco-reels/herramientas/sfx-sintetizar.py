# Genera whoosh.wav, pop.wav, ding.wav, buzz.wav, teclas.wav, hit.wav (sin descargar nada)
import numpy as np,wave
from scipy.signal import butter,lfilter
sr=44100;rng=np.random.default_rng(1)
def save(n,x):
    x=np.clip(x/np.max(np.abs(x)+1e-9)*0.9,-1,1);w=wave.open(n,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x*32767).astype(np.int16).tobytes());w.close()
t=np.arange(int(sr*0.45))/sr;n=rng.normal(0,1,len(t));env=np.sin(np.pi*t/t[-1])**2;out=np.zeros_like(n)
for i in range(0,len(n),512):
    f=600+5000*(i/len(n));b,a=butter(2,[max(100,f*0.6)/(sr/2),min(f*1.4,20000)/(sr/2)],'band');out[i:i+512]=lfilter(b,a,n[max(0,i-2048):i+512])[-len(n[i:i+512]):]
save('whoosh.wav',out*env)
t=np.arange(int(sr*0.09))/sr;f=900*np.exp(-t*30)+300;save('pop.wav',np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*45))
t=np.arange(int(sr*1.2))/sr;save('ding.wav',(np.sin(2*np.pi*1568*t)+0.5*np.sin(2*np.pi*2352*t)+0.25*np.sin(2*np.pi*3136*t))*np.exp(-t*4))
t=np.arange(int(sr*0.5))/sr;g=((t%0.25)<0.18).astype(float);save('buzz.wav',np.sin(2*np.pi*170*t)*(0.6+0.4*np.sign(np.sin(2*np.pi*30*t)))*g)
t=np.arange(int(sr*1.2))/sr;x=np.zeros_like(t)
for k in range(14):
    s=int((0.04+k*0.08+rng.uniform(-.015,.015))*sr);L=int(0.02*sr);x[s:s+L]+=rng.normal(0,1,L)*np.exp(-np.arange(L)/sr*300)*rng.uniform(.5,1)
save('teclas.wav',x)
t=np.arange(int(sr*0.3))/sr;save('hit.wav',np.sin(2*np.pi*(60+120*np.exp(-t*25))*t)*np.exp(-t*14)+0.2*rng.normal(0,1,len(t))*np.exp(-t*60))
