#!/usr/bin/env python3
"""Build hub/data/offers.json: every offer we can verify, per merchant, with history.

Sources
  temp/awin_promotions.json   Awin vouchers + sale-type promotions (joined programmes, US)
  temp/impact_promocodes.json Impact promo codes attached to publisher 5929369
  hub/data/personal_codes.json  classified audience codes (only publish:true reach the site)

History is retained: an offer that disappears from the feed is not deleted, it is kept
with its last known end date so the merchant page can show it under Expired.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path

ROOT = Path(__file__).parent
TEMP = Path("/work/temp")
TODAY = dt.date.today().isoformat()
OUT = ROOT / "data" / "offers.json"


ALIAS = {
    "Dr.Dabber3": "Dr.Dabber",
    "Orbit Mobile Limited": "Orbit Mobile",
    "High Tide": "Smoke Cartel",   # same program, Smoke Cartel is the storefront
    "FreshQ INC.": None,           # another publisher's program, not ours
}


def clean(s: str | None) -> str:
    s = (s or "").strip()
    return "" if s in {".", "-", "n/a", "N/A"} else s


def key(o: dict) -> str:
    return f'{o["merchant"]}|{o.get("code") or ""}|{o.get("title","")[:60]}'


def from_awin() -> list[dict]:
    path = TEMP / "awin_promotions.json"
    if not path.exists():
        return []
    out = []
    for p in json.loads(path.read_text()):
        v = p.get("voucher") or {}
        out.append({
            "merchant": p["advertiser"]["name"],
            "network": "Awin",
            "code": v.get("code") or None,
            "kind": "code" if v.get("code") else "sale",
            "title": clean(p.get("title")),
            "description": clean(p.get("description")),
            "terms": clean(p.get("terms")),
            "starts": (p.get("startDate") or "")[:10],
            "ends": (p.get("endDate") or "")[:10],
            "link": p.get("urlTracking") or "",
            "exclusive": bool(v.get("exclusive")),
            "attributable": bool(v.get("attributable")),
            "source": "Awin promotions feed",
            "last_seen": TODAY,
        })
    return out


def from_impact() -> list[dict]:
    path = TEMP / "impact_promocodes.json"
    if not path.exists():
        return []
    out = []
    for c in json.loads(path.read_text()):
        if c.get("State") != "ACTIVE":
            continue
        out.append({
            "merchant": (c.get("Advertiser") or {}).get("Name") or c["Program"]["Name"],
            "network": "Impact",
            "code": c["Code"],
            "kind": "code",
            "title": "", "description": "", "terms": "",
            "starts": (c.get("CreatedDate") or "")[:10], "ends": "",
            "link": "", "exclusive": False, "attributable": True,
            "source": "Impact promo code API",
            "last_seen": TODAY,
        })
    return out


def from_personal() -> list[dict]:
    out = []
    for c in json.loads((ROOT / "data" / "personal_codes.json").read_text()):
        if not c.get("publish"):
            continue
        out.append({
            "merchant": c.get("registry_name") or c["merchant"],
            "display_merchant": c["merchant"],
            "network": c["attribution"],
            "code": c["code"],
            "kind": "code",
            "title": c["discount"],
            "description": "", "terms": "",
            "starts": "", "ends": c.get("ends", ""),
            "link": c.get("link") or "",
            "exclusive": True, "attributable": True,
            "personal": True,
            "status": c["status"],
            "source": c["source"],
            "last_confirmed": c["last_confirmed"],
            "no_expiry": bool(c.get("no_expiry")),
            "last_seen": TODAY,
        })
    return out


def main() -> None:
    history = {key(o): o for o in json.loads(OUT.read_text())} if OUT.exists() else {}
    current = from_awin() + from_impact() + from_personal()
    seen = set()
    for o in current:
        k = key(o)
        seen.add(k)
        prev = history.get(k, {})
        o["first_seen"] = prev.get("first_seen", TODAY)
        history[k] = o
    # anything not in this pull keeps its record but stops being "seen"
    for k, o in history.items():
        if k not in seen:
            o.setdefault("first_seen", o.get("last_seen", TODAY))
    for o in list(history.values()):
        tgt = ALIAS.get(o["merchant"], o["merchant"])
        if tgt is None:
            history.pop(key(o), None)
            continue
        if tgt != o["merchant"]:
            o.setdefault("display_merchant", o["merchant"])
            o["merchant"] = tgt
    offers = sorted(history.values(), key=lambda o: (o["merchant"].lower(), o.get("code") or "~"))
    OUT.write_text(json.dumps(offers, indent=1))
    live = sum(1 for o in offers if o["last_seen"] == TODAY and (not o["ends"] or o["ends"] >= TODAY))
    print(f"{len(offers)} offers ({live} currently live) -> {OUT}")


if __name__ == "__main__":
    main()
