from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

W, H = 1080, 1350
BASE = r"C:\Users\tonyb\.openclaw\workspace\tonybeal-site"
PHOTO = os.path.join(BASE, "headshot-new.png")
ASSETS = os.path.join(BASE, "assets", "linkedin-carousel-v3-exec")
OUT = os.path.join(BASE, "..", "outputs", "linkedin-banners")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def ft(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

F = {
    "eyebrow": ft("arialbd.ttf", 26),
    "h1": ft("ariblk.ttf", 86),
    "h2": ft("ariblk.ttf", 70),
    "body": ft("arial.ttf", 36),
    "body_b": ft("arialbd.ttf", 36),
    "small": ft("arial.ttf", 28),
    "cta": ft("arialbd.ttf", 40),
}

PALETTE = {
    "bg_top": (10, 16, 30),
    "bg_bottom": (18, 30, 52),
    "panel": (255, 255, 255, 14),
    "panel_border": (150, 182, 230, 90),
    "text": (245, 248, 255),
    "muted": (194, 210, 236),
    "accent": (129, 178, 255),
    "accent2": (97, 226, 196),
    "cta": (122, 170, 255),
}


def clean_bg():
    img = Image.new("RGBA", (W, H), PALETTE["bg_top"] + (255,))
    d = ImageDraw.Draw(img)

    for y in range(H):
        t = y / (H - 1)
        r = int(PALETTE["bg_top"][0] * (1 - t) + PALETTE["bg_bottom"][0] * t)
        g = int(PALETTE["bg_top"][1] * (1 - t) + PALETTE["bg_bottom"][1] * t)
        b = int(PALETTE["bg_top"][2] * (1 - t) + PALETTE["bg_bottom"][2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # subtle top/bottom bands
    d.rectangle([0, 0, W, 74], fill=(0, 0, 0, 90))
    d.rectangle([0, H - 88, W, H], fill=(0, 0, 0, 110))

    # restrained accent line
    d.rectangle([80, 118, 380, 124], fill=PALETTE["accent"] + (220,))
    return img


def add_photo(img):
    p = Image.open(PHOTO).convert("RGB")
    p = ImageEnhance.Brightness(p).enhance(0.96)
    p = ImageEnhance.Contrast(p).enhance(1.08)

    target_w, target_h = 430, 560
    scale = max(target_w / p.size[0], target_h / p.size[1])
    p = p.resize((int(p.size[0] * scale), int(p.size[1] * scale)), Image.LANCZOS)
    x0 = (p.size[0] - target_w) // 2
    y0 = (p.size[1] - target_h) // 2
    p = p.crop((x0, y0, x0 + target_w, y0 + target_h))

    # rounded mask
    mask = Image.new("L", (target_w, target_h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, target_w, target_h], radius=38, fill=255)

    p = p.convert("RGBA")
    p.putalpha(mask)

    px, py = 620, 220
    # shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([px + 6, py + 10, px + target_w + 6, py + target_h + 10], radius=38, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, sh)
    img.paste(p, (px, py), p)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px - 2, py - 2, px + target_w + 2, py + target_h + 2], radius=40, outline=PALETTE["accent"] + (170,), width=2)
    return img


def header(d, title):
    d.text((82, 24), "TONY BEAL  •  REVOPS / AI SALES SYSTEMS", font=F["eyebrow"], fill=PALETTE["muted"])
    tw = int(d.textlength(title, font=F["small"]))
    d.text((W - tw - 82, H - 66), title, font=F["small"], fill=PALETTE["muted"])


def panel(d, x, y, w, h, title, body):
    d.rounded_rectangle([x, y, x + w, y + h], radius=26, fill=PALETTE["panel"], outline=PALETTE["panel_border"], width=2)
    d.text((x + 26, y + 22), title, font=F["body_b"], fill=PALETTE["text"])
    d.text((x + 26, y + 78), body, font=F["small"], fill=PALETTE["muted"])


def slide1():
    img = add_photo(clean_bg())
    d = ImageDraw.Draw(img)
    header(d, "Executive Brief — 01")
    d.text((82, 165), "Revenue Systems", font=F["h2"], fill=PALETTE["text"])
    d.text((82, 246), "Operator", font=F["h2"], fill=PALETTE["accent"])
    d.text((82, 352), "I build predictable pipeline engines for B2B teams.", font=F["body"], fill=PALETTE["muted"])
    panel(d, 82, 820, 916, 210, "$20M+ pipeline generated", "15+ years in B2B • RevOps + AI execution")
    return img


def slide2():
    img = clean_bg()
    d = ImageDraw.Draw(img)
    header(d, "Executive Brief — 02")
    d.text((82, 165), "The Results", font=F["h1"], fill=PALETTE["text"])
    panel(d, 82, 340, 916, 176, "$20M+", "Pipeline created across complex B2B cycles")
    panel(d, 82, 548, 916, 176, "15+ years", "Sales, BD, RevOps leadership")
    panel(d, 82, 756, 916, 176, "11K+ audience", "Market-facing authority and demand signal")
    panel(d, 82, 964, 916, 176, "3,700+ accounts", "Hands-on GTM and account motion exposure")
    return img


def slide3():
    img = clean_bg()
    d = ImageDraw.Draw(img)
    header(d, "Executive Brief — 03")
    d.text((82, 165), "What I Build", font=F["h1"], fill=PALETTE["text"])
    panel(d, 82, 360, 916, 190, "Revenue Operations", "Forecast rigor • funnel architecture • KPI visibility")
    panel(d, 82, 582, 916, 190, "AI Sales Systems", "Prospecting workflows • lead scoring • follow-up automation")
    panel(d, 82, 804, 916, 190, "GTM Execution", "ICP precision • messaging • pipeline acceleration")
    return img


def slide4():
    img = add_photo(clean_bg())
    d = ImageDraw.Draw(img)
    header(d, "Executive Brief — 04")
    d.text((82, 165), "Growth is", font=F["h1"], fill=PALETTE["text"])
    d.text((82, 260), "engineered.", font=F["h1"], fill=PALETTE["accent"])
    d.text((82, 380), "System by system. Pipeline by pipeline.", font=F["body"], fill=PALETTE["muted"])
    panel(d, 82, 840, 916, 190, "Tony Beal", "Revenue Architect • RevOps Leader • AI-enabled GTM")
    return img


def slide5():
    img = clean_bg()
    d = ImageDraw.Draw(img)
    header(d, "Executive Brief — 05")
    d.text((82, 165), "Open to", font=F["h1"], fill=PALETTE["text"])
    d.text((82, 260), "the right role.", font=F["h1"], fill=PALETTE["accent"])
    panel(d, 82, 430, 916, 200, "Target roles", "RevOps Manager/Director • Sales Ops • GTM Systems")

    x, y, w, h = 220, 760, 640, 116
    d.rounded_rectangle([x, y, x + w, y + h], radius=58, fill=PALETTE["cta"] + (230,), outline=(195, 218, 255, 255), width=3)
    txt = "LET'S CONNECT"
    tw = int(d.textlength(txt, font=F["cta"]))
    d.text((x + (w - tw) // 2, y + 34), txt, font=F["cta"], fill=(20, 26, 40))

    d.text((280, 930), "linkedin.com/in/tonybeal", font=F["body"], fill=PALETTE["text"])
    d.text((392, 985), "tonybeal.net", font=F["body"], fill=PALETTE["accent"])
    return img


def main():
    slides = [slide1(), slide2(), slide3(), slide4(), slide5()]
    names = [
        "linkedin-carousel-v3-exec-slide1.png",
        "linkedin-carousel-v3-exec-slide2.png",
        "linkedin-carousel-v3-exec-slide3.png",
        "linkedin-carousel-v3-exec-slide4.png",
        "linkedin-carousel-v3-exec-slide5.png",
    ]

    out_paths = []
    for img, n in zip(slides, names):
        p1 = os.path.join(ASSETS, n)
        p2 = os.path.join(OUT, n)
        img.convert("RGB").save(p1, "PNG")
        img.convert("RGB").save(p2, "PNG")
        out_paths.append(p2)
        print("Saved", p2)

    pdf = os.path.join(OUT, "linkedin-carousel-v3-executive-1080x1350.pdf")
    pages = [Image.open(p).convert("RGB") for p in out_paths]
    pages[0].save(pdf, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
    print("Saved", pdf)


if __name__ == "__main__":
    main()
