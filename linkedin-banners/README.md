# Tony Beal — LinkedIn Banner Slides

## Overview
5-slide LinkedIn Premium banner set for **Tony Beal** (tonybeal.net).
Size: **1584 × 396 px** each. Format: PNG.

## Files
| File | Slide | Content |
|------|-------|---------|
| `../assets/linkedin-banner-v2.png` | Slide 1 | Name + expertise bars + stat cards |
| `../assets/linkedin-banner-slide2.png` | Slide 2 | Big proof numbers (2×2 grid) |
| `../assets/linkedin-banner-slide3.png` | Slide 3 | What I Build — 3 service pillars |
| `../assets/linkedin-banner-slide4.png` | Slide 4 | Bold quote / manifesto |
| `../assets/linkedin-banner-slide5.png` | Slide 5 | CTA — Book a call |

## Generator Script
`scripts/make_all_banners_v5.py` — Python/Pillow. Run:
```
cd tonybeal-site
python scripts/make_all_banners_v5.py
```

## Design Spec
- **Background**: Dark navy `(4,6,20)` + mesh gradient orbs + hex grid overlay
- **Photo**: `headshot-new.png` (768×768, light bg) — circle crop R=170, CX=1300, CY=198
- **Left margin**: `LX = 200` (clears LinkedIn profile picture overlay ~180px)
- **Content zone**: LX=200 → CX-R-40 (~1090px) — fills ~70% of banner width
- **Font stack**: `ariblk.ttf` (Arial Black), `arialbd.ttf` (Arial Bold), `arial.ttf`
- **Accent colors**: Blue `(96,165,250)`, Purple `(99,102,241)`, Green `(52,211,153)`, Gold `(245,158,11)`

## Brand Stats (use these exactly)
- `$20M+` pipeline generated
- `15+` years in B2B
- `11K+` LinkedIn followers
- `3,700+` accounts developed
- `1,000+` customers acquired

## Tony Beal Identity
- **Title**: Revenue Architect | AI Sales Strategist | GTM Leader
- **Focus**: Revenue Operations, AI Sales Systems, GTM Strategy
- **Site**: tonybeal.net
- **LinkedIn**: linkedin.com/in/tony-beal40/
- **Available for**: Consulting, BD Director roles, RevOps leadership

## Agent Instructions
To modify banners:
1. Edit `scripts/make_all_banners_v5.py`
2. Run the script (requires `pillow` — `pip install pillow`)
3. Output goes to `assets/linkedin-banner-v2.png` and `assets/linkedin-banner-slide2-5.png`
4. Commit and push `assets/*.png` + the script

Key layout constants (in `build_base()`):
- `R = 170` — photo circle radius
- `CX = 1300` — photo center X (move left = photo moves left, content gets more room)
- `LX = 200` — left text margin in every slide function
