from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

W, H = 1584, 396
BASE = r"C:\Users\tonyb\.openclaw\workspace\tonybeal-site"
PHOTO = os.path.join(BASE, "headshot-new.png")
ASSETS = os.path.join(BASE, "assets", "linkedin-banners-v6-exec")
OUT = os.path.join(BASE, "..", "outputs", "linkedin-banners")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def ft(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

F = {
    "eyebrow": ft("arialbd.ttf", 20),
    "h1": ft("ariblk.ttf", 66),
    "h2": ft("ariblk.ttf", 52),
    "body": ft("arial.ttf", 30),
    "small": ft("arial.ttf", 22),
    "label": ft("arialbd.ttf", 18),
}

PAL = {
    "top": (10, 16, 30),
    "bot": (19, 32, 55),
    "text": (246, 248, 255),
    "muted": (188, 206, 234),
    "accent": (125, 176, 255),
    "panel": (255, 255, 255, 16),
    "border": (145, 180, 232, 90),
}


def bg():
    img = Image.new("RGBA", (W, H), PAL["top"] + (255,))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        r = int(PAL["top"][0] * (1 - t) + PAL["bot"][0] * t)
        g = int(PAL["top"][1] * (1 - t) + PAL["bot"][1] * t)
        b = int(PAL["top"][2] * (1 - t) + PAL["bot"][2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))
    d.rectangle([0, 0, W, 42], fill=(0, 0, 0, 90))
    d.rectangle([0, H - 44, W, H], fill=(0, 0, 0, 110))
    d.rectangle([72, 66, 310, 70], fill=PAL["accent"] + (255,))
    return img


def add_photo(img):
    p = Image.open(PHOTO).convert("RGB")
    p = ImageEnhance.Brightness(p).enhance(0.96)
    p = ImageEnhance.Contrast(p).enhance(1.08)

    tw, th = 300, 330
    scale = max(tw / p.size[0], th / p.size[1])
    p = p.resize((int(p.size[0] * scale), int(p.size[1] * scale)), Image.LANCZOS)
    x0 = (p.size[0] - tw) // 2
    y0 = (p.size[1] - th) // 2
    p = p.crop((x0, y0, x0 + tw, y0 + th)).convert("RGBA")

    mask = Image.new("L", (tw, th), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, tw, th], radius=32, fill=255)
    p.putalpha(mask)

    px, py = 1220, 34
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([px + 6, py + 8, px + tw + 6, py + th + 8], radius=32, fill=(0, 0, 0, 100))
    img = Image.alpha_composite(img, sh)
    img.paste(p, (px, py), p)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px - 2, py - 2, px + tw + 2, py + th + 2], radius=34, outline=PAL["accent"] + (180,), width=2)
    return img


def header(d, tag):
    d.text((72, 12), "TONY BEAL  •  REVOPS / AI SALES SYSTEMS", font=F["label"], fill=PAL["muted"])
    tw = int(d.textlength(tag, font=F["label"]))
    d.text((W - tw - 72, H - 30), tag, font=F["label"], fill=PAL["muted"])


def panel(d, x, y, w, h, title, sub):
    d.rounded_rectangle([x, y, x + w, y + h], radius=20, fill=PAL["panel"], outline=PAL["border"], width=2)
    d.text((x + 18, y + 12), title, font=F["body"], fill=PAL["text"])
    d.text((x + 18, y + 48), sub, font=F["small"], fill=PAL["muted"])


def s1():
    img = add_photo(bg())
    d = ImageDraw.Draw(img)
    header(d, "Executive Banner 01")
    d.text((72, 88), "Revenue Systems", font=F["h2"], fill=PAL["text"])
    d.text((72, 144), "Operator", font=F["h2"], fill=PAL["accent"])
    d.text((72, 210), "I build predictable B2B pipeline engines.", font=F["body"], fill=PAL["muted"])
    panel(d, 72, 256, 1030, 96, "$20M+ pipeline generated", "15+ years in sales, BD, RevOps execution")
    return img


def s2():
    img = bg()
    d = ImageDraw.Draw(img)
    header(d, "Executive Banner 02")
    d.text((72, 88), "The Results", font=F["h1"], fill=PAL["text"])
    panel(d, 72, 178, 470, 84, "$20M+", "Pipeline generated")
    panel(d, 560, 178, 470, 84, "15+ years", "B2B experience")
    panel(d, 72, 272, 470, 84, "11K+", "LinkedIn audience")
    panel(d, 560, 272, 470, 84, "3,700+", "Accounts engaged")
    return img


def s3():
    img = bg()
    d = ImageDraw.Draw(img)
    header(d, "Executive Banner 03")
    d.text((72, 88), "What I Build", font=F["h1"], fill=PAL["text"])
    panel(d, 72, 180, 960, 78, "Revenue Operations", "Forecast rigor • funnel architecture • KPI visibility")
    panel(d, 72, 266, 960, 78, "AI Sales Systems", "Scoring, automation, and follow-up workflows")
    return img


def s4():
    img = add_photo(bg())
    d = ImageDraw.Draw(img)
    header(d, "Executive Banner 04")
    d.text((72, 88), "Growth is", font=F["h1"], fill=PAL["text"])
    d.text((72, 160), "engineered.", font=F["h1"], fill=PAL["accent"])
    d.text((72, 238), "System by system. Pipeline by pipeline.", font=F["body"], fill=PAL["muted"])
    panel(d, 72, 278, 1030, 74, "Tony Beal", "Revenue Architect • RevOps Leader • AI-enabled GTM")
    return img


def s5():
    img = bg()
    d = ImageDraw.Draw(img)
    header(d, "Executive Banner 05")
    d.text((72, 88), "Open to the", font=F["h1"], fill=PAL["text"])
    d.text((72, 160), "right role.", font=F["h1"], fill=PAL["accent"])
    panel(d, 72, 250, 820, 96, "RevOps / Sales Ops / GTM Systems", "Remote or hybrid • outcome-focused leadership")
    d.text((72, 356), "linkedin.com/in/tonybeal  •  tonybeal.net", font=F["body"], fill=PAL["text"])
    return img


def main():
    slides = [s1(), s2(), s3(), s4(), s5()]
    names = [
        "linkedin-banner-v6-exec-slide1.png",
        "linkedin-banner-v6-exec-slide2.png",
        "linkedin-banner-v6-exec-slide3.png",
        "linkedin-banner-v6-exec-slide4.png",
        "linkedin-banner-v6-exec-slide5.png",
    ]
    for im, n in zip(slides, names):
        p1 = os.path.join(ASSETS, n)
        p2 = os.path.join(OUT, n)
        im.convert("RGB").save(p1, "PNG")
        im.convert("RGB").save(p2, "PNG")
        print("Saved", p2)


if __name__ == "__main__":
    main()
