# DeepSeek Whale Maid Plush Pillows — 14 Designs (Photo Catalogue)

English-language photo catalogue of the **DeepSeek whale mascot maid plush pillow** — a chibi blue whale-girl in a navy-and-cream maid uniform, produced as **die-cut decorative cushions**: the character silhouette (hair, twin tails, whale tail, and any prop) is cut out of the fabric instead of printed onto a rectangle.

**Live gallery:** <https://bd-ram.github.io/deepseek-whale-plushies/>

**Ordering / quotes:** Telegram [@DK88878](https://t.me/DK88878) — send the design number and your country.

---

## What's in the set

| # | Design | Shape | Page |
|---|--------|-------|------|
| 01 | Standing Front View | Square character die-cut | [open](docs/designs/deepseek-whale-maid-plush-pillow-front-view.html) |
| 02 | Tall Body Pillow | Head-to-flipper body pillow | [open](docs/designs/deepseek-whale-maid-body-pillow-tall.html) |
| 03 | Waving Long Body Pillow | Head-to-flipper body pillow | [open](docs/designs/deepseek-whale-maid-plush-waving-long-body-pillow.html) |
| 04 | Hungry Rice Bowl | Square die-cut + prop lobe | [open](docs/designs/deepseek-whale-maid-plush-hungry-rice-bowl.html) |
| 05 | Sitting On A Chair | Square die-cut + chair base | [open](docs/designs/deepseek-whale-maid-plush-sitting-on-chair.html) |
| 06 | Full Belly Edition | Wide landscape cushion | [open](docs/designs/deepseek-whale-maid-plush-full-belly-rub.html) |
| 07 | Holding The Sign | Square character die-cut | [open](docs/designs/deepseek-whale-maid-plush-holding-zone-sign.html) |
| 08 | Release Date Interrogation | Square die-cut, heavy printed art | [open](docs/designs/deepseek-whale-maid-plush-release-date-interrogation.html) |
| 09 | Desk Scene — Notebook & Whale Mug | Wide landscape cushion | [open](docs/designs/deepseek-whale-maid-plush-desk-notebook-coffee.html) |
| 10 | Big Fat Fish Rice Bowl | Square die-cut, three lobes | [open](docs/designs/deepseek-whale-maid-plush-rice-bowl-chopsticks-big-fat-fish.html) |
| 11 | Arms Crossed | Square character die-cut | [open](docs/designs/deepseek-whale-maid-plush-arms-crossed-jealous.html) |
| 12 | Notepad — Counting Characters | Square character die-cut | [open](docs/designs/deepseek-whale-maid-plush-notepad-counting.html) |
| 13 | Thinking Panel Meme | Wide landscape cushion | [open](docs/designs/deepseek-whale-maid-plush-thinking-panel-meme.html) |
| 14 | Standing Front View — Alternate Cut | Square character die-cut | [open](docs/designs/deepseek-whale-maid-plush-front-view-alternate.html) |

Three shape families, chosen by where the plush is going to live:

- **Square character die-cuts** (01, 04, 07, 14) — stand upright on a desk, shelf or monitor riser.
- **Tall body-pillow cuts** (02, 03) — back and lumbar support for a gaming chair or headboard.
- **Wide scene cushions** (06, 09, 13) — sit flat along the back of a sofa; the widest reads as a printed scene rather than a character portrait.

## Product notes

- **Material:** short-pile plush fabric, dye-sublimation printed face. The gradient blue hair is the part that shows print quality first — bad sublimation bands the cyan-to-navy transition.
- **Shapes:** die-cut outline, stuffed to a soft pillow loft; props (bowl, chair, notepad, reasoning panel) are separate padded lobes on the outline.
- **Photos:** 1200 × 1200 JPEG, indoor daylight, neutral sofa / bedroom sets, 640 px thumbnails for the grid.
- **Sizing and price:** quoted per order — sizes, filling density and fabric options vary by quantity.
- **Bulk:** mixed sets and multi-unit orders available; ask for a quote.

## SEO implementation (what this repo does and why)

- One indexable page **per design** with a unique `<title>`, meta description, H1 and image `alt` text — 14 long-tail entry points instead of one gallery page.
- Descriptive **file names** for every image (`deepseek-whale-maid-plush-hungry-rice-bowl.jpg`) instead of WeChat export names.
- **JSON-LD**: `CollectionPage` + `ItemList` on the index, `ImageObject` + `Product` + `BreadcrumbList` per design. No price is published, so the `Product` nodes carry `additionalProperty` instead of a fabricated `Offer` price.
- **Open Graph / Twitter** large-image cards on every page, `canonical` links, `sitemap.xml`, `robots.txt`, `.nojekyll`.
- **Performance:** 640 px progressive thumbnails on the grid, full 1200 px only on the detail page (`fetchpriority="high"`), explicit `width`/`height` to avoid layout shift, `loading="lazy"` below the fold.
- **Internal linking:** every design page links to the previous and next design plus the gallery, so crawl depth is 2 from the root.

## Repo layout

```
build_site.py          # generator: source images -> docs/
docs/                  # <- GitHub Pages publishes this directory
  index.html           # gallery
  designs/*.html       # one page per design
  images/*.jpg         # full-size 1200x1200
  images/thumb/*.jpg   # 640px grid thumbnails
  assets/style.css
  sitemap.xml robots.txt 404.html .nojekyll
```

## Build

```bash
python build_site.py     # reads C:/Users/Administrator/Desktop/dafeiyu, writes docs/
```

Requires Pillow. Edit the `ITEMS` table in `build_site.py` to add or change designs — slugs, titles, alt text and descriptions all live there.

## Credits and disclaimer

Unofficial, fan-made merch catalogue. **Not affiliated with, sponsored by, or endorsed by DeepSeek.** Character artwork is AI-generated fan art of a mascot character; images are illustrative and final fabric, print and colour may differ from the mock-ups. DeepSeek names and marks belong to their respective owner.

Site code and copy in this repository are released under the MIT licence.
