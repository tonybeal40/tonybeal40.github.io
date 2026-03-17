"""
LinkedIn banner slideshow v3 — All 5 slides
Each slide: 1584x396 | Photo LEFT with glow | Futuristic neon design | Bold text RIGHT
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1584, 396
PHOTO_PATH = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\headshot-hero.png"
BASE       = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets"

# ── Layout zones ──────────────────────────────────────────────────────────────
PHOTO_CX = 210   # photo circle center x
PHOTO_CY = 198   # photo circle center y
PHOTO_R  = 158   # photo circle radius
TXT_L    = 432   # left edge of text zone
TXT_R    = 1558  # right edge of text zone

# ── Fonts ─────────────────────────────────────────────────────────────────────
def load_fonts():
    f = {}
    specs = [
        ("name",  "arialbd.ttf", 110),
        ("lg",    "arialbd.ttf",  76),
        ("md",    "arialbd.ttf",  40),
        ("sm",    "arial.ttf",    30),
        ("xs",    "arial.ttf",    20),
        ("badge", "arialbd.ttf",  19),
        ("stat",  "arialbd.ttf",  40),
        ("lbl",   "arial.ttf",    17),
        ("pill",  "arialbd.ttf",  26),
    ]
    for key, fname, size in specs:
        try:
            f[key] = ImageFont.truetype(f"C:/Windows/Fonts/{fname}", size)
        except:
            f[key] = ImageFont.load_default()
    return f

F = load_fonts()

# ── Photo helper ──────────────────────────────────────────────────────────────
def get_photo_circle(diameter):
    photo = Image.open(PHOTO_PATH).convert("RGBA")
    pw, ph = photo.size
    side = min(pw, ph)
    left = (pw - side) // 2
    top  = max(0, (ph - side) // 5)   # slight top bias to capture face
    photo = photo.crop((left, top, left + side, top + side))
    photo = photo.resize((diameter, diameter), Image.LANCZOS)
    mask  = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diameter-1, diameter-1], fill=255)
    photo.putalpha(mask)
    return photo

# ── Background builders ───────────────────────────────────────────────────────
def make_base():
    img = Image.new("RGBA", (W, H))
    d   = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0,y),(W,y)], fill=(int(6+3*t), int(8+4*t), int(22+10*t), 255))
    return img

def add_hex_grid(img, color=(37,99,235), alpha=9):
    d = ImageDraw.Draw(img)
    r = 22
    hs = r * math.sqrt(3)
    for row in range(-1, int(H/hs)+3):
        for col in range(-1, int(W/(r*1.5))+3):
            cx = col*r*3 + (r*1.5 if row%2 else 0)
            cy = row * hs
            verts = [(cx + r*math.cos(math.radians(60*i-30)),
                      cy + r*math.sin(math.radians(60*i-30))) for i in range(6)]
            d.polygon(verts, outline=(*color, alpha))

def add_glow_orb(img, cx, cy, radius, color=(37,99,235)):
    d = ImageDraw.Draw(img)
    for r in range(radius, 0, -6):
        a = int(35 * (r/radius) * (1 - r/radius) * 4)
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, a))

def add_scan_lines(img, accent=(37,99,235)):
    d = ImageDraw.Draw(img)
    for yp in range(0, H, 44):
        d.line([(TXT_L, yp), (W, yp)], fill=(*accent, 8), width=1)

def add_circuit_deco(img, accent=(37,99,235)):
    d = ImageDraw.Draw(img)
    # Top-right corner circuit
    segs = [
        [(TXT_R-140, 18), (TXT_R-60, 18), (TXT_R-60, 46), (TXT_R-20, 46)],
        [(TXT_R-100, H-18), (TXT_R-30, H-18), (TXT_R-30, H-44)],
        [(TXT_L+20, 14), (TXT_L+90, 14), (TXT_L+90, 40)],
    ]
    for seg in segs:
        d.line(seg, fill=(*accent, 50), width=1)
        ex, ey = seg[-1]
        d.ellipse([ex-3, ey-3, ex+3, ey+3], fill=(*accent, 120))

def add_photo_glow(canvas, cx, cy, r, accent=(37,99,235)):
    d = ImageDraw.Draw(canvas)
    # Outer diffuse glow
    for gr in range(r+70, r+5, -5):
        a = max(0, int(30 * (1 - (gr - r - 5) / 65)))
        d.ellipse([cx-gr, cy-gr, cx+gr, cy+gr], outline=(*accent, a), width=1)
    # Crisp rings
    for gr, col, w in [
        (r+5,  (255,255,255,180), 3),
        (r+14, (*accent, 120),   2),
        (r+24, (*accent, 60),    1),
        (r+38, (*accent, 30),    1),
    ]:
        d.ellipse([cx-gr, cy-gr, cx+gr, cy+gr], outline=col, width=w)
    # Tick marks
    for angle in range(0, 360, 12):
        rad = math.radians(angle)
        ri  = r + 28
        ro  = r + 38 if angle % 90 == 0 else (r+33 if angle%45==0 else r+30)
        a   = 200 if angle%90==0 else (110 if angle%45==0 else 40)
        d.line([(cx+ri*math.cos(rad), cy+ri*math.sin(rad)),
                (cx+ro*math.cos(rad), cy+ro*math.sin(rad))],
               fill=(*accent, a), width=1)
    # Orbiting dots
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        pr  = r + 58 + 8*math.sin(math.radians(angle*4))
        px, py = cx + pr*math.cos(rad), cy + pr*math.sin(rad)
        ds  = 4 if angle % 60 == 0 else 2
        d.ellipse([px-ds, py-ds, px+ds, py+ds], fill=(*accent, 140))

def composite_photo(canvas, cx, cy, r, accent=(37,99,235)):
    add_photo_glow(canvas, cx, cy, r, accent)
    diam  = r * 2
    photo = get_photo_circle(diam)
    canvas.paste(photo, (cx - r, cy - r), photo)

# ── Text helpers ──────────────────────────────────────────────────────────────
def rtxt(d, text, font, y, color, rx=TXT_R):
    w = d.textlength(text, font=font)
    d.text((rx - w, y), text, font=font, fill=color)

def ctxt(d, text, font, y, color, zone_l=TXT_L, zone_r=TXT_R):
    w  = d.textlength(text, font=font)
    cx = (zone_l + zone_r) // 2
    d.text((cx - w//2, y), text, font=font, fill=color)

def shadow(d, text, font, x, y, color, shade=(4,10,40)):
    d.text((x+3, y+3), text, font=font, fill=(*shade, 210))
    d.text((x+1, y+1), text, font=font, fill=(*shade, 120))
    d.text((x,   y),   text, font=font, fill=color)

def pill(d, text, x, y, bg, border, tc=(255,255,255), font=None):
    fn = font or F["badge"]
    tw = d.textlength(text, font=fn)
    pw, ph = int(tw) + 32, 40
    d.rounded_rectangle([x, y, x+pw, y+ph], radius=20, fill=bg, outline=border, width=2)
    d.text((x+16, y+10), text, font=fn, fill=tc)
    return pw   # return width for chaining

def vbar(d, accent):
    """Left divider bar of text zone."""
    d.line([(TXT_L-4, 18), (TXT_L-4, H-18)], fill=(*accent, 90), width=3)

def save(img, name):
    path = f"{BASE}/{name}"
    img.convert("RGB").save(path, "PNG")
    print(f"Saved: {path}")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Main Brand Banner
# ════════════════════════════════════════════════════════════════════════════════
def slide1():
    A = (37, 99, 235)   # Blue
    c = make_base()
    add_hex_grid(c, A, 11)
    add_glow_orb(c, 1380, 190, 320, A)
    add_scan_lines(c, A)
    add_circuit_deco(c, A)
    composite_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    d = ImageDraw.Draw(c)
    vbar(d, A)

    # AVAILABLE badge
    pill(d, "  ● AVAILABLE NOW", TXT_L+16, 26, (8,28,18), (52,211,153), (52,211,153))

    # Overline
    over = "REVENUE OPERATIONS  ·  AI SALES SYSTEMS  ·  GTM STRATEGY"
    ow   = d.textlength(over, font=F["badge"])
    d.text((TXT_R - ow, 86), over, font=F["badge"], fill=(96,165,250))
    d.line([(TXT_R - ow, 110), (TXT_R, 110)], fill=(*A,), width=1)

    # Name
    name = "Tony Beal"
    nw   = d.textlength(name, font=F["name"])
    shadow(d, name, F["name"], int(TXT_R - nw), 116, (255,255,255))

    # Tagline
    tag = "AI-Powered Revenue Systems  ·  B2B Companies"
    tw  = d.textlength(tag, font=F["sm"])
    d.text((TXT_R - tw, 242), tag, font=F["sm"], fill=(170,195,240))

    # Stats
    stats = [
        ("$20M+", "PIPELINE",  (37,99,235),  (255,255,255)),
        ("15+",   "YRS B2B",   (99,102,241), (255,255,255)),
        ("11K+",  "FOLLOWERS", (16,185,129), (52,211,153)),
        ("3,700+","ACCOUNTS",  (37,99,235),  (255,255,255)),
    ]
    cw, ch = 160, 80
    total  = len(stats)*cw + (len(stats)-1)*10
    sx     = TXT_R - total
    for i, (val, lbl, border, tc) in enumerate(stats):
        cx = sx + i*(cw+10); cy = 272
        d.rounded_rectangle([cx,cy,cx+cw,cy+ch], radius=10,
                             fill=(12,20,50), outline=border, width=2)
        vw = d.textlength(val,  font=F["stat"])
        lw = d.textlength(lbl,  font=F["lbl"])
        d.text((cx+(cw-vw)//2, cy+8),  val, font=F["stat"], fill=tc)
        d.text((cx+(cw-lw)//2, cy+55), lbl, font=F["lbl"],  fill=(148,163,184))

    rtxt(d, "tonybeal.net", F["xs"], 366, (71,85,105))
    save(c, "linkedin-banner-v2.png")


# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Proof Numbers   (green accent)
# ════════════════════════════════════════════════════════════════════════════════
def slide2():
    A = (16, 185, 129)  # Green
    c = make_base()
    add_hex_grid(c, A, 10)
    add_glow_orb(c, 1360, 180, 300, A)
    add_scan_lines(c, A)
    add_circuit_deco(c, A)
    composite_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    d = ImageDraw.Draw(c)
    vbar(d, A)

    # Header
    hdr = "★  PROVEN RESULTS  ★"
    ctxt(d, hdr, F["badge"], 20, (52,211,153))
    hw = d.textlength(hdr, font=F["badge"])
    zc = (TXT_L+TXT_R)//2
    d.line([(zc - hw//2 - 30, 46), (zc + hw//2 + 30, 46)], fill=(*A,60), width=1)

    # 2 × 2 big numbers
    stats = [
        ("$20M+",  "Pipeline Generated",  (52,211,153)),
        ("11K+",   "LinkedIn Followers",  (96,165,250)),
        ("3,700+", "Accounts Managed",    (129,140,248)),
        ("15+",    "Years in B2B Sales",  (52,211,153)),
    ]
    zw   = TXT_R - TXT_L
    colw = zw // 2
    for i, (val, label, col) in enumerate(stats):
        ci   = i % 2
        ri   = i // 2
        ccx  = TXT_L + colw*ci + colw//2
        base_y = 62 + ri * 152
        vw   = d.textlength(val,   font=F["lg"])
        lw   = d.textlength(label, font=F["sm"])
        shadow(d, val,   F["lg"], ccx - vw//2, base_y,    col)
        d.text((ccx - lw//2, base_y + 84), label, font=F["sm"], fill=(148,163,184))
        if ci == 0:  # column divider
            d.line([(TXT_L+colw, base_y+10), (TXT_L+colw, base_y+120)],
                   fill=(*A, 45), width=1)
    # Row divider
    d.line([(TXT_L+40, 62+152-12), (TXT_R-40, 62+152-12)], fill=(*A,35), width=1)

    ctxt(d, "Tony Beal  ·  tonybeal.net", F["xs"], 374, (71,85,105))
    save(c, "linkedin-banner-slide2.png")


# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — What I Build   (purple accent)
# ════════════════════════════════════════════════════════════════════════════════
def slide3():
    A = (99, 102, 241)  # Purple
    c = make_base()
    add_hex_grid(c, A, 10)
    add_glow_orb(c, 1380, 200, 300, A)
    add_scan_lines(c, A)
    add_circuit_deco(c, A)
    composite_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    d = ImageDraw.Draw(c)
    vbar(d, A)

    # Header
    hdr = "WHAT I BUILD"
    shadow(d, hdr, F["md"], TXT_L+22, 18, (255,255,255))
    hw = d.textlength(hdr, font=F["md"])
    d.line([(TXT_L+22, 64), (TXT_L+22+hw, 64)], fill=(*A,), width=2)

    services = [
        ("⚙  REVENUE OPERATIONS",
         "CRM  ·  Pipeline Design  ·  Forecasting  ·  Process Automation",
         (37,99,235)),
        ("◆  AI SALES SYSTEMS",
         "Outbound AI  ·  Lead Scoring  ·  Sequence Automation  ·  Analytics",
         (99,102,241)),
        ("▲  GTM STRATEGY",
         "ICP Definition  ·  Territory Planning  ·  Partners  ·  Sales Enablement",
         (16,185,129)),
    ]
    for i, (title, desc, col) in enumerate(services):
        y0 = 80 + i * 96
        # colored accent bar
        d.rounded_rectangle([TXT_L+18, y0+4, TXT_L+24, y0+68], radius=3, fill=col)
        d.text((TXT_L+38, y0+4),  title, font=F["badge"], fill=col)
        d.text((TXT_L+38, y0+34), desc,  font=F["xs"],    fill=(148,163,184))
        if i < 2:
            d.line([(TXT_L+38, y0+82), (TXT_R-30, y0+82)], fill=(*A,25), width=1)

    ctxt(d, "tonybeal.net", F["xs"], 376, (71,85,105))
    save(c, "linkedin-banner-slide3.png")


# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Bold Quote   (cyan accent)
# ════════════════════════════════════════════════════════════════════════════════
def slide4():
    A = (6, 182, 212)  # Cyan
    c = make_base()
    add_hex_grid(c, A, 9)
    add_glow_orb(c, 1360, 200, 300, A)
    add_scan_lines(c, A)
    add_circuit_deco(c, A)
    composite_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    d = ImageDraw.Draw(c)
    vbar(d, A)

    # Large faint quote mark
    d.text((TXT_L+8, -8), "\u201c", font=F["name"], fill=(*A, 28))

    q1 = "Most companies don\u2019t have a sales problem."
    q2 = "They have a system problem."
    q3 = "I fix that."

    q1w = d.textlength(q1, font=F["sm"])
    q2w = d.textlength(q2, font=F["lg"])
    q3w = d.textlength(q3, font=F["md"])

    d.text((TXT_L+28, 56),  q1, font=F["sm"], fill=(168,185,210))
    shadow(d, q2, F["lg"], TXT_L+28, 90,  (255,255,255))
    shadow(d, q3, F["md"], TXT_L+28, 178, A + (255,))

    d.line([(TXT_L+28, 236), (TXT_L+500, 236)], fill=(*A, 80), width=1)

    d.text((TXT_L+28, 248), "— Tony Beal  |  tonybeal.net",
           font=F["xs"], fill=(96,165,250))
    d.text((TXT_L+28, 292),
           "Building revenue systems that create predictable, scalable pipeline.",
           font=F["xs"], fill=(90,105,125))

    # small badge row
    badges = [
        ("RevOps",          (37,99,235)),
        ("AI Sales",        (99,102,241)),
        ("GTM Strategy",    (16,185,129)),
    ]
    bx = TXT_L + 28
    for label, col in badges:
        bw = pill(d, label, bx, 334, (10,20,44), col, col)
        bx += bw + 12

    save(c, "linkedin-banner-slide4.png")


# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — CTA   (gold accent)
# ════════════════════════════════════════════════════════════════════════════════
def slide5():
    A = (245, 158, 11)  # Gold
    c = make_base()
    add_hex_grid(c, A, 10)
    add_glow_orb(c, 1360, 180, 300, A)
    add_scan_lines(c, A)
    add_circuit_deco(c, A)
    composite_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    d = ImageDraw.Draw(c)
    vbar(d, A)

    # Available badge
    pill(d, "  ● AVAILABLE NOW", TXT_L+16, 22, (28,18,4), A, A)

    # CTA headline
    l1 = "Ready to scale your"
    l2 = "Revenue System?"
    d.text((TXT_L+22, 80), l1, font=F["sm"], fill=(190,175,140))
    shadow(d, l2, F["lg"], TXT_L+22, 114, (255,255,255))

    # Sub line
    d.text((TXT_L+22, 212),
           "RevOps  ·  AI Sales Automation  ·  GTM  ·  B2B Pipeline",
           font=F["xs"], fill=(160,140,90))

    d.line([(TXT_L+22, 248), (TXT_R-30, 248)], fill=(*A, 45), width=1)

    # CTA buttons
    bx = TXT_L + 22
    bw1 = pill(d, "  Visit tonybeal.net  ", bx, 264, (40,28,4), A,
               (255,225,100), F["badge"])
    pill(d, "  Book a Strategy Call  ", bx + bw1 + 18, 264,
         (12,20,52), (37,99,235), (96,165,250), F["badge"])

    d.text((TXT_L+22, 326),
           "30-min call  ·  No pitch  ·  Just clarity on your revenue gaps",
           font=F["xs"], fill=(80,70,46))

    save(c, "linkedin-banner-slide5.png")


# ── Run all ───────────────────────────────────────────────────────────────────
slide1()
slide2()
slide3()
slide4()
slide5()
print("\nAll 5 slides done!")
