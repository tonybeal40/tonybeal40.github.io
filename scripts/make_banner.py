from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1584, 396

# ── Layer 1: dark navy gradient background ──────────────────────────────────
bg = Image.new("RGBA", (W, H), (8, 12, 28, 255))
draw_bg = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    draw_bg.line([(0, y), (W, y)], fill=(int(8+4*t), int(12+6*t), int(28+12*t), 255))

# ── Layer 2: tech decoration (arcs + dots) — kept to right 25% ──────────────
deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_d = ImageDraw.Draw(deco)

# Dot grid — full width but faint
for gx in range(0, W, 30):
    for gy in range(0, H, 30):
        draw_d.ellipse([gx, gy, gx+2, gy+2], fill=(37, 99, 235, 18))

# Arcs anchored to far right edge, won't overlap text
arc_cx, arc_cy = 1584, 198
for r in [120, 170, 220, 270, 320]:
    draw_d.arc([arc_cx-r, arc_cy-r, arc_cx+r, arc_cy+r],
               start=150, end=210, fill=(37, 99, 235, 55), width=2)

# Horizontal scan lines — right 20% only
for yp in range(60, 340, 36):
    draw_d.line([(1260, yp), (1584, yp)], fill=(37, 99, 235, 22), width=1)

# Left vertical accent bar
for y in range(H):
    dist = abs(y - H/2) / (H/2)
    a = int(220 * (1 - dist*dist))
    if a > 8:
        draw_d.line([(64, y), (67, y)], fill=(37, 99, 235, a))

# ── Layer 3: dark scrim over text zone (right 60%) so text pops ─────────────
scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_s = ImageDraw.Draw(scrim)
# Gradient scrim: transparent on left → semi-dark on right
for x in range(700, W):
    t = (x - 700) / (W - 700)
    a = int(140 * t)
    draw_s.line([(x, 0), (x, H)], fill=(5, 8, 20, a))

# ── Composite background layers ─────────────────────────────────────────────
canvas = Image.alpha_composite(bg, deco)
canvas = Image.alpha_composite(canvas, scrim)
draw = ImageDraw.Draw(canvas)

# ── Fonts ────────────────────────────────────────────────────────────────────
try:
    font_name  = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 88)
    font_tag   = ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   22)
    font_over  = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
    font_stat  = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
    font_lbl   = ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   12)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
    font_url   = ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   14)
except:
    font_name = font_tag = font_over = font_stat = font_lbl = font_badge = font_url = ImageFont.load_default()

RIGHT = 1530  # right anchor x

# ── AVAILABLE NOW badge ──────────────────────────────────────────────────────
bx, by = 62, 34
draw.rounded_rectangle([bx, by, bx+165, by+38], radius=19,
                        fill=(10, 38, 28), outline=(52, 211, 153), width=2)
draw.ellipse([bx+14, by+14, bx+27, by+27], fill=(52, 211, 153))
draw.text((bx+34, by+10), "AVAILABLE NOW", font=font_badge, fill=(52, 211, 153))

# ── Overline ─────────────────────────────────────────────────────────────────
overline = "REVENUE OPERATIONS  ·  AI SALES SYSTEMS  ·  GTM STRATEGY"
ow = draw.textlength(overline, font=font_over)
draw.text((RIGHT - ow, 88), overline, font=font_over, fill=(96, 165, 250))

# Thin separator line under overline
draw.line([(RIGHT - ow, 108), (RIGHT, 108)], fill=(37, 99, 235), width=1)

# ── Name: WHITE with blue drop shadow ────────────────────────────────────────
name = "Tony Beal"
nw = draw.textlength(name, font=font_name)
nx = int(RIGHT - nw)
# Multi-layer shadow for depth
draw.text((nx+4, 122+4), name, font=font_name, fill=(5, 15, 50))    # deep shadow
draw.text((nx+2, 122+2), name, font=font_name, fill=(30, 60, 140))  # mid shadow
draw.text((nx,   122),   name, font=font_name, fill=(255, 255, 255)) # pure white

# ── Tagline: bright light gray ───────────────────────────────────────────────
tag = "Building AI-driven revenue systems that generate pipeline for B2B companies"
tw = draw.textlength(tag, font=font_tag)
draw.text((RIGHT - tw, 224), tag, font=font_tag, fill=(210, 220, 240))

# ── Stat cards ───────────────────────────────────────────────────────────────
stats = [
    ("$20M+",  "PIPELINE",   (37, 99, 235),  (255, 255, 255)),
    ("15+",    "YRS B2B",    (99, 102, 241), (255, 255, 255)),
    ("11K+",   "FOLLOWERS",  (16, 185, 129), (52, 211, 153)),
    ("3,700+", "ACCOUNTS",   (37, 99, 235),  (255, 255, 255)),
]
card_w, card_h = 148, 62
# right-align the row of cards
total_cards_w = len(stats) * card_w + (len(stats)-1) * 10
sx = RIGHT - total_cards_w

for i, (val, lbl, border, text_c) in enumerate(stats):
    cx = sx + i * (card_w + 10)
    cy = 280
    draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=8,
                            fill=(14, 22, 50), outline=border, width=2)
    vw = draw.textlength(val, font=font_stat)
    draw.text((cx + (card_w-vw)//2, cy+7), val, font=font_stat, fill=text_c)
    lw = draw.textlength(lbl, font=font_lbl)
    draw.text((cx + (card_w-lw)//2, cy+38), lbl, font=font_lbl, fill=(148, 163, 184))

# ── tonybeal.net ─────────────────────────────────────────────────────────────
url = "tonybeal.net"
uw = draw.textlength(url, font=font_url)
draw.text((RIGHT - uw, 360), url, font=font_url, fill=(96, 116, 139))

# ── Save ─────────────────────────────────────────────────────────────────────
out_path = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets\linkedin-banner-v2.png"
canvas.convert("RGB").save(out_path, "PNG")
print(f"Saved: {out_path}")
