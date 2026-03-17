"""
LinkedIn Banner - Cinematic Magazine Style
All 5 slides: 1584x396 | Photo left | Editorial/Film look
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1584, 396
PHOTO_PATH = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\headshot-hero.png"
BASE       = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets"

PHOTO_CX = 200
PHOTO_CY = 198
PHOTO_R  = 158
TXT_L    = 410   # pushed right to clear photo + glow rings
TXT_R    = 1558

# ── Fonts ─────────────────────────────────────────────────────────────────────
def F():
    def ft(fname, size):
        try:    return ImageFont.truetype(f"C:/Windows/Fonts/{fname}", size)
        except: return ImageFont.load_default()
    return {
        "name":    ft("ariblk.ttf", 130),    # Arial Black = bold condensed
        "sub":     ft("arialbd.ttf", 28),
        "tag":     ft("arial.ttf",   24),
        "xs":      ft("arial.ttf",   18),
        "badge":   ft("arialbd.ttf", 17),
        "stat":    ft("arialbd.ttf", 42),
        "statlbl": ft("arial.ttf",   15),
        "over":    ft("arialbd.ttf", 14),
        "md":      ft("arialbd.ttf", 38),
        "lg":      ft("ariblk.ttf",  70),
        "pill":    ft("arialbd.ttf", 22),
    }

# ── Photo ─────────────────────────────────────────────────────────────────────
def photo_circle(diam):
    p = Image.open(PHOTO_PATH).convert("RGBA")
    pw, ph = p.size
    s  = min(pw, ph)
    l  = (pw - s)//2
    t  = max(0, (ph - s)//6)
    p  = p.crop((l, t, l+s, t+s)).resize((diam, diam), Image.LANCZOS)
    m  = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(m).ellipse([0,0,diam-1,diam-1], fill=255)
    p.putalpha(m)
    return p

# ── Canvas ────────────────────────────────────────────────────────────────────
def dark_base(r1=(5,5,18), r2=(12,10,30)):
    img = Image.new("RGBA", (W, H))
    d   = ImageDraw.Draw(img)
    for y in range(H):
        t = y/H
        d.line([(0,y),(W,y)], fill=(
            int(r1[0] + (r2[0]-r1[0])*t),
            int(r1[1] + (r2[1]-r1[1])*t),
            int(r1[2] + (r2[2]-r1[2])*t), 255))
    return img

def light_sweep(img, cx, cy, color=(255,240,180), strength=38):
    """Cinematic light beam from behind the subject."""
    d = ImageDraw.Draw(img)
    for r in range(460, 0, -4):
        a = int(strength * math.exp(-((r/220)**2)))
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, a))

def dramatic_vignette(img):
    """Dark edges — cinematic letterbox feel."""
    d = ImageDraw.Draw(img)
    for i in range(60):
        a = int(160 * (i/60)**2)
        # sides
        d.rectangle([0, 0, i, H], fill=(0,0,0,a))
        d.rectangle([W-i, 0, W, H], fill=(0,0,0,a))
        # top/bottom bars
        d.rectangle([0, 0, W, i//2], fill=(0,0,0,a))
        d.rectangle([0, H-i//2, W, H], fill=(0,0,0,a))

def fine_grain(img, zone_x=TXT_L):
    """Subtle noise texture in text zone for print feel."""
    d = ImageDraw.Draw(img)
    import random; random.seed(42)
    for _ in range(2000):
        x = random.randint(zone_x, W)
        y = random.randint(0, H)
        v = random.randint(50,120)
        d.point((x,y), fill=(v,v,v,6))

def editorial_lines(img, accent):
    """Thin horizontal editorial rules."""
    d = ImageDraw.Draw(img)
    d.line([(TXT_L, 20),  (TXT_R, 20)],  fill=(*accent, 80), width=1)
    d.line([(TXT_L, H-20),(TXT_R, H-20)], fill=(*accent, 80), width=1)

def photo_glow(canvas, cx, cy, r, accent, style="cinematic"):
    d = ImageDraw.Draw(canvas)
    # Subtle dark backdrop circle so photo pops against any slide color
    for gr in range(r+55, r+2, -3):
        a = int(18 * (1 - (gr-r-2)/53))
        d.ellipse([cx-gr, cy-gr, cx+gr, cy+gr], fill=(0, 0, 0, a))
    # Glow rings
    for gr, alpha, width in [
        (r+4,  220, 3),
        (r+14, 110, 1),
        (r+26, 55,  1),
    ]:
        d.ellipse([cx-gr, cy-gr, cx+gr, cy+gr], outline=(*accent, alpha), width=width)
    # Arc segment decorations
    for angle, arc_r, arc_len in [(30, r+38, 40), (150, r+38, 40), (270, r+38, 40)]:
        d.arc([cx-arc_r, cy-arc_r, cx+arc_r, cy+arc_r],
              start=angle-arc_len//2, end=angle+arc_len//2,
              fill=(*accent, 160), width=2)

def place_photo(canvas, cx, cy, r, accent=(96,165,250)):
    photo_glow(canvas, cx, cy, r, accent)
    diam  = r*2
    photo = photo_circle(diam)
    canvas.paste(photo, (cx-r, cy-r), photo)

# ── Text helpers ──────────────────────────────────────────────────────────────
def shadow_text(d, text, font, x, y, color, offset=3):
    d.text((x+offset, y+offset), text, font=font, fill=(0,0,0,180))
    d.text((x+1,      y+1),      text, font=font, fill=(0,0,10,100))
    d.text((x,        y),        text, font=font, fill=color)

def rtxt(d, text, font, y, color, rx=TXT_R):
    x = rx - d.textlength(text, font=font)
    shadow_text(d, text, font, int(x), y, color)

def ltxt(d, text, font, y, color, lx=TXT_L+22):
    shadow_text(d, text, font, lx, y, color)

def ctxt(d, text, font, y, color):
    x = (TXT_L + TXT_R)//2 - d.textlength(text, font=font)//2
    shadow_text(d, text, font, int(x), y, color)

def badge_pill(d, text, x, y, bg, border, tc, font):
    tw = int(d.textlength(text, font=font))
    pw, ph = tw+34, 42
    d.rounded_rectangle([x, y, x+pw, y+ph], radius=21, fill=bg, outline=border, width=2)
    d.text((x+17, y+11), text, font=font, fill=tc)
    return pw+16

def stat_card(d, val, lbl, cx, cy, w, h, accent, font_val, font_lbl):
    d.rounded_rectangle([cx,cy,cx+w,cy+h], radius=6, fill=(255,255,255,8), outline=(*accent,120), width=1)
    vw = d.textlength(val, font=font_val)
    lw = d.textlength(lbl, font=font_lbl)
    d.text((cx+(w-vw)//2, cy+6),      val, font=font_val, fill=(255,255,255))
    d.text((cx+(w-lw)//2, cy+h-26),   lbl, font=font_lbl, fill=(148,163,184))

def save(img, name):
    path = f"{BASE}/{name}"
    img.convert("RGB").save(path, "PNG")
    print(f"Saved: {path}")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Main Brand
# ═══════════════════════════════════════════════════════════════════════════════
def slide1(f):
    A  = (96, 165, 250)
    c  = dark_base((4,4,16),(14,12,32))
    editorial_lines(c, A)
    fine_grain(c)
    place_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    dramatic_vignette(c)
    d  = ImageDraw.Draw(c)

    # Vertical left rule of text zone
    d.line([(TXT_L, 24), (TXT_L, H-24)], fill=(*A, 90), width=2)

    # Available pill
    badge_pill(d, "● AVAILABLE NOW", TXT_L+18, 22, (8,25,16), (52,211,153),
               (52,211,153), f["badge"])

    # Overline — right aligned, small caps feel
    over = "REVENUE OPERATIONS  ·  AI SALES SYSTEMS  ·  GTM STRATEGY"
    rtxt(d, over, f["over"], 74, A)
    ow = d.textlength(over, font=f["over"])
    d.line([(TXT_R-ow, 92), (TXT_R, 92)], fill=(*A, 100), width=1)

    # NAME — right aligned, fits in one line, leaves room for stats
    name = "TONY BEAL"
    nw   = d.textlength(name, font=f["name"])
    nx   = int(TXT_R - nw)
    d.text((nx+5, 96), name, font=f["name"], fill=(10,20,60,220))
    d.text((nx+2, 94), name, font=f["name"], fill=(40,70,180,160))
    d.text((nx,   92), name, font=f["name"], fill=(255,255,255))

    # Tagline — directly under name
    tag = "AI-Powered Revenue Systems  ·  B2B Companies"
    rtxt(d, tag, f["tag"], 238, (180,200,240))

    # Thin divider
    d.line([(TXT_L+18, 256), (TXT_R, 256)], fill=(*A,40), width=1)

    # Stats row — 4 cards right-aligned
    stats = [("$20M+","PIPELINE",(37,99,235)),("15+","YRS B2B",(99,102,241)),
             ("11K+","FOLLOWERS",(16,185,129)),("3,700+","ACCOUNTS",(37,99,235))]
    cw, ch = 156, 100
    total  = len(stats)*cw + (len(stats)-1)*10
    sx     = TXT_R - total
    for i,(v,l,ac) in enumerate(stats):
        cx = sx + i*(cw+10); cy = 264
        d.rounded_rectangle([cx, cy, cx+cw, cy+ch], radius=8,
                             fill=(12,20,50,180), outline=(*ac, 150), width=2)
        vw = d.textlength(v, font=f["stat"])
        lw = d.textlength(l, font=f["statlbl"])
        d.text((cx+(cw-vw)//2, cy+12),    v, font=f["stat"],    fill=(255,255,255))
        d.text((cx+(cw-lw)//2, cy+ch-24), l, font=f["statlbl"], fill=(148,163,184))

    # Website
    rtxt(d, "tonybeal.net", f["xs"], H-30, (70,84,103))

    save(c, "linkedin-banner-v2.png")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Proof Numbers (Emerald)
# ═══════════════════════════════════════════════════════════════════════════════
def slide2(f):
    A = (52, 211, 153)
    c = dark_base((4,14,10),(10,22,18))
    editorial_lines(c, A)
    fine_grain(c)
    place_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    dramatic_vignette(c)
    d = ImageDraw.Draw(c)
    d.line([(TXT_L, 24), (TXT_L, H-24)], fill=(*A, 90), width=2)

    # Headline
    ctxt(d, "THE NUMBERS", f["md"], 22, A)
    hw = d.textlength("THE NUMBERS", font=f["md"])
    zc = (TXT_L+TXT_R)//2
    d.line([(zc-hw//2-40, 64), (zc+hw//2+40, 64)], fill=(*A,60), width=1)

    # 2x2 grid of stats
    numbers = [
        ("$20M+",  "Pipeline Generated",   (52,211,153)),
        ("11K+",   "LinkedIn Followers",   (96,165,250)),
        ("3,700+", "Accounts Managed",     (129,140,248)),
        ("15+",    "Years in B2B Sales",   (52,211,153)),
    ]
    zw   = TXT_R - TXT_L
    colw = zw // 2
    for i,(v,l,col) in enumerate(numbers):
        ci, ri = i%2, i//2
        ccx    = TXT_L + colw*ci + colw//2
        y0     = 78 + ri*142
        vw = d.textlength(v, f["lg"])
        lw = d.textlength(l, f["sub"])
        d.text((ccx - vw//2 + 2, y0+2), v, font=f["lg"], fill=(0,0,0,150))
        d.text((ccx - vw//2,     y0),   v, font=f["lg"], fill=col)
        d.text((ccx - lw//2, y0+80),    l, font=f["sub"], fill=(160,175,190))
        if ci == 0:
            d.line([(TXT_L+colw, y0+4), (TXT_L+colw, y0+110)], fill=(*A,30), width=1)
    d.line([(TXT_L+40, 78+142-8), (TXT_R-40, 78+142-8)], fill=(*A,30), width=1)

    rtxt(d, "tonybeal.net", f["xs"], H-30, (60,100,80))
    save(c, "linkedin-banner-slide2.png")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — What I Build (Purple)
# ═══════════════════════════════════════════════════════════════════════════════
def slide3(f):
    A = (129, 140, 248)
    c = dark_base((6,4,20),(14,10,34))
    editorial_lines(c, A)
    fine_grain(c)
    place_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    dramatic_vignette(c)
    d = ImageDraw.Draw(c)
    d.line([(TXT_L, 24), (TXT_L, H-24)], fill=(*A, 90), width=2)

    ltxt(d, "WHAT I BUILD", f["md"], 16, A)
    hw = d.textlength("WHAT I BUILD", font=f["md"])
    d.line([(TXT_L+22, 60), (TXT_L+22+hw, 60)], fill=(*A,120), width=2)

    services = [
        ("⚙  Revenue Operations",
         "CRM Architecture  ·  Pipeline Design  ·  Forecasting  ·  Automation",
         (96,165,250)),
        ("◈  AI Sales Systems",
         "Outbound AI  ·  Lead Scoring  ·  Sequence Automation  ·  Analytics",
         (129,140,248)),
        ("▲  GTM Strategy",
         "ICP Definition  ·  Territory Planning  ·  Partner Ecosystems  ·  Enablement",
         (52,211,153)),
    ]
    for i,(title,desc,col) in enumerate(services):
        y0 = 72 + i*96
        d.rounded_rectangle([TXT_L+22, y0+2, TXT_L+28, y0+72], radius=3, fill=col)
        shadow_text(d, title, f["badge"], TXT_L+44, y0+6,  (255,255,255))
        d.text((TXT_L+44, y0+36), desc, font=f["xs"], fill=(140,155,175))
        if i < 2:
            d.line([(TXT_L+44, y0+86),(TXT_R-30, y0+86)], fill=(*A,22), width=1)

    rtxt(d, "tonybeal.net", f["xs"], H-30, (90,85,140))
    save(c, "linkedin-banner-slide3.png")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Cinematic Quote (Cyan)
# ═══════════════════════════════════════════════════════════════════════════════
def slide4(f):
    A = (6, 182, 212)
    c = dark_base((4,8,16),(10,18,28))
    editorial_lines(c, A)
    fine_grain(c)
    place_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    dramatic_vignette(c)
    d = ImageDraw.Draw(c)
    d.line([(TXT_L, 24), (TXT_L, H-24)], fill=(*A, 90), width=2)

    # Faint large quote mark watermark
    d.text((TXT_L+10, -22), "\u201c", font=f["name"], fill=(*A, 22))

    q1 = "Most companies don\u2019t have a sales problem."
    q2 = "They have a system problem."
    q3 = "I fix that."

    # Use sub/md fonts that fit within TXT_R
    ltxt(d, q1, f["sub"], 36, (160,185,210))

    # q2 — use md font (38pt) so it fits comfortably
    try:
        fq2 = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 56)
    except:
        fq2 = f["md"]
    q2w = int(d.textlength(q2, font=fq2))
    lx  = TXT_L + 26
    d.text((lx+3, 80), q2, font=fq2, fill=(0,0,10,200))
    d.text((lx+1, 78), q2, font=fq2, fill=(20,60,160,140))
    d.text((lx,   76), q2, font=fq2, fill=(255,255,255))

    # q3 — colored accent
    shadow_text(d, q3, f["md"], lx, 148, A)

    d.line([(lx, 202), (min(lx+600, TXT_R-20), 202)], fill=(*A, 80), width=1)
    ltxt(d, "— Tony Beal  |  Revenue Operations  ·  AI Sales  ·  GTM", f["xs"], 216, (96,165,250))
    ltxt(d, "Building systems that turn pipeline into predictable, scalable revenue.", f["xs"], 252, (80,100,120))

    # Badges
    bx = lx
    for lbl, col in [("RevOps",(37,99,235)),("AI Sales",(99,102,241)),("GTM",(16,185,129))]:
        bx += badge_pill(d, lbl, bx, 298, (10,18,44), col, col, f["badge"]) + 4

    rtxt(d, "tonybeal.net", f["xs"], H-30, (60,100,110))
    save(c, "linkedin-banner-slide4.png")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — CTA (Gold/Amber)
# ═══════════════════════════════════════════════════════════════════════════════
def slide5(f):
    A = (245, 158, 11)
    c = dark_base((10,6,2),(22,14,4))
    editorial_lines(c, A)
    fine_grain(c)
    place_photo(c, PHOTO_CX, PHOTO_CY, PHOTO_R, A)
    dramatic_vignette(c)
    d = ImageDraw.Draw(c)
    d.line([(TXT_L, 24), (TXT_L, H-24)], fill=(*A, 90), width=2)

    badge_pill(d, "● AVAILABLE NOW", TXT_L+18, 26, (28,16,2), A, A, f["badge"])

    ltxt(d, "Ready to scale your", f["sub"], 82,  (180,155,100))
    l2 = "Revenue System?"
    d.text((TXT_L+26+4, 120), l2, font=f["lg"], fill=(0,0,0,200))
    d.text((TXT_L+26+2, 118), l2, font=f["lg"], fill=(80,50,0,140))
    d.text((TXT_L+26,   116), l2, font=f["lg"], fill=(255,255,255))

    ltxt(d, "RevOps  ·  AI Sales Automation  ·  GTM Strategy  ·  B2B Pipeline",
         f["xs"], 200, (150,130,80))

    d.line([(TXT_L+26, 236),(TXT_R-30, 236)], fill=(*A,50), width=1)

    # CTA buttons
    bx = TXT_L + 26
    bw1 = badge_pill(d, "Visit tonybeal.net", bx, 252, (42,28,2), A, (255,225,80), f["pill"])
    badge_pill(d, "Book a Strategy Call", bx+bw1+20, 252,
               (12,18,50), (37,99,235), (96,165,250), f["pill"])

    ltxt(d, "30-min call  ·  No pitch  ·  Just clarity on your revenue gaps",
         f["xs"], 320, (90,75,40))

    rtxt(d, "tonybeal.net", f["xs"], H-30, (100,80,36))
    save(c, "linkedin-banner-slide5.png")

# ── Run ───────────────────────────────────────────────────────────────────────
fonts = F()
slide1(fonts)
slide2(fonts)
slide3(fonts)
slide4(fonts)
slide5(fonts)
print("\nAll 5 cinematic slides done!")
