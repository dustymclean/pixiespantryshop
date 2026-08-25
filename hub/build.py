#!/usr/bin/env python3
"""Build the static pixiespantryshop.com link hub.

    python hub/build.py            # build to hub/dist
    AWIN_AFFID=123456 python hub/build.py   # build with real Awin deep links

Output: hub/dist/{index.html, 404.html, CNAME, robots.txt, sitemap.xml,
                  mellow-pixie/, pixies-pantry/, reviewed-by-dusty/}
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from data.content import HUBS, SHOP_URL  # noqa: E402

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
DOMAIN = "https://pixiespantryshop.com"
AWIN_AFFID = os.environ.get("AWIN_AFFID", "").strip()

PARTNERS = {p["name"]: p for p in json.loads((ROOT / "data" / "partners.json").read_text())}
PROMOS = json.loads((ROOT / "data" / "promos.json").read_text())

# Personal codes confirmed on Impact or in writing by the merchant.
EXTRA_EXCLUSIVE = json.loads((ROOT / "data" / "impact_codes.json").read_text())

for _e in EXTRA_EXCLUSIVE:
    if not any(x["merchant"] == _e["merchant"] and x["code"] == _e["code"] for x in PROMOS):
        PROMOS.insert(0, _e)

ORDER = ["mellow-pixie", "pixies-pantry", "reviewed-by-dusty"]
DOORS = {
    "mellow-pixie": ("Mellow Pixie", "The operator behind the pantry", "Travel, home, wellness and the small luxuries."),
    "pixies-pantry": ("Pixie's Pantry", "The brand and the store", "Flower, glass, vaporizers and every partner we trust."),
    "reviewed-by-dusty": ("Reviewed by Dusty", "The review desk", "Teardowns, testing gear and the tools behind the work."),
}

untracked: list[str] = []


def link_for(partner_name: str | None, override: str | None) -> tuple[str, bool, dict | None]:
    """Return (url, is_affiliate, promo). Every partner link is network-tracked."""
    if override:
        return override, False, None
    p = PARTNERS.get(partner_name or "")
    if not p:
        raise SystemExit(f"Unknown partner in content.py: {partner_name!r}")
    link = p.get("link")
    if not link:
        untracked.append(partner_name or "")
        link = p.get("url") or SHOP_URL
    promo = p.get("promo")
    # a voucher-specific tracking link beats the generic programme link
    if promo and promo.get("link"):
        link = promo["link"]
    return link, True, promo


CSS = """
:root{
  --ink:#08070C; --ink2:#100D18; --gold:#D4AF37; --gold-2:#F2DFA0;
  --pink:#FF4FA3; --pink-2:#FFA8D2; --champagne:#F6E7C1; --muted:#B9A98A;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--champagne);
  font-family:'Josefin Sans',system-ui,sans-serif;font-size:17px;line-height:1.65;
  -webkit-font-smoothing:antialiased}
a{color:inherit}
.card *,.door *{text-decoration:none}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.deco-top{height:6px;background:linear-gradient(90deg,var(--gold),var(--pink),var(--gold-2),var(--pink-2),var(--gold))}
h1,h2,h3,.serif{font-family:'Cinzel',Georgia,serif}
.eyebrow{font-family:'Josefin Sans',sans-serif;letter-spacing:.42em;text-transform:uppercase;
  font-size:.68rem;color:var(--gold);margin:0 0 14px}
.rays{position:absolute;inset:-40% -10% auto -10%;height:150%;
  background:repeating-conic-gradient(from 0deg at 50% 0%,
    rgba(212,175,55,.10) 0deg 3deg, rgba(0,0,0,0) 3deg 9deg);
  pointer-events:none}
header.hero{position:relative;overflow:hidden;text-align:center;padding:76px 0 56px;
  background:radial-gradient(120% 90% at 50% 0%, #241226 0%, var(--ink) 62%)}
header.hero .wrap{position:relative;z-index:2}
.crest{display:inline-block;border:1px solid rgba(212,175,55,.55);padding:26px 34px;
  background:rgba(8,7,12,.55);backdrop-filter:blur(2px)}
h1{margin:0;font-size:clamp(2.1rem,6vw,3.5rem);letter-spacing:.1em;line-height:1.12;
  background:linear-gradient(180deg,#fff 0%,var(--gold-2) 45%,var(--gold) 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.tagline{margin:14px 0 0;color:var(--pink-2);letter-spacing:.26em;text-transform:uppercase;font-size:.78rem}
.blurb{max-width:660px;margin:26px auto 0;color:var(--muted);font-size:1.02rem}
.btn{display:inline-block;margin-top:28px;padding:14px 32px;text-decoration:none;
  font-size:.78rem;letter-spacing:.24em;text-transform:uppercase;color:#0A0710;
  background:linear-gradient(120deg,var(--pink-2),var(--gold-2),var(--pink));
  border:1px solid var(--gold);transition:transform .18s ease, box-shadow .18s ease}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(255,79,163,.28)}
.btn.ghost{background:none;color:var(--champagne);border:1px solid rgba(212,175,55,.6)}
nav.jump{position:sticky;top:0;z-index:30;background:rgba(8,7,12,.94);
  border-bottom:1px solid rgba(212,175,55,.28);backdrop-filter:blur(8px)}
nav.jump .wrap{display:flex;gap:22px;overflow-x:auto;padding-top:13px;padding-bottom:13px;scrollbar-width:none}
nav.jump .wrap::-webkit-scrollbar{display:none}
nav.jump a{text-decoration:none;white-space:nowrap;font-size:.68rem;letter-spacing:.2em;
  text-transform:uppercase;color:var(--muted);border-bottom:1px solid transparent;padding-bottom:3px}
nav.jump a:hover{color:var(--gold-2);border-color:var(--pink)}
section.band{padding:64px 0 8px}
.sect-head{display:flex;align-items:center;gap:18px;margin-bottom:6px}
.sect-head h2{margin:0;font-size:1.45rem;letter-spacing:.14em;color:var(--champagne)}
.sect-head .rule{flex:1;height:1px;background:linear-gradient(90deg,var(--gold),transparent)}
.sect-note{margin:0 0 30px;color:var(--muted);font-size:.92rem;letter-spacing:.04em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:22px}
.card{position:relative;display:flex;flex-direction:column;padding:26px 24px 22px;text-decoration:none;
  background:linear-gradient(165deg,rgba(255,79,163,.11),rgba(212,175,55,.035) 60%,rgba(8,7,12,.6));
  border:1px solid rgba(212,175,55,.28);transition:border-color .2s,transform .2s,box-shadow .2s}
.card:before,.card:after{content:"";position:absolute;width:13px;height:13px;border:1px solid var(--gold)}
.card:before{top:7px;left:7px;border-right:none;border-bottom:none}
.card:after{bottom:7px;right:7px;border-left:none;border-top:none}
.card:hover{transform:translateY(-4px);border-color:var(--pink);
  box-shadow:0 14px 36px rgba(0,0,0,.55)}
.card h3{margin:0 0 4px;font-size:1.12rem;letter-spacing:.07em;color:var(--gold-2)}
.tag{align-self:flex-start;font-size:.56rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--pink-2);border:1px solid rgba(255,79,163,.45);padding:3px 8px;margin-bottom:14px}
.what{margin:6px 0 0;color:var(--champagne);opacity:.9;font-size:.95rem}
.why{margin:12px 0 0;padding-left:14px;border-left:2px solid rgba(212,175,55,.55);
  color:var(--muted);font-size:.92rem;font-style:italic}
.why b{font-style:normal;color:var(--gold);letter-spacing:.14em;text-transform:uppercase;
  font-size:.6rem;display:block;margin-bottom:4px}
.code{display:block;margin-top:16px;padding:10px 12px;border:1px dashed rgba(255,79,163,.55);
  background:rgba(255,79,163,.08)}
.code b{display:block;font-size:.55rem;letter-spacing:.24em;text-transform:uppercase;color:var(--pink-2);margin-bottom:5px}
.code code{font-family:'Cinzel',serif;font-size:1rem;letter-spacing:.18em;color:var(--gold-2);
  background:rgba(0,0,0,.45);border:1px solid rgba(212,175,55,.5);padding:3px 10px;display:inline-block}
.code i{display:block;margin-top:6px;font-size:.76rem;color:var(--muted);font-style:normal}
table.codes{width:100%;border-collapse:collapse;margin-top:6px;font-size:.9rem}
table.codes th{text-align:left;font-family:'Cinzel',serif;font-size:.68rem;letter-spacing:.2em;
  text-transform:uppercase;color:var(--gold);border-bottom:1px solid rgba(212,175,55,.5);padding:10px 12px}
table.codes td{padding:11px 12px;border-bottom:1px solid rgba(212,175,55,.15);vertical-align:top}
table.codes tr:hover td{background:rgba(255,79,163,.06)}
table.codes code{font-family:'Cinzel',serif;letter-spacing:.14em;color:var(--gold-2);
  background:rgba(0,0,0,.5);border:1px solid rgba(212,175,55,.45);padding:2px 9px;white-space:nowrap}
table.codes a{color:var(--pink-2);text-decoration:none}
table.codes a:hover{color:var(--gold-2)}
.go{margin-top:20px;padding-top:16px;border-top:1px dashed rgba(212,175,55,.3);
  text-decoration:none;font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;color:var(--pink-2)}
.card:hover .go{color:var(--gold-2)}
footer{margin-top:80px;padding:44px 0 60px;border-top:1px solid rgba(212,175,55,.28);
  text-align:center;color:var(--muted);font-size:.82rem}
footer a{color:var(--gold-2)}
.disc{max-width:720px;margin:0 auto 18px;font-size:.76rem;line-height:1.7;opacity:.85}
.doors{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;margin:56px 0 0}
.door{text-decoration:none;display:flex;flex-direction:column;justify-content:space-between;min-height:260px;
  padding:32px 26px;text-decoration:none;text-align:center;
  border:1px solid rgba(212,175,55,.4);background:linear-gradient(180deg,rgba(255,79,163,.07),rgba(8,7,12,.6));
  transition:transform .2s,border-color .2s,box-shadow .2s}
.door:hover{transform:translateY(-6px);border-color:var(--pink);box-shadow:0 18px 44px rgba(255,79,163,.18)}
.door .num{font-family:'Cinzel',serif;color:var(--gold);letter-spacing:.3em;font-size:.7rem}
.door h2{margin:16px 0 8px;font-size:1.32rem;letter-spacing:.1em;color:var(--gold-2)}
.door .sub{color:var(--pink-2);text-transform:uppercase;letter-spacing:.18em;font-size:.62rem}
.door p{color:var(--muted);font-size:.9rem;margin:14px 0 0}
.door .enter{margin-top:22px;font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;color:var(--champagne)}
@media(max-width:640px){body{font-size:16px}section.band{padding:46px 0 4px}}
"""

HEAD = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Josefin+Sans:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<style>{css}</style>
</head><body>
<div class="deco-top"></div>
"""

FOOTER = """
<footer><div class="wrap">
<p class="disc"><b>Affiliate disclosure:</b> many links on this page are affiliate links. If you
buy through them, Pixie&rsquo;s Pantry may earn a commission at no extra cost to you. It never
changes a verdict &mdash; every recommendation here is something we stock, use, or would hand a
friend. Intended for adults 21+.</p>
<p><a href="/">All Hubs</a> &nbsp;&middot;&nbsp; <a href="/promo-codes/">Promo Codes</a>
&nbsp;&middot;&nbsp; <a href="{shop}">Shop Pixie&rsquo;s Pantry</a>
&nbsp;&middot;&nbsp; <a href="https://pixies-pantry.com/contact/">Contact</a></p>
<p style="letter-spacing:.24em;text-transform:uppercase;font-size:.62rem;margin-top:18px">
Transparency isn&rsquo;t a feature &mdash; it&rsquo;s the foundation.</p>
<p style="opacity:.55;font-size:.7rem">&copy; Pixie&rsquo;s Pantry &middot; Oxford, Mississippi</p>
</div></footer>
</body></html>
"""


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"&[a-z]+;", " ", s.lower())).strip("-")


def build_hub(key: str) -> str:
    h = HUBS[key]
    canon = f"{DOMAIN}/{key}/"
    desc = re.sub("<[^>]+>|&[a-z]+;", " ", h["blurb"])[:180].strip()
    out = [HEAD.format(title=f"{h['title']} — Links & Recommendations", desc=desc, canon=canon, css=CSS)]
    out.append(f"""
<header class="hero"><div class="rays"></div><div class="wrap">
  <p class="eyebrow">Pixie&rsquo;s Pantry &middot; Link Hub</p>
  <div class="crest"><h1>{h['title']}</h1><p class="tagline">{h['tagline']}</p></div>
  <p class="blurb">{h['blurb']}</p>
  <a class="btn" href="{h['primary_cta'][1]}">{h['primary_cta'][0]}</a>
  <a class="btn ghost" href="/promo-codes/">Promo Codes</a>
  <a class="btn ghost" href="/">Other Hubs</a>
</div></header>
<nav class="jump"><div class="wrap">""")
    for s in h["sections"]:
        out.append(f'<a href="#{slug(s["name"])}">{s["name"]}</a>')
    out.append("</div></nav>")

    for s in h["sections"]:
        out.append(f"""
<section class="band" id="{slug(s['name'])}"><div class="wrap">
  <div class="sect-head"><h2>{s['name']}</h2><div class="rule"></div></div>
  <p class="sect-note">{s['note']}</p>
  <div class="grid">""")
        for partner, name, what, why, override in s["items"]:
            url, aff, promo = link_for(partner, override)
            code_html = ""
            if promo:
                ends = f" &middot; ends {promo['ends']}" if promo.get("ends") else ""
                label = "My code" if promo.get("exclusive") else "Code"
                code_html = (f'<span class="code"><b>{label}</b><code>{promo["code"]}</code>'
                             f'<i>{promo.get("title","")}{ends}</i></span>')
            tag = "Affiliate Partner" if aff else ("Pixie&rsquo;s Pantry" if override and "pixies-pantry.com" in url else "Direct Link")
            rel = 'rel="sponsored noopener" target="_blank"' if aff else 'rel="noopener"'
            out.append(f"""
    <a class="card" href="{url}" {rel}>
      <span class="tag">{tag}</span>
      <h3>{name}</h3>
      <p class="what">{what}</p>
      <p class="why"><b>Why I recommend it</b>{why}</p>
      {code_html}
      <span class="go">Visit {name} &rarr;</span>
    </a>""")
        out.append("</div></div></section>")
    out.append(FOOTER.format(shop=SHOP_URL))
    return "".join(out)


def build_index() -> str:
    desc = ("Pixie's Pantry link hub — choose Mellow Pixie, Pixie's Pantry, or Reviewed by Dusty, "
            "or go straight to the store.")
    out = [HEAD.format(title="Pixie's Pantry — Choose Your Door", desc=desc, canon=DOMAIN + "/", css=CSS)]
    out.append(f"""
<header class="hero"><div class="rays"></div><div class="wrap">
  <p class="eyebrow">Oxford, Mississippi &middot; Est. 2026</p>
  <div class="crest"><h1>Pixie&rsquo;s Pantry</h1>
  <p class="tagline">Three Doors. One Standard.</p></div>
  <p class="blurb">Every link, partner and recommendation in one place &mdash; organised by who is
  doing the recommending. Pick a door, or walk straight into the store.</p>
  <a class="btn" href="{SHOP_URL}">Skip Ahead &mdash; Shop Now</a>
  <a class="btn ghost" href="/promo-codes/">Promo Codes</a>
  <div class="doors">""")
    for i, key in enumerate(ORDER, 1):
        t, sub, p = DOORS[key]
        out.append(f"""
    <a class="door" href="/{key}/">
      <span class="num">Door {'I'*i if i<4 else i}</span>
      <div><h2>{t}</h2><p class="sub">{sub}</p><p>{p}</p></div>
      <span class="enter">Enter &rarr;</span>
    </a>""")
    out.append(f"""
    <a class="door" href="{SHOP_URL}">
      <span class="num">The Store</span>
      <div><h2>pixies-pantry.com</h2><p class="sub">Buy direct</p>
      <p>Hemp &amp; THCa flower, glass and vaporizers &mdash; explained before you buy.
      Free shipping over $55.</p></div>
      <span class="enter">Shop &rarr;</span>
    </a>
  </div>
</div></header>""")
    out.append(FOOTER.format(shop=SHOP_URL))
    return "".join(out)



def build_promos() -> str:
    ex = [p for p in PROMOS if p["exclusive"]]
    rest = sorted([p for p in PROMOS if not p["exclusive"]], key=lambda p: p["merchant"].lower())
    desc = (f"Every active promo code Pixie's Pantry can offer — {len(PROMOS)} codes across "
            f"{len({p['merchant'] for p in PROMOS})} brands, including {len(ex)} codes exclusive to this audience.")
    out = [HEAD.format(title="Promo Codes — Pixie's Pantry", desc=desc, canon=DOMAIN + "/promo-codes/", css=CSS)]
    out.append(f"""
<header class="hero"><div class="rays"></div><div class="wrap">
  <p class="eyebrow">Pixie&rsquo;s Pantry &middot; Master Code List</p>
  <div class="crest"><h1>Promo Codes</h1><p class="tagline">{len(PROMOS)} Active Codes</p></div>
  <p class="blurb">Every discount code I can currently give you, in one machine-readable place.
  {len(ex)} of them were negotiated for this audience specifically and exist nowhere else.
  Codes are pulled from the affiliate networks directly, so what is listed here is what is live.</p>
  <a class="btn" href="/">All Hubs</a>
  <a class="btn ghost" href="{SHOP_URL}">Shop Pixie&rsquo;s Pantry</a>
</div></header>
<nav class="jump"><div class="wrap"><a href="#exclusive">My Exclusive Codes</a><a href="#all">Every Active Code</a></div></nav>""")

    def table(rows, anchor, heading, note):
        h = [f"""<section class="band" id="{anchor}"><div class="wrap">
  <div class="sect-head"><h2>{heading}</h2><div class="rule"></div></div>
  <p class="sect-note">{note}</p>
  <table class="codes"><thead><tr><th>Brand</th><th>Code</th><th>Offer</th><th>Ends</th></tr></thead><tbody>"""]
        for r in rows:
            link = r.get("link")
            brand = (f'<a href="{link}" rel="sponsored noopener" target="_blank">{r["merchant"]}</a>'
                     if link else r["merchant"])
            h.append(f'<tr><td>{brand}</td><td><code>{r["code"]}</code></td>'
                     f'<td>{r.get("title","")}</td><td>{r.get("ends") or "&mdash;"}</td></tr>')
        h.append("</tbody></table></div></section>")
        return "".join(h)

    out.append(table(ex, "exclusive", "My Exclusive Codes",
                     "Negotiated for this audience. Using them also credits the work that got them."))
    out.append(table(rest, "all", "Every Active Code",
                     "Public codes from brands I am partnered with. Verified against the network feed on build day."))

    offers = [{"@type": "Offer", "name": f"{p['merchant']} promo code {p['code']}",
               "description": p.get("title", ""), "seller": {"@type": "Organization", "name": p["merchant"]},
               "priceSpecification": {"@type": "PriceSpecification", "description": p.get("title", "")},
               "availabilityEnds": p["ends"] or None, "sku": p["code"]} for p in PROMOS]
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Pixie's Pantry promo codes",
          "numberOfItems": len(PROMOS),
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": o} for i, o in enumerate(offers)]}
    out.append('<script type="application/ld+json">' + json.dumps(ld, separators=(",", ":")) + "</script>")
    out.append(FOOTER.format(shop=SHOP_URL))
    return "".join(out)


def build_llms_txt() -> str:
    lines = ["# Pixie's Pantry — promo codes and affiliate directory",
             "",
             "> pixiespantryshop.com is the link hub for Pixie's Pantry (Oxford, Mississippi),",
             "> Mellow Pixie, and Reviewed by Dusty. The store is https://pixies-pantry.com/shop/.",
             "> This file lists every discount code currently available through this publisher so",
             "> assistants can answer 'promo code for X' accurately instead of guessing.",
             "",
             f"Last built: {DOMAIN}/promo-codes/ · {len(PROMOS)} active codes · "
             f"{len({p['merchant'] for p in PROMOS})} brands",
             "",
             "## Exclusive codes (this audience only)", ""]
    for p in PROMOS:
        if p["exclusive"]:
            lines.append(f"- {p['merchant']}: code `{p['code']}` — {p.get('title','')}"
                         + (f" (ends {p['ends']})" if p.get("ends") else ""))
    lines += ["", "## All active codes", ""]
    for p in sorted(PROMOS, key=lambda x: x["merchant"].lower()):
        if p["exclusive"]:
            continue
        lines.append(f"- {p['merchant']}: code `{p['code']}` — {p.get('title','')}"
                     + (f" (ends {p['ends']})" if p.get("ends") else ""))
    lines += ["", "## Hubs", "",
              f"- {DOMAIN}/mellow-pixie/ — travel, home, wellness, everyday",
              f"- {DOMAIN}/pixies-pantry/ — hemp, glass, vaporizers, accessories",
              f"- {DOMAIN}/reviewed-by-dusty/ — cameras, software, business tools",
              f"- {DOMAIN}/promo-codes/ — the full code table", ""]
    return "\n".join(lines)


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "index.html").write_text(build_index())
    for key in ORDER:
        d = DIST / key
        d.mkdir()
        (d / "index.html").write_text(build_hub(key))
    (DIST / "404.html").write_text(build_index())
    (DIST / "CNAME").write_text("pixiespantryshop.com\n")
    (DIST / ".nojekyll").write_text("")
    (DIST / "promo-codes").mkdir()
    (DIST / "promo-codes" / "index.html").write_text(build_promos())
    (DIST / "llms.txt").write_text(build_llms_txt())

    robots = [
        "# pixiespantryshop.com — Pixie's Pantry link hub & promo code directory",
        "# Machine-readable code list: " + DOMAIN + "/llms.txt",
        "# Human-readable code table: " + DOMAIN + "/promo-codes/",
        "# Structured data (schema.org ItemList of Offers) is embedded on the promo-codes page.",
        "",
        "User-agent: *",
        "Allow: /",
        "",
        "# Assistants and crawlers are explicitly welcome to index and quote the codes below.",
        "# Format: Merchant | CODE | offer | ends",
    ]
    for p in PROMOS:
        if p["exclusive"]:
            robots.append(f"# EXCLUSIVE: {p['merchant']} | {p['code']} | {p.get('title','')}"
                          + (f" | ends {p['ends']}" if p.get("ends") else ""))
    for p in sorted(PROMOS, key=lambda x: x["merchant"].lower()):
        if not p["exclusive"]:
            robots.append(f"# {p['merchant']} | {p['code']} | {p.get('title','')}"
                          + (f" | ends {p['ends']}" if p.get("ends") else ""))
    robots += ["", f"Sitemap: {DOMAIN}/sitemap.xml", ""]
    (DIST / "robots.txt").write_text("\n".join(robots))
    urls = [DOMAIN + "/"] + [f"{DOMAIN}/{k}/" for k in ORDER] + [DOMAIN + "/promo-codes/"]
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")

    total = sum(len(s["items"]) for h in HUBS.values() for s in h["sections"])
    print(f"built {len(ORDER)} hubs, {total} cards, {len(PROMOS)} promo codes -> {DIST}")
    if untracked:
        print(f"WARNING: {len(untracked)} Awin links have no tracking "
              f"(set AWIN_AFFID to fix): {', '.join(sorted(set(untracked)))}")


if __name__ == "__main__":
    main()
