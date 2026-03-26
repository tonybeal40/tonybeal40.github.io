from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1584, 396
img = Image.new('RGB', (W, H), '#050C1A')
d = ImageDraw.Draw(img)

# Deep gradient background
for y in range(H):
    t = y / H
    d.line([(0,y),(W,y)], fill=(int(5+t*8), int(10+t*12), int(24+t*18)))

# Grid lines
for x in range(0, W, 54): d.line([(x,0),(x,H)], fill=(13,21,38))
for y in range(0, H, 54): d.line([(0,y),(W,y)], fill=(13,21,38))

# Blue glow right side
glow = Image.new('RGBA', (800,800), (0,0,0,0))
gd = ImageDraw.Draw(glow)
for r in range(400, 0, -1):
    a = int(55*(1-r/400))
    gd.ellipse([400-r,400-r,400+r,400+r], fill=(59,130,246,a))
glow = glow.filter(ImageFilter.GaussianBlur(35))
img.paste(glow, (1000, -200), glow)

# Left accent bar gradient
for y in range(H):
    t = y / H
    a = int(255 * 4 * t * (1-t))
    d.line([(40,y),(43,y)], fill=(int(59*a/255), int(130*a/255), int(246*a/255)))

def fnt(size, bold=False):
    for f in ([r'C:\Windows\Fonts\arialbd.ttf', r'C:\Windows\Fonts\calibrib.ttf'] if bold
              else [r'C:\Windows\Fonts\arial.ttf', r'C:\Windows\Fonts\calibri.ttf']):
        if os.path.exists(f):
            try: return ImageFont.truetype(f, size)
            except: pass
    return ImageFont.load_default()

# Safe zone: profile pic covers bottom-left ~0-250px
# Content: x=260 to x=1544 (40px right margin)
SAFE_L = 260
SAFE_R = W - 40  # 1544

# TOP ROW: pill left, keywords right
TOP = 28
pill_f = fnt(12, bold=True)
d.rounded_rectangle([SAFE_L, TOP, SAFE_L+186, TOP+26], radius=13, fill=(6,78,59), outline=(16,185,129))
d.ellipse([SAFE_L+11, TOP+9, SAFE_L+19, TOP+17], fill='#10B981')
d.text((SAFE_L+25, TOP+6), 'AVAILABLE NOW', font=pill_f, fill='#10B981')

kw_f = fnt(13, bold=True)
kw = 'REVENUE OPERATIONS  \u00b7  AI SALES SYSTEMS  \u00b7  GTM STRATEGY'
kw_w = int(d.textlength(kw, font=kw_f))
d.text((SAFE_R - kw_w, TOP+6), kw, font=kw_f, fill='#3B82F6')

# NAME large, right-aligned
name_f = fnt(108, bold=True)
name_w = int(d.textlength('Tony Beal', font=name_f))
NY = 50
d.text((SAFE_R - name_w, NY), 'Tony Beal', font=name_f, fill='#F8FAFC')

# SUBTITLE right-aligned
sub_f = fnt(19)
sub = 'AI-driven revenue systems that generate pipeline for B2B companies'
sub_w = int(d.textlength(sub, font=sub_f))
SY = NY + 112 + 6
d.text((SAFE_R - sub_w, SY), sub, font=sub_f, fill='#94A3B8')

# STAT BOXES bottom-right
stats = [('$20M+','PIPELINE'), ('15+','YRS B2B'), ('11K+','FOLLOWERS'), ('3,700+','ACCOUNTS')]
BOX_W  = 120
BOX_H  = 56
BOX_GAP = 10
stat_f = fnt(26, bold=True)
lbl_f  = fnt(11, bold=True)
total_w = len(stats)*BOX_W + (len(stats)-1)*BOX_GAP
SX = SAFE_R - total_w
BY = SY + 26 + 10

for i, (num, label) in enumerate(stats):
    bx = SX + i*(BOX_W + BOX_GAP)
    is_green = (num == '11K+')
    d.rounded_rectangle([bx, BY, bx+BOX_W, BY+BOX_H], radius=8,
                         fill=(8,16,34), outline=(16,185,129) if is_green else (30,58,95))
    nw = int(d.textlength(num, font=stat_f))
    d.text((bx+(BOX_W-nw)//2, BY+5),  num,   font=stat_f, fill='#10B981' if is_green else '#3B82F6')
    lw = int(d.textlength(label, font=lbl_f))
    d.text((bx+(BOX_W-lw)//2, BY+34), label, font=lbl_f, fill='#475569')

# Border lines
d.rectangle([0, 0, W, 2], fill='#1E3A5F')
d.rectangle([0, H-2, W, H], fill='#1E3A5F')

# Watermark
d.text((SAFE_L, H-20), 'tonybeal.net', font=fnt(12, bold=True), fill='#1E2D45')

out = r'C:\Users\tonyb\tonybeal.net\assets\linkedin-banner.png'
img.save(out, 'PNG', optimize=True)
print('Saved:', out)
