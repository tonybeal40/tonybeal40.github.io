"""
LinkedIn Banners v5 — All 5 slides, Modern Tech / Canva-Adobe style
1584x396 | Photo RIGHT | Mesh gradient bg | Unique content per slide
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, random, os

W, H   = 1584, 396
BASE   = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site"
PHOTO  = os.path.join(BASE, "headshot-new.png")
ASSETS = os.path.join(BASE, "assets")

def ft(f, s):
    try:    return ImageFont.truetype(f"C:/Windows/Fonts/{f}", s)
    except: return ImageFont.load_default()

F = {
    "name":  ft("ariblk.ttf",  110),
    "role":  ft("arialbd.ttf",  32),
    "tag":   ft("arial.ttf",    22),
    "sm":    ft("arial.ttf",    18),
    "badge": ft("arialbd.ttf",  16),
    "stat":  ft("ariblk.ttf",   40),
    "stlbl": ft("arial.ttf",    14),
    "h2":    ft("ariblk.ttf",   52),
    "h3":    ft("arialbd.ttf",  28),
    "big":   ft("ariblk.ttf",   72),
    "quote": ft("arial.ttf",    26),
}

# ─────────────────────────────────────────────────────────────────────────────
# SHARED: build background + photo layer (returns canvas + draw + photo_e + px)
# ─────────────────────────────────────────────────────────────────────────────
def build_base(orb_palette=None, seed=12):
    random.seed(seed)

    # Base dark navy
    canvas = Image.new("RGBA", (W, H), (4, 6, 20, 255))

    # ── Glowing orbs ──
    default_orbs = [
        (300,  -80,  420, (99,  102, 241), 40),
        (-60,  280,  380, (37,   99, 235), 35),
        (820,  200,  500, (6,   182, 212), 30),
        (1400, -50,  450, (139,  92, 246), 38),
        (1500, 350,  380, (16,  185, 129), 25),
        (600,  400,  350, (245, 158,  11), 20),
    ]
    orbs = orb_palette or default_orbs
    orb_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    od = ImageDraw.Draw(orb_layer)
    for ox, oy, orb_r, col, strength in orbs:
        r,g,b = col
        for radius in range(orb_r, 0, -4):
            t = radius / orb_r
            a = int(strength * math.exp(-((1-t)*3.5)**1.5))
            od.ellipse([ox-radius,oy-radius,ox+radius,oy+radius], fill=(r,g,b,a))
    orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, orb_layer)

    # ── Hex grid ──
    hex_r  = 28
    hex_hs = hex_r * math.sqrt(3)
    hex_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    hd = ImageDraw.Draw(hex_layer)
    for row in range(-1, int(H/hex_hs)+3):
        for col in range(-1, int(W/(hex_r*1.5))+3):
            hcx = col*hex_r*3 + (hex_r*1.5 if row%2 else 0)
            hcy = row * hex_hs
            verts = [(hcx + hex_r*math.cos(math.radians(60*i-30)),
                      hcy + hex_r*math.sin(math.radians(60*i-30))) for i in range(6)]
            hd.polygon(verts, outline=(96, 165, 250, 14))
    canvas = Image.alpha_composite(canvas, hex_layer)

    # ── Particle network ──
    pd = ImageDraw.Draw(canvas)
    nodes = [(random.randint(0,W), random.randint(0,H)) for _ in range(80)]
    for nx, ny in nodes:
        sz = random.choice([1,1,1,2,3])
        a  = random.randint(20, 80)
        c  = random.choice([(96,165,250,a),(52,211,153,a),(139,92,246,a),(255,255,255,a)])
        pd.ellipse([nx, ny, nx+sz, ny+sz], fill=c)
    for i, (nx, ny) in enumerate(nodes[:40]):
        for mx, my in nodes[i+1:i+4]:
            dist = math.hypot(mx-nx, my-ny)
            if dist < 120:
                a = int(30 * (1 - dist/120))
                pd.line([(nx,ny),(mx,my)], fill=(96,165,250,a), width=1)
    for _ in range(1500):
        x = random.randint(0,W); y = random.randint(0,H)
        v = random.randint(50,100)
        pd.point((x,y), fill=(v,v,v,random.randint(4,10)))

    # ── Photo — circle portrait, far right, doesn't touch text ──
    R        = 178          # circle radius
    CX       = W - R - 30  # circle center x (far right, clear of text)
    CY       = H // 2      # vertically centered

    # Multi-ring glow behind circle
    hl = Image.new("RGBA", (W, H), (0,0,0,0))
    hd2 = ImageDraw.Draw(hl)
    for rad in range(R+60, R-1, -3):
        t = (rad - R) / 60
        a = int(28 * math.exp(-t * 3))
        hd2.ellipse([CX-rad, CY-rad, CX+rad, CY+rad], fill=(99,102,241,a))
    canvas = Image.alpha_composite(canvas, hl)

    # Load + scale photo to fill circle
    photo = Image.open(PHOTO).convert("RGBA")
    pw, ph = photo.size
    diam   = R * 2
    scale  = diam / min(pw, ph)
    nw2    = int(pw * scale); nh2 = int(ph * scale)
    photo  = photo.resize((nw2, nh2), Image.LANCZOS)
    # Centre-crop to exact circle diameter
    cx_off = (nw2 - diam) // 2; cy_off = (nh2 - diam) // 2
    photo  = photo.crop((cx_off, cy_off, cx_off+diam, cy_off+diam))

    # Create circular mask
    mask = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mask).ellipse([0,0,diam,diam], fill=255)

    # Darken/blend the light background of new photo
    rgb3   = ImageEnhance.Brightness(photo.convert("RGB")).enhance(0.85)
    rgb3   = ImageEnhance.Contrast(rgb3).enhance(1.2)
    photo_rgb = rgb3.convert("RGBA")
    photo_rgb.putalpha(mask)

    # Paste circle onto canvas
    canvas.paste(photo_rgb, (CX - R, CY - R), photo_rgb)

    # Decorative ring border on top
    bd = ImageDraw.Draw(canvas)
    bd.ellipse([CX-R-3, CY-R-3, CX+R+3, CY+R+3], outline=(96,165,250,200), width=3)
    bd.ellipse([CX-R-7, CY-R-7, CX+R+7, CY+R+7], outline=(96,165,250,50),  width=2)

    # Dark scrim left zone
    scrim = Image.new("RGBA",(W,H),(0,0,0,0))
    sd = ImageDraw.Draw(scrim)
    for x in range(900):
        t = 1-(x/900)**0.6
        sd.line([(x,0),(x,H)], fill=(0,0,0,int(100*t)))
    canvas = Image.alpha_composite(canvas, scrim)

    draw = ImageDraw.Draw(canvas)
    return canvas, draw

def accent_stripe(draw):
    for xi in range(6):
        a = int(180*(1-xi/6))
        draw.line([(xi,0),(xi,H)], fill=(96,165,250,a), width=1)

def edge_lines(draw):
    for x in range(W):
        t = x/W
        rc = int(37+(139-37)*t); gc = int(99+(92-99)*t); bc = int(235+(246-235)*t)
        draw.point((x,0),   fill=(rc,gc,bc))
        draw.point((x,1),   fill=(rc,gc,bc))
        draw.point((x,2),   fill=(rc,gc,bc,120))
        draw.point((x,H-1), fill=(rc,gc,bc))
        draw.point((x,H-2), fill=(rc,gc,bc))

def draw_name(draw, LX=50):
    t1, t2 = "TONY", " BEAL"
    t1w = int(draw.textlength(t1, font=F["name"]))
    draw.text((LX+3,63), t1+t2, font=F["name"], fill=(0,0,0,160))
    draw.text((LX,  60), t1,    font=F["name"], fill=(255,255,255))
    draw.text((LX+t1w,60), t2,  font=F["name"], fill=(96,165,250))
    for dx in [LX-20, LX+t1w+int(draw.textlength(t2,font=F["name"]))+8]:
        draw.polygon([(dx+6,72),(dx+12,66),(dx+18,72),(dx+12,78)], fill=(96,165,250,160))

def draw_divider(draw, LX=50, y=174):
    for xi in range(720):
        t = xi/720
        rc=int(37+(139-37)*t); gc=int(99+(92-99)*t); bc=int(235+(246-235)*t)
        al=int(220*(1-t**0.5))
        draw.point((LX+xi,y),   fill=(rc,gc,bc,al))
        draw.point((LX+xi,y+1), fill=(rc,gc,bc,al//2))

def draw_url(draw, LX=50):
    txt = ">>  tonybeal.net"
    uw = int(draw.textlength(txt, font=F["role"]))
    draw.rounded_rectangle([LX-6,H-40,LX+uw+14,H-6], radius=14,
                            fill=(6,15,45,220), outline=(96,165,250,180), width=2)
    draw.text((LX+3,H-38), txt, font=F["role"], fill=(96,165,250))

def save(canvas, name):
    out = os.path.join(ASSETS, name)
    canvas.convert("RGB").save(out, "PNG")
    print(f"Saved: {out}")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 1 — Intro: name + expertise bars + stat cards
# ─────────────────────────────────────────────────────────────────────────────
def slide1():
    canvas, draw = build_base()
    LX = 50
    accent_stripe(draw)

    # Available badge
    bx,by,bw,bh = LX,16,260,36
    draw.rounded_rectangle([bx-2,by-2,bx+bw+2,by+bh+2], radius=20, fill=None, outline=(52,211,153,50), width=3)
    draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=18, fill=(4,26,18,230), outline=(52,211,153,220), width=2)
    draw.ellipse([bx+12,by+12,bx+24,by+24], fill=(52,211,153))
    draw.text((bx+32,by+8), "AVAILABLE FOR CONSULTING", font=F["badge"], fill=(52,211,153))

    draw_name(draw, LX)
    draw_divider(draw, LX)

    # Expertise bars
    roles = [
        ("▲  Revenue Operations", (37,99,235),  93),
        (">> AI Sales Systems",   (99,102,241), 87),
        ("►  GTM Strategy",       (16,185,129), 97),
    ]
    for i,(label,col,pct) in enumerate(roles):
        oy = 182 + i*28
        draw.text((LX,oy), label, font=F["tag"], fill=(255,255,255))
        lw     = int(draw.textlength(label, font=F["tag"]))
        bstart = LX+lw+14; bend = bstart+250
        draw.rounded_rectangle([bstart,oy+5,bend,oy+17], radius=5, fill=(255,255,255,18))
        fill_x = bstart+int(250*pct/100)
        draw.rounded_rectangle([bstart,oy+5,fill_x,oy+17], radius=5, fill=(*col,210))
        draw.ellipse([fill_x-5,oy+4,fill_x+5,oy+18], fill=(255,255,255,180))
        draw.text((bend+10,oy+2), f"{pct}%", font=F["sm"], fill=col)

    # Stat cards
    stats = [("$20M+","PIPELINE",(245,158,11),82),("15+","YRS IN B2B",(99,102,241),94),
             ("11K+","FOLLOWERS",(52,211,153),88),("3.7K+","ACCOUNTS",(96,165,250),76)]
    sx,sy,cw,ch = LX,272,140,84
    for val,lbl,col,gauge in stats:
        draw.rounded_rectangle([sx+3,sy+3,sx+cw+3,sy+ch+3], radius=10, fill=(0,0,0,80))
        draw.rounded_rectangle([sx,sy,sx+cw,sy+ch], radius=10, fill=(6,10,30,200), outline=(*col,120), width=1)
        for xi in range(cw-4):
            t=xi/(cw-4)
            draw.line([(sx+2+xi,sy+1),(sx+2+xi,sy+5)],
                      fill=(int(col[0]*(0.6+0.4*t)),int(col[1]*(0.6+0.4*t)),int(col[2]*(0.6+0.4*t)),220))
        vw=int(draw.textlength(val,font=F["stat"]))
        draw.text((sx+(cw-vw)//2,sy+10), val, font=F["stat"], fill=(255,255,255))
        lw2=int(draw.textlength(lbl,font=F["stlbl"]))
        draw.text((sx+(cw-lw2)//2,sy+52), lbl, font=F["stlbl"], fill=col)
        gw=int((cw-16)*gauge/100)
        draw.rounded_rectangle([sx+8,sy+ch-12,sx+cw-8,sy+ch-4], radius=3, fill=(255,255,255,15))
        draw.rounded_rectangle([sx+8,sy+ch-12,sx+8+gw,sy+ch-4], radius=3, fill=(*col,180))
        sx += cw+10

    draw_url(draw, LX)
    edge_lines(draw)
    save(canvas, "linkedin-banner-v2.png")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 2 — Proof: big numbers with icon rings
# ─────────────────────────────────────────────────────────────────────────────
def slide2():
    canvas, draw = build_base(seed=13)
    LX = 50
    accent_stripe(draw)

    # Top label
    draw.text((LX,18), "THE NUMBERS DON'T LIE", font=F["badge"], fill=(245,158,11))
    draw_divider(draw, LX, y=46)

    # Big 4 stat tiles in 2x2 grid
    tiles = [
        ("$20M+",  "Pipeline Generated",  (245,158,11)),
        ("15+",    "Years in B2B Sales",  (99, 102,241)),
        ("11K+",   "LinkedIn Followers",  (52, 211,153)),
        ("3,700+", "Accounts Worked",     (96, 165,250)),
    ]
    cols2  = 2
    tw, th = 310, 136
    gap    = 18
    start_x = LX
    start_y = 60
    for i,(val,lbl,col) in enumerate(tiles):
        col_i = i % cols2; row_i = i // cols2
        tx = start_x + col_i*(tw+gap)
        ty = start_y + row_i*(th+gap)
        # Glow ring
        cx2 = tx + tw//2; cy2 = ty + th//2
        for rad in range(90,0,-5):
            t = rad/90; a = int(20*math.exp(-((1-t)*4)**1.2))
            draw.ellipse([cx2-rad,cy2-rad,cx2+rad,cy2+rad], fill=(*col,a))
        # Card
        draw.rounded_rectangle([tx+3,ty+3,tx+tw+3,ty+th+3], radius=14, fill=(0,0,0,100))
        draw.rounded_rectangle([tx,ty,tx+tw,ty+th], radius=14,
                                fill=(6,10,30,210), outline=(*col,160), width=2)
        # Left accent bar
        draw.rounded_rectangle([tx+1,ty+16,tx+5,ty+th-16], radius=3, fill=(*col,220))
        # Value
        vw = int(draw.textlength(val, font=F["h2"]))
        draw.text((tx+(tw-vw)//2, ty+16), val, font=F["h2"], fill=(255,255,255))
        # Label
        lw2 = int(draw.textlength(lbl, font=F["badge"]))
        draw.text((tx+(tw-lw2)//2, ty+80), lbl, font=F["badge"], fill=col)
        # Bottom gauge
        gw = int((tw-24)*0.8)
        draw.rounded_rectangle([tx+12,ty+th-16,tx+tw-12,ty+th-6], radius=4, fill=(255,255,255,12))
        draw.rounded_rectangle([tx+12,ty+th-16,tx+12+gw,ty+th-6], radius=4, fill=(*col,160))

    draw_url(draw, LX)
    edge_lines(draw)
    save(canvas, "linkedin-banner-slide2.png")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 3 — What I Build: 3 service pillars with icon circles
# ─────────────────────────────────────────────────────────────────────────────
def slide3():
    canvas, draw = build_base(seed=14)
    LX = 50
    accent_stripe(draw)

    draw.text((LX,18), "WHAT I BUILD FOR YOU", font=F["badge"], fill=(99,102,241))
    # underline
    uw = int(draw.textlength("WHAT I BUILD FOR YOU", font=F["badge"]))
    draw.line([(LX,38),(LX+uw,38)], fill=(99,102,241,180), width=2)

    pillars = [
        ("Revenue\nOperations",  "CRM  |  Pipeline\nProcess  |  Metrics", (37,99,235),  "01"),
        ("AI Sales\nSystems",    "Outreach  |  Scoring\nAutomation  |  AI Tools",(99,102,241),"02"),
        ("GTM\nStrategy",        "Positioning  |  ICP\nPlaybooks  |  Enablement",(16,185,129),"03"),
    ]
    pw2 = 200; ph2 = 290; gap2 = 20; sy2 = 52
    for i,(title,desc,col,num) in enumerate(pillars):
        tx2 = LX + i*(pw2+gap2)
        # Shadow
        draw.rounded_rectangle([tx2+3,sy2+3,tx2+pw2+3,sy2+ph2+3], radius=14, fill=(0,0,0,100))
        # Card
        draw.rounded_rectangle([tx2,sy2,tx2+pw2,sy2+ph2], radius=14,
                                fill=(6,10,30,210), outline=(*col,140), width=1)
        # Top stripe
        for xi2 in range(pw2-4):
            t = xi2/(pw2-4)
            rc=int(col[0]*(0.5+0.5*t)); gc=int(col[1]*(0.5+0.5*t)); bc=int(col[2]*(0.5+0.5*t))
            draw.line([(tx2+2+xi2,sy2+1),(tx2+2+xi2,sy2+6)], fill=(rc,gc,bc,230))
        # Number badge
        draw.ellipse([tx2+pw2-36,sy2+8,tx2+pw2-8,sy2+36], fill=(*col,50), outline=(*col,180), width=1)
        nw2 = int(draw.textlength(num, font=F["badge"]))
        draw.text((tx2+pw2-36+(28-nw2)//2, sy2+14), num, font=F["badge"], fill=col)
        # Icon circle
        cx3 = tx2+pw2//2; cy3 = sy2+70
        draw.ellipse([cx3-28,cy3-28,cx3+28,cy3+28], fill=(*col,30), outline=(*col,160), width=2)
        icon = ["$", "AI", ">>"][i]
        iw = int(draw.textlength(icon, font=F["h3"]))
        draw.text((cx3-iw//2, cy3-18), icon, font=F["h3"], fill=(255,255,255))
        # Title
        for li, line in enumerate(title.split("\n")):
            lw2 = int(draw.textlength(line, font=F["sm"]))
            draw.text((tx2+(pw2-lw2)//2, sy2+108+li*24), line, font=F["sm"], fill=(255,255,255))
        # Desc
        for li, line in enumerate(desc.split("\n")):
            lw2 = int(draw.textlength(line, font=F["stlbl"]))
            draw.text((tx2+(pw2-lw2)//2, sy2+168+li*18), line, font=F["stlbl"], fill=(*col,220))
        # Bottom glow line
        draw.line([(tx2+20,sy2+ph2-6),(tx2+pw2-20,sy2+ph2-6)], fill=(*col,100), width=2)

    draw_url(draw, LX)
    edge_lines(draw)
    save(canvas, "linkedin-banner-slide3.png")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 4 — Bold quote / manifesto with decorative frame
# ─────────────────────────────────────────────────────────────────────────────
def slide4():
    canvas, draw = build_base(seed=15)
    LX = 50
    accent_stripe(draw)

    # Decorative corner accent lines instead of quote mark
    for xi in range(40):
        draw.line([(LX+xi, 14),(LX+xi, 16)], fill=(96,165,250, int(120*(1-xi/40))))
    for yi in range(40):
        draw.line([(LX, 14+yi),(LX+2, 14+yi)], fill=(96,165,250, int(120*(1-yi/40))))

    lines = [
        "Revenue doesn't grow on its own.",
        "It's built — system by system,",
        "pipeline by pipeline.",
    ]
    line_cols = [(255,255,255),(255,255,255),(96,165,250)]
    for i,(line,col) in enumerate(zip(lines,line_cols)):
        draw.text((LX+2, 22+i*58+2), line, font=F["h3"], fill=(0,0,0,140))
        draw.text((LX,   22+i*58),   line, font=F["h3"], fill=col)

    # Accent rule
    draw.line([(LX,210),(LX+480,210)], fill=(96,165,250,160), width=2)

    # Attribution
    draw.text((LX, 222), "— Tony Beal  |  Revenue Architect  |  AI Sales Strategist",
              font=F["badge"], fill=(180,200,255))

    # Tag chips row
    tags = [("#RevOps",(37,99,235)),("#AI Sales",(99,102,241)),
            ("#GTM",(16,185,129)),("#B2B",(245,158,11))]
    tx3 = LX; ty3 = 260
    for tag,col in tags:
        tw3 = int(draw.textlength(tag, font=F["badge"]))
        draw.rounded_rectangle([tx3,ty3,tx3+tw3+20,ty3+30], radius=15,
                                fill=(*col,30), outline=(*col,200), width=1)
        draw.text((tx3+10,ty3+6), tag, font=F["badge"], fill=(255,255,255))
        tx3 += tw3+30

    draw_url(draw, LX)
    edge_lines(draw)
    save(canvas, "linkedin-banner-slide4.png")

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 5 — CTA: Book a call / Let's connect
# ─────────────────────────────────────────────────────────────────────────────
def slide5():
    canvas, draw = build_base(seed=16)
    LX = 50
    accent_stripe(draw)

    # Glowing CTA headline
    cta_lines = ["Ready to scale", "your revenue?"]
    for i,line in enumerate(cta_lines):
        lw2 = int(draw.textlength(line, font=F["big"]))
        draw.text((LX+3, 22+i*82+3), line, font=F["big"], fill=(0,0,0,160))
        draw.text((LX,   22+i*82),   line, font=F["big"],
                  fill=(255,255,255) if i==0 else (96,165,250))

    # Glow line
    draw.line([(LX,200),(LX+560,200)], fill=(245,158,11,180), width=3)

    # Sub-line
    draw.text((LX, 212), "Let's build something that actually drives results.", font=F["tag"],
              fill=(200,215,255))

    # Big CTA button
    bx5,by5,bw5,bh5 = LX,252,300,56
    # Outer glow
    for gi in range(8,0,-1):
        draw.rounded_rectangle([bx5-gi,by5-gi,bx5+bw5+gi,by5+bh5+gi], radius=30,
                                fill=(245,158,11, int(10*(8-gi+1))))
    draw.rounded_rectangle([bx5,by5,bx5+bw5,by5+bh5], radius=28,
                            fill=(245,158,11,230), outline=(255,200,50,255), width=2)
    btxt = ">> BOOK A CALL NOW"
    btw  = int(draw.textlength(btxt, font=F["h3"]))
    draw.text((bx5+(bw5-btw)//2, by5+12), btxt, font=F["h3"], fill=(0,0,0))

    # Secondary CTA
    stxt = "DM me on LinkedIn  |  tonybeal.net"
    draw.text((LX, by5+72), stxt, font=F["badge"], fill=(150,180,255))

    draw_url(draw, LX)
    edge_lines(draw)
    save(canvas, "linkedin-banner-slide5.png")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Building all 5 LinkedIn banner slides...")
    slide1()
    slide2()
    slide3()
    slide4()
    slide5()
    print("Done! All 5 slides saved to assets/")
