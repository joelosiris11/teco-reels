# Aula real de T-ECO con MacBook: la cámara arranca abierta y se acerca hasta la pantalla.
import sys,glob,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
src=cv2.imread('teco-aula-mac.jpg');out=sys.argv[1];only=[float(x) for x in sys.argv[2:]]
W,H=1080,1920;DUR=27.0;EDELAY=2.0
# pantalla verde
hsv=cv2.cvtColor(src,cv2.COLOR_BGR2HSV);m=cv2.inRange(hsv,(40,90,90),(85,255,255))
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);c=max(cs,key=cv2.contourArea)
pts=c.reshape(-1,2).astype(np.float32);sm=pts.sum(1);df=pts[:,0]-pts[:,1]
q=np.array([pts[sm.argmin()],pts[df.argmax()],pts[sm.argmax()],pts[df.argmin()]],np.float32)
cen=q.mean(0);q=cen+(q-cen)*1.012          # un pelín más grande para tapar el borde verde
# quitar verde residual de la foto
g=src.astype(np.float32);sp=np.clip(g[...,1]-np.maximum(g[...,0],g[...,2]),0,None);g[...,1]-=sp*0.9;src=np.clip(g,0,255).astype(np.uint8)
# foto a 9:16: alto 1920, recorte horizontal hacia la laptop
s0=H/src.shape[0];base=cv2.resize(src,(round(src.shape[1]*s0),H),interpolation=cv2.INTER_CUBIC)
x0=int(np.clip(cen[0]*s0-W/2,0,base.shape[1]-W));base=base[:,x0:x0+W].copy();B=np.float32([[s0,0,-x0],[0,s0,0],[0,0,1]])
qb=(np.c_[q,np.ones(4)]@B.T)[:,:2].astype(np.float32);scx,scy=qb.mean(0);sw=float(np.ptp(qb[:,0]))
print('pantalla en base',qb.round().tolist(),'ancho',sw)
zEnd=0.9*W/sw
# texto
cap=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(cap);f=ImageFont.truetype('/tmp/inter-700.ttf',76)
txt='El poder de la IA';bb=d.textbbox((0,0),txt,font=f);tw=bb[2]-bb[0];th=bb[3]-bb[1]
X=(W-tw)//2;Y=300;d.rounded_rectangle((X-34,Y-18,X+tw+34,Y+th+30),18,fill=(0,0,0,255));d.text((X-bb[0],Y-bb[1]+4),txt,font=f,fill='white')
cap=np.array(cap).astype(np.float32);ca=cap[...,3:4]/255;capbgr=cap[...,[2,1,0]]
ed0=cv2.imread('/tmp/edfr/e0000.jpg');eh,ew=ed0.shape[:2]
Hq=cv2.getPerspectiveTransform(np.float32([[0,0],[ew,0],[ew,eh],[0,eh]]),qb)
white=np.full((eh,ew),255,np.uint8)
ei=lambda x:x*x*(3-2*x)
rng=np.random.default_rng(5);NF=round(DUR*30)
frames=[round(t*30) for t in only] if only else range(NF)
for i in frames:
    t=i/30
    # acercamiento: 0-1.5 casi quieto, 1.5-6.5 entra a la pantalla, luego deriva suave
    a=ei(np.clip((t-1.5)/5.0,0,1))
    z=(1+0.04*min(t,1.5)/1.5)*(1-a)+zEnd*a + 0.03*max(0,t-6.5)/17
    cx=W/2*(1-a)+scx*a; cy=H/2*(1-a)+(scy)*a
    ty=H/2+80*a   # la pantalla queda un poco por debajo del texto
    sx=np.sin(t*1.3)*6+np.sin(t*3.1+1)*3;sy=np.cos(t*1.1)*5+np.sin(t*2.7)*3;rz=np.radians(np.sin(t*.9)*.5)
    R=np.float32([[np.cos(rz),-np.sin(rz)],[np.sin(rz),np.cos(rz)]])*z
    A=np.eye(3,dtype=np.float32);A[:2,:2]=R;A[:2,2]=np.float32([W/2+sx,ty+sy])-R@np.float32([cx,cy])
    img=cv2.warpAffine(base,A[:2],(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    # el fondo se desenfoca un poco al acercarse (profundidad de campo)
    if a>0.05:img=cv2.GaussianBlur(img,(0,0),0.5+2.5*a)
    te=max(0.0,t-EDELAY);k=min(round(te*30),674)
    ed=cv2.imread(f'/tmp/edfr/e{k:04d}.jpg')
    Hf=A@Hq
    scr=cv2.warpPerspective(ed,Hf,(W,H),flags=cv2.INTER_AREA if z<2 else cv2.INTER_LINEAR).astype(np.float32)
    msk=cv2.warpPerspective(white,Hf,(W,H),flags=cv2.INTER_LINEAR).astype(np.float32)[...,None]/255
    scr=scr*1.04+6
    img=img*(1-msk)+scr*msk
    img+=rng.normal(0,4,(H,W,1)).astype(np.float32)
    cv2.imwrite(f'{out}/c{i:04d}.jpg',np.clip(img,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,90])
print('ok')
