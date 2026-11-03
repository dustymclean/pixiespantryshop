#!/usr/bin/env python3
"""Refresh the registry, offers and banners from an Awin + Impact account export.

    python3 hub/import_export.py /path/to/Pixies        # the folder from the export zip

Reads (never copies) the raw export. The raw files contain account identifiers, so they
must stay out of this public repo; only the cleaned data below is written:

  data/partners.json   one record per partner we are *currently* paid by (joined / active)
  data/offers.json     every offer with history; last_seen = export date
  data/banners.json    static Impact banners (image + tracking link + impression pixel)
  data/retired.json    partners that left (suspended / expired / gone) -> pages redirect
  data/meta.json       {"data_date": ...} -- the date the network data was pulled.
                       Pages say "verified <data_date>", never "verified <build day>".

Partners are matched on network IDs (Awin advertiser ID, Impact campaign ID), not names,
so a merchant renaming itself on the network never changes its URL here.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
AWIN_PUB = "2520915"
IMPACT_PUB = "5929369"

# Banner seasons that make sense to show; everything else is out of season or past.
SEASON_OK = {"", "FALL", "WINTER", "BLACK_FRIDAY", "CYBER_MONDAY", "CHRISTMAS"}
NON_NETWORK = {"In-house", "GoAffPro / in-house", "Referral"}


def rd_csv(p: Path) -> list[dict]:
    return list(csv.DictReader(p.open(encoding="utf-8-sig")))


def clean(s) -> str:
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return "" if s in {".", "-", "n/a", "N/A"} else s


def ids_of(p: dict) -> tuple[str | None, str | None]:
    blob = (p.get("link") or "") + " " + json.dumps(p.get("promo") or {}) + " " + json.dumps(p.get("ids") or {})
    a = re.search(r'(?:mid|awinmid)=(\d+)|"awin": "(\d+)"', blob)
    i = re.search(r'/c/\d+/\d+/(\d+)|"impact": "(\d+)"', blob)
    return ((a.group(1) or a.group(2)) if a else None, (i.group(1) or i.group(2)) if i else None)


def main(export: Path) -> None:
    am, ia = export / "Affiliate_Master" / "Awin", export / "Affiliate_Master" / "Impact"
    created = json.loads((am / "EXPORT_SUMMARY.json").read_text())["created_utc"]
    # The export ran in the evening US Central time; date it the way the owner would.
    data_date = (dt.datetime.fromisoformat(created) - dt.timedelta(hours=6)).date().isoformat()
    today = dt.date.today().isoformat()

    # ---------------------------------------------------------------- network rosters
    awin = {r["Advertiser ID"]: r for r in rd_csv(am / "AWIN_PROGRAMMES_ALL_RELATIONSHIPS.csv")}
    awin_links = {r["Advertiser ID"]: r for r in rd_csv(export / "Awin" / "AWIN_ALL_AFFILIATE_LINKS.csv")}
    awin_det = {k: v for k, v in json.loads((am / "PROGRAMME_DETAILS.json").read_text()).items() if v}
    awin_raw = {str(p["id"]): p for p in json.loads((export / "Awin" / "AWIN_PROGRAMMES_RAW.json").read_text())}
    imp = {r["Programme ID"]: r for r in rd_csv(export / "Impact" / "IMPACT_ALL_AFFILIATE_LINKS.csv")}
    imp_camp = {c["CampaignId"]: c for c in json.loads((ia / "campaigns_raw.json").read_text())}

    def awin_ok(aid):  # joined, not a programme that announced closure
        r = awin.get(aid)
        return bool(r) and r["Relationship"] == "joined" and "CLOSED" not in r["Brand"].upper()

    def imp_ok(cid):
        r = imp.get(cid)
        return bool(r) and r["Contract Status"] == "Active"

    old = json.loads((DATA / "partners.json").read_text())
    partners, retired, claimed_a, claimed_i = [], [], set(), set()

    def enrich(p: dict, aid: str | None, cid: str | None) -> dict:
        p.setdefault("ids", {})
        if aid and awin_ok(aid):
            r, d = awin[aid], (awin_det.get(aid) or {})
            info, kpi = d.get("programmeInfo") or {}, d.get("kpi") or {}
            raw = awin_raw.get(aid, {})
            p["ids"]["awin"] = aid
            p["link"] = (awin_links.get(aid) or {}).get("Affiliate Link") or r["Affiliate Link"] or p.get("link")
            p["url"] = r["Brand Website"] or info.get("displayUrl") or p.get("url")
            p["sector"] = (raw.get("primarySector") or {}).get("name") if isinstance(raw.get("primarySector"), dict) \
                else (raw.get("primarySector") or p.get("sector"))
            p["desc"] = clean(info.get("description") or r.get("Description") or p.get("desc"))
            p["logo"] = info.get("logoUrl") or r.get("Logo URL") or p.get("logo")
            p["deeplink"] = bool(info.get("deeplinkEnabled", True))
            if kpi.get("epc") is not None:
                p["epc"] = round(float(kpi["epc"]), 2)
                p["conv_rate"] = round(float(kpi.get("conversionRate") or 0), 2)
            p["region"] = r.get("Region") or ""
            claimed_a.add(aid)
        if cid and imp_ok(cid):
            r, c = imp[cid], imp_camp.get(cid) or {}
            p["ids"]["impact"] = cid
            if "awin" not in p["ids"]:
                p["link"] = r["Affiliate Link"] or c.get("TrackingLink") or p.get("link")
                p["url"] = r["Brand Website"] or c.get("CampaignUrl") or p.get("url")
                p["desc"] = clean(c.get("CampaignDescription") or p.get("desc"))
            p["deeplink"] = r.get("Deep Linking Allowed", "true") == "true"
            claimed_i.add(cid)
        p["network"] = ("Awin+Impact" if {"awin", "impact"} <= set(p["ids"]) else
                        "Awin" if "awin" in p["ids"] else "Impact" if "impact" in p["ids"] else p.get("network"))
        p.pop("promo", None)          # recomputed from offers at build time
        return p

    for p in old:
        aid, cid = ids_of(p)
        if p.get("network") in NON_NETWORK and not (aid or cid):
            partners.append(p)        # in-house / referral relationships live outside the networks
            continue
        if (aid and awin_ok(aid)) or (cid and imp_ok(cid)):
            partners.append(enrich(p, aid if aid and awin_ok(aid) else None, cid if cid and imp_ok(cid) else None))
        else:
            why = (awin.get(aid or "", {}).get("Relationship") or imp.get(cid or "", {}).get("Contract Status")
                   or "no longer in the network export")
            retired.append({"name": p["name"], "network": p.get("network"), "reason": why, "retired": data_date})

    existing = {p["name"] for p in partners}

    def unique(name: str) -> str:
        n, k = name, 2
        while n in existing:
            n, k = f"{name} ({k})", k + 1
        existing.add(n)
        return n

    for aid, r in awin.items():
        if aid not in claimed_a and awin_ok(aid):
            partners.append(enrich({"name": unique(clean(r["Brand"])), "new": data_date}, aid, None))
    for cid, r in imp.items():
        if cid not in claimed_i and imp_ok(cid):
            partners.append(enrich({"name": unique(clean(r["Programme"] or r["Brand"])), "new": data_date}, None, cid))

    # keep prior retirements (their URLs still need redirect pages)
    prev_ret = json.loads((DATA / "retired.json").read_text()) if (DATA / "retired.json").exists() else []
    live_names = {p["name"] for p in partners}
    seen_ret = {r["name"] for r in retired}
    retired += [r for r in prev_ret if r["name"] not in seen_ret and r["name"] not in live_names]

    by_aid = {p["ids"]["awin"]: p["name"] for p in partners if p.get("ids", {}).get("awin")}
    by_cid = {p["ids"]["impact"]: p["name"] for p in partners if p.get("ids", {}).get("impact")}

    # ---------------------------------------------------------------- offers
    def us(o):
        reg = o.get("regions") or {}
        return reg.get("all") or any(x.get("countryCode") == "US" for x in reg.get("list") or [])

    current = []
    for o in json.loads((am / "OFFERS_ALL_RAW.json").read_text()):
        name = by_aid.get(str(o["advertiser"]["id"]))
        if not name or o.get("status") not in ("active", "expiringSoon") or not us(o):
            continue
        v = o.get("voucher") or {}
        current.append({
            "merchant": name, "network": "Awin", "code": v.get("code") or None,
            "kind": "code" if v.get("code") else "sale",
            "title": clean(o.get("title")), "description": clean(o.get("description")),
            "terms": clean(o.get("terms")),
            "starts": (o.get("startDate") or "")[:10], "ends": (o.get("endDate") or "")[:10],
            "link": o.get("urlTracking") or "", "exclusive": bool(v.get("exclusive")),
            "attributable": bool(v.get("attributable")), "source": "Awin promotions feed",
            "last_seen": data_date})
    for c in json.loads((ia / "promo_codes_raw.json").read_text()):
        name = by_cid.get(str((c.get("Program") or {}).get("Id")))
        if not name or c.get("State") != "ACTIVE":
            continue
        current.append({
            "merchant": name, "network": "Impact", "code": c["Code"], "kind": "code",
            "title": "", "description": "", "terms": "",
            "starts": (c.get("CreatedDate") or "")[:10], "ends": "", "link": "",
            "exclusive": False, "attributable": True, "source": "Impact promo code API",
            "last_seen": data_date})
    for c in json.loads((DATA / "personal_codes.json").read_text()):
        if not c.get("publish"):
            continue
        current.append({
            "merchant": c.get("registry_name") or c["merchant"], "display_merchant": c["merchant"],
            "network": c["attribution"], "code": c["code"], "kind": "code", "title": c["discount"],
            "description": "", "terms": "", "starts": "", "ends": c.get("ends", ""),
            "link": c.get("link") or "", "exclusive": True, "attributable": True, "personal": True,
            "status": c["status"], "source": c["source"], "last_confirmed": c["last_confirmed"],
            "no_expiry": bool(c.get("no_expiry")), "last_seen": data_date})

    key = lambda o: f'{o["merchant"]}|{o.get("code") or ""}|{o.get("title", "")[:60]}'
    history = {key(o): o for o in json.loads((DATA / "offers.json").read_text())}
    for o in current:
        o["first_seen"] = history.get(key(o), {}).get("first_seen", data_date)
        history[key(o)] = o
    offers = sorted((o for o in history.values() if o["merchant"] in live_names),
                    key=lambda o: (o["merchant"].lower(), o.get("code") or "~"))

    # ---------------------------------------------------------------- banners
    banners = []
    for a in json.loads((ia / "ads_raw.json").read_text()):
        name = by_cid.get(str(a.get("CampaignId")))
        if (a.get("Type") != "BANNER" or not name or not a.get("CreativeUrl")
                or (a.get("EndDate") and a["EndDate"][:10] < today)
                or (a.get("StartDate") or "")[:10] > today
                or (a.get("Season") or "") not in SEASON_OK):
            continue
        w, h = int(a["Width"] or 0), int(a["Height"] or 0)
        if not (w and h):
            continue
        banners.append({
            "id": a["Id"], "campaign": a["CampaignId"], "partner": name, "w": w, "h": h,
            "img": "https:" + a["CreativeUrl"] if a["CreativeUrl"].startswith("//") else a["CreativeUrl"],
            "href": a["TrackingLink"],
            "pixel": f"https://imp.pxf.io/i/{IMPACT_PUB}/{a['Id']}/{a['CampaignId']}",
            "alt": clean(a.get("Description") or a.get("Name"))[:120],
            "season": a.get("Season") or "", "top": a.get("TopSeller") == "true"})

    partners.sort(key=lambda p: p["name"].lower())
    (DATA / "partners.json").write_text(json.dumps(partners, indent=1, ensure_ascii=False))
    (DATA / "offers.json").write_text(json.dumps(offers, indent=1, ensure_ascii=False))
    (DATA / "banners.json").write_text(json.dumps(banners, indent=1, ensure_ascii=False))
    (DATA / "retired.json").write_text(json.dumps(sorted(retired, key=lambda r: r["name"].lower()), indent=1))
    (DATA / "meta.json").write_text(json.dumps({"data_date": data_date, "awin_publisher": AWIN_PUB,
                                                "impact_publisher": IMPACT_PUB}, indent=1))
    live = [o for o in offers if o["last_seen"] == data_date and (not o["ends"] or o["ends"] >= today)]
    print(f"data date {data_date}: {len(partners)} partners "
          f"({sum(1 for p in partners if p.get('new') == data_date)} new), {len(retired)} retired, "
          f"{len(offers)} offers ({len(live)} live, {sum(1 for o in live if o.get('code'))} codes), "
          f"{len(banners)} banners from {len({b['partner'] for b in banners})} partners")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]))
