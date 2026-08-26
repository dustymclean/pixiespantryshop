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
import datetime as dt
import shutil

import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
import merchant_pages  # noqa: E402
import search as ppsearch  # noqa: E402
from data.content import HUBS, SHOP_URL  # noqa: E402

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
DOMAIN = "https://pixiespantryshop.com"
AWIN_AFFID = os.environ.get("AWIN_AFFID", "").strip()

PARTNERS = {p["name"]: p for p in json.loads((ROOT / "data" / "partners.json").read_text())}
PROMOS = json.loads((ROOT / "data" / "promos.json").read_text())

TODAY = dt.date.today().isoformat()

# Drop anything the network feed says has already ended.
PROMOS = [p for p in PROMOS if not p.get("ends") or p["ends"] >= TODAY]

# Personal codes, each classified and provenance-tracked in data/personal_codes.json.
PERSONAL = json.loads((ROOT / "data" / "personal_codes.json").read_text())
EXTRA_EXCLUSIVE = [
    {"merchant": c["merchant"], "code": c["code"], "exclusive": True,
     "title": c["discount"], "ends": c.get("ends", ""), "link": c.get("link"),
     "status": c["status"], "last_confirmed": c["last_confirmed"],
     "registry_name": c.get("registry_name")}
    for c in PERSONAL if c["publish"]
]

for _e in EXTRA_EXCLUSIVE:
    if not any(x["merchant"] == _e["merchant"] and x["code"] == _e["code"] for x in PROMOS):
        PROMOS.insert(0, _e)

OFFERS = json.loads((ROOT / "data" / "offers.json").read_text())
PARTNER_LIST = json.loads((ROOT / "data" / "partners.json").read_text())
SLUGS = merchant_pages.build_slugs(PARTNER_LIST)
OFFERS_BY_MERCHANT: dict[str, list] = {}
for _o in OFFERS:
    OFFERS_BY_MERCHANT.setdefault(_o["merchant"], []).append(_o)


def merchant_url(name: str) -> str:
    return f"/promo-codes/{SLUGS[name]}/"


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
    for _pc in EXTRA_EXCLUSIVE:
        if _pc.get("registry_name") == partner_name:
            promo = _pc
            break
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

/* ---- merchant promo pages ---- */
nav.crumbs{border-bottom:1px solid rgba(212,175,55,.22);padding:14px 0;font-size:.74rem;
 letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
nav.crumbs a{color:var(--gold)}
main.merch{padding:44px 0 70px;max-width:860px}
main.merch h1{font-family:'Cinzel',serif;font-size:clamp(1.7rem,4.4vw,2.7rem);color:var(--gold-2);
 line-height:1.15;margin:0 0 14px}
main.merch h2{font-family:'Cinzel',serif;font-size:1.12rem;color:var(--gold);margin:38px 0 10px;
 padding-top:16px;border-top:1px solid rgba(212,175,55,.18)}
main.merch p{line-height:1.72;margin:0 0 12px}
main.merch .lede{font-size:1.06rem;color:#f0e6d2}
main.merch .answerbox{border:1px solid rgba(212,175,55,.42);border-left:3px solid #d4af37;
background:linear-gradient(180deg,rgba(212,175,55,.07),rgba(0,0,0,0));padding:.35rem 1.15rem;margin:1.4rem 0 1.8rem}
main.merch .arow{display:flex;gap:1rem;padding:.6rem 0;border-bottom:1px solid rgba(212,175,55,.14);
align-items:baseline;flex-wrap:wrap}
main.merch .arow:last-child{border-bottom:0}
main.merch .ak{flex:0 0 12.5rem;font-family:'Cinzel',serif;font-size:.76rem;letter-spacing:.11em;
text-transform:uppercase;color:#d4af37}
main.merch .av{flex:1 1 14rem;color:#f4ecdd}
main.merch .acode{font-family:'Courier New',monospace;color:#ff5fa2;border:1px dashed #ff5fa2;
border-radius:3px;padding:.12rem .55rem;letter-spacing:.09em;font-weight:700}
@media(max-width:620px){main.merch .ak{flex-basis:100%}}
main.merch .verified{font-size:.78rem;color:var(--muted);letter-spacing:.06em}
.hero-offer{margin:26px 0 8px;padding:26px 24px;border:1px solid var(--gold);border-radius:4px;
 background:linear-gradient(160deg,rgba(255,77,157,.10),rgba(212,175,55,.07));text-align:center;
 position:relative}
.hero-offer:before,.hero-offer:after{content:"";position:absolute;width:16px;height:16px;
 border:2px solid var(--gold-2)}
.hero-offer:before{top:7px;left:7px;border-right:0;border-bottom:0}
.hero-offer:after{bottom:7px;right:7px;border-left:0;border-top:0}
.hero-offer .badge{font-family:'Cinzel',serif;letter-spacing:.22em;text-transform:uppercase;
 font-size:.68rem;color:var(--pink);margin:0 0 10px}
.hero-offer .bigcode{font-family:'Cinzel',serif;font-size:clamp(1.9rem,6vw,2.9rem);color:#fff;
 letter-spacing:.14em;margin:0;text-shadow:0 0 22px rgba(255,77,157,.4)}
.hero-offer .bigoff{font-size:1.25rem;color:var(--gold-2);margin:4px 0 6px;letter-spacing:.04em}
.hero-offer .hmeta{font-size:.76rem;color:var(--muted);margin:0 0 16px}
.hero-offer .hnote{font-size:.78rem;color:var(--muted);margin:14px 0 0;line-height:1.6}
a.cta{display:inline-block;background:var(--pink);color:#1a0010;font-family:'Cinzel',serif;
 letter-spacing:.14em;text-transform:uppercase;font-size:.8rem;padding:13px 26px;border-radius:2px;
 text-decoration:none;font-weight:600}
a.cta:hover{background:var(--gold-2);color:#150f00}
a.cta.small{background:transparent;border:1px solid var(--gold);color:var(--gold-2);font-size:.72rem;
 padding:10px 20px}
a.cta.small:hover{background:var(--gold);color:#120d00}
table.offers{width:100%;border-collapse:collapse;margin:14px 0 6px;font-size:.85rem}
table.offers th{font-family:'Cinzel',serif;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;
 color:var(--gold);text-align:left;padding:8px 10px;border-bottom:1px solid rgba(212,175,55,.3)}
table.offers td{padding:10px;border-bottom:1px solid rgba(255,255,255,.07);vertical-align:top}
table.offers code{color:var(--pink);font-size:.92rem;letter-spacing:.08em}
table.offers .ex{display:inline-block;margin-left:7px;font-size:.56rem;letter-spacing:.14em;
 text-transform:uppercase;color:#1a0010;background:var(--gold-2);padding:2px 6px;border-radius:2px}
.terms{color:var(--muted);font-size:.78rem;line-height:1.5}
ul.cats{list-style:none;padding:0;margin:14px 0;display:flex;flex-wrap:wrap;gap:8px}
ul.cats li{border:1px solid rgba(212,175,55,.34);border-radius:2px;padding:6px 13px;
 font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--gold-2);
 background:rgba(212,175,55,.05)}
ul.sales{list-style:none;padding:0;margin:12px 0}
ul.sales li{padding:11px 0;border-bottom:1px solid rgba(255,255,255,.07);line-height:1.6}
ul.sales a{color:var(--gold-2);text-decoration:none}
ul.sales a:hover{color:var(--pink)}
.smeta{color:var(--muted);font-size:.76rem}
.warn{color:var(--muted);font-size:.82rem}
ul.expired{list-style:none;padding:0;margin:10px 0;opacity:.62;font-size:.82rem}
ul.expired li{padding:7px 0;border-bottom:1px solid rgba(255,255,255,.05)}
.xtag{display:inline-block;font-size:.56rem;letter-spacing:.14em;background:#5a1020;color:#ffb9cd;
 padding:2px 6px;border-radius:2px;margin-right:8px}
.xlinks a{color:var(--gold-2)}
.disclose{margin-top:34px;padding-top:16px;border-top:1px solid rgba(212,175,55,.2);
 font-size:.78rem;color:var(--muted);line-height:1.6}
/* directory */
.dirgrid{columns:3;column-gap:26px;margin:10px 0 0;font-size:.86rem}
.dirgrid a{display:block;padding:4px 0;color:#e8dcc8;text-decoration:none;break-inside:avoid}
.dirgrid a:hover{color:var(--pink)}
.dirgrid .n{color:var(--muted);font-size:.72rem}
.dirletter{font-family:'Cinzel',serif;color:var(--gold);margin:16px 0 4px;letter-spacing:.14em;
 break-after:avoid}
@media(max-width:860px){.dirgrid{columns:2}main.merch h1{font-size:1.55rem}}
@media(max-width:560px){.dirgrid{columns:1}table.offers .terms{display:none}}
.card .golinks{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:auto}
.card a.go{text-decoration:none}
.card a.mp{font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
 text-decoration:none;border-bottom:1px dotted rgba(212,175,55,.5);padding-bottom:1px}
.card a.mp:hover{color:var(--pink)}
table.codes td.conf{font-size:.74rem;color:var(--muted);white-space:nowrap}
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

CSS = CSS + ppsearch.SEARCH_CSS

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
  {ppsearch.search_html(key)}
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
                if promo.get("status", "").startswith("HISTORICALLY"):
                    ends = f" &middot; terms last confirmed {promo['last_confirmed']}"
                code_html = (f'<span class="code"><b>{label}</b><code>{promo["code"]}</code>'
                             f'<i>{promo.get("title","")}{ends}</i></span>')
            tag = "Affiliate Partner" if aff else ("Pixie&rsquo;s Pantry" if override and "pixies-pantry.com" in url else "Direct Link")
            rel = 'rel="sponsored noopener" target="_blank"' if aff else 'rel="noopener"'
            mp = f'<a class="mp" href="{merchant_url(partner)}">Codes &amp; deals</a>' if partner in SLUGS else ""
            out.append(f"""
    <div class="card">
      <span class="tag">{tag}</span>
      <h3>{name}</h3>
      <p class="what">{what}</p>
      <p class="why"><b>Why I recommend it</b>{why}</p>
      {code_html}
      <span class="golinks"><a class="go" href="{url}" {rel}>Visit {name} &rarr;</a>{mp}</span>
    </div>""")
        out.append("</div></div></section>")
    out.append(ppsearch.search_js())
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
  {ppsearch.search_html("home")}
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
    out.append(ppsearch.search_js())
    out.append(FOOTER.format(shop=SHOP_URL))
    return "".join(out)


def build_directory_section() -> str:
    """A-Z index linking every registry partner to its canonical promo page. No orphans."""
    groups: dict[str, list] = {}
    for part in sorted(PARTNER_LIST, key=lambda x: x["name"].lower()):
        c = part["name"][0].upper()
        groups.setdefault(c if c.isalpha() else "#", []).append(part)
    h = ['<section class="band" id="merchants"><div class="wrap">',
         '<div class="sect-head"><h2>Every Partner, A&ndash;Z</h2><div class="rule"></div></div>',
         f'<p class="sect-note">One permanent page per merchant &mdash; {len(PARTNER_LIST)} of them. '
         'Each shows that brand&rsquo;s current codes, current sales, exact terms and last-verified date, '
         'even when there is nothing running.</p>',
         '<div class="dirgrid">']
    for letter in sorted(groups):
        h.append(f'<div class="dirletter">{letter}</div>')
        for part in groups[letter]:
            offs = OFFERS_BY_MERCHANT.get(part["name"], [])
            n = sum(1 for o in offs if o.get("code") and o.get("last_seen") == TODAY
                    and (not o.get("ends") or o["ends"] >= TODAY))
            ex = any(o.get("personal") for o in offs)
            tag = (' <span class="n">&middot; my code</span>' if ex else
                   (f' <span class="n">&middot; {n} code{"s" if n != 1 else ""}</span>' if n else
                    ' <span class="n">&middot; deals</span>'))
            h.append(f'<a href="{merchant_url(part["name"])}">{part["name"]}{tag}</a>')
    h.append('</div></div></section>')
    return "".join(h)


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
  {ppsearch.search_html("promo-codes")}
</div></header>
<nav class="jump"><div class="wrap"><a href="#exclusive">My Exclusive Codes</a><a href="#merchants">Every Partner A&ndash;Z</a><a href="#all">Every Active Code</a></div></nav>""")

    def table(rows, anchor, heading, note):
        h = [f"""<section class="band" id="{anchor}"><div class="wrap">
  <div class="sect-head"><h2>{heading}</h2><div class="rule"></div></div>
  <p class="sect-note">{note}</p>
  <table class="codes"><thead><tr><th>Brand</th><th>Code</th><th>Offer</th><th>Ends</th><th>Confirmed</th></tr></thead><tbody>"""]
        for r in rows:
            link = r.get("link")
            reg = r.get("registry_name") or r["merchant"]
            brand = (f'<a href="{merchant_url(reg)}">{r["merchant"]}</a>' if reg in SLUGS
                     else (f'<a href="{link}" rel="sponsored noopener" target="_blank">{r["merchant"]}</a>'
                           if link else r["merchant"]))
            conf = r.get("last_confirmed") or "network feed"
            if r.get("status", "").startswith("HISTORICALLY"):
                conf = f'{r["last_confirmed"]} &middot; recheck'
            h.append(f'<tr><td>{brand}</td><td><code>{r["code"]}</code></td>'
                     f'<td>{r.get("title","")}</td><td>{r.get("ends") or "&mdash;"}</td>'
                     f'<td class="conf">{conf}</td></tr>')
        h.append("</tbody></table></div></section>")
        return "".join(h)

    out.append(table(ex, "exclusive", "My Exclusive Codes",
                     "Negotiated for this audience. Using them also credits the work that got them."))
    out.append(build_directory_section())
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
    out.append(ppsearch.search_js())
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
    lines += ["", "## Merchant pages (one canonical URL each)", "",
              "Every partner below has a permanent page answering '<brand> promo code',",
              "'<brand> coupon code', '<brand> discount code' and '<brand> deals' with",
              "verified data and a last-verified date. Machine-readable mirror: "
              + DOMAIN + "/promotions.json", ""]
    for part in sorted(PARTNER_LIST, key=lambda x: x["name"].lower()):
        offs = OFFERS_BY_MERCHANT.get(part["name"], [])
        live = [o for o in offs if o.get("last_seen") == TODAY and (not o.get("ends") or o["ends"] >= TODAY)]
        cs = [o["code"] for o in live if o.get("code")]
        ex = [o["code"] for o in live if o.get("personal")]
        state = ("exclusive code " + ", ".join(ex)) if ex else (
            f"{len(cs)} code(s): " + ", ".join(cs[:6]) if cs else (
                f"{len(live)} current deal(s), no code" if live else "no current code or deal"))
        lines.append(f"- {part['name']}: {DOMAIN}/promo-codes/{SLUGS[part['name']]}/ — {state}")
    lines += ["", "## Hubs", "",
              f"- {DOMAIN}/mellow-pixie/ — travel, home, wellness, everyday",
              f"- {DOMAIN}/pixies-pantry/ — hemp, glass, vaporizers, accessories",
              f"- {DOMAIN}/reviewed-by-dusty/ — cameras, software, business tools",
              f"- {DOMAIN}/promo-codes/ — the full code table and A-Z merchant index",
              f"- {DOMAIN}/promotions.json — full machine-readable offer database", ""]
    return "\n".join(lines)


class _Ctx:
    """Everything merchant_pages needs from the main build."""
    HEAD = None; FOOTER = None; CSS = None
    DOMAIN = DOMAIN; SHOP_URL = SHOP_URL

    @staticmethod
    def hubs_for(name: str):
        out = []
        for key in ORDER:
            for sec in HUBS[key]["sections"]:
                if any(i[0] == name for i in sec["items"]):
                    out.append((key, HUBS[key]["title"]))
                    break
        return out


def build_merchant_pages() -> list[tuple[str, str]]:
    """Write one canonical page per registry partner. Returns [(slug, name)]."""
    _Ctx.HEAD, _Ctx.FOOTER, _Ctx.CSS = HEAD, FOOTER, CSS
    root = DIST / "promo-codes"
    made = []
    for part in PARTNER_LIST:
        sl = SLUGS[part["name"]]
        d = root / sl
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            merchant_pages.build_merchant_page(
                part, OFFERS_BY_MERCHANT.get(part["name"], []), sl, _Ctx))
        made.append((sl, part["name"]))
    return made


def build_promotions_json() -> dict:
    """Machine-readable database. Must agree exactly with the rendered pages."""
    out = []
    for part in PARTNER_LIST:
        name = part["name"]
        offs = OFFERS_BY_MERCHANT.get(name, [])
        live = [o for o in offs if o.get("last_seen") == TODAY and (not o.get("ends") or o["ends"] >= TODAY)]
        rec = {
            "merchant": name,
            "page": f"{DOMAIN}/promo-codes/{SLUGS[name]}/",
            "network": part.get("network"),
            "tracked_url": part.get("link") or part.get("url"),
            "last_verified": TODAY,
            "offers": [],
        }
        for o in offs:
            active = o in live
            rec["offers"].append({
                "code": o.get("code"),
                "type": "code" if o.get("code") else "sale",
                "discount": o.get("title") or None,
                "restrictions": o.get("terms") or o.get("description") or None,
                "starts": o.get("starts") or None,
                "ends": o.get("ends") or None,
                "verified": o.get("last_confirmed") or o.get("last_seen"),
                "source": o.get("source"),
                "network": o.get("network"),
                "exclusive": bool(o.get("personal")),
                "status": "ACTIVE" if active else "EXPIRED",
                "link": o.get("link") or part.get("link"),
            })
        out.append(rec)
    return {
        "generated": TODAY,
        "publisher": "pixiespantryshop.com",
        "note": ("One canonical page per merchant at /promo-codes/<slug>/. "
                 "Codes marked exclusive:true are assigned to this publisher's affiliate account. "
                 "Nothing here is invented: every offer traces to an affiliate network feed or a "
                 "dated merchant confirmation."),
        "partners": len(out),
        "merchants": out,
    }


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
    made = build_merchant_pages()
    (DIST / "promotions.json").write_text(json.dumps(build_promotions_json(), indent=1))
    (DIST / "llms.txt").write_text(build_llms_txt())

    # Visitor search index, generated from the same registry as the merchant pages.
    _idx = ppsearch.build_index(PARTNER_LIST, PROMOS, OFFERS_BY_MERCHANT, SLUGS, PERSONAL, HUBS)
    (DIST / "search-index.json").write_text(json.dumps(_idx, separators=(",", ":")))
    print(f"  search index: {len(_idx)} merchants, "
          f"{sum(len(m['cd']) for m in _idx)} codes, "
          f"{len(json.dumps(_idx, separators=(',', ':')))//1024} KB")

    robots = [
        "# pixiespantryshop.com — Pixie's Pantry link hub & promo code directory",
        "# Machine-readable code list: " + DOMAIN + "/llms.txt",
        "# Human-readable code table: " + DOMAIN + "/promo-codes/",
        "# Machine-readable offer database: " + DOMAIN + "/promotions.json",
        "# One canonical page per merchant: " + DOMAIN + "/promo-codes/<merchant-slug>/",
        f"# {len(PARTNER_LIST)} merchant pages, all listed in the sitemap.",
        "# Structured data (schema.org FAQPage + ItemList of Offers) is embedded on every merchant page.",
        "",
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {DOMAIN}/sitemap.xml",
        "",]
    for _bot in ("Googlebot", "Googlebot-Image", "Google-Extended", "bingbot", "OAI-SearchBot",
                 "GPTBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "anthropic-ai",
                 "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended",
                 "Amazonbot", "DuckDuckBot", "meta-externalagent", "CCBot", "Bytespider"):
        robots += [f"User-agent: {_bot}", "Allow: /", ""]
    robots += [
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
    robots += [""]
    (DIST / "robots.txt").write_text("\n".join(robots))

    # Google Search Console site verification (URL-prefix property).
    # Must survive every rebuild or the property silently loses verification.
    GSC_TOKEN = "google7aa59ca628135813.html"
    (DIST / GSC_TOKEN).write_text(f"google-site-verification: {GSC_TOKEN}\n")
    # IndexNow key file. Must be publicly reachable at the domain root or every
    # IndexNow submission is rejected with 403. Regenerated on every build.
    _ink = (ROOT / "data" / "indexnow_key.txt").read_text().strip()
    (DIST / f"{_ink}.txt").write_text(_ink + "\n")

    urls = ([(DOMAIN + "/", "1.0")]
            + [(f"{DOMAIN}/{k}/", "0.9") for k in ORDER]
            + [(DOMAIN + "/promo-codes/", "0.9")]
            + [(f"{DOMAIN}/promo-codes/{sl}/", "0.8") for sl, _ in sorted(made)])
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n"
                  for u, pr in urls) + "</urlset>\n")
    print(f"  {len(made)} merchant pages, {len(urls)} sitemap URLs")

    total = sum(len(s["items"]) for h in HUBS.values() for s in h["sections"])
    print(f"built {len(ORDER)} hubs, {total} cards, {len(PROMOS)} promo codes -> {DIST}")
    if untracked:
        print(f"WARNING: {len(untracked)} Awin links have no tracking "
              f"(set AWIN_AFFID to fix): {', '.join(sorted(set(untracked)))}")


if __name__ == "__main__":
    main()
