"""
Generate og-now.png — 1200x630 LinkedIn banner for tonybeal.net/now
Requires: pillow, requests
"""
import os, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR   = os.path.join(os.path.dirname(__file__), "assets")
OUT_PATH  = os.path.join(OUT_DIR, "og-now.png")
HEADSHOT  = os.path.join(OUT_DIR, "_headshot_tmp.png")
HS_URL    = "https://tonybeal.net/headshot-final.png"

os.makedirs(OUT_DIR, exist_ok=True)

# ----- Download headshot -----
print("Downloading headshot...")
urllib.request.urlretrieve(HS_URL, HEADSHOT)

# ----- Canvas -----
W, H = 1200, 630
img  = Image.new("RGB", (W, H), "#0A0F1E")
d    = ImageDraw.Draw(img)

# --- Background gradient bands ---
for y in range(H):
    t = y / H
    r = int(10  + t * 5)
    g = int(15  + t * 15)
    b = int(30  + t * 35)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# --- Grid lines ---
for x in range(0, W, 60):
    d.line([(x, 0), (x, H)], fill=(30, 45, 70))
for y in range(0, H, 60):
    d.line([(0, y), (W, y)], fill=(30, 45, 70))

# --- Blue accent glow (top-right) ---
glow = Image.new("RGBA", (700, 700), (0,0,0,0))
gd   = ImageDraw.Draw(glow)
for r in range(350, 0, -1):
    alpha = int(55 * (1 - r/350))
    gd.ellipse([350-r, 350-r, 350+r, 350+r], fill=(59, 130, 246, alpha))
glow = glow.filter(ImageFilter.GaussianBlur(30))
img.paste(glow, (600, -100), glow)

# ----- Headshot circle -----
hs_size = 220
hs_raw  = Image.open(HEADSHOT).convert("RGBA").resize((hs_size, hs_size), Image.LANCZOS)

# Circular mask
mask = Image.new("L", (hs_size, hs_size), 0)
ImageDraw.Draw(mask).ellipse([0,0,hs_size,hs_size], fill=255)

# Blue ring background (slightly larger circle)
ring_size = hs_size + 16
ring = Image.new("RGBA", (ring_size, ring_size), (0,0,0,0))
ImageDraw.Draw(ring).ellipse([0,0,ring_size,ring_size], fill=(59,130,246,255))

hs_x, hs_y = 70, (H - hs_size) // 2  # vertically centered
img.paste(ring, (hs_x - 8, hs_y - 8), ring)

hs_circle = Image.new("RGBA", (hs_size, hs_size), (0,0,0,0))
hs_circle.paste(hs_raw, (0,0), mask)
img.paste(hs_circle, (hs_x, hs_y), hs_circle)

# Green "available" dot
dot_r = 18
d.ellipse([hs_x+hs_size-dot_r*2+4, hs_y+hs_size-dot_r*2+4,
           hs_x+hs_size+4,          hs_y+hs_size+4],          fill="#0A0F1E")
d.ellipse([hs_x+hs_size-dot_r*2+8, hs_y+hs_size-dot_r*2+8,
           hs_x+hs_size,            hs_y+hs_size],             fill="#10B981")

# ----- Typography -----
def font(size, bold=False):
    """Try to load a good system font, fall back to default."""
    faces = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for f in faces:
        if os.path.exists(f):
            try: return ImageFont.truetype(f, size)
            except: pass
    return ImageFont.load_default()

cx = hs_x + hs_size + 55  # content left edge

# Eyebrow
eyebrow_font = font(18, bold=True)
d.text((cx, 155), "AVAILABLE NOW  ·  ST. LOUIS METRO OR REMOTE",
       font=eyebrow_font, fill="#60A5FA")

# Name
name_font = font(88, bold=True)
d.text((cx, 185), "Tony Beal", font=name_font, fill="#F1F5F9")

# Title
title_font = font(24)
d.text((cx, 290), "RevOps  ·  Business Development  ·  Sales Operations",
       font=title_font, fill="#94A3B8")

# --- Stats row ---
stats = [("$20M+", "Pipeline Built"), ("3,700+", "Accounts Managed"),
         ("8 yrs", "Quota Streak"),   ("15+",    "Years B2B")]
sx = cx
sy = 345
num_font   = font(32, bold=True)
label_font = font(14)
for i, (num, label) in enumerate(stats):
    d.text((sx, sy),      num,   font=num_font,   fill="#60A5FA")
    d.text((sx, sy + 38), label, font=label_font, fill="#64748B")
    # divider
    if i < len(stats)-1:
        bx = sx + 95
        d.line([(bx, sy), (bx, sy+55)], fill="#1E2A3A", width=1)
    sx += 120

# --- Tag pills ---
def pill(draw, x, y, text, bg, border, fg, r=16):
    tw = len(text) * 9 + 28
    draw.rounded_rectangle([x, y, x+tw, y+32], radius=r, fill=bg, outline=border)
    draw.text((x+14, y+7), text, font=font(13, bold=True), fill=fg)
    return x + tw + 12

px = cx
py = 455
px = pill(d, px, py, "RevOps Leader",       "#1E3A5F", "#3B82F6", "#60A5FA")
px = pill(d, px, py, "BD Strategy",         "#1E3A5F", "#3B82F6", "#60A5FA")
px = pill(d, px, py, "● Available Now",     "#064E3B", "#10B981", "#10B981")

# URL watermark
url_font = font(18, bold=True)
d.text((cx, 510), "tonybeal.net/now", font=url_font, fill="#334155")

# ----- Save -----
img.save(OUT_PATH, "PNG", optimize=True)
print(f"✅  Saved → {OUT_PATH}")

# Cleanup
os.remove(HEADSHOT)
