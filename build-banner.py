from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1584, 396
img = Image.new('RGB', (W, H), '#050C1A')
d = ImageDraw.Draw(img)

for y in range(H):
    t = y/H
    d.line([(0,y),(W,y)], fill=(int(5+t*10), int(10+t*12), int(26+t*20)))
for x in range(0,W,54): d.line([(x,0),(x,H)], fill=(14,22,40))
for y in range(0,H,54): d.line([(0,y),(W,y)], fill=(14,22,40))

glow = Image.new('RGBA',(900,900),(0,0,0,0))
gd = ImageDraw.Draw(glow)
for r in range(450,0,-1):
    a = int(60*(1-r/450))
    gd.ellipse([450-r,450-r,450+r,450+r], fill=(59,130,246,a))
glow = glow.filter(ImageFilter.GaussianBlur(40))
img.paste(glow,(950,-250),glow)

for y in range(H):
    t = y/H
    a = int(255*4*t*(1-t))
    d.line([(42,y),(45,y)], fill=(int(59*a/255), int(130*a/255), int(246*a/255)))

def fnt(size, bold=False):
    for f in ([r'C:\Windows\Fonts\arialbd.ttf', r'C:\Windows\Fonts\calibrib.ttf'] if bold else [r'C:\Windows\Fonts\arial.ttf', r'C:\Windows\Fonts\calibri.ttf']):
        if os.path.exists(f):
            try: return ImageFont.truetype(f, size)
            except: pass
    return ImageFont.load_default()

CX = 268
TOP = 106

# Available Now pill
pf = fnt(12, bold=True)
d.rounded_rectangle([CX, TOP, CX+196, TOP+28], radius=14, fill=(6,78,59), outline=(16,185,129))
d.ellipse([CX+12, TOP+9, CX+20, TOP+17], fill='#10B981')
d.text((CX+26, TOP+6), 'AVAILABLE NOW', font=pf, fill='#10B981')

# Name
nf = fnt(96, bold=True)
NY = TOP + 28 + 10
d.text((CX, NY), 'Tony Beal', font=nf, fill='#F8FAFC')
nw = int(d.textlength('Tony Beal', font=nf))
d.rectangle([CX, NY+100, CX+nw, NY+103], fill='#3B82F6')

# Title
tf = fnt(18)
TY = NY + 100 + 14
d.text((CX+2, TY), 'Revenue Operations   \u00b7   AI Sales Systems   \u00b7   GTM Strategy   \u00b7   Remote Nationwide', font=tf, fill='#64748B')

# Divider
DX = 980
for y in range(50, H-50):
    t = (y-50)/(H-100)
    a = int(255*4*t*(1-t))
    d.line([(DX,y),(DX+1,y)], fill=(int(30*a/255+14), int(58*a/255+22), int(95*a/255+40)))

# Stats — 4 boxes filling right panel exactly
SMID = H // 2
nuf  = fnt(36, bold=True)
lbf  = fnt(13)

stats = [
    ('$20M+',  'Pipeline Built'),
    ('3,700+', 'Accounts Mgd'),
    ('8 Yrs',  'Quota Streak'),
    ('15+',    'Years B2B'),
]

RIGHT_START = DX + 18
RIGHT_END   = W - 18
panel_w     = RIGHT_END - RIGHT_START
GAP         = 12
BOX_W       = (panel_w - 3 * GAP) // 4

sx = RIGHT_START
for num, label in stats:
    bx = sx
    d.rounded_rectangle([bx, SMID-66, bx+BOX_W, SMID+52], radius=10, fill=(8,16,36), outline=(20,36,68))
    tw = int(d.textlength(num, font=nuf))
    tx = bx + (BOX_W - tw) // 2
    d.text((tx, SMID-60), num, font=nuf, fill='#3B82F6')
    lw = int(d.textlength(label, font=lbf))
    lx = bx + (BOX_W - lw) // 2
    d.text((lx, SMID+14), label, font=lbf, fill='#475569')
    sx += BOX_W + GAP

d.rectangle([0, 0, W, 2], fill='#1E3A5F')
d.rectangle([0, H-2, W, H], fill='#1E3A5F')
d.text((W-150, H-22), 'tonybeal.net', font=fnt(12, bold=True), fill='#1E2D45')

out = r'C:\Users\tonyb\tonybeal.net\assets\linkedin-banner.png'
img.save(out, 'PNG', optimize=True)
print('Saved:', out)
