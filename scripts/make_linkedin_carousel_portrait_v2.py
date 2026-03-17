from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os, random, math

W, H = 1080, 1350
BASE = r"C:\Users\tonyb\.openclaw\workspace\tonybeal-site"
PHOTO = os.path.join(BASE, "headshot-new.png")
ASSETS = os.path.join(BASE, "assets", "linkedin-carousel-v2")
OUT = os.path.join(BASE, "..", "outputs", "linkedin-banners")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def ft(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

F = {
    "kicker": ft("arialbd.ttf", 34),
    "title": ft("ariblk.ttf", 92),
    "title2": ft("ariblk.ttf", 72),
    "body": ft("arial.ttf", 40),
    "body_b": ft("arialbd.ttf", 40),
    "small": ft("arial.ttf", 28),
    "cta": ft("arialbd.ttf", 42),
}


def bg(seed=1):
    random.seed(seed)
    img = Image.new("RGBA", (W, H), (8, 12, 28, 255))
    d = ImageDraw.Draw(img)

    # Vertical gradient
    for y in range(H):
        t = y / H
        r = int(8 + 20 * t)
        g = int(12 + 12 * t)
        b = int(28 + 22 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Cinematic glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    orbs = [
        (140, 210, 360, (255, 90, 30), 52),
        (930, 190, 420, (80, 130, 255), 44),
        (760, 980, 520, (40, 95, 240), 36),
    ]
    for cx, cy, R, c, strength in orbs:
        for r in range(R, 0, -8):
            t = r / R
            a = int(strength * math.exp(-((1 - t) * 3.2) ** 1.5))
            gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*c, a))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, glow)

    # Vignette
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    cx, cy = W // 2, H // 2
    maxr = int((W * W + H * H) ** 0.5 / 2)
    for r in range(maxr, 0, -14):
        t = 1 - (r / maxr)
        a = int(150 * (t ** 1.7))
        vd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 0, 0, a), width=20)
    img = Image.alpha_composite(img, vig)

    # Grain
    gr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grd = ImageDraw.Draw(gr)
    for _ in range(13000):
        x, y = random.randint(0, W - 1), random.randint(0, H - 1)
        v = random.randint(130, 255)
        grd.point((x, y), fill=(v, v, v, random.randint(6, 20)))
    gr = gr.filter(ImageFilter.GaussianBlur(0.35))
    img = Image.alpha_composite(img, gr)

    # Letterbox bars
    bd = ImageDraw.Draw(img)
    bd.rectangle([0, 0, W, 56], fill=(0, 0, 0, 225))
    bd.rectangle([0, H - 70, W, H], fill=(0, 0, 0, 235))

    return img


def add_header(draw, ep, subtitle):
    top = f"TONY BEAL // REVENUE SYSTEMS // EP {ep}"
    tw = int(draw.textlength(top, font=F["small"]))
    draw.text(((W - tw) // 2, 14), top, font=F["small"], fill=(220, 220, 220, 235))
    sw = int(draw.textlength(subtitle, font=F["small"]))
    draw.text(((W - sw) // 2, H - 56), subtitle, font=F["small"], fill=(245, 245, 245, 245))


def add_headshot(img):
    p = Image.open(PHOTO).convert("RGB")
    p = ImageEnhance.Contrast(ImageEnhance.Brightness(p).enhance(0.90)).enhance(1.15)

    R = 240
    diam = R * 2
    scale = diam / min(p.size)
    p = p.resize((int(p.size[0] * scale), int(p.size[1] * scale)), Image.LANCZOS)
    x0 = (p.size[0] - diam) // 2
    y0 = (p.size[1] - diam) // 2
    p = p.crop((x0, y0, x0 + diam, y0 + diam)).convert("RGBA")

    mask = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diam, diam], fill=255)
    p.putalpha(mask)

    # glow under photo
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = 760, 610
    for r in range(R + 70, R, -6):
        t = (r - R) / 70
        a = int(42 * math.exp(-t * 2.8))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 130, 255, a))
    img = Image.alpha_composite(img, layer)

    img.paste(p, (cx - R, cy - R), p)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - R - 4, cy - R - 4, cx + R + 4, cy + R + 4], outline=(110, 170, 255, 220), width=4)
    return img


def card(draw, x, y, w, h, title, body):
    draw.rounded_rectangle([x + 4, y + 4, x + w + 4, y + h + 4], radius=22, fill=(0, 0, 0, 120))
    draw.rounded_rectangle([x, y, x + w, y + h], radius=22, fill=(8, 14, 38, 205), outline=(110, 170, 255, 140), width=2)
    draw.text((x + 28, y + 24), title, font=F["body_b"], fill=(255, 255, 255))
    draw.text((x + 28, y + 84), body, font=F["small"], fill=(210, 220, 245))


def slide1():
    img = add_headshot(bg(21))
    d = ImageDraw.Draw(img)
    add_header(d, "01", "Pilot Episode")
    d.text((90, 180), "TONY", font=F["title"], fill=(255, 255, 255))
    d.text((90, 280), "BEAL", font=F["title"], fill=(120, 180, 255))
    d.text((90, 400), "Revenue Ops + AI Sales Systems", font=F["body"], fill=(232, 240, 255))
    d.text((90, 455), "Built to drive pipeline, not noise.", font=F["small"], fill=(200, 215, 245))
    card(d, 90, 820, 900, 210, "$20M+ Pipeline", "15+ years B2B • 11K+ audience • 3,700+ accounts")
    return img


def slide2():
    img = bg(22)
    d = ImageDraw.Draw(img)
    add_header(d, "02", "The Numbers")
    d.text((90, 160), "THE NUMBERS", font=F["title2"], fill=(255, 255, 255))
    d.text((90, 245), "DON'T LIE", font=F["title2"], fill=(255, 170, 90))
    metrics = [
        ("$20M+", "Pipeline Generated"),
        ("15+", "Years in B2B Sales"),
        ("11K+", "LinkedIn Followers"),
        ("3,700+", "Accounts Worked"),
    ]
    y = 420
    for v, l in metrics:
        card(d, 90, y, 900, 180, v, l)
        y += 200
    return img


def slide3():
    img = bg(23)
    d = ImageDraw.Draw(img)
    add_header(d, "03", "What I Build")
    d.text((90, 170), "WHAT I BUILD", font=F["title2"], fill=(255, 255, 255))
    d.text((90, 250), "FOR TEAMS", font=F["title2"], fill=(130, 180, 255))
    card(d, 90, 430, 900, 210, "Revenue Operations", "CRM architecture • forecast accuracy • funnel visibility")
    card(d, 90, 670, 900, 210, "AI Sales Systems", "outbound automation • scoring • signal-driven follow-up")
    card(d, 90, 910, 900, 210, "GTM Strategy", "ICP refinement • messaging • execution playbooks")
    return img


def slide4():
    img = add_headshot(bg(24))
    d = ImageDraw.Draw(img)
    add_header(d, "04", "Manifesto")
    d.text((90, 180), "REVENUE GROWTH", font=F["title2"], fill=(255, 255, 255))
    d.text((90, 260), "IS DESIGNED.", font=F["title2"], fill=(125, 178, 255))
    d.text((90, 375), "System by system.", font=F["body"], fill=(225, 235, 255))
    d.text((90, 430), "Pipeline by pipeline.", font=F["body"], fill=(225, 235, 255))
    card(d, 90, 860, 900, 230, "Tony Beal", "Revenue Architect • AI Sales Strategist • RevOps Operator")
    return img


def slide5():
    img = bg(25)
    d = ImageDraw.Draw(img)
    add_header(d, "05", "Final CTA")
    d.text((90, 180), "READY TO SCALE", font=F["title2"], fill=(255, 255, 255))
    d.text((90, 260), "PIPELINE?", font=F["title2"], fill=(255, 170, 90))
    card(d, 90, 470, 900, 210, "Let's Build", "Revenue systems that actually convert")

    # CTA button
    x, y, w, h = 190, 770, 700, 120
    d.rounded_rectangle([x - 4, y - 4, x + w + 4, y + h + 4], radius=60, fill=(0, 0, 0, 120))
    d.rounded_rectangle([x, y, x + w, y + h], radius=60, fill=(255, 150, 40, 232), outline=(255, 215, 130, 255), width=3)
    txt = "BOOK A CALL"
    tw = int(d.textlength(txt, font=F["cta"]))
    d.text((x + (w - tw) // 2, y + 34), txt, font=F["cta"], fill=(20, 20, 20))

    d.text((270, 940), "linkedin.com/in/tonybeal", font=F["body"], fill=(220, 232, 255))
    d.text((390, 998), "tonybeal.net", font=F["body"], fill=(130, 180, 255))
    return img


def main():
    slides = [slide1(), slide2(), slide3(), slide4(), slide5()]
    names = [
        "linkedin-carousel-v2-slide1.png",
        "linkedin-carousel-v2-slide2.png",
        "linkedin-carousel-v2-slide3.png",
        "linkedin-carousel-v2-slide4.png",
        "linkedin-carousel-v2-slide5.png",
    ]

    saved = []
    for im, n in zip(slides, names):
        p1 = os.path.join(ASSETS, n)
        p2 = os.path.join(OUT, n)
        im.convert("RGB").save(p1, "PNG")
        im.convert("RGB").save(p2, "PNG")
        saved.append(p2)
        print("Saved", p2)

    pdf = os.path.join(OUT, "linkedin-netflix-carousel-v2-1080x1350.pdf")
    imgs = [Image.open(p).convert("RGB") for p in saved]
    imgs[0].save(pdf, "PDF", save_all=True, append_images=imgs[1:], resolution=150.0)
    print("Saved", pdf)


if __name__ == "__main__":
    main()
