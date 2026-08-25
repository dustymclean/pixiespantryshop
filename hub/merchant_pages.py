#!/usr/bin/env python3
"""Generate one canonical promo-code page per registry partner.

One merchant = one permanent URL: /promo-codes/<slug>/
Never invents an offer. If a merchant has no verified code, the page says so plainly
and shows whatever sales/deals can actually be verified instead.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path
from data.deep_dives import DEEP_DIVES
from pathlib import Path

TODAY = dt.date.today()
TODAY_S = TODAY.isoformat()
MONTH_YEAR = TODAY.strftime("%B %Y")
NICE_TODAY = TODAY.strftime("%B %-d, %Y")


def slugify(s: str) -> str:
    s = re.sub(r"&[a-z]+;", " ", s.lower())
    s = s.replace("&", " and ")
    s = re.sub(r"\b(us|usa|uk|inc|ltd|llc|limited|co)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "merchant"


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def nice(d: str) -> str:
    try:
        return dt.date.fromisoformat(d).strftime("%B %-d, %Y")
    except Exception:
        return d or ""


def is_live(o: dict) -> bool:
    return not o.get("ends") or o["ends"] >= TODAY_S


def build_slugs(partners: list[dict]) -> dict[str, str]:
    """Stable, unique slug per partner name. One canonical URL each."""
    slugs, used = {}, {}
    for p in sorted(partners, key=lambda x: x["name"].lower()):
        base = slugify(p["name"])
        s = base
        n = 2
        while s in used:
            s = f"{base}-{n}"
            n += 1
        used[s] = p["name"]
        slugs[p["name"]] = s
    return slugs


# ---------------------------------------------------------------- copy helpers

def first_sentences(text: str, limit: int = 460) -> str:
    """Trim a merchant description to whole sentences, stripping recruitment fluff."""
    t = re.sub(r"\s+", " ", (text or "")).strip()
    t = re.sub(r"(?i)(join|earn|sign up for|apply to|partner with)[^.]*affiliate program[^.]*\.?", "", t)
    t = re.sub(r"(?i)^\W*(who we are|about us)\W*", "", t).strip()
    if len(t) <= limit:
        return t
    cut = t[:limit]
    dot = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return (cut[:dot + 1] if dot > 120 else cut.rstrip() + "\u2026").strip()


AUDIENCE = {
    "Vaporizers": "anyone shopping for dry herb or concentrate hardware",
    "Glass & Accessories": "smokers replacing glass, grinders or cleaning supplies",
    "Fashion & Apparel": "shoppers refreshing a wardrobe without paying full retail",
    "Outdoors & Camping": "campers, overlanders and anyone kitting out a vehicle",
    "Consumer Electronics": "buyers comparing budget gadgets against name brands",
    "Business & Software": "operators and creators automating a workload",
    "Home & Garden": "anyone furnishing, repairing or upgrading a home",
    "Travel": "travellers booking flights, stays or connectivity",
    "Health & Beauty": "shoppers restocking supplements, skincare or wellness gear",
}


def audience_line(p: dict, sector: str) -> str:
    for k, v in AUDIENCE.items():
        if sector and (k.lower() in sector.lower() or sector.lower() in k.lower()):
            return v
    if sector:
        return f"shoppers in the {sector.lower().rstrip('.')} category"
    return "shoppers comparing prices before checking out"


try:
    FACTS = json.loads((Path(__file__).parent / "data" / "merchant_facts.json").read_text())
except Exception:
    FACTS = {}


def fact_block(name: str, disp: str) -> list[str]:
    """Render facts observed on the merchant's own storefront. Observation only:
    anything not actually seen on the site is omitted rather than guessed."""
    f = FACTS.get(name) or {}
    if f.get("status") != 200:
        return []
    out, rows = [], []
    when = nice(f.get("checked", "")) or f.get("checked", "")

    cats = f.get("categories") or []
    if cats:
        out.append(f'<h2>What {esc(disp)} sells</h2>')
        out.append(f'<p>These are the product categories {esc(disp)} lists in its own storefront '
                   f'navigation, which is the clearest signal of what a code will actually apply to:</p>')
        out.append('<ul class="cats">' + "".join(f'<li>{esc(c)}</li>' for c in cats) + '</ul>')

    if f.get("free_shipping_over"):
        rows.append(("Free shipping", f'On orders over ${f["free_shipping_over"]}'))
    elif f.get("free_shipping_all"):
        rows.append(("Free shipping", "Advertised on all orders"))
    if f.get("returns_days"):
        rows.append(("Returns window", f'{f["returns_days"]} days'))
    if f.get("warranty_years"):
        rows.append(("Warranty", f'{f["warranty_years"]}-year warranty advertised'))
    if f.get("platform"):
        rows.append(("Checkout platform", esc(f["platform"])))
    if f.get("one_code_per_order"):
        rows.append(("Code stacking", "One discount code per order \u2014 codes do not stack"))

    if rows:
        out.append(f'<h2>{esc(disp)} shipping, returns and code stacking</h2>')
        out.append('<table class="offers"><tbody>' + "".join(
            f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in rows) + '</tbody></table>')
        out.append(f'<p class="terms">Observed directly on the {esc(disp)} storefront on {esc(when)}. '
                   f'Merchants change these without notice \u2014 confirm at checkout.</p>')

    if f.get("platform") in ("Shopify", "WooCommerce", "BigCommerce"):
        where = {"Shopify": "the <b>Discount code</b> box on the checkout page, to the right of the order "
                            "summary \u2014 not on the cart page",
                 "WooCommerce": "the <b>Apply coupon</b> link at the top of the cart page, which expands "
                                "into a code field",
                 "BigCommerce": "the <b>Coupon code</b> or <b>Gift certificate</b> field in the cart "
                                "summary"}[f["platform"]]
        out.append(f'<p><b>Where the code goes:</b> {esc(disp)} runs on {esc(f["platform"])}, so the code '
                   f'goes in {where}. The order total should drop before you reach the payment step.</p>')
    return out


DISC_RE = re.compile(r"(\d{1,3})\s*%|\$\s*(\d{1,4})")


def strength(o: dict) -> float:
    """Rough ranking so the biggest verified discount leads the list."""
    m = DISC_RE.search(o.get("title") or "")
    if not m:
        return 0.0
    return float(m.group(1)) if m.group(1) else float(m.group(2)) / 3.0


def how_to_use(name: str, has_code: bool, tracked: bool, referral: bool = False) -> str:
    if referral:
        return (f"There is no code to enter. Use the tracked signup link on this page and the referral is "
                f"recorded automatically when you create the account. If {esc(name)} later issues an actual "
                f"promo code or signup credit, it will appear here.")
    if has_code:
        return (f"Click through to {esc(name)} from this page, add what you want to the cart, then paste the "
                f"code into the discount or promo field at checkout and apply it before paying. Confirm the "
                f"total actually drops before you complete the order.")
    return (f"There is no code to enter right now. Click through to {esc(name)} from this page and the "
            f"current sale pricing applies automatically at checkout"
            + (" \u2014 the link is tracked, which is what supports this site." if tracked else "."))


TROUBLESHOOT = (
    "If a code is rejected, it is almost always one of four things: the offer has ended since it was last "
    "verified, your cart is under the minimum spend, the items are excluded (sale items and new releases "
    "usually are), or another discount is already applied and the store only allows one. Try it on a clean "
    "cart first. Codes are re-checked against the network feeds every week and anything dead is moved down "
    "to the expired section rather than left sitting at the top of the page."
)


# ---------------------------------------------------------------- page builder

def build_merchant_page(p: dict, offers: list[dict], slug: str, ctx) -> str:
    """ctx supplies HEAD/FOOTER/CSS/DOMAIN/SHOP_URL and hub back-links."""
    name = p["name"]
    disp = re.sub(r"\s+(US|USA|UK)$", "", name).strip()
    canon = f"{ctx.DOMAIN}/promo-codes/{slug}/"
    tracked = p.get("link") or p.get("url") or ctx.SHOP_URL
    is_tracked = bool(p.get("link"))
    referral = bool(p.get("referral"))
    shop_label = p.get("cta") or f"Shop {disp} \u2192"

    live = [o for o in offers if is_live(o) and o.get("last_seen") == TODAY_S]
    dead = [o for o in offers if o not in live]
    codes = [o for o in live if o.get("code")]
    sales = [o for o in live if not o.get("code")]
    codes.sort(key=strength, reverse=True)
    hero = next((o for o in codes if o.get("personal")), None)
    if hero:
        codes = [o for o in codes if o is not hero]

    n_codes = len(codes) + (1 if hero else 0)
    if hero:
        summary = (f"{disp} promo code {hero['code']} gets you {hero['title']}, verified "
                   f"{nice(hero['last_confirmed'])}.")
    elif codes:
        best = codes[0]
        summary = (f"{n_codes} verified {disp} promo code{'s' if n_codes != 1 else ''} "
                   f"as of {NICE_TODAY}, including {best['code']}.")
    elif sales:
        summary = (f"No verified {disp} coupon code is available through my partner account right now. "
                   f"{len(sales)} current {disp} deal{'s' if len(sales) != 1 else ''} verified {NICE_TODAY}.")
    else:
        summary = ((f"{disp} has no promo code \u2014 my {disp} referral link is the tracked way in, "
                    f"verified {NICE_TODAY}.") if referral else
                   (f"No verified {disp} promo code or current deal through my partner account as of "
                    f"{NICE_TODAY}. This page updates as offers appear."))

    title = f"{disp} Promo Codes & Coupons \u2014 Updated {MONTH_YEAR}"
    meta = summary[:180]

    h = [ctx.HEAD.format(title=esc(title), desc=esc(meta), canon=canon, css=ctx.CSS)]
    h.append(f'''<nav class="crumbs"><div class="wrap"><a href="/">Home</a> &rsaquo;
<a href="/promo-codes/">Promo Codes</a> &rsaquo; <span>{esc(disp)}</span></div></nav>''')
    h.append('<main class="wrap merch">')
    h.append(f'<h1>{esc(disp)} Promo Codes, Coupons &amp; Deals</h1>')
    h.append(f'<p class="lede">{esc(summary)}</p>')
    h.append(f'<p class="verified">Last verified: <b>{NICE_TODAY}</b> &nbsp;&middot;&nbsp; '
             f'Network: {esc(p.get("network") or "direct")}</p>')

    # ---- extractable direct-answer block (visible HTML, key/value, near the top)
    def _row(k, v):
        return f'<div class="arow"><span class="ak">{esc(k)}</span><span class="av">{v}</span></div>'

    ab = []
    if referral:
        ab.append(_row(f"Current {disp} promo code",
                       "No verified coupon code &mdash; this is a referral link, not a coupon."))
        ab.append(_row("Referral link",
                       f'<a href="{esc(tracked)}" rel="sponsored nofollow noopener" target="_blank">{esc(tracked)}</a>'))
    elif hero:
        exp_txt = ("No published expiration found" if hero.get("no_expiry")
                   else (nice(hero["ends"]) if hero.get("ends") else "No published expiration found"))
        ab.append(_row(f"Current {disp} promo code", f'<code class="acode">{esc(hero["code"])}</code>'))
        ab.append(_row("Discount", esc(hero["title"])))
        ab.append(_row("Verified", nice(hero["last_confirmed"])))
        ab.append(_row("Expiration", esc(exp_txt)))
        if hero.get("attributable"):
            ab.append(_row("Affiliate attribution", "code-based attribution confirmed"))
    elif codes:
        best = codes[0]
        ab.append(_row(f"Current {disp} promo code", f'<code class="acode">{esc(best["code"])}</code>'))
        if best.get("title"):
            ab.append(_row("Discount", esc(best["title"])))
        ab.append(_row("Verified", NICE_TODAY))
        ab.append(_row("Expiration", nice(best["ends"]) if best.get("ends") else "No published expiration found"))
        if len(codes) > 1:
            ab.append(_row("Other verified codes", f'{len(codes) - 1} more listed below'))
    else:
        ab.append(_row(f"Current {disp} promo code",
                       "No verified coupon is currently available through my partner account."))
        if sales:
            ab.append(_row("Current deal", esc(sales[0].get("title") or "See verified deals below")))
            if sales[0].get("ends"):
                ab.append(_row("Deal ends", nice(sales[0]["ends"])))
        ab.append(_row("Last checked", NICE_TODAY))
    h.append('<section class="answerbox">' + "".join(ab) + '</section>')

    # ---- hero (audience-exclusive code wins the page)
    if hero:
        exp = ("No published expiration found \u2014 currently active" if hero.get("no_expiry")
               else (f"Expires {nice(hero['ends'])}" if hero.get("ends") else "No published expiration found"))
        h.append(f'''<section class="hero-offer">
<p class="badge">Reviewed by Dusty &middot; Audience Exclusive</p>
<p class="bigcode">{esc(hero["code"])}</p>
<p class="bigoff">{esc(hero["title"])}</p>
<p class="hmeta">Verified {nice(hero["last_confirmed"])} &middot; {esc(exp)}</p>
<p><a class="cta" href="{esc(hero.get("link") or tracked)}" rel="sponsored nofollow noopener"
 target="_blank">Use code {esc(hero["code"])} &rarr; Shop {esc(disp)}</a></p>
<p class="hnote">This code is assigned to my affiliate account, so it credits the partnership whether you
click my link or just type the code at checkout. Source: {esc(hero["source"])}.</p>
</section>''')

    # ---- direct answer block
    h.append(f'<h2>What is the current {esc(disp)} promo code?</h2>')
    if hero:
        h.append(f'<p>The best {esc(disp)} code I can verify is <code>{esc(hero["code"])}</code> for '
                 f'{esc(hero["title"])}. It is exclusive to my audience rather than a public sitewide code, '
                 f'and it was confirmed on {nice(hero["last_confirmed"])}.'
                 + (f' There {"are" if len(codes)>1 else "is"} also {len(codes)} public '
                    f'{esc(disp)} offer{"s" if len(codes)!=1 else ""} listed below.' if codes else '') + '</p>')
    elif codes:
        h.append(f'<p>Yes \u2014 {esc(disp)} currently has {len(codes)} verified '
                 f'code{"s" if len(codes) != 1 else ""} running through my affiliate relationship. '
                 f'The strongest one right now is <code>{esc(codes[0]["code"])}</code>'
                 + (f' ({esc(codes[0]["title"])})' if codes[0].get("title") else '')
                 + f'. All of them are listed below with their exact terms and end dates. I do not have a '
                   f'personal {esc(disp)} code assigned to me at the moment.</p>')
    elif sales:
        h.append(f'<p><b>No verified {esc(disp)} coupon code is currently available through my partner '
                 f'account.</b> These are the {esc(disp)} offers and sales I can currently verify instead. '
                 f'I would rather tell you that than publish a code that fails at checkout.</p>')
    else:
        if referral:
            h.append(f'<p><b>There is no {esc(disp)} promo code or percentage discount that I can verify.</b> '
                     f'What I do have is a tracked referral link. {p.get("referral_note","")}</p>')
            h.append(f'<table class="offers"><tbody>'
                     f'<tr><th>Referral link</th><td><a href="{esc(tracked)}" rel="sponsored nofollow noopener" '
                     f'target="_blank">{esc(tracked)}</a></td></tr>'
                     f'<tr><th>Promo code</th><td>None currently verified</td></tr>'
                     f'<tr><th>Last verified</th><td>{NICE_TODAY}</td></tr></tbody></table>')
        else:
            h.append(f'<p><b>No verified {esc(disp)} coupon code or current sale is available through my partner '
                     f'account as of {NICE_TODAY}.</b> I am partnered with {esc(disp)}, so this page updates '
                     f'automatically the moment they run an offer \u2014 it is re-checked against the network '
                     f'feed every week. I am not going to invent a code so the page looks busier.</p>')

    # ---- current codes table
    if codes:
        h.append(f'<h2>Current {esc(disp)} coupon codes</h2>')
        h.append('<table class="offers"><thead><tr><th>Code</th><th>Discount</th><th>Restrictions</th>'
                 '<th>Ends</th><th>Verified</th></tr></thead><tbody>')
        for o in codes:
            terms = o.get("terms") or o.get("description") or "\u2014"
            h.append(f'<tr><td><code>{esc(o["code"])}</code>'
                     + ('<span class="ex">exclusive</span>' if o.get("exclusive") else '')
                     + f'</td><td>{esc(o.get("title") or "See merchant")}</td>'
                     f'<td class="terms">{esc(terms[:220])}</td>'
                     f'<td>{nice(o.get("ends")) or "no end date"}</td>'
                     f'<td>{NICE_TODAY}</td></tr>')
        h.append('</tbody></table>')
        h.append(f'<p><a class="cta small" href="{esc(tracked)}" rel="sponsored nofollow noopener" '
                 f'target="_blank">Shop {esc(disp)} &rarr;</a></p>')

    # ---- current sales
    if sales:
        h.append(f'<h2>Current {esc(disp)} sales and deals</h2>')
        h.append('<ul class="sales">')
        for o in sales[:20]:
            end = f' &middot; ends {nice(o["ends"])}' if o.get("ends") else ""
            body = o.get("description") or o.get("terms") or ""
            h.append(f'<li><a href="{esc(o.get("link") or tracked)}" rel="sponsored nofollow noopener" '
                     f'target="_blank">{esc(o.get("title") or "Current offer")}</a>'
                     f'<span class="smeta">{end}</span>'
                     + (f'<br><span class="terms">{esc(body[:200])}</span>' if body else '') + '</li>')
        h.append('</ul>')

    if not codes and not sales and not hero:
        h.append(f'<p><a class="cta small" href="{esc(tracked)}" rel="sponsored nofollow noopener" '
                 f'target="_blank">{esc(shop_label)}</a></p>')

    # ---- about
    desc = first_sentences(p.get("desc", ""))
    h.append(f'<h2>What is {esc(disp)}?</h2>')
    if desc:
        h.append(f'<p>{esc(desc)}</p>')
    else:
        h.append(f'<p>{esc(disp)} is a merchant I am partnered with through '
                 f'{esc(p.get("network") or "a direct affiliate relationship")}. '
                 f'The offers above come straight from that relationship.</p>')
    sector = p.get("sector") or ""
    h.append(f'<p><b>Who these {esc(disp)} offers are useful for:</b> {esc(audience_line(p, sector))}.'
             + (f' Category: {esc(sector)}.' if sector else '') + '</p>')

    for _dh, _dbody in DEEP_DIVES.get(name, []):
        h.append(f'<h2>{esc(_dh)}</h2>')
        h.append(_dbody)

    h.extend(fact_block(name, disp))

    # ---- how to use / troubleshooting
    h.append(f'<h2>How to use the {esc(disp)} referral link</h2>' if referral
             else f'<h2>How to use a {esc(disp)} promo code</h2>')
    h.append(f'<p>{how_to_use(disp, bool(codes or hero), is_tracked, referral)}</p>')
    h.append(f'<h2>Why isn&rsquo;t my {esc(disp)} coupon working?</h2>')
    h.append(f'<p>{TROUBLESHOOT}</p>')

    # ---- expired
    if dead:
        h.append('<h2>Previous / expired promo codes</h2>')
        h.append('<p class="warn">These are kept for reference. <b>They are expired and will not '
                 'work.</b></p><ul class="expired">')
        for o in sorted(dead, key=lambda x: x.get("ends") or "", reverse=True)[:25]:
            lbl = f'{o["code"]}' if o.get("code") else (o.get("title") or "offer")
            when = nice(o.get("ends")) or f'last seen {nice(o.get("last_seen"))}'
            h.append(f'<li><span class="xtag">EXPIRED</span> <code>{esc(lbl)}</code> '
                     f'&mdash; {esc(o.get("title") or "")} &middot; ended {esc(when)}</li>')
        h.append('</ul>')

    # ---- internal links, no orphans
    hubs = ctx.hubs_for(name)
    links = " ".join(f'<a href="/{k}/">{esc(v)}</a>' for k, v in hubs)
    h.append('<h2>More from Pixie&rsquo;s Pantry</h2><p class="xlinks">'
             + (f'{esc(disp)} is recommended on: {links} &nbsp;&middot;&nbsp; ' if hubs else '')
             + '<a href="/promo-codes/">All promo codes</a> &nbsp;&middot;&nbsp; '
               f'<a href="{ctx.SHOP_URL}">Shop Pixie&rsquo;s Pantry</a></p>')

    h.append(f'<p class="disclose"><b>Affiliate disclosure:</b> the {esc(disp)} links on this page are '
             f'affiliate links. If you buy through them I may earn a commission at no extra cost to you. '
             f'It never changes what I say about a product, and I do not publish codes I cannot verify.</p>')
    h.append('</main>')

    # ---- structured data: agrees exactly with the visible page
    offers_ld = []
    for o in ([hero] if hero else []) + codes:
        ld = {"@type": "Offer", "name": o.get("title") or f"{disp} promo code",
              "seller": {"@type": "Organization", "name": disp},
              "url": canon, "availability": "https://schema.org/InStock"}
        if o.get("ends"):
            ld["priceValidUntil"] = o["ends"]
        offers_ld.append(ld)
    faq = [
        (f"What is the current {disp} promo code?",
         (f"{hero['code']} \u2014 {hero['title']}, verified {nice(hero['last_confirmed'])}." if hero else
          (f"{codes[0]['code']} \u2014 {codes[0].get('title') or 'see merchant for details'}." if codes else
           f"No verified {disp} promo code is currently available through this partner account."))),
        (f"Does {disp} have a coupon right now?",
         (f"Yes \u2014 {n_codes} verified code{'s' if n_codes != 1 else ''} as of {NICE_TODAY}." if n_codes else
          (f"No verified code, but {len(sales)} current deal{'s' if len(sales) != 1 else ''} as of {NICE_TODAY}."
           if sales else f"No verified {disp} coupon or deal as of {NICE_TODAY}."))),
        (f"How do I use a {disp} promo code?", re.sub("<[^>]+>", "", how_to_use(disp, bool(codes or hero), is_tracked))),
        (f"Why isn't my {disp} coupon working?", TROUBLESHOOT),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "url": canon, "name": title, "description": meta,
         "dateModified": TODAY_S,
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Promo Codes", "item": f"{ctx.DOMAIN}/promo-codes/"},
             {"@type": "ListItem", "position": 2, "name": disp, "item": canon}]}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    if offers_ld:
        ld["@graph"].append({"@type": "ItemList", "name": f"{disp} promo codes",
                             "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": o}
                                                 for i, o in enumerate(offers_ld)]})
    h.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    h.append(ctx.FOOTER.format(shop=ctx.SHOP_URL))
    return "\n".join(h)
