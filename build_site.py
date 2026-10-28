#!/usr/bin/env python3
"""Build the static SEO gallery site for the DeepSeek whale-maid plush catalogue.

Source images live in SRCDIR (the WeChat export). Output goes to ./dist and is
what gets pushed to GitHub Pages.
"""
import os
import re
import hashlib
import shutil
from pathlib import Path

SRC = Path(r"C:/Users/Administrator/Desktop/dafeiyu")
OUT = Path(__file__).parent / "docs"

SITE_NAME = "DeepSeek Whale Maid Plushies"
SITE_URL = "https://bd-ram.github.io/deepseek-whale-plushies"
TG_HANDLE = "@DK88878"
TG_URL = "https://t.me/DK88878"
CONTACT_LINE = f"Order or ask for a quote on Telegram — {TG_HANDLE}"

# slug, source file, title, short alt, long description, keywords
ITEMS = [
    dict(
        n=1,
        src="微信图片_20261028173604_34_3.jpg",
        slug="deepseek-whale-maid-plush-pillow-front-view",
        name="Standing Front View — Whale Maid Plush Pillow",
        alt="DeepSeek whale mascot maid plush pillow shown front-on, blue gradient twin-tail hair, navy ruffle dress with a small whale apron patch and a crescent tail curving to the right, resting on a beige sofa",
        desc="The clean hero shot. Chibi whale-girl in a navy and cream maid uniform, hands clasped, standing on a beige sofa cushion with soft window light behind her. The whole character is die-cut into one plush silhouette, so the tail, hair and hair-clip all read as part of the pillow outline.",
        keywords="deepseek plush, whale maid pillow, ai mascot plush, kawaii anime cushion, deepseek merch",
    ),
    dict(
        n=2,
        src="微信图片_20261028173605_35_3.jpg",
        slug="deepseek-whale-maid-body-pillow-tall",
        name="Tall Body Pillow — Whale Maid Long Cushion",
        alt="Long body-pillow cut of the DeepSeek whale maid plush, full head-to-flipper silhouette on a linen armchair, hands together under the chin, navy skirt with white apron and whale flower pattern",
        desc="The tall cut: a full body-pillow proportion, head to flipper, resting upright in a linen armchair by a window. Best shape for back support on a desk chair or for leaning against a headboard — the whale tail curls out at the base as an extra padded foot.",
        keywords="body pillow, dakimakura style cushion, long anime pillow, deepseek whale plush, desk chair cushion",
    ),
    dict(
        n=3,
        src="微信图片_20261028173606_36_3.jpg",
        slug="deepseek-whale-maid-plush-waving-long-body-pillow",
        name="Waving Long Body Pillow",
        alt="DeepSeek whale maid plush in a waving pose, one hand raised, full-length body pillow standing on an armchair, navy dress with white frilled apron and whale embroidery, tail sweeping right",
        desc="Same body-pillow cut as the tall design, in a greeting pose: one hand up, one hand open, mouth open mid-hello. Reads well in a product grid because the raised arm breaks the silhouette and makes the shape obvious at thumbnail size.",
        keywords="waving anime plush, deepseek mascot pillow, whale girl cushion, greeting pose plush",
    ),
    dict(
        n=4,
        src="微信图片_20261028173607_37_3.jpg",
        slug="deepseek-whale-maid-plush-hungry-rice-bowl",
        name="Hungry Rice Bowl Edition",
        alt="DeepSeek whale maid plush with hands on hips and an empty rice bowl beside her, speech bubble printed on the pillow reading a Chinese line, navy maid dress on a beige sofa",
        desc="Hands on hips, empty bowl, printed speech bubble — the hungry version. The bowl is part of the die-cut shape, so the pillow has two padded lobes: the character and the prop. Printed text is baked into the fabric, not embroidered.",
        keywords="hungry anime plush, rice bowl cushion, meme pillow, deepseek meme merch, funny plush pillow",
    ),
    dict(
        n=5,
        src="微信图片_20261028173610_38_3.jpg",
        slug="deepseek-whale-maid-plush-sitting-on-chair",
        name="Sitting On A Chair Edition",
        alt="DeepSeek whale maid plush sitting on a miniature wooden chair with legs dangling, printed speech bubble with a heart, navy maid uniform with white apron, crescent hair clip",
        desc="The seated variant: a tiny wooden chair is part of the silhouette, legs dangling, hands folded in the lap, speech bubble with a heart at the shoulder. The chair legs give the pillow a flat base so it stands upright on a shelf without a prop.",
        keywords="sitting plush pillow, shelf decoration anime, deepseek whale cushion, chibi maid plush",
    ),
    dict(
        n=6,
        src="微信图片_20261028173612_39_3.jpg",
        slug="deepseek-whale-maid-plush-full-belly-rub",
        name="Full Belly Edition",
        alt="DeepSeek whale maid plush reclining with legs kicked out to one side, one hand on a full round belly, printed speech bubble reading a Chinese dinner line, whale tail at the right edge",
        desc="Reclining pose with the legs kicked out and a hand over a full belly. Widest of the set — the horizontal spread of the legs and tail makes a low, sofa-friendly shape that sits flat on a cushion rather than leaning.",
        keywords="reclining anime pillow, belly plush, novelty cushion, deepseek whale maid, kawaii room decor",
    ),
    dict(
        n=7,
        src="微信图片_20261028173613_40_3.jpg",
        slug="deepseek-whale-maid-plush-holding-zone-sign",
        name="Holding The Sign Edition",
        alt="DeepSeek whale maid plush holding a white card printed with a single Chinese character, question-mark speech bubble above, navy dress with whale apron, sitting on a beige sofa",
        desc="She is holding up a card with a single character on it and asking what it means. The card and speech bubble are both part of the printed pillow face. Popular with people who work with tokenisers and want the joke on their desk.",
        keywords="sign holding plush, tokenizer joke pillow, deepseek meme plush, developer desk decor",
    ),
    dict(
        n=8,
        src="微信图片_20261028173615_41_3.jpg",
        slug="deepseek-whale-maid-plush-release-date-interrogation",
        name="Release Date Interrogation Edition",
        alt="DeepSeek whale maid plush strapped into a miniature interrogation chair with a coil above the head, two printed speech bubbles in Chinese, navy maid dress, lightning doodles around the frame",
        desc="The interrogation gag: strapped into a tin chair under a coil, one bubble demanding a release date and the other refusing to talk. Heaviest printed artwork of the set — two bubbles, a chair, and lightning doodles all die-cut into the outline.",
        keywords="interrogation meme plush, funny anime cushion, computer chair joke, deepseek meme merch",
    ),
    dict(
        n=9,
        src="微信图片_20261028173617_42_3.jpg",
        slug="deepseek-whale-maid-plush-desk-notebook-coffee",
        name="Desk Scene Edition — Notebook And Whale Mug",
        alt="Wide DeepSeek whale maid plush showing her writing in a spiral notebook at a desk with a whale-shaped mug, ink bottle and book stack, printed banner across the top in Chinese",
        desc="The widest piece in the catalogue: a full desk scene, notebook, whale mug, ink bottle and book stack all die-cut into one long landscape pillow. Printed banner runs across the top. Sits best along the back of a sofa or against a monitor riser.",
        keywords="landscape anime pillow, desk scene plush, whale mug, wide cushion, deepseek whale merch",
    ),
    dict(
        n=10,
        src="微信图片_20261028173619_43_3.jpg",
        slug="deepseek-whale-maid-plush-rice-bowl-chopsticks-big-fat-fish",
        name="Big Fat Fish Rice Bowl Edition",
        alt="DeepSeek whale maid plush holding a bowl of rice in one hand and chopsticks in the other, printed banner across the top in Chinese, navy maid dress with whale apron, beige sofa background",
        desc="Bowl in one hand, chopsticks in the other, big printed banner overhead. Named after the joke on the pillow. The bowl and chopsticks are separate padded lobes on the outline, so the shape has three bumps instead of a plain rectangle.",
        keywords="big fat fish plush, rice bowl pillow, funny deepseek merch, chibi whale girl cushion",
    ),
    dict(
        n=11,
        src="微信图片_20261028173621_44_3.jpg",
        slug="deepseek-whale-maid-plush-arms-crossed-jealous",
        name="Arms Crossed Edition",
        alt="DeepSeek whale maid plush with arms crossed and a jealous expression, printed speech bubble above, standing on a pastel bed with a whale cushion and figure in the background",
        desc="Arms crossed, one eyebrow down, speech bubble claiming ownership. Styled here on a pastel bed set with a matching whale cushion behind — the shot most people use when they post the plush next to their keyboard.",
        keywords="jealous anime plush, arms crossed pillow, tsundere cushion, deepseek whale girl plush",
    ),
    dict(
        n=12,
        src="微信图片_20261028173623_45_3.jpg",
        slug="deepseek-whale-maid-plush-notepad-counting",
        name="Notepad Edition — Counting Characters",
        alt="DeepSeek whale maid plush holding a spiral notepad with a whale logo and a blue pen, small printed speech bubble, navy dress with white apron, seated on a light blue sofa",
        desc="Pen in one hand, whale-branded notepad in the other, small bubble overhead. Shot on a pale blue sofa so the navy dress reads cleanly. The notepad and pen are printed flat, so no hard edges poke out of the cushion.",
        keywords="notepad plush, writer gift anime, deepseek whale cushion, study desk plush",
    ),
    dict(
        n=13,
        src="微信图片_20261028173625_46_3.jpg",
        slug="deepseek-whale-maid-plush-thinking-panel-meme",
        name="Thinking Panel Meme Edition",
        alt="DeepSeek whale maid plush holding a wide printed reasoning-panel sign in front of her body, blue sofa background, one hand raised, sweat drop above the eyebrow",
        desc="The thinking-panel gag: a wide printed sign with the reasoning-panel UI across the front of the pillow, hand raised, sweat drop. Because the sign fills the lower half, this one is the most legible at a distance — it works as a shelf joke piece.",
        keywords="thinking panel meme, ai reasoning joke pillow, deepseek meme plush, wide sign cushion",
    ),
    dict(
        n=14,
        src="微信图片_20261028173627_47_3.jpg",
        slug="deepseek-whale-maid-plush-front-view-alternate",
        name="Standing Front View — Alternate Cut",
        alt="Alternate front-view cut of the DeepSeek whale maid plush pillow, hands clasped, navy and cream dress with whale apron patch, tail curving right, beige sofa and cushion behind",
        desc="The alternate take on design 01: same character, slightly different arm placement and a cleaner tail curve. If you want two of the same character for a pair, this is the one that reads as a sibling rather than a copy.",
        keywords="alternate plush cut, deepseek whale pillow pair, kawaii anime plush set",
    ),
]

CSSVER = "v1"
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ogimage}">
<meta property="og:image:alt" content="{ogalt}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1200">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{ogimage}">
<link rel="stylesheet" href="{root}assets/style.css?v={cssver}">
<link rel="sitemap" type="application/xml" href="{root}sitemap.xml">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<header class="site-head">
  <a class="brand" href="{root}index.html">🐋 DeepSeek Whale Maid Plushies</a>
  <a class="tg-btn" href="{tg}" rel="noopener">Telegram {handle}</a>
</header>
"""

FOOT = """<footer class="site-foot">
  <p class="cta">Want one? Message <a href="{tg}" rel="noopener">{handle}</a> on Telegram for price, sizes and shipping.</p>
  <p class="fine">Unofficial fan-made merch gallery. Not affiliated with or endorsed by DeepSeek. Artwork shown is AI-generated fan art of a mascot character. Images are illustrative; final fabric, print and colour may differ from the mock-ups.</p>
  <p class="fine"><a href="{root}index.html">All designs</a> · <a href="{root}README.md">About this catalogue</a> · <a href="{tg}" rel="noopener">Order on Telegram</a></p>
</footer>
</body>
</html>
"""

CSS = """
:root {
  --ink: #0d1526;
  --ink-2: #182742;
  --paper: #f6f8fc;
  --line: #dfe6f2;
  --blue: #2f6fed;
  --blue-deep: #1b3f8b;
  --muted: #5c6b85;
  --radius: 18px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font: 16px/1.65 "Segoe UI", -apple-system, Inter, system-ui, sans-serif;
  color: var(--ink);
  background: var(--paper);
}
a { color: var(--blue); }
img { max-width: 100%; display: block; }

/* header */
.site-head {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px clamp(16px, 5vw, 48px);
  background: var(--ink); color: #fff;
  position: sticky; top: 0; z-index: 20;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.brand { color: #fff; text-decoration: none; font-weight: 700; letter-spacing: .2px; }
.tg-btn {
  background: linear-gradient(160deg, #37aee2, #1e88c7);
  color: #fff; text-decoration: none; font-weight: 600; font-size: 14px;
  padding: 9px 16px; border-radius: 999px; white-space: nowrap;
  box-shadow: 0 6px 18px rgba(30,136,199,.35);
}
.tg-btn:hover { filter: brightness(1.07); }

/* hero */
.hero {
  padding: clamp(36px, 7vw, 84px) clamp(16px, 5vw, 48px) 24px;
  max-width: 1080px; margin: 0 auto;
}
.hero h1 {
  font-size: clamp(28px, 4.6vw, 50px); line-height: 1.1;
  margin: 0 0 14px; letter-spacing: -.6px;
}
.hero p.lede { font-size: clamp(16px, 1.5vw, 19px); color: var(--muted); max-width: 62ch; margin: 0 0 18px; }
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 0; }
.pill {
  font-size: 13px; color: var(--blue-deep); background: #e8f0ff;
  border: 1px solid #cfdeff; border-radius: 999px; padding: 5px 12px;
}
.hero-cta { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 26px; }
.btn {
  display: inline-block; text-decoration: none; font-weight: 600;
  padding: 12px 22px; border-radius: 12px; font-size: 15px;
}
.btn-primary { background: var(--blue); color: #fff; box-shadow: 0 10px 24px rgba(47,111,237,.28); }
.btn-ghost { background: #fff; color: var(--ink); border: 1px solid var(--line); }

/* grid */
.gallery {
  display: grid; gap: clamp(16px, 2vw, 26px);
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  max-width: 1180px; margin: 0 auto;
  padding: 24px clamp(16px, 5vw, 48px) 56px;
}
.card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius);
  overflow: hidden; text-decoration: none; color: inherit;
  transition: transform .18s ease, box-shadow .18s ease;
  display: flex; flex-direction: column;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(13,21,38,.12); }
.card img { width: 100%; height: auto; aspect-ratio: 1/1; object-fit: cover; }
.card-body { padding: 13px 15px 17px; }
.card-kicker { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--blue); font-weight: 700; }
.card h2 { font-size: 15.5px; margin: 6px 0 6px; line-height: 1.35; }
.card p { font-size: 13px; color: var(--muted); margin: 0; }

/* design page */
.design-wrap {
  max-width: 1080px; margin: 0 auto; padding: 26px clamp(16px, 5vw, 48px) 60px;
  display: grid; gap: clamp(20px, 3vw, 44px);
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
  align-items: start;
}
@media (max-width: 760px) { .design-wrap { grid-template-columns: 1fr; } }
.design-shot { border-radius: var(--radius); overflow: hidden; border: 1px solid var(--line); background:#fff; }
.design-shot img { width: 100%; height: auto; }
.crumbs { font-size: 13px; color: var(--muted); margin: 0 0 10px; }
.design-info h1 { font-size: clamp(23px, 3vw, 34px); line-height: 1.18; margin: 0 0 12px; letter-spacing: -.3px; }
.design-info > p { color: #2b3a55; }
.spec { list-style: none; padding: 0; margin: 22px 0; border-top: 1px solid var(--line); }
.spec li { display: flex; gap: 10px; padding: 9px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
.spec b { min-width: 108px; color: var(--ink); }
.spec span { color: var(--muted); }
.order-box {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius);
  padding: 18px 20px; margin: 22px 0;
}
.order-box p { margin: 0 0 12px; font-size: 14.5px; }
.pager { display: flex; justify-content: space-between; gap: 12px; margin-top: 30px; font-size: 14px; }

/* footer */
.site-foot {
  border-top: 1px solid var(--line); background: #fff;
  padding: 30px clamp(16px, 5vw, 48px) 46px; text-align: center;
}
.site-foot .cta { font-size: 17px; font-weight: 600; margin: 0 0 14px; }
.site-foot .fine { font-size: 12.5px; color: var(--muted); max-width: 78ch; margin: 0 auto 10px; }
"""


def fmt(tpl: str, **kw) -> str:
    kw.setdefault("cssver", CSSVER)
    return tpl.format(**kw)


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def index_jsonld():
    items = []
    for it in ITEMS:
        items.append({
            "@type": "ListItem",
            "position": it["n"],
            "url": f"{SITE_URL}/designs/{it['slug']}.html",
            "name": it["name"],
            "image": f"{SITE_URL}/images/{it['slug']}.jpg",
        })
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{SITE_URL}/#page",
                "url": f"{SITE_URL}/",
                "name": "DeepSeek Whale Maid Plush Pillow Gallery — 14 Designs",
                "description": "English-language catalogue of 14 DeepSeek whale mascot maid plush pillow designs with photos, descriptions, and a Telegram ordering channel.",
                "inLanguage": "en",
                "isFamilyFriendly": True,
                "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE_URL}/images/{ITEMS[0]['slug']}.jpg"},
                "mainEntity": {"@id": f"{SITE_URL}/#itemlist"},
            },
            {
                "@type": "ItemList",
                "@id": f"{SITE_URL}/#itemlist",
                "name": "DeepSeek whale maid plush pillow designs",
                "numberOfItems": len(ITEMS),
                "itemListElement": items,
            },
            {
                "@type": "Organization",
                "name": "DeepSeek Whale Maid Plushies (unofficial fan merch)",
                "url": f"{SITE_URL}/",
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "sales",
                    "name": "Telegram",
                    "url": TG_URL,
                    "availableLanguage": ["en", "zh"],
                },
            },
        ],
    }
    import json
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def item_jsonld(it):
    import json
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ImageObject",
                "@id": f"{SITE_URL}/designs/{it['slug']}.html#image",
                "url": f"{SITE_URL}/images/{it['slug']}.jpg",
                "contentUrl": f"{SITE_URL}/images/{it['slug']}.jpg",
                "name": f"{it['name']} — DeepSeek whale maid plush pillow",
                "description": it["alt"],
                "caption": it["name"],
                "width": 1200,
                "height": 1200,
                "encodingFormat": "image/jpeg",
                "creator": {"@type": "Organization", "name": "DeepSeek Whale Maid Plushies (fan project)"},
                "creditText": "Unofficial AI-assisted fan art",
                "isPartOf": {"@id": f"{SITE_URL}/#page"},
            },
            {
                "@type": "Product",
                "name": f"{it['name']} — DeepSeek whale mascot maid plush pillow",
                "image": [f"{SITE_URL}/images/{it['slug']}.jpg"],
                "description": it["desc"],
                "category": "Plush pillow / decorative cushion",
                "brand": {"@type": "Brand", "name": "DeepSeek Whale Maid Plushies"},
                "audience": {"@type": "Audience", "audienceType": "Anime fans, developers, AI hobbyists"},
                "url": f"{SITE_URL}/designs/{it['slug']}.html",
                "isRelatedTo": {"@type": "Product", "name": "DeepSeek whale maid plush pillow series"},
                "additionalProperty": [
                    {"@type": "PropertyValue", "name": "Ordering", "value": f"Telegram {TG_HANDLE} ({TG_URL})"},
                    {"@type": "PropertyValue", "name": "Material", "value": "Short-pile plush fabric, dye-sublimation print"},
                    {"@type": "PropertyValue", "name": "Shape", "value": shape_for(it["slug"])},
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "All designs", "item": f"{SITE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": it["name"], "item": f"{SITE_URL}/designs/{it['slug']}.html"},
                ],
            },
        ],
    }
    # No price is published, so the Offer carries no price field — keep it honest.
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "images").mkdir(parents=True)
    (OUT / "designs").mkdir(parents=True)
    (OUT / "assets").mkdir(parents=True)

    # copy + rename images, plus a 640px thumbnail for the grid
    from PIL import Image
    (OUT / "images" / "thumb").mkdir(parents=True, exist_ok=True)
    for it in ITEMS:
        srcp = SRC / it["src"]
        if not srcp.exists():
            raise SystemExit(f"missing source image: {srcp}")
        dst = OUT / "images" / f"{it['slug']}.jpg"
        shutil.copy2(srcp, dst)
        im = Image.open(dst)
        im.thumbnail((640, 640), Image.LANCZOS)
        im.save(OUT / "images" / "thumb" / f"{it['slug']}.jpg", "JPEG",
                quality=82, optimize=True, progressive=True)

    global CSSVER
    CSSVER = hashlib.sha1(CSS.encode()).hexdigest()[:8]
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    # index
    cards = []
    for it in ITEMS:
        cards.append(f"""  <a class="card" href="designs/{it['slug']}.html">
    <img src="images/thumb/{it['slug']}.jpg" alt="{esc(it['alt'])}" width="640" height="640" loading="lazy" decoding="async">
    <div class="card-body">
      <span class="card-kicker">Design {it['n']:02d}</span>
      <h2>{esc(it['name'])}</h2>
      <p>{esc(it['desc'].split('. ')[0])}.</p>
    </div>
  </a>""")

    title = "DeepSeek Whale Maid Plush Pillows — 14 Kawaii AI Mascot Cushion Designs (Photos)"
    desc = ("Photo gallery of 14 DeepSeek whale mascot maid plush pillow designs: front view, body pillow, "
            "meme editions and desk-scene cushions. English descriptions, sizing notes, order via Telegram.")
    html = fmt(HEAD, 
        title=esc(title), description=esc(desc),
        keywords=("deepseek plush, deepseek whale plush, whale maid plush pillow, ai mascot plush, "
                  "kawaii anime cushion, anime body pillow, meme plush pillow, developer desk decor, "
                  "deepseek merch, whale girl plush, buy anime plush pillow"),
        canonical=f"{SITE_URL}/", ogtype="website", site=SITE_NAME,
        ogimage=f"{SITE_URL}/images/{ITEMS[0]['slug']}.jpg", ogalt=esc(ITEMS[0]["alt"]),
        root="", jsonld=index_jsonld(), tg=TG_URL, handle=TG_HANDLE,
    )
    html += f"""<main>
<section class="hero">
  <h1>DeepSeek Whale Maid Plush Pillows — 14 Designs</h1>
  <p class="lede">A full photo catalogue of the blue whale-girl maid plush: die-cut pillows in navy and cream, printed meme editions, tall body-pillow cuts and a wide desk-scene cushion. Every listing has the exact shape, pose and printed artwork, in English.</p>
  <div class="pill-row">
    <span class="pill">14 designs</span>
    <span class="pill">Die-cut plush</span>
    <span class="pill">1200 × 1200 photos</span>
    <span class="pill">Chibi whale-girl mascot</span>
    <span class="pill">Ships worldwide via Telegram order</span>
  </div>
  <div class="hero-cta">
    <a class="btn btn-primary" href="{TG_URL}" rel="noopener">Order on Telegram {TG_HANDLE}</a>
    <a class="btn btn-ghost" href="#catalogue">Browse all 14 designs</a>
  </div>
</section>

<section id="catalogue">
<div class="gallery">
{chr(10).join(cards)}
</div>
</section>

<section class="hero" style="padding-top:0">
  <h2>What these plush pillows are</h2>
  <p class="lede">Each piece is a die-cut cushion: the character silhouette — hair, twin tails, whale tail, plus any prop like a chair, bowl or notepad — is cut out of the fabric instead of being printed on a rectangle. Face and outfit are printed by dye sublimation, which is why the gradient blue hair holds detail across a 1200&nbsp;px photo.</p>
  <p class="lede">The set splits into three shapes: <strong>single-character die-cuts</strong> (designs 01, 04, 07, 14) that stand on a desk, <strong>tall body-pillow cuts</strong> (02, 03) that work as back support, and <strong>wide scene cushions</strong> (06, 09, 13) that sit flat along the back of a sofa. Designs 05, 08, 11 and 12 are the pose variations with a paper prop or indoor prop built into the outline.</p>
  <h2>Ordering, sizing and shipping</h2>
  <p class="lede">Sizes, fabric options and per-unit pricing are quoted on request — message <a href="{TG_URL}" rel="noopener">{TG_HANDLE}</a> on Telegram with the design number (e.g. “design 07”) and your country. Bulk quantities and mixed sets are available.</p>
</section>
</main>
"""
    html += fmt(FOOT, root="", tg=TG_URL, handle=TG_HANDLE)
    (OUT / "index.html").write_text(html, encoding="utf-8")

    # per design pages
    for i, it in enumerate(ITEMS):
        prev_it = ITEMS[i - 1] if i > 0 else None
        next_it = ITEMS[i + 1] if i + 1 < len(ITEMS) else None
        ptitle = f"{it['name']} — DeepSeek Whale Maid Plush Pillow | Design {it['n']:02d}"
        pdesc = it["desc"][:150]
        page = fmt(HEAD, 
            title=esc(ptitle), description=esc(pdesc), keywords=esc(it["keywords"]),
            canonical=f"{SITE_URL}/designs/{it['slug']}.html", ogtype="article", site=SITE_NAME,
            ogimage=f"{SITE_URL}/images/{it['slug']}.jpg", ogalt=esc(it["alt"]),
            root="../", jsonld=item_jsonld(it), tg=TG_URL, handle=TG_HANDLE,
        )
        pager = []
        if prev_it:
            pager.append(f'<a href="{prev_it["slug"]}.html">← Design {prev_it["n"]:02d}: {esc(prev_it["name"])}</a>')
        else:
            pager.append("<span></span>")
        if next_it:
            pager.append(f'<a href="{next_it["slug"]}.html">Design {next_it["n"]:02d}: {esc(next_it["name"])} →</a>')
        else:
            pager.append("<span></span>")

        page += f"""<main class="design-wrap">
  <div>
    <div class="design-shot">
      <img src="../images/{it['slug']}.jpg" alt="{esc(it['alt'])}" width="1200" height="1200" fetchpriority="high" decoding="async">
    </div>
  </div>
  <div class="design-info">
    <p class="crumbs"><a href="../index.html">All designs</a> / Design {it['n']:02d}</p>
    <h1>{esc(it['name'])}</h1>
    <p>{esc(it['desc'])}</p>
    <ul class="spec">
      <li><b>Design</b><span>{it['n']:02d} of {len(ITEMS)}</span></li>
      <li><b>Shape</b><span>{shape_for(it['slug'])}</span></li>
      <li><b>Colours</b><span>Navy, cream white, glacier-blue gradient hair</span></li>
      <li><b>Finish</b><span>Dye-sublimation printed plush face, soft short-pile fabric</span></li>
      <li><b>Photo</b><span>1200 × 1200 JPEG, indoor daylight, neutral sofa / bedroom setting</span></li>
      <li><b>Ordering</b><span>Quote on request — Telegram <a href="{TG_URL}" rel="noopener">{TG_HANDLE}</a></span></li>
    </ul>
    <div class="order-box">
      <p><strong>Want this design?</strong> Send the design number ({it['n']:02d}) plus your country to <a href="{TG_URL}" rel="noopener">{TG_HANDLE}</a> on Telegram and you'll get size options, fabric choices and a quote.</p>
      <a class="btn btn-primary" href="{TG_URL}" rel="noopener">Message {TG_HANDLE} on Telegram</a>
    </div>
    <div class="pager">{pager[0]}{pager[1]}</div>
  </div>
</main>
"""
        page += fmt(FOOT, root="../", tg=TG_URL, handle=TG_HANDLE)
        (OUT / "designs" / f"{it['slug']}.html").write_text(page, encoding="utf-8")

    # sitemap
    import datetime
    today = datetime.date.today().isoformat()
    urls = [f"{SITE_URL}/"] + [f"{SITE_URL}/designs/{it['slug']}.html" for it in ITEMS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == f"{SITE_URL}/" else "0.8"
        img = "" 
        sm.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>"
                  f"<changefreq>monthly</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + f"{SITE_URL}/sitemap.xml\n", encoding="utf-8")

    (OUT / "404.html").write_text(
        fmt(HEAD, title="Page not found — DeepSeek Whale Maid Plushies",
                    description="That page does not exist. Browse all 14 DeepSeek whale maid plush pillow designs.",
                    keywords="deepseek plush, whale maid pillow", canonical=f"{SITE_URL}/404.html",
                    ogtype="website", site=SITE_NAME, ogimage=f"{SITE_URL}/images/{ITEMS[0]['slug']}.jpg",
                    ogalt="DeepSeek whale maid plush pillow", root="/", jsonld="{}",
                    tg=TG_URL, handle=TG_HANDLE)
        + f"""<main class="hero"><h1>404 — no plush here</h1>
<p class="lede">That link is dead. All 14 designs are on the <a href="/index.html">gallery page</a>.</p></main>"""
        + fmt(FOOT, root="/", tg=TG_URL, handle=TG_HANDLE),
        encoding="utf-8")

    print(f"built {len(ITEMS)} design pages -> {OUT}")


def shape_for(slug: str) -> str:
    if "body-pillow" in slug:
        return "Tall body pillow (head-to-flipper die-cut)"
    if any(k in slug for k in ("desk-notebook", "thinking-panel", "full-belly")):
        return "Wide landscape cushion (~4:3 die-cut)"
    return "Square character die-cut (~1200 px footprint)"


if __name__ == "__main__":
    build()
