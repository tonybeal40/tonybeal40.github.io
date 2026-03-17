"""
YAP-style LinkedIn Banner for Tony Beal
1584x396 | Photo centered full-height | Text left + right | Colored highlight boxes
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1584, 396
PHOTO = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\headshot-hero.png"
OUT   = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets\linkedin-banner-yap.png"

# ── Fonts ─────────────────────────────────────────────────────────────────────
def ft(fname, size):
    try:    return ImageFont.truetype(f"C:/Windows/Fonts/{fname}", size)
    except: return ImageFont.load_default()

F = {
    "hero":    ft("ariblk.ttf",  82),   # Big headline
    "hero2":   ft("ariblk.ttf",  54),
    "bold":    ft("arialbd.ttf", 26),
    "semi":    ft("arialbd.ttf", 20),
    "body":    ft("arial.ttf",   20),
    "sm":      ft("arial.ttf",   17),
    "badge":   ft("arialbd.ttf", 15),
    "xs":      ft("arial.ttf",   14),
    "right_h": ft("ariblk.ttf",  38),   # Right block headline
}

# ── Background: deep navy gradient ───────────────────────────────────────────
canvas = Image.new("RGB", (W, H))
draw   = ImageDraw.Draw(canvas)
for y in range(H):
    t = y / H
    draw.line([(0,y),(W,y)], fill=(
        int(6  + 8*t),
        int(14 + 12*t),
        int(52 + 20*t),
    ))

# Subtle radial glow center-right
for r in range(400, 0, -8):
    a = int(18 * math.exp(-((r/250)**2)))
    cx, cy = 1100, 200
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(20, 50, 140, a))

# Fine dot texture
import random; random.seed(7)
for _ in range(1200):
    x, y = random.randint(0,W), random.randint(0,H)
    v = random.randint(40,90)
    draw.point((x,y), fill=(v,v,v+20))

# ── Photo (centered, full height, blended) ────────────────────────────────────
photo = Image.open(PHOTO).convert("RGBA")
pw, ph = photo.size
# Scale to fill banner height
scale  = H / ph
nw, nh = int(pw * scale), H
photo  = photo.resize((nw, nh), Image.LANCZOS)

# Blend edges: left fade, right fade so photo merges with background
fade_w = 90
for x in range(fade_w):
    alpha = int(255 * (x / fade_w))
    for y_px in range(nh):
        if x < photo.size[0]:
            r2, g2, b2, a2 = photo.getpixel((x, y_px))
            photo.putpixel((x, y_px), (r2, g2, b2, min(a2, alpha)))

for x in range(fade_w):
    rx = photo.size[0] - 1 - x
    alpha = int(255 * (x / fade_w))
    for y_px in range(nh):
        if 0 <= rx < photo.size[0]:
            r2, g2, b2, a2 = photo.getpixel((rx, y_px))
            photo.putpixel((rx, y_px), (r2, g2, b2, min(a2, alpha)))

# Center photo
px = (W - nw) // 2
canvas_rgba = canvas.convert("RGBA")
canvas_rgba.paste(photo, (px, 0), photo)
canvas = canvas_rgba.convert("RGB")
draw   = ImageDraw.Draw(canvas)

# ── Helper: highlight box behind text ────────────────────────────────────────
def hbox(text, font, x, y, bg, tc=(255,255,255), pad_x=12, pad_y=6):
    tw = int(draw.textlength(text, font=font))
    bh = font.size + pad_y*2
    draw.rectangle([x, y, x+tw+pad_x*2, y+bh], fill=bg)
    draw.text((x+pad_x, y+pad_y), text, font=font, fill=tc)
    return tw + pad_x*2, bh  # return box width, height

def plain(text, font, x, y, color):
    draw.text((x, y), text, font=font, fill=color)

def shadow_plain(text, font, x, y, color):
    draw.text((x+2, y+2), text, font=font, fill=(0,0,0,160))
    draw.text((x,   y),   text, font=font, fill=color)

# ── LEFT ZONE  (x: 26 → 560) ─────────────────────────────────────────────────
LX = 36
# Small badge top-left
draw.rectangle([LX, 18, LX+80, 54], fill=(6,185,129))   # green badge
draw.text((LX+6, 22),  "TONY",  font=F["badge"], fill=(255,255,255))
draw.text((LX+6, 38),  "BEAL",  font=F["badge"], fill=(255,255,255))

# Main headline with cyan highlight box - two lines
bw1, bh1 = hbox("REVENUE", F["hero"], LX, 68, (6, 182, 212), (0,0,0))
bw2, bh2 = hbox("OPERATIONS", F["hero"], LX, 68+bh1+4, (6, 182, 212), (0,0,0))

y_after_headline = 68 + bh1 + 4 + bh2 + 12

# Sub-headline in white box
bw3, bh3 = hbox("& AI Sales Systems", F["bold"], LX, y_after_headline,
                 (255,255,255), (10,14,50))

y3 = y_after_headline + bh3 + 14

# Tagline
plain("15+ years building B2B revenue engines", F["sm"], LX, y3, (180,210,240))
plain("for Fortune 50 & high-growth companies.", F["sm"], LX, y3+22, (180,210,240))

# Bottom: available badge
y_bot = H - 48
draw.rounded_rectangle([LX, y_bot, LX+190, y_bot+34], radius=17,
                        fill=(8,30,20), outline=(6,185,129), width=2)
draw.ellipse([LX+14, y_bot+12, LX+26, y_bot+24], fill=(6,185,129))
draw.text((LX+32, y_bot+8), "AVAILABLE NOW", font=F["badge"], fill=(6,185,129))

# ── RIGHT ZONE  (x: 1060 → 1558) ────────────────────────────────────────────
RX = 1065
RW = 1555

# Small top label
plain("tonybeal.net", F["xs"], RX, 20, (100,140,200))

# Right headline with lime-green box
bw4, bh4 = hbox("TONY BEAL", F["right_h"], RX, 44, (132, 204, 22), (0,0,0))

# Description — with inline highlighted words
desc_lines = [
    ("Award-winning",  None),
    ("B2B Revenue Expert",    (30, 90, 200)),
    ("specializing in",  None),
    ("AI Sales Systems,",  (6, 182, 212)),
    ("RevOps & GTM Strategy.",  None),
    ("",  None),
    ("$20M+ pipeline generated",  None),
    ("11K+ LinkedIn followers",  None),
    ("3,700+ accounts managed",  None),
]

dy = 44 + bh4 + 10
for text, highlight in desc_lines:
    if not text:
        dy += 8
        continue
    if highlight:
        # draw colored highlight box
        tw = int(draw.textlength(text, font=F["sm"]))
        draw.rectangle([RX, dy-2, RX+tw+8, dy+F["sm"].size+2], fill=highlight)
        draw.text((RX+4, dy), text, font=F["sm"], fill=(255,255,255))
    else:
        draw.text((RX, dy), text, font=F["sm"], fill=(200,215,240))
    dy += F["sm"].size + 6

# ── Bottom thin accent lines ──────────────────────────────────────────────────
draw.line([(0, H-3), (W, H-3)], fill=(6,182,212), width=3)
draw.line([(0, 2),   (W, 2)],   fill=(6,182,212), width=2)

# ── Save ─────────────────────────────────────────────────────────────────────
canvas.save(OUT, "PNG")
print(f"Saved: {OUT}")
