from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1584, 396
OUT = r"C:\Users\tonyb\.openclaw\workspace\outputs\linkedin-banners-v7"
ASSETS = r"C:\Users\tonyb\.openclaw\workspace\tonybeal-site\assets\linkedin-banners-v7"
os.makedirs(OUT, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)


def f(name, size):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except:
        return ImageFont.load_default()

FONT_H = f("ariblk.ttf", 58)
FONT_S = f("arial.ttf", 26)
FONT_T = f("arialbd.ttf", 20)
FONT_B = f("arialbd.ttf", 24)


def gradient(c1, c2):
    img = Image.new("RGB", (W, H), c1)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def draw_common(d, accent, textc, muted, label):
    d.rectangle([0, 0, W, 44], fill=(0, 0, 0, 45))
    d.rectangle([0, H - 42, W, H], fill=(0, 0, 0, 65))
    d.text((72, 12), "TONY BEAL  •  REVOPS / AI SALES SYSTEMS", font=FONT_T, fill=muted)
    d.line([(72, 70), (270, 70)], fill=accent, width=4)
    tw = int(d.textlength(label, font=FONT_T))
    d.text((W - tw - 72, H - 31), label, font=FONT_T, fill=muted)


def banner_corporate():
    img = gradient((11, 27, 51), (24, 53, 94))
    d = ImageDraw.Draw(img)
    text = (246, 249, 255)
    muted = (190, 211, 240)
    accent = (125, 173, 255)
    draw_common(d, accent, text, muted, "Corporate")

    # safe zone content starts at x=460
    x = 500
    d.text((x, 90), "Revenue Operations", font=FONT_H, fill=text)
    d.text((x, 156), "& AI Sales Systems", font=FONT_H, fill=accent)
    d.text((x, 234), "Predictable B2B pipeline performance.", font=FONT_S, fill=muted)
    d.rounded_rectangle([x, 282, x + 460, 344], radius=16, outline=(145, 180, 232), width=2, fill=(255, 255, 255, 16))
    d.text((x + 18, 301), "$20M+ Pipeline Generated", font=FONT_B, fill=text)
    return img


def banner_luxury():
    img = gradient((14, 16, 23), (29, 35, 49))
    d = ImageDraw.Draw(img)
    text = (248, 246, 242)
    muted = (216, 209, 195)
    accent = (201, 169, 106)
    draw_common(d, accent, text, muted, "Luxury")

    x = 500
    d.text((x, 96), "Tony Beal", font=FONT_H, fill=text)
    d.text((x, 168), "Revenue Architecture", font=FONT_H, fill=accent)
    d.text((x, 238), "for High-Performance GTM Teams", font=FONT_S, fill=muted)
    d.rounded_rectangle([x, 284, x + 420, 344], radius=16, outline=(190, 158, 96), width=2, fill=(255, 255, 255, 10))
    d.text((x + 18, 302), "$20M+ Pipeline Impact", font=FONT_B, fill=text)
    return img


def banner_bold():
    img = gradient((10, 16, 32), (26, 48, 93))
    d = ImageDraw.Draw(img)
    text = (246, 250, 255)
    muted = (184, 210, 245)
    accent = (94, 213, 255)
    draw_common(d, accent, text, muted, "Bold")

    x = 500
    d.text((x, 92), "Build Pipeline", font=FONT_H, fill=text)
    d.text((x, 160), "That Actually Converts", font=FONT_H, fill=accent)
    d.text((x, 236), "RevOps + AI execution with measurable outcomes.", font=FONT_S, fill=muted)
    d.rounded_rectangle([x, 284, x + 450, 344], radius=16, outline=(110, 206, 237), width=2, fill=(255, 255, 255, 12))
    d.text((x + 18, 302), "15+ Years  •  $20M+ Pipeline", font=FONT_B, fill=text)
    return img


def save(im, name):
    p1 = os.path.join(OUT, name)
    p2 = os.path.join(ASSETS, name)
    im.save(p1, "PNG")
    im.save(p2, "PNG")
    print("Saved", p1)


def main():
    corp = banner_corporate()
    lux = banner_luxury()
    bold = banner_bold()

    save(corp, "linkedin-banner-v7-corporate.png")
    save(lux, "linkedin-banner-v7-luxury.png")
    save(bold, "linkedin-banner-v7-bold.png")

    # recommended final
    save(corp, "linkedin-banner-v7-recommended-final.png")


if __name__ == "__main__":
    main()
