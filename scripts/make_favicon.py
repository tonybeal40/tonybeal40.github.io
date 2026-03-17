from PIL import Image, ImageDraw, ImageFont

sizes = [16, 32, 48]
frames = []

for sz in sizes:
    img = Image.new("RGBA", (sz, sz), (0,0,0,0))
    d = ImageDraw.Draw(img)
    pad = max(1, sz//16)
    d.rounded_rectangle([0,0,sz-1,sz-1], radius=max(2,sz//8), fill=(4,6,26,255))
    d.rounded_rectangle([pad,pad,sz-1-pad,sz-1-pad], radius=max(1,sz//10), fill=None, outline=(37,99,235,255), width=max(1,sz//16))
    try:
        fnt = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", int(sz*0.65))
    except:
        fnt = ImageFont.load_default()
    tw = int(d.textlength("T", font=fnt))
    d.text(((sz-tw)//2, int(sz*0.08)), "T", font=fnt, fill=(255,255,255,255))
    frames.append(img)

out = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site\favicon.ico"
frames[0].save(out, format="ICO", sizes=[(16,16),(32,32),(48,48)], append_images=frames[1:])
print(f"Saved {out}")
