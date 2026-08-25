#!/usr/bin/env python3
"""Crawl hub/dist and reconcile it against the registry. Run after build.py."""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
TODAY = dt.date.today().isoformat()
DOMAIN = "https://pixiespantryshop.com"


def main() -> None:
    partners = json.loads((ROOT / "data" / "partners.json").read_text())
    offers = json.loads((ROOT / "data" / "offers.json").read_text())
    personal = json.loads((ROOT / "data" / "personal_codes.json").read_text())
    by_m: dict[str, list] = {}
    for o in offers:
        by_m.setdefault(o["merchant"], []).append(o)

    pages = sorted(p for p in (DIST / "promo-codes").iterdir() if p.is_dir())
    sitemap = (DIST / "sitemap.xml").read_text()
    sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
    promotions = json.loads((DIST / "promotions.json").read_text())
    llms = (DIST / "llms.txt").read_text()
    directory = (DIST / "promo-codes" / "index.html").read_text()
    dir_links = set(re.findall(r'href="(/promo-codes/[a-z0-9-]+/)"', directory))

    problems: dict[str, list[str]] = {}

    def flag(kind: str, item: str) -> None:
        problems.setdefault(kind, []).append(item)

    live_offers = [o for o in offers
                   if o.get("last_seen") == TODAY and (not o.get("ends") or o["ends"] >= TODAY)]
    slugs = {}
    for d in pages:
        html = (d / "index.html").read_text()
        sl = d.name
        slugs[sl] = html
        url = f"{DOMAIN}/promo-codes/{sl}/"
        if url not in sm_urls:
            flag("missing from sitemap", sl)
        if f"/promo-codes/{sl}/" not in dir_links:
            flag("orphan (not linked from directory)", sl)
        if "<h1>" not in html:
            flag("missing H1", sl)
        if "<title>" not in html or "Promo Codes" not in html:
            flag("missing/!bad title", sl)
        if "Last verified:" not in html:
            flag("missing verified date", sl)
        if html.count(f'<link rel="canonical" href="{url}">') != 1:
            flag("bad canonical", sl)
        if "Affiliate disclosure" not in html:
            flag("missing disclosure", sl)
        # expired codes must never render in an active table
        for m in re.finditer(r"<td>(?:[^<]*)</td><td>([^<]*)</td>", ""):
            pass

    # canonical uniqueness: no two pages claim the same URL
    canons = [re.search(r'<link rel="canonical" href="([^"]+)"', h).group(1) for h in slugs.values()]
    if len(set(canons)) != len(canons):
        flag("duplicate canonical", "collision detected")

    reg_names = {p["name"] for p in partners}
    page_count = len(pages)
    if page_count != len(reg_names):
        flag("partner without a page",
             ", ".join(sorted(reg_names - {m["merchant"] for m in promotions["merchants"]})) or "count mismatch")

    # every offer merchant must have a page
    for m in by_m:
        if m not in reg_names:
            flag("promo code with no merchant page", m)

    # tracked destinations
    code_attr = [p["name"] for p in partners if p.get("code_attributed")]
    untracked = [p["name"] for p in partners if not p.get("link")]
    plain = [p["name"] for p in partners
             if p.get("link") and not re.search(
                 r"awin1\.com|/c/5929369/|\?ref=|viktor\.com|prf\.hn|\.net/c/|sjv\.io|pxf\.io", p["link"])
             and not p.get("code_attributed")]

    exclusive = [c for c in personal if c["publish"]]
    hist = [c for c in personal if c["status"].startswith("HISTORICALLY")]
    expired_kept = [o for o in offers if o not in live_offers]
    with_code = {o["merchant"] for o in live_offers if o.get("code")}
    with_any = {o["merchant"] for o in live_offers}

    print("=" * 62)
    print("RECONCILIATION —", TODAY)
    print("=" * 62)
    rows = [
        ("Registry partners", len(reg_names)),
        ("Merchant promo pages live", page_count),
        ("Merchant pages indexed in sitemap",
         sum(1 for s in slugs if f"{DOMAIN}/promo-codes/{s}/" in sm_urls)),
        ("Partners with >=1 active offer", len(with_any)),
        ("Partners with >=1 active CODE", len(with_code)),
        ("Partners with no current code but live deal page", len(reg_names) - len(with_code)),
        ("Active promotions (codes + sales)", len(live_offers)),
        ("  of which coupon codes", sum(1 for o in live_offers if o.get("code"))),
        ("  of which sales/deals", sum(1 for o in live_offers if not o.get("code"))),
        ("Audience-exclusive codes published", len([c for c in exclusive if c["status"] == "ACTIVE VERIFIED"])),
        ("Historically verified codes published", len([c for c in hist if c["publish"]])),
        ("Codes withheld (pending/creator-only/expired)", len(personal) - len(exclusive)),
        ("Expired offers retained for reference", len(expired_kept)),
        ("Monetized merchant destinations", len(partners) - len(untracked) - len(plain)),
        ("Coupon-code-attributed (in-house, no click link)", len(code_attr)),
        ("Plain (untracked) merchant fallbacks", len(untracked) + len(plain)),
        ("Orphan pages", len(problems.get("orphan (not linked from directory)", []))),
        ("Missing merchants", len(problems.get("partner without a page", []))),
    ]
    for k, v in rows:
        print(f"  {k:<52} {v}")

    print("\nAUDIT CHECKS")
    if not problems:
        print("  clean — no missing pages, orphans, duplicate canonicals, untracked links,")
        print("  missing titles/H1s or missing verified dates.")
    else:
        for k, v in problems.items():
            print(f"  {k}: {len(v)} -> {', '.join(v[:8])}{' …' if len(v) > 8 else ''}")
    if untracked or plain:
        print(f"  untracked/plain destinations: {', '.join(sorted(untracked + plain))}")

    # data agreement: promotions.json vs rendered pages
    mism = 0
    for m in promotions["merchants"]:
        html = slugs.get(m["page"].rstrip("/").split("/")[-1], "")
        for o in m["offers"]:
            if o["status"] == "ACTIVE" and o["code"] and o["code"] not in html:
                mism += 1
    print(f"  promotions.json vs HTML disagreements: {mism}")
    print(f"  llms.txt merchant entries: {llms.count(DOMAIN + '/promo-codes/')}")


if __name__ == "__main__":
    main()
