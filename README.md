# pixiespantryshop.com — Link Hub

The public site is a **static link hub** ("linktree, but Great Gatsby"). It is generated,
not hand-edited.

```
/                    door chooser — Mellow Pixie · Pixie's Pantry · Reviewed by Dusty · Shop
/mellow-pixie/       the operator: travel, points, home, wellness, style, pets
/pixies-pantry/      the brand: store links, vaporizers, glass, accessories, hemp/CBD
/reviewed-by-dusty/  the review desk: capture gear, software, back office, tech
```

## Editing the content

All copy lives in **`hub/data/content.py`** — one Python dict, one tuple per card:

```python
("Partner Name In partners.json" | None, "Display Name",
 "What it actually is.", "Why I recommend it.", "https://override-url" | None)
```

- Pass the partner name to auto-resolve the affiliate link.
- Pass `None` + an override URL for non-affiliate links (our own pages, etc.).

**`hub/data/partners.json`** is the affiliate registry (351 Awin + Impact programs) exported
from the affiliate/vendor master workbook: network, category, merchant URL, Impact tracking
link, Awin `advertiserId`, payout and cookie length.

## Building & deploying

```bash
AWIN_AFFID=<your awin publisher id> python3 hub/build.py   # -> hub/dist/
```

Link resolution order: Impact tracking link → Awin deep link
(`awin1.com/cread.php?awinmid=<advertiserId>&awinaffid=$AWIN_AFFID&ued=<merchant url>`) →
plain merchant URL. Without `AWIN_AFFID` the build prints a warning listing every Awin
partner that fell back to an untracked link — **never ship a build with that warning.**

GitHub Pages serves the **`gh-pages`** branch, so deploy = copy `hub/dist/` onto `gh-pages`
and push. `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml` and a `404.html` fallback are
generated automatically.

## `legacy-react/`

The previous Vite/React site, kept for reference only. Nothing builds from it.
