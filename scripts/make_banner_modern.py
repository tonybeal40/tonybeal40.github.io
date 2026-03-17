"""
LinkedIn Banner - Modern Tech Website Style
Photo RIGHT | Mesh gradient background | Dynamic text left | 1584x396
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, random

W, H = 1584, 396
PHOTO = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\headshot-hero.png"
OUT   = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets\linkedin-banner-movie.png"
random.seed(12)

def ft(f, s):
    try:    return ImageFont.truetype(f"C:/Windows/Fonts/{f}", s)
    except: return ImageFont.load_default()

F = {
    "name":   ft("ariblk.ttf",  110),
    "role":   ft("arialbd.ttf",  32),
    "tag":    ft("arial.ttf",    22),
    "sm":     ft("arial.ttf",    18),
    "badge":  ft("arialbd.ttf",  16),
    "stat":   ft("ariblk.ttf",   40),
    "stlbl":  ft("arial.ttf",    14),
    "url":    ft("arialbd.ttf",  17),
}

# ── 1. MESH GRADIENT BACKGROUND ──────────────────────────────────────────────
# Base: very dark navy
canvas = Image.new("RGBA", (W, H), (4, 6, 20, 255))
d = ImageDraw.Draw(canvas)

# Large glowing orbs — modern SaaS style
orbs = [
    (300,  -80,  420, (99,  102, 241, 1), 40),   # purple top-left
    (-60,  280,  380, (37,  99,  235, 1), 35),    # blue bottom-left
    (820,  200,  500, (6,   182, 212, 1), 30),    # cyan center
    (1400, -50,  450, (139, 92,  246, 1), 38),    # violet top-right
    (1500, 350,  380, (16,  185, 129, 1), 25),    # green bottom-right
    (600,  400,  350, (245, 158,  11, 1), 20),    # amber bottom
]

orb_layer = Image.new("RGBA", (W, H), (0,0,0,0))
od = ImageDraw.Draw(orb_layer)
for ox, oy, orb_r, (r,g,b,_), strength in orbs:
    for radius in range(orb_r, 0, -4):
        t = radius / orb_r
        a = int(strength * math.exp(-((1-t)*3.5)**1.5))
        od.ellipse([ox-radius, oy-radius, ox+radius, oy+radius],
                   fill=(r, g, b, a))

orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(18))
canvas = Image.alpha_composite(canvas, orb_layer)

# Subtle hex grid (not plain squares)
import math as _math
hex_r = 28
hex_hs = hex_r * _math.sqrt(3)
hex_layer = Image.new("RGBA", (W, H), (0,0,0,0))
hd = ImageDraw.Draw(hex_layer)
for row in range(-1, int(H/hex_hs)+3):
    for col in range(-1, int(W/(hex_r*1.5))+3):
        hcx = col*hex_r*3 + (hex_r*1.5 if row%2 else 0)
        hcy = row * hex_hs
        verts = [(hcx + hex_r*_math.cos(_math.radians(60*i-30)),
                  hcy + hex_r*_math.sin(_math.radians(60*i-30))) for i in range(6)]
        hd.polygon(verts, outline=(96, 165, 250, 14))
canvas = Image.alpha_composite(canvas, hex_layer)

# Particle dots (network nodes)
pd = ImageDraw.Draw(canvas)
nodes = [(random.randint(0,W), random.randint(0,H)) for _ in range(80)]
for nx, ny in nodes:
    size = random.choice([1,1,1,2,3])
    a    = random.randint(20, 80)
    col  = random.choice([(96,165,250,a),(52,211,153,a),(139,92,246,a),(255,255,255,a)])
    pd.ellipse([nx, ny, nx+size, ny+size], fill=col)

# Connect some nearby nodes
for i, (nx, ny) in enumerate(nodes[:40]):
    for mx, my in nodes[i+1:i+4]:
        dist = math.hypot(mx-nx, my-ny)
        if dist < 120:
            a = int(30 * (1 - dist/120))
            pd.line([(nx,ny),(mx,my)], fill=(96,165,250,a), width=1)

# Film grain texture
for _ in range(1500):
    x = random.randint(0,W); y = random.randint(0,H)
    v = random.randint(50,100)
    pd.point((x,y), fill=(v,v,v,random.randint(4,10)))

# ── 2. PHOTO (right side, LARGE, full height, blended) ───────────────────────
photo = Image.open(PHOTO).convert("RGBA")
pw, ph = photo.size

# Target photo width = 62% of banner so it fills center-right with no gap
target_w = int(W * 0.62)          # ~982px
scale    = target_w / pw
nw       = target_w
nh       = int(ph * scale)

# If scaled height < banner, scale by height instead
if nh < H:
    scale = H / ph
    nh    = H
    nw    = int(pw * scale)

photo = photo.resize((nw, nh), Image.LANCZOS)

# Crop to banner height — start 25% down so face is centered, not cut off
y_off = int(nh * 0.22)
photo = photo.crop((0, y_off, nw, y_off + H))

# Boost contrast
rgb     = ImageEnhance.Contrast(photo.convert("RGB")).enhance(1.35)
rgb     = ImageEnhance.Brightness(rgb).enhance(1.15)
photo_e = rgb.convert("RGBA")

orig_raw = Image.open(PHOTO).convert("RGBA").resize((nw, nh), Image.LANCZOS).crop((0, y_off, nw, y_off + H))
photo_e.putalpha(orig_raw.split()[3])

# Left-edge fade (smooth blend into background) — wider so text stays clear
fade_w = min(380, nw)
for x in range(fade_w):
    a = int(255 * (x / fade_w) ** 1.5)
    for yp in range(H):
        r2, g2, b2, a2 = photo_e.getpixel((x, yp))
        photo_e.putpixel((x, yp), (r2, g2, b2, min(a2, a)))

# Right-edge fade so edge blends to bg
for xi in range(30):
    x = nw - 1 - xi
    a = int(255 * (xi / 30) ** 0.7)
    for yp in range(H):
        r2, g2, b2, a2 = photo_e.getpixel((x, yp))
        photo_e.putpixel((x, yp), (r2, g2, b2, min(a2, a)))

# Place photo flush right
px = W - nw
canvas.paste(photo_e, (px, 0), photo_e)

# Glow halo behind Tony's head area (top-right zone)
halo_cx = px + nw // 2
halo_cy = H // 2
halo_layer = Image.new("RGBA", (W, H), (0,0,0,0))
hd2 = ImageDraw.Draw(halo_layer)
for r in range(260, 0, -5):
    t = r / 260
    a = int(18 * math.exp(-((1-t)*3)**1.5))
    hd2.ellipse([halo_cx-r, halo_cy-r, halo_cx+r, halo_cy+r], fill=(99,102,241,a))
canvas = Image.alpha_composite(canvas, halo_layer)
canvas.paste(photo_e, (px, 0), photo_e)  # re-paste photo on top of glow

# ── 3. Dark scrim on LEFT text zone so text always readable ──────────────────
scrim = Image.new("RGBA", (W, H), (0,0,0,0))
sd   = ImageDraw.Draw(scrim)
for x in range(900):
    t = 1 - (x/900)**0.6
    sd.line([(x,0),(x,H)], fill=(0,0,0,int(100*t)))
canvas = Image.alpha_composite(canvas, scrim)

draw = ImageDraw.Draw(canvas)

LX = 50   # left margin

# ── 4. LEFT TEXT — Canva / Adobe style ───────────────────────────────────────

# ─ Far-left glowing accent stripe ─
for xi in range(6):
    a = int(180 * (1 - xi/6))
    draw.line([(xi, 0),(xi, H)], fill=(96,165,250,a), width=1)

# ─ AVAILABLE FOR CONSULTING — double-border glow pill ─
bx, by, bw, bh = LX, 16, 260, 36
draw.rounded_rectangle([bx-2, by-2, bx+bw+2, by+bh+2], radius=20,
                        fill=None, outline=(52,211,153,50), width=3)
draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=18,
                        fill=(4,26,18,230), outline=(52,211,153,220), width=2)
draw.ellipse([bx+12, by+12, bx+24, by+24], fill=(52,211,153))
draw.text((bx+32, by+8), "AVAILABLE FOR CONSULTING", font=F["badge"], fill=(52,211,153))

# ─ NAME — "TONY" white, "BEAL" blue accent ─
t1, t2 = "TONY", " BEAL"
t1w = int(draw.textlength(t1, font=F["name"]))
# Drop shadows
draw.text((LX+3, 60+3), t1+t2, font=F["name"], fill=(0,0,0,160))
draw.text((LX,   60),   t1,    font=F["name"], fill=(255,255,255))
draw.text((LX+t1w, 60), t2,    font=F["name"], fill=(96,165,250))

# Small decorative diamonds flanking name
for dx in [LX-20, LX+t1w+int(draw.textlength(t2,font=F["name"]))+8]:
    draw.polygon([(dx+6,72),(dx+12,66),(dx+18,72),(dx+12,78)],
                 fill=(96,165,250,160))

# ─ Thin gradient divider under name ─
div_y = 174
div_len = 720
for xi in range(div_len):
    t = xi / div_len
    rc = int(37  + (139-37)*t)
    gc = int(99  + (92-99)*t)
    bc = int(235 + (246-235)*t)
    al = int(220 * (1 - t**0.5))
    draw.point((LX+xi, div_y),   fill=(rc,gc,bc,al))
    draw.point((LX+xi, div_y+1), fill=(rc,gc,bc,al//2))

# ─ Role rows with EXPERTISE BARS (progress bars) ─
role_data = [
    ("▲  Revenue Operations",  (37, 99, 235),  93),
    (">>  AI Sales Systems",    (99, 102, 241), 87),
    ("►  GTM Strategy",        (16, 185, 129), 97),
]
ry0      = 182
row_gap  = 28
bar_len  = 250  # total bar track length

for i, (label, col, pct) in enumerate(role_data):
    oy = ry0 + i * row_gap
    draw.text((LX, oy), label, font=F["tag"], fill=(255,255,255))
    lbl_w = int(draw.textlength(label, font=F["tag"]))
    bstart = LX + lbl_w + 14
    bend   = bstart + bar_len

    # Track
    draw.rounded_rectangle([bstart, oy+5, bend, oy+17], radius=5,
                            fill=(255,255,255,18))
    # Glow fill
    fill_x = bstart + int(bar_len * pct / 100)
    draw.rounded_rectangle([bstart, oy+5, fill_x, oy+17], radius=5,
                            fill=(*col, 210))
    # Bright tip
    draw.ellipse([fill_x-5, oy+4, fill_x+5, oy+18], fill=(255,255,255,180))
    # % label
    draw.text((bend+10, oy+2), f"{pct}%", font=F["sm"], fill=col)

# ─ Stats — styled cards with colored stripe, big number, gauge bar ─
stats = [
    ("$20M+", "PIPELINE",   (245,158,11),  82),
    ("15+",   "YRS IN B2B", (99, 102,241), 94),
    ("11K+",  "FOLLOWERS",  (52, 211,153), 88),
    ("3.7K+", "ACCOUNTS",   (96, 165,250), 76),
]
sx, sy = LX, 272
cw, ch = 140, 84

for val, lbl, col, gauge in stats:
    # Card shadow
    draw.rounded_rectangle([sx+3, sy+3, sx+cw+3, sy+ch+3], radius=10,
                            fill=(0,0,0,80))
    # Card body
    draw.rounded_rectangle([sx, sy, sx+cw, sy+ch], radius=10,
                            fill=(6,10,30,200), outline=(*col,120), width=1)
    # Top accent stripe (gradient fill)
    for xi in range(cw-4):
        t = xi/(cw-4)
        rc2 = int(col[0]*0.6 + col[0]*0.4*t)
        gc2 = int(col[1]*0.6 + col[1]*0.4*t)
        bc2 = int(col[2]*0.6 + col[2]*0.4*t)
        draw.line([(sx+2+xi, sy+1),(sx+2+xi, sy+5)], fill=(rc2,gc2,bc2,220))
    # Value
    vw = int(draw.textlength(val, font=F["stat"]))
    draw.text((sx+(cw-vw)//2, sy+10), val, font=F["stat"], fill=(255,255,255))
    # Label
    lw = int(draw.textlength(lbl, font=F["stlbl"]))
    draw.text((sx+(cw-lw)//2, sy+52), lbl, font=F["stlbl"], fill=col)
    # Bottom gauge bar
    gauge_w = int((cw-16) * gauge/100)
    draw.rounded_rectangle([sx+8, sy+ch-12, sx+cw-8, sy+ch-4], radius=3,
                            fill=(255,255,255,15))
    draw.rounded_rectangle([sx+8, sy+ch-12, sx+8+gauge_w, sy+ch-4], radius=3,
                            fill=(*col, 180))
    sx += cw + 10

# ─ Website URL in a bold glowing pill ─
url_txt = ">>  tonybeal.net"
uw = int(draw.textlength(url_txt, font=F["role"]))
draw.rounded_rectangle([LX-6, H-40, LX+uw+14, H-6], radius=14,
                        fill=(6,15,45,220), outline=(96,165,250,180), width=2)
draw.text((LX+3, H-38), url_txt, font=F["role"], fill=(96,165,250))

# ── 5. EDGE ACCENT LINES (top + bottom gradient) ─────────────────────────────
for x in range(W):
    t   = x / W
    r_c = int(37  + (139-37)*t)
    g_c = int(99  + (92-99)*t)
    b_c = int(235 + (246-235)*t)
    draw.point((x, 0),   fill=(r_c, g_c, b_c))
    draw.point((x, 1),   fill=(r_c, g_c, b_c))
    draw.point((x, 2),   fill=(r_c, g_c, b_c, 120))
    draw.point((x, H-1), fill=(r_c, g_c, b_c))
    draw.point((x, H-2), fill=(r_c, g_c, b_c))

# Save
canvas.convert("RGB").save(OUT, "PNG")
print(f"Saved: {OUT}")
