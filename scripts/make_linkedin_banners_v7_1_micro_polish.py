from PIL import Image, ImageDraw, ImageFont
import os

W,H=1584,396
OUT=r"C:\Users\tonyb\.openclaw\workspace\outputs\linkedin-banners-v7.1"
ASSETS=r"C:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets\linkedin-banners-v7.1"
os.makedirs(OUT,exist_ok=True)
os.makedirs(ASSETS,exist_ok=True)

def f(name,size):
    try:return ImageFont.truetype(f"C:/Windows/Fonts/{name}",size)
    except:return ImageFont.load_default()

H1=f("ariblk.ttf",56); H2=f("ariblk.ttf",50); B=f("arial.ttf",25); T=f("arialbd.ttf",20); C=f("arialbd.ttf",24)

def grad(a,b):
    im=Image.new("RGB",(W,H),a); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/(H-1); col=tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)); d.line([(0,y),(W,y)],fill=col)
    return im

def make(name,title1,title2,sub,chip,c1,c2,accent,muted):
    im=grad(c1,c2); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,42],fill=(0,0,0,48)); d.rectangle([0,H-40,W,H],fill=(0,0,0,62))
    d.text((72,11),"TONY BEAL  •  REVOPS / AI SALES SYSTEMS",font=T,fill=muted)
    d.line([(72,68),(276,68)],fill=accent,width=4)

    x=500
    d.text((x,88),title1,font=H1,fill=(245,248,255))
    d.text((x,154),title2,font=H2,fill=accent)
    d.text((x,230),sub,font=B,fill=muted)
    d.rounded_rectangle([x,282,x+470,344],radius=16,outline=accent,width=2,fill=(255,255,255,14))
    d.text((x+18,301),chip,font=C,fill=(248,250,255))

    p1=os.path.join(OUT,name); p2=os.path.join(ASSETS,name)
    im.save(p1,"PNG"); im.save(p2,"PNG"); print('Saved',p1)

def main():
    make("linkedin-banner-v7.1-corporate.png","Revenue Operations","& AI Sales Systems","Predictable B2B pipeline performance.","$20M+ Pipeline Generated",(10,25,49),(22,50,92),(125,173,255),(192,212,241))
    make("linkedin-banner-v7.1-luxury.png","Tony Beal","Revenue Architecture","for High-Performance GTM Teams","$20M+ Pipeline Impact",(13,15,22),(28,34,47),(201,169,106),(218,210,196))
    make("linkedin-banner-v7.1-bold.png","Build Pipeline","That Actually Converts","RevOps + AI execution with measurable outcomes.","15+ Years  •  $20M+ Pipeline",(9,15,31),(25,46,90),(94,213,255),(186,211,245))
    make("linkedin-banner-v7.1-recommended-final.png","Revenue Operations","& AI Sales Systems","Predictable B2B pipeline performance.","$20M+ Pipeline Generated",(8,23,46),(20,47,88),(132,181,255),(196,216,244))

if __name__=='__main__': main()
