# Título «El poder de la creatividad» animado + cierre con el logo de T-ECO.
import sys,glob,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
src,out=sys.argv[1],sys.argv[2];only=[float(x) for x in sys.argv[3:]]
W,H=1080,1920
F6=lambda s:ImageFont.truetype('/tmp/sora-600.ttf',s);F7=lambda s:ImageFont.truetype('/tmp/sora-700.ttf',s)
NAVY=(8,37,103);CREAM=(246,243,236)
def grad(w,h):
    stops=[(0,(79,195,240)),(.5,(108,194,74)),(1,(255,209,42))];x=np.linspace(0,1,w);c=np.zeros((w,3))
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
        m=(x>=a)&(x<=b);k=((x[m]-a)/(b-a))[:,None];c[m]=np.array(ca)*(1-k)+np.array(cb)*k
    return Image.fromarray(np.repeat(c[None],h,0).astype(np.uint8))
def sprite(txt,font,fill=None,gradient=None,stroke=0,ref=None):
    bb=list(font.getbbox(txt))
    if ref:rb=font.getbbox(ref);bb[1],bb[3]=rb[1],rb[3]
    w,h=bb[2]-bb[0]+40,bb[3]-bb[1]+40
    m=Image.new('L',(w,h));ImageDraw.Draw(m).text((20-bb[0],20-bb[1]),txt,font=font,fill=255)
    sh=m.filter(ImageFilter.GaussianBlur(10))
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    im.paste((5,15,45,170),(0,0),sh.point(lambda v:v*0.85))
    if stroke:
        st=m.filter(ImageFilter.MaxFilter(stroke*2+1));im.paste(NAVY+(255,),(0,0),st)
    body=gradient.resize((w,h)) if gradient else Image.new('RGB',(w,h),fill)
    im.paste(body,(0,0),m);return im
# línea 1 y letras de la línea 2
L1=sprite('El poder de la',F6(62),fill=(255,255,255))
f2=F7(132);word='creatividad';G=grad(900,200)
bbw=f2.getbbox(word);ww=bbw[2]-bbw[0];x0=(W-ww)//2
letters=[]
for i,ch in enumerate(word):
    px=f2.getlength(word[:i]);cw=f2.getlength(ch)
    g=G.crop((int(px*900/ww),0,int((px+cw)*900/ww)+1,200))
    letters.append((x0+px-20,sprite(ch,f2,gradient=g,stroke=3,ref='dgfl')))
logo=Image.open('/home/claude/bm/teco-plataforma/assets/teco-logo.png').convert('RGBA')
url=sprite('t-ecogroup.net',F6(54),fill=NAVY);url=Image.new('RGBA',url.size,(0,0,0,0))
uimg=Image.new('RGBA',(700,120),(0,0,0,0));d=ImageDraw.Draw(uimg);fu=F6(52);tw=fu.getlength('t-ecogroup.net');d.text(((700-tw)/2,30),'t-ecogroup.net',font=fu,fill=NAVY)
timg=Image.new('RGBA',(1000,140),(0,0,0,0));d=ImageDraw.Draw(timg);ft=F7(64);s1='Crea, aprende y sube de nivel';tw=ft.getlength(s1);d.text(((1000-tw)/2,30),s1,font=ft,fill=NAVY)
eo=lambda x:1-(1-x)**3
def eb(x):c1=1.9;c3=c1+1;return 1+c3*(x-1)**3+c1*(x-1)**2
cl=lambda x:max(0.,min(1.,x))
def put(base,spr,x,y,alpha=1,scale=1):
    if alpha<=0:return
    s=spr
    if abs(scale-1)>1e-3:
        s=spr.resize((max(1,round(spr.width*scale)),max(1,round(spr.height*scale))),Image.LANCZOS);x+= (spr.width-s.width)/2;y+=(spr.height-s.height)/2
    if alpha<1:a=s.getchannel('A').point(lambda v:v*alpha);s=s.copy();s.putalpha(a)
    base.alpha_composite(s,(round(x),round(y)))
E0=23.4
TOP=np.zeros((560,W,4),np.uint8);TOP[...,3]=(np.linspace(1,0,560)**1.6*170).astype(np.uint8)[:,None];TOP[...,:3]=(5,12,35);TOPI=Image.fromarray(TOP,'RGBA')
files=sorted(glob.glob(src+'/c*.jpg'))
idx=[round(t*30) for t in only] if only else range(len(files))
for i in idx:
    t=i/30;im=Image.open(f'{src}/c{i:04d}.jpg').convert('RGBA')
    if t<E0+0.35:
        sh=cl(t/0.4)*(1-cl((t-(E0-0.3))/0.3));im.alpha_composite(Image.fromarray(TOP).point(lambda v:v) if False else TOPI if sh>=1 else Image.blend(Image.new('RGBA',TOPI.size,(0,0,0,0)),TOPI,sh),(0,0))
        fo=1-cl((t-(E0-0.3))/0.3)
        a=eo(cl((t-0.2)/0.5));put(im,L1,(W-L1.width)/2,215+40*(1-a),a*fo)
        for k,(lx,sp) in enumerate(letters):
            p=cl((t-0.55-k*0.06)/0.35)
            if p<=0:continue
            put(im,sp,lx,285+60*(1-eo(p)),min(1,p*2)*fo,0.6+0.4*eb(p))
        # brillo que recorre la palabra cada pocos segundos
    if t>=E0:
        st=np.floor(eo(cl((t-E0)/0.3))*6)/6;h=round(H*st)
        if h>0:im.alpha_composite(Image.new('RGBA',(W,h),CREAM+(255,)),(0,H-h))
        lp=cl((t-E0-0.35)/0.45)
        if lp>0:
            sc=0.35+0.65*eb(lp)+0.015*np.sin((t-E0)*2*np.pi*152/60)*np.exp(-(t-E0-0.8)*0.5)
            L=logo.resize((round(560*sc),round(560*sc)),Image.LANCZOS);im.alpha_composite(L,((W-L.width)//2,round(760-L.height/2)))
        a=eo(cl((t-E0-0.85)/0.3));put(im,timg,(W-1000)/2,1090+30*(1-a),a)
        a=eo(cl((t-E0-1.15)/0.3));put(im,uimg,(W-700)/2,1210+30*(1-a),a)
    im.convert('RGB').save(f'{out}/c{i:04d}.jpg',quality=90)
print('ok')
