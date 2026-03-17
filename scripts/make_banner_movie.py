"""
LinkedIn Banner - Hollywood Movie Poster Style
1584x396 | Cinematic | Dramatic lighting | Movie title treatment
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, random

W, H = 1584, 396
PHOTO = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\headshot-hero.png"
OUT   = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets\linkedin-banner-movie.png"

random.seed(42)

def ft(fname, size):
    try:    return ImageFont.truetype(f"C:/Windows/Fonts/{fname}", size)
    except: return ImageFont.load_default()

F = {
    "title":    ft("ariblk.ttf",  148),
    "subtitle": ft("arialbd.ttf",  24),
    "tag":      ft("arial.ttf",    19),
    "credit":   ft("arial.ttf",    14),
    "badge":    ft("arialbd.ttf",  15),
    "stat":     ft("arialbd.ttf",  34),
    "statlbl":  ft("arial.ttf",    14),
    "avail":    ft("arialbd.ttf",  16),
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. BACKGROUND: deep cinematic black-to-dark-blue
# ─────────────────────────────────────────────────────────────────────────────
bg = Image.new("RGB", (W, H), (0,0,0))
d  = ImageDraw.Draw(bg)
for y in range(H):
    t = y/H
    d.line([(0,y),(W,y)], fill=(int(2+4*t), int(2+6*t), int(6+16*t)))

# 2. DRAMATIC LIGHT RAYS from behind (right-center, like a spotlight)
light_layer = Image.new("RGBA", (W, H), (0,0,0,0))
ld = ImageDraw.Draw(light_layer)

# Warm golden backlight glow (where Tony will stand)
lcx, lcy = 1100, -20
for r in range(700, 0, -6):
    t    = r / 700
    warm = (int(180*(1-t)*0.6), int(130*(1-t)*0.4), int(60*(1-t)*0.2))
    a    = int(22 * math.exp(-(t*2.2)**2))
    ld.ellipse([lcx-r, lcy-r, lcx+r, lcy+r], fill=(*warm, a))

# Cool blue-purple ambient fill (left)
for r in range(600, 0, -6):
    t = r / 600
    a = int(14 * math.exp(-(t*2.0)**2))
    ld.ellipse([-100-r, H//2-r, -100+r, H//2+r], fill=(30, 50, 160, a))

bg_rgba = bg.convert("RGBA")
bg_rgba = Image.alpha_composite(bg_rgba, light_layer)

# 3. Light beam rays (angled streaks)
ray_layer = Image.new("RGBA", (W, H), (0,0,0,0))
rd = ImageDraw.Draw(ray_layer)
for angle in range(0, 180, 12):
    rad   = math.radians(angle)
    x1    = lcx + 30*math.cos(rad)
    y1    = lcy + 30*math.sin(rad)
    length = random.randint(600, 900)
    x2    = x1 + length*math.cos(rad)
    y2    = y1 + length*math.sin(rad)
    alpha = random.randint(4, 14)
    rd.line([(x1, y1),(x2, y2)], fill=(200, 180, 120, alpha), width=random.randint(2,8))

# Blur rays slightly for softness
ray_layer = ray_layer.filter(ImageFilter.GaussianBlur(3))
bg_rgba   = Image.alpha_composite(bg_rgba, ray_layer)

# 4. Fine film grain
grain_layer = Image.new("RGBA", (W, H), (0,0,0,0))
gd = ImageDraw.Draw(grain_layer)
for _ in range(3500):
    x = random.randint(0, W)
    y = random.randint(0, H)
    v = random.randint(60, 140)
    gd.point((x, y), fill=(v, v, v, random.randint(4, 12)))
bg_rgba = Image.alpha_composite(bg_rgba, grain_layer)

canvas = bg_rgba.convert("RGB")
draw   = ImageDraw.Draw(canvas)

# ─────────────────────────────────────────────────────────────────────────────
# 5. WATERMARK "TONY BEAL" — huge ghost text behind everything
# ─────────────────────────────────────────────────────────────────────────────
wm_layer = Image.new("RGBA", (W, H), (0,0,0,0))
wd = ImageDraw.Draw(wm_layer)
wm_text = "TONY BEAL"
try:
    wm_font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 220)
except:
    wm_font = F["title"]
ww = int(wd.textlength(wm_text, font=wm_font))
wd.text(((W-ww)//2, H//2-120), wm_text, font=wm_font, fill=(180,150,60,12))
wm_layer = wm_layer.filter(ImageFilter.GaussianBlur(2))
canvas_rgba = canvas.convert("RGBA")
canvas_rgba = Image.alpha_composite(canvas_rgba, wm_layer)
canvas = canvas_rgba.convert("RGB")
draw   = ImageDraw.Draw(canvas)

# ─────────────────────────────────────────────────────────────────────────────
# 6. PHOTO — right-center, dramatic, blended
# ─────────────────────────────────────────────────────────────────────────────
photo = Image.open(PHOTO).convert("RGBA")
pw, ph = photo.size

# Scale so photo height = banner height
scale = H / ph
nw    = int(pw * scale)
photo = photo.resize((nw, H), Image.LANCZOS)

# Boost contrast for cinematic punch
enh   = ImageEnhance.Contrast(photo.convert("RGB"))
photo_rgb = enh.enhance(1.35)
enh2  = ImageEnhance.Brightness(photo_rgb)
photo_rgb = enh2.enhance(1.1)
photo = photo_rgb.convert("RGBA")
# Re-apply original alpha mask
orig  = Image.open(PHOTO).convert("RGBA").resize((nw, H), Image.LANCZOS)
photo.putalpha(orig.split()[3])

# Left-edge fade (blend into bg)
fade_left = 110
for x in range(fade_left):
    a = int(255 * (x / fade_left)**1.5)
    for yp in range(H):
        if x < nw:
            r2,g2,b2,a2 = photo.getpixel((x, yp))
            photo.putpixel((x, yp), (r2,g2,b2, min(a2, a)))

# Right-edge fade
fade_right = 80
for x in range(fade_right):
    rx = nw - 1 - x
    a  = int(255 * (x / fade_right)**1.5)
    for yp in range(H):
        if 0 <= rx < nw:
            r2,g2,b2,a2 = photo.getpixel((rx, yp))
            photo.putpixel((rx, yp), (r2,g2,b2, min(a2, a)))

# Position: slightly right of center
px = (W - nw)//2 + 80
cv = canvas.convert("RGBA")
cv.paste(photo, (px, 0), photo)
canvas = cv.convert("RGB")
draw   = ImageDraw.Draw(canvas)

# ─────────────────────────────────────────────────────────────────────────────
# 7. HORIZONTAL LETTERBOX BARS (top + bottom) — cinematic black strips
# ─────────────────────────────────────────────────────────────────────────────
for bar_h in range(22):
    a = int(220 * ((22 - bar_h)/22)**2)
    draw.line([(0, bar_h), (W, bar_h)],           fill=(0,0,0))
    draw.line([(0, H-1-bar_h), (W, H-1-bar_h)],   fill=(0,0,0))

# Thin gold accent lines
draw.line([(0, 22),(W, 22)],   fill=(200,160,40), width=1)
draw.line([(0, H-23),(W, H-23)], fill=(200,160,40), width=1)

# ─────────────────────────────────────────────────────────────────────────────
# 8. LEFT TEXT BLOCK
# ─────────────────────────────────────────────────────────────────────────────
LX = 36

# Overline — spaced caps style
over = "T O N Y   B E A L"
ow   = int(draw.textlength(over, font=F["subtitle"]))
draw.text((LX, 32), over, font=F["subtitle"], fill=(200, 160, 40))
draw.line([(LX, 60), (LX+ow+60, 60)], fill=(200,160,40), width=1)

# Main title — two lines, metallic gold/white
line1, line2 = "REVENUE", "ARCHITECT"
try:
    title_font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 108)
except:
    title_font = F["title"]

def movie_text(text, x, y, font):
    tw = int(draw.textlength(text, font=font))
    # Deep shadow
    draw.text((x+5, y+5), text, font=font, fill=(0,0,0,220))
    draw.text((x+2, y+2), text, font=font, fill=(60,40,0,150))
    # Gold gradient simulation: draw white then overlay
    draw.text((x,   y),   text, font=font, fill=(255,240,180))

movie_text(line1, LX, 66, title_font)
th1 = title_font.size
movie_text(line2, LX, 66 + th1 - 14, title_font)

# Tagline — movie style
draw.text((LX, 66 + th1*2 - 22),
          "Revenue Operations  ·  AI Sales Systems  ·  GTM Strategy",
          font=F["tag"], fill=(160, 175, 200))

# ─────────────────────────────────────────────────────────────────────────────
# 9. RIGHT TEXT BLOCK
# ─────────────────────────────────────────────────────────────────────────────
RX = 1240

# Stat cards — stacked vertically on right
stats = [
    ("$20M+", "PIPELINE",   (200,160,40)),
    ("11K+",  "FOLLOWERS",  (96,165,250)),
    ("3,700+","ACCOUNTS",   (52,211,153)),
    ("15+",   "YRS B2B",    (200,160,40)),
]
cw, ch = 148, 70
sy     = 28
for i, (val, lbl, col) in enumerate(stats):
    cx = RX + (i % 2)*(cw+10)
    cy = sy + (i // 2)*(ch+8)
    draw.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=6,
                            fill=(0,0,0,160), outline=(*col,160), width=1)
    vw = int(draw.textlength(val, font=F["stat"]))
    lw = int(draw.textlength(lbl, font=F["statlbl"]))
    draw.text((cx+(cw-vw)//2, cy+6),     val, font=F["stat"],    fill=(255,255,255))
    draw.text((cx+(cw-lw)//2, cy+ch-22), lbl, font=F["statlbl"], fill=col)

# Vertical "movie credits" style text bottom-right
credits = "TONYBEAL.NET  ·  AVAILABLE NOW  ·  B2B REVENUE EXPERT"
cred_w  = int(draw.textlength(credits, font=F["credit"]))
draw.text((W - cred_w - 30, H-18), credits, font=F["credit"], fill=(120,100,60))

# ─────────────────────────────────────────────────────────────────────────────
# 10. Center bottom tag line — movie release style
# ─────────────────────────────────────────────────────────────────────────────
release = '"Building AI-driven revenue systems that generate pipeline."'
rw = int(draw.textlength(release, font=F["tag"]))
draw.text(((W-rw)//2, H-20), release, font=F["tag"], fill=(140,120,80))

# Save
canvas.save(OUT, "PNG")
print(f"Saved: {OUT}")
