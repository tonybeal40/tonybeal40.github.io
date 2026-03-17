"""
LinkedIn Article Cover Image - NYT Magazine Style
1200 x 644px
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

W, H = 1200, 644
BASE = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site"

def ft(f, s):
    try:    return ImageFont.truetype(f"C:/Windows/Fonts/{f}", s)
    except: return ImageFont.load_default()

# ── Canvas: dark navy ──
canvas = Image.new("RGBA", (W, H), (4, 6, 20, 255))

# ── Mesh gradient orbs ──
orbs = [
    (200,  -60, 500, (37,  99, 235), 45),
    (-80,  400, 420, (99, 102, 241), 35),
    (700,  100, 600, (6,  182, 212), 28),
    (1100, -40, 480, (139, 92, 246), 38),
    (1150, 580, 400, (245,158,  11), 22),
    (500,  700, 380, (16, 185, 129), 20),
]
orb_layer = Image.new("RGBA", (W, H), (0,0,0,0))
od = ImageDraw.Draw(orb_layer)
for ox, oy, r, col, strength in orbs:
    for rad in range(r, 0, -5):
        t = rad/r
        a = int(strength * math.exp(-((1-t)*3.2)**1.5))
        od.ellipse([ox-rad,oy-rad,ox+rad,oy+rad], fill=(*col,a))
orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(22))
canvas = Image.alpha_composite(canvas, orb_layer)

# ── Subtle hex grid ──
import random
random.seed(42)
hex_r  = 36
hex_hs = hex_r * math.sqrt(3)
hex_layer = Image.new("RGBA", (W, H), (0,0,0,0))
hd = ImageDraw.Draw(hex_layer)
for row in range(-1, int(H/hex_hs)+3):
    for col in range(-1, int(W/(hex_r*1.5))+3):
        hcx = col*hex_r*3 + (hex_r*1.5 if row%2 else 0)
        hcy = row * hex_hs
        verts = [(hcx + hex_r*math.cos(math.radians(60*i-30)),
                  hcy + hex_r*math.sin(math.radians(60*i-30))) for i in range(6)]
        hd.polygon(verts, outline=(96,165,250,10))
canvas = Image.alpha_composite(canvas, hex_layer)

# ── Dark scrim left 70% for text readability ──
scrim = Image.new("RGBA",(W,H),(0,0,0,0))
sd = ImageDraw.Draw(scrim)
for x in range(W):
    t = 1 - (x/W)**0.5
    sd.line([(x,0),(x,H)], fill=(0,0,0,int(130*t)))
canvas = Image.alpha_composite(canvas, scrim)

draw = ImageDraw.Draw(canvas)

# ── Top gradient line ──
for x in range(W):
    t = x/W
    r=int(37+(139-37)*t); g=int(99+(92-99)*t); b=int(235+(246-235)*t)
    draw.point((x,0), fill=(r,g,b))
    draw.point((x,1), fill=(r,g,b))
    draw.point((x,2), fill=(r,g,b,120))

# ── TONY BEAL tag top-left ──
f_badge = ft("arialbd.ttf", 18)
f_tag   = ft("arial.ttf",   16)
f_label = ft("arialbd.ttf", 14)

draw.rounded_rectangle([48,30,220,58], radius=14, fill=(37,99,235,200), outline=(96,165,250,160), width=1)
draw.text((62, 36), "TONY BEAL  ·  tonybeal.net", font=f_badge, fill=(255,255,255))

# ── Category label ──
draw.text((48, 76), "REVENUE OPERATIONS  ·  AI SALES SYSTEMS  ·  GTM STRATEGY", font=f_label, fill=(96,165,250,200))

# ── Accent rule ──
for x in range(420):
    t = x/420
    a = int(220*(1-t))
    draw.line([(48,100),(48+x,100)], fill=(96,165,250,a), width=1)

# ── Main headline ──
f_h1a = ft("ariblk.ttf", 80)
f_h1b = ft("ariblk.ttf", 62)
f_sub  = ft("arial.ttf",  24)

line1 = "I Built a $20M Pipeline"
line2 = "With AI. Here's Exactly"
line3 = "How I Did It."

draw.text((50, 114), line1, font=f_h1a, fill=(255,255,255))
draw.text((50, 204), line2, font=f_h1a, fill=(255,255,255))
# line3 in blue accent
draw.text((50, 294), line3, font=f_h1b, fill=(96,165,250))

# ── Subheadline ──
draw.text((50, 382), "The exact system, tools, and thinking that turned", font=f_sub, fill=(180,200,255,220))
draw.text((50, 412), "cold accounts into $20M+ in cumulative pipeline.", font=f_sub, fill=(180,200,255,220))

# ── Bottom accent bar ──
for x in range(W):
    t = x/W
    r=int(37+(139-37)*t); g=int(99+(92-99)*t); b=int(235+(246-235)*t)
    draw.point((x,H-1), fill=(r,g,b))
    draw.point((x,H-2), fill=(r,g,b))

# ── Stat badges bottom left ──
stats = [("$20M+","Pipeline",(245,158,11)), ("3,700+","Accounts",(52,211,153)), ("15+","Years B2B",(99,102,241))]
sx = 48
for val, lbl, col in stats:
    f_sv = ft("ariblk.ttf", 28)
    f_sl = ft("arial.ttf",  13)
    vw = int(draw.textlength(val, font=f_sv))
    lw = int(draw.textlength(lbl, font=f_sl))
    bw = max(vw, lw) + 24
    draw.rounded_rectangle([sx, H-90, sx+bw, H-14], radius=8,
                            fill=(6,10,30,210), outline=(*col,160), width=1)
    draw.line([(sx+1,H-90),(sx+1,H-14)], fill=(*col,220), width=3)
    draw.text((sx+12, H-86), val, font=f_sv, fill=(255,255,255))
    draw.text((sx+12, H-52), lbl, font=f_sl, fill=col)
    sx += bw + 14

# ── Right side: photo circle ──
PHOTO = os.path.join(BASE, "headshot-new.png")
R  = 220
CX = 970
CY = H // 2 + 20

# Glow rings
hl = Image.new("RGBA", (W, H), (0,0,0,0))
hd2 = ImageDraw.Draw(hl)
for rad in range(R+80, R-1, -4):
    t = (rad-R)/80
    a = int(25 * math.exp(-t*3))
    hd2.ellipse([CX-rad,CY-rad,CX+rad,CY+rad], fill=(99,102,241,a))
canvas = Image.alpha_composite(canvas, hl)

photo = Image.open(PHOTO).convert("RGBA")
pw, ph = photo.size
diam   = R * 2
scale  = diam / min(pw, ph)
nw2 = int(pw*scale); nh2 = int(ph*scale)
photo = photo.resize((nw2, nh2), Image.LANCZOS)
cx_off = (nw2-diam)//2; cy_off = (nh2-diam)//2
photo = photo.crop((cx_off, cy_off, cx_off+diam, cy_off+diam))
mask = Image.new("L", (diam,diam), 0)
ImageDraw.Draw(mask).ellipse([0,0,diam,diam], fill=255)
rgb3 = ImageEnhance.Brightness(photo.convert("RGB")).enhance(0.88)
rgb3 = ImageEnhance.Contrast(rgb3).enhance(1.15)
photo_rgb = rgb3.convert("RGBA")
photo_rgb.putalpha(mask)
canvas.paste(photo_rgb, (CX-R, CY-R), photo_rgb)
bd = ImageDraw.Draw(canvas)
bd.ellipse([CX-R-3,CY-R-3,CX+R+3,CY+R+3], outline=(96,165,250,220), width=3)
bd.ellipse([CX-R-8,CY-R-8,CX+R+8,CY+R+8], outline=(96,165,250,60),  width=2)

# Name under photo
draw = ImageDraw.Draw(canvas)
f_nm = ft("arialbd.ttf", 20)
f_rl = ft("arial.ttf",   15)
nm = "Tony Beal"
nw3 = int(draw.textlength(nm, font=f_nm))
draw.text((CX-nw3//2, CY+R+14), nm, font=f_nm, fill=(255,255,255))
rl = "Revenue Operations Leader"
rw = int(draw.textlength(rl, font=f_rl))
draw.text((CX-rw//2, CY+R+40), rl, font=f_rl, fill=(96,165,250))

out = os.path.join(BASE, "assets", "linkedin-article-cover-v2.png")
canvas.convert("RGB").save(out, "PNG")
print(f"Saved: {out}")
