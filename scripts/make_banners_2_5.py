"""
LinkedIn banner slideshow - slides 2-5 (1584x396 each)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1584, 396

def load_fonts():
    try:
        return {
            "xl":    ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 130),
            "lg":    ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 88),
            "md":    ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   38),
            "sm":    ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   28),
            "xs":    ImageFont.truetype("C:/Windows/Fonts/arial.ttf",   20),
            "badge": ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 20),
            "stat":  ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36),
            "pill":  ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28),
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
    center_text(d, "PROVEN RESULTS  ·  B2B REVENUE & PIPELINE", F["xs"], 20,
                (96, 165, 250))
    d.line([(W//2 - 320, 48), (W//2 + 320, 48)], fill=(37, 99, 235), width=1)

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
        d.text((cx - vw//2, 60), val, font=F["lg"], fill=col)
        lw = d.textlength(label, font=F["sm"])
        d.text((cx - lw//2, 168), label, font=F["sm"], fill=(148, 163, 184))
        if i < 3:
            d.line([(col_w*(i+1), 70), (col_w*(i+1), 200)],
                   fill=(37, 99, 235), width=1)

    # Tagline
    tag = "Tony Beal  ·  Revenue Operations & AI Sales Systems"
    tw = d.textlength(tag, font=F["sm"])
    d.text(((W - tw)//2, 220), tag, font=F["sm"], fill=(210, 220, 240))

    # Bottom bar
    for x in range(W):
        t = x / W
        d.line([(x, 282), (x, 288)],
               fill=(int(37 + 62*t), int(99), int(235 - 100*t)))

    center_text(d, "tonybeal.net", F["xs"], 310, (71, 85, 105))

    save(img, "linkedin-banner-slide2.png")

# ── SLIDE 3: Three service pillars ───────────────────────────────────────────
def slide3():
    img = dark_canvas()
    add_dot_grid(img)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    # Top label
    center_text(d, "WHAT I DO", F["badge"], 14, (96, 165, 250))
    tw = d.textlength("WHAT I DO", font=F["badge"])
    d.line([((W-tw)//2 - 50, 42), ((W-tw)//2, 42)], fill=(37,99,235), width=1)
    d.line([((W+tw)//2, 42), ((W+tw)//2 + 50, 42)], fill=(37,99,235), width=1)

    pillars = [
        ("⚙", "Revenue\nOperations",
         "CRM · Pipeline Design\nForecasting · Automation",
         (37, 99, 235)),
        ("AI", "AI Sales\nSystems",
         "Outbound AI · Lead Scoring\nSequences · Analytics",
         (99, 102, 241)),
        ("📈", "GTM\nStrategy",
         "ICP · Territory Planning\nPartner · Sales Enablement",
         (16, 185, 129)),
    ]

    card_w = 460
    gap = (W - 3 * card_w) // 4
    for i, (icon, title, desc, border) in enumerate(pillars):
        cx = gap + i * (card_w + gap)
        cy = 54
        ch = 310
        d.rounded_rectangle([cx, cy, cx+card_w, cy+ch], radius=10,
                             fill=(14, 22, 50), outline=border, width=2)
        # icon / label
        iw = d.textlength(icon, font=F["md"])
        d.text((cx + (card_w-iw)//2, cy+10), icon, font=F["md"], fill=border)
        # title lines
        t_lines = title.split("\n")
        ty = cy + 62
        for line in t_lines:
            lw = d.textlength(line, font=F["stat"])
            d.text((cx + (card_w-lw)//2, ty), line, font=F["stat"],
                   fill=(255, 255, 255))
            ty += 44
        # desc
        d_lines = desc.split("\n")
        dy = ty + 8
        for line in d_lines:
            lw = d.textlength(line, font=F["xs"])
            d.text((cx + (card_w-lw)//2, dy), line, font=F["xs"],
                   fill=(148, 163, 184))
            dy += 28

    center_text(d, "tonybeal.net", F["xs"], 374, (71, 85, 105))
    save(img, "linkedin-banner-slide3.png")

# ── SLIDE 4: Bold quote ───────────────────────────────────────────────────────
def slide4():
    img = dark_canvas()
    add_dot_grid(img, spacing=28, alpha=12)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    for r in [120, 170, 220]:
        d.arc([W-r, H//2-r, W+r, H//2+r], start=145, end=215,
              fill=(37, 99, 235, 45), width=2)

    # Quote — two lines, tighter layout for bigger fonts
    q1 = "Most companies don't have a sales problem."
    q2 = "They have a system problem."
    q1w = d.textlength(q1, font=F["md"])
    q2w = d.textlength(q2, font=F["lg"])

    d.text(((W - q1w)//2, 60), q1, font=F["md"], fill=(210, 220, 240))
    d.text(((W - q2w)//2 + 3, 108), q2, font=F["lg"], fill=(5, 15, 50))
    d.text(((W - q2w)//2 + 1, 106), q2, font=F["lg"], fill=(37, 80, 180))
    d.text(((W - q2w)//2,     104), q2, font=F["lg"], fill=(255, 255, 255))

    d.line([(W//2 - 220, 210), (W//2 + 220, 210)], fill=(37, 99, 235), width=1)

    attr = "— Tony Beal  |  Revenue Operations  ·  AI Sales Systems"
    aw = d.textlength(attr, font=F["sm"])
    d.text(((W - aw)//2, 222), attr, font=F["sm"], fill=(96, 165, 250))

    sub = "I build systems that turn pipeline into predictable revenue."
    sw = d.textlength(sub, font=F["xs"])
    d.text(((W - sw)//2, 276), sub, font=F["xs"], fill=(100, 116, 139))

    center_text(d, "tonybeal.net", F["xs"], 340, (71, 85, 105))
    save(img, "linkedin-banner-slide4.png")

# ── SLIDE 5: CTA ─────────────────────────────────────────────────────────────
def slide5():
    img = dark_canvas()
    add_dot_grid(img, spacing=26, alpha=14)
    add_left_bar(img)
    d = ImageDraw.Draw(img)

    for r in range(160, 0, -4):
        a = int(18 * (1 - r/160))
        d.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], outline=(37,99,235,a))

    # Available badge — centered
    bx = W//2 - 115
    by = 18
    d.rounded_rectangle([bx, by, bx+230, by+50], radius=25,
                         fill=(10,38,28), outline=(52,211,153), width=2)
    d.ellipse([bx+16, by+17, bx+33, by+34], fill=(52,211,153))
    d.text((bx+42, by+13), "AVAILABLE NOW", font=F["badge"], fill=(52,211,153))

    line1 = "Let's Build Your"
    line2 = "Revenue System."
    l1w = d.textlength(line1, font=F["md"])
    l2w = d.textlength(line2, font=F["lg"])
    d.text(((W-l1w)//2, 82), line1, font=F["md"], fill=(148, 163, 184))
    d.text(((W-l2w)//2+3, 126), line2, font=F["lg"], fill=(5,15,50))
    d.text(((W-l2w)//2+1, 124), line2, font=F["lg"], fill=(30,70,180))
    d.text(((W-l2w)//2,   122), line2, font=F["lg"], fill=(255,255,255))

    sub = "AI Sales Systems  ·  Revenue Operations  ·  GTM Strategy"
    sw = d.textlength(sub, font=F["sm"])
    d.text(((W-sw)//2, 226), sub, font=F["sm"], fill=(96,165,250))

    d.line([(W//2-240, 268), (W//2+240, 268)], fill=(37,99,235), width=1)

    # Website pill button
    pill_text = "  tonybeal.net  "
    pw = d.textlength(pill_text, font=F["pill"])
    px = (W - pw) // 2 - 20
    py = 282
    d.rounded_rectangle([px, py, px+pw+40, py+56], radius=28,
                         fill=(37,99,235), outline=(96,165,250), width=2)
    d.text((px+20, py+13), pill_text, font=F["pill"], fill=(255,255,255))

    tag = "B2B companies · 30-min strategy call · no pitch, just clarity"
    tw = d.textlength(tag, font=F["xs"])
    d.text(((W-tw)//2, 355), tag, font=F["xs"], fill=(71,85,105))

    save(img, "linkedin-banner-slide5.png")

# ── Run all ───────────────────────────────────────────────────────────────────
slide2()
slide3()
slide4()
slide5()
print("All 4 slides generated.")
