"""
LinkedIn banner slideshow - slides 2-5 (1584x396 each)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1584, 396

def load_fonts():
    try:
        return {
            "xl":    ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 96),
            "lg":    ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64),
            "md":    ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   28),
            "sm":    ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   20),
            "xs":    ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   15),
            "badge": ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14),
            "stat":  ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26),
            "pill":  ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20),
        }
    except:
        d = ImageFont.load_default()
        return {k: d for k in ["xl","lg","md","sm","xs","badge","stat","pill"]}

F = load_fonts()
BASE = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets"

# ── Shared helpers ────────────────────────────────────────────────────────────

def dark_canvas():
    """Navy gradient base."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0,y),(W,y)], fill=(int(8+4*t), int(12+6*t), int(28+12*t), 255))
    return img

def add_dot_grid(img, spacing=30, alpha=16):
    d = ImageDraw.Draw(img)
    for gx in range(0, W, spacing):
        for gy in range(0, H, spacing):
            d.ellipse([gx, gy, gx+2, gy+2], fill=(37, 99, 235, alpha))

def add_left_bar(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        dist = abs(y - H/2) / (H/2)
        a = int(220 * (1 - dist*dist))
        if a > 8:
            d.line([(64, y), (67, y)], fill=(37, 99, 235, a))

def center_text(draw, text, font, y, color):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=color)

def right_text(draw, text, font, y, color, rx=1530):
    w = draw.textlength(text, font=font)
    draw.text((rx - w, y), text, font=font, fill=color)

def save(img, name):
    path = f"{BASE}/{name}"
    img.convert("RGB").save(path, "PNG")
    print(f"Saved: {path}")

# ── SLIDE 2: Big proof numbers ────────────────────────────────────────────────
def slide2():
    img = dark_canvas()
    add_dot_grid(img)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    # Right side arcs
    for r in [100, 150, 200, 250]:
        d.arc([W-r, H//2-r, W+r, H//2+r], start=150, end=210,
              fill=(37, 99, 235, 50), width=2)

    # Top label
    center_text(d, "PROVEN RESULTS  ·  B2B REVENUE & PIPELINE", F["xs"], 38,
                (96, 165, 250))
    d.line([(W//2 - 300, 62), (W//2 + 300, 62)], fill=(37, 99, 235), width=1)

    # 4 big stats, evenly spaced
    stats = [
        ("$20M+",   "Pipeline Generated",  (96, 165, 250)),
        ("11K+",    "LinkedIn Followers",  (52, 211, 153)),
        ("3,700+",  "Accounts Managed",    (129, 140, 248)),
        ("15+",     "Years in B2B Sales",  (96, 165, 250)),
    ]
    col_w = W // 4
    for i, (val, label, col) in enumerate(stats):
        cx = col_w * i + col_w // 2
        vw = d.textlength(val, font=F["lg"])
        d.text((cx - vw//2, 100), val, font=F["lg"], fill=col)
        lw = d.textlength(label, font=F["sm"])
        d.text((cx - lw//2, 182), label, font=F["sm"], fill=(148, 163, 184))
        # divider (not after last)
        if i < 3:
            d.line([(col_w*(i+1), 110), (col_w*(i+1), 200)],
                   fill=(37, 99, 235), width=1)

    # Tagline
    tag = "Tony Beal  ·  Revenue Operations & AI Sales Systems"
    tw = d.textlength(tag, font=F["sm"])
    d.text(((W - tw)//2, 256), tag, font=F["sm"], fill=(210, 220, 240))

    # Bottom bar
    for x in range(W):
        t = x / W
        d.line([(x, 310), (x, 314)],
               fill=(int(37 + 62*t), int(99), int(235 - 100*t)))

    # CTA
    center_text(d, "tonybeal.net", F["xs"], 330, (71, 85, 105))

    save(img, "linkedin-banner-slide2.png")

# ── SLIDE 3: Three service pillars ───────────────────────────────────────────
def slide3():
    img = dark_canvas()
    add_dot_grid(img)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    # Top label
    center_text(d, "WHAT I DO", F["badge"], 34, (96, 165, 250))
    tw = d.textlength("WHAT I DO", font=F["badge"])
    d.line([((W-tw)//2 - 40, 56), ((W-tw)//2, 56)], fill=(37,99,235), width=1)
    d.line([((W+tw)//2, 56), ((W+tw)//2 + 40, 56)], fill=(37,99,235), width=1)

    pillars = [
        ("⚙", "Revenue\nOperations",
         "CRM · Pipeline Design\nForecasting · Process Automation",
         (37, 99, 235)),
        ("🤖", "AI Sales\nSystems",
         "Outbound AI · Lead Scoring\nSequence Automation · Analytics",
         (99, 102, 241)),
        ("📈", "GTM\nStrategy",
         "ICP · Territory Planning\nPartner Ecosystems · Sales Enablement",
         (16, 185, 129)),
    ]

    card_w = 440
    gap = (W - 3 * card_w) // 4
    for i, (icon, title, desc, border) in enumerate(pillars):
        cx = gap + i * (card_w + gap)
        cy = 72
        ch = 282
        d.rounded_rectangle([cx, cy, cx+card_w, cy+ch], radius=10,
                             fill=(14, 22, 50), outline=border, width=2)
        # icon
        iw = d.textlength(icon, font=F["md"])
        d.text((cx + (card_w-iw)//2, cy+14), icon, font=F["md"], fill=border)
        # title lines
        t_lines = title.split("\n")
        ty = cy + 58
        for line in t_lines:
            lw = d.textlength(line, font=F["stat"])
            d.text((cx + (card_w-lw)//2, ty), line, font=F["stat"],
                   fill=(255, 255, 255))
            ty += 34
        # desc
        d_lines = desc.split("\n")
        dy = ty + 10
        for line in d_lines:
            lw = d.textlength(line, font=F["xs"])
            d.text((cx + (card_w-lw)//2, dy), line, font=F["xs"],
                   fill=(148, 163, 184))
            dy += 22

    center_text(d, "tonybeal.net", F["xs"], 368, (71, 85, 105))
    save(img, "linkedin-banner-slide3.png")

# ── SLIDE 4: Bold quote ───────────────────────────────────────────────────────
def slide4():
    img = dark_canvas()
    add_dot_grid(img, spacing=28, alpha=12)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    # Large faint quote mark
    qw = d.textlength("\u201c", font=F["xl"])
    d.text(((W - qw)//2 - 20, 10), "\u201c", font=F["xl"],
           fill=(37, 99, 235, 30))

    # Right side arcs for depth
    for r in [120, 170, 220]:
        d.arc([W-r, H//2-r, W+r, H//2+r], start=145, end=215,
              fill=(37, 99, 235, 45), width=2)

    # Quote — two lines
    q1 = "Most companies don't have a sales problem."
    q2 = "They have a system problem."
    q1w = d.textlength(q1, font=F["md"])
    q2w = d.textlength(q2, font=F["lg"])

    d.text(((W - q1w)//2, 100), q1, font=F["md"], fill=(210, 220, 240))
    # Shadow then white for q2
    d.text(((W - q2w)//2 + 3, 148), q2, font=F["lg"], fill=(5, 15, 50))
    d.text(((W - q2w)//2 + 1, 146), q2, font=F["lg"], fill=(37, 80, 180))
    d.text(((W - q2w)//2,     144), q2, font=F["lg"], fill=(255, 255, 255))

    # Separator
    d.line([(W//2 - 180, 232), (W//2 + 180, 232)], fill=(37, 99, 235), width=1)

    # Attribution
    attr = "— Tony Beal  |  Revenue Operations  ·  AI Sales Systems"
    aw = d.textlength(attr, font=F["sm"])
    d.text(((W - aw)//2, 248), attr, font=F["sm"], fill=(96, 165, 250))

    # Bottom tagline
    sub = "I build systems that turn pipeline into predictable revenue."
    sw = d.textlength(sub, font=F["xs"])
    d.text(((W - sw)//2, 296), sub, font=F["xs"], fill=(100, 116, 139))

    center_text(d, "tonybeal.net", F["xs"], 352, (71, 85, 105))
    save(img, "linkedin-banner-slide4.png")

# ── SLIDE 5: CTA ─────────────────────────────────────────────────────────────
def slide5():
    img = dark_canvas()
    add_dot_grid(img, spacing=26, alpha=14)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    # Glowing circle center
    for r in range(160, 0, -4):
        a = int(18 * (1 - r/160))
        d.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], outline=(37,99,235,a))

    # Available badge
    bx = W//2 - 82
    by = 30
    d.rounded_rectangle([bx, by, bx+165, by+38], radius=19,
                         fill=(10,38,28), outline=(52,211,153), width=2)
    d.ellipse([bx+14, by+14, bx+27, by+27], fill=(52,211,153))
    d.text((bx+34, by+10), "AVAILABLE NOW", font=F["badge"], fill=(52,211,153))

    # Big CTA line
    line1 = "Let's Build Your"
    line2 = "Revenue System."
    l1w = d.textlength(line1, font=F["md"])
    l2w = d.textlength(line2, font=F["lg"])
    d.text(((W-l1w)//2, 92), line1, font=F["md"], fill=(148, 163, 184))
    d.text(((W-l2w)//2+3, 132), line2, font=F["lg"], fill=(5,15,50))
    d.text(((W-l2w)//2+1, 130), line2, font=F["lg"], fill=(30,70,180))
    d.text(((W-l2w)//2,   128), line2, font=F["lg"], fill=(255,255,255))

    # Sub
    sub = "AI Sales Systems  ·  Revenue Operations  ·  GTM Strategy"
    sw = d.textlength(sub, font=F["sm"])
    d.text(((W-sw)//2, 212), sub, font=F["sm"], fill=(96,165,250))

    d.line([(W//2-220, 250), (W//2+220, 250)], fill=(37,99,235), width=1)

    # Website pill button
    pill_text = "  tonybeal.net  "
    pw = d.textlength(pill_text, font=F["pill"])
    px = (W - pw) // 2 - 16
    py = 268
    d.rounded_rectangle([px, py, px+pw+32, py+44], radius=22,
                         fill=(37,99,235), outline=(96,165,250), width=2)
    d.text((px+16, py+10), pill_text, font=F["pill"], fill=(255,255,255))

    # Tagline
    tag = "B2B companies · 30-min strategy call · no pitch, just clarity"
    tw = d.textlength(tag, font=F["xs"])
    d.text(((W-tw)//2, 330), tag, font=F["xs"], fill=(71,85,105))

    save(img, "linkedin-banner-slide5.png")

# ── Run all ───────────────────────────────────────────────────────────────────
slide2()
slide3()
slide4()
slide5()
print("All 4 slides generated.")
