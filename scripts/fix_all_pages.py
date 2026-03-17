"""
Clean fix for all secondary HTML pages:
- Remove any old GA tag (G-JRCNHM3NHP)
- Ensure correct GA tag (G-1GMYP4KZ7C) exists once
- Add favicon links
- Add lazy loading to images
- Add Person schema to resume pages
"""
import re, os

BASE = r"c:\Users\tonyb\.openclaw\workspace\tonybeal-site"

GA_TAG = '''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-1GMYP4KZ7C"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-1GMYP4KZ7C');
  </script>'''

FAVICON = '''  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/favicon.svg" />'''

PERSON_SCHEMA = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Tony Beal",
    "url": "https://tonybeal.net",
    "image": "https://tonybeal.net/headshot-final.png",
    "jobTitle": "Revenue Operations Leader",
    "description": "Revenue Operations Leader and AI Sales Systems expert with 15+ years B2B experience. $20M+ pipeline generated.",
    "email": "tonybeal40@gmail.com",
    "sameAs": ["https://linkedin.com/in/tony-beal40/", "https://tonybeal.net"],
    "knowsAbout": ["Revenue Operations", "AI Sales Systems", "GTM Strategy", "Pipeline Generation", "CRM Optimization"],
    "address": {"@type": "PostalAddress", "addressRegion": "Missouri", "addressCountry": "US"}
  }
  </script>'''

pages = {
    "cover-letters.html":          {"og": True,  "schema": False, "canonical": "https://tonybeal.net/cover-letters.html",
                                     "title": "Cover Letter Kit | Tony Beal",
                                     "desc": "Cover letter templates for RevOps, Sales Operations, and Business Development roles by Tony Beal — $20M+ pipeline generated, 15+ years B2B leadership."},
    "job-targets.html":            {"og": False, "schema": False, "canonical": None},
    "resume.html":                 {"og": False, "schema": True,  "canonical": None},
    "resume-revops.html":          {"og": False, "schema": True,  "canonical": None},
    "resume-business-development.html": {"og": False, "schema": True, "canonical": None},
    "resume-sales-operations.html":{"og": False, "schema": True,  "canonical": None},
}

for fname, opts in pages.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Remove ALL GA script blocks (both old and new)
    c = re.sub(r'\s*<!-- Google tag \(gtag\.js\) -->.*?</script>', '', c, flags=re.DOTALL)
    c = re.sub(r'\s*<script>\s*window\.dataLayer.*?gtag\(\'config\'.*?\);\s*</script>', '', c, flags=re.DOTALL)

    # 2. Remove old favicon links if any
    c = re.sub(r'\s*<link rel="(icon|apple-touch-icon)"[^>]+favicon[^>]+/?>', '', c)

    # 3. Remove old Person schema if any
    c = re.sub(r'\s*<script type="application/ld\+json">\s*\{[^}]*schema\.org[^<]*</script>', '', c, flags=re.DOTALL)

    # 4. Inject clean GA tag right after <head>
    c = re.sub(r'(<head[^>]*>)', r'\1\n' + GA_TAG, c)

    # 5. Inject favicon links before </head>
    if 'favicon' not in c:
        c = c.replace('</head>', FAVICON + '\n</head>', 1)

    # 6. Add OG/canonical for cover-letters if missing
    if opts.get("og") and 'og:title' not in c:
        og_block = f'''  <link rel="canonical" href="{opts['canonical']}" />
  <meta property="og:title" content="{opts['title']}" />
  <meta property="og:description" content="{opts['desc']}" />
  <meta property="og:url" content="{opts['canonical']}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="https://tonybeal.net/assets/linkedin-banner-v2.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{opts['title']}" />
  <meta name="twitter:description" content="{opts['desc']}" />
  <meta name="twitter:image" content="https://tonybeal.net/assets/linkedin-banner-v2.png" />'''
        c = c.replace('</head>', og_block + '\n</head>', 1)

    # 7. Add Person schema to resume pages
    if opts.get("schema") and 'schema.org/Person' not in c:
        c = c.replace('</head>', PERSON_SCHEMA + '\n</head>', 1)

    # 8. Add lazy loading to images (not hero - only ones below fold)
    c = re.sub(r'<img src="headshot-final\.png"', '<img src="headshot-final.png" loading="lazy"', c)
    c = re.sub(r'<img src="headshot-about\.png"', '<img src="headshot-about.png" loading="lazy"', c)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

    # Verify
    has_ga    = 'G-1GMYP4KZ7C' in c
    no_old    = 'G-JRCNHM3NHP' not in c
    has_fav   = 'favicon' in c
    print(f"{fname}: GA={'✅' if has_ga else '❌'} OLD_GA={'✅ clean' if no_old else '❌ STILL THERE'} FAV={'✅' if has_fav else '❌'}")

print("\nAll done!")
