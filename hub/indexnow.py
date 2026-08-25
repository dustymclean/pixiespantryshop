#!/usr/bin/env python3
"""IndexNow change-notification layer for pixiespantryshop.com.

IndexNow tells participating engines (Bing, Yandex, Seznam, Naver — and Bing shares
submissions across the IndexNow network) that a URL CHANGED. It is a discovery
accelerator, NOT an indexing guarantee: engines still decide independently whether
to crawl, index or rank anything submitted.

The sitemap remains the full-site discovery mechanism. This only ever submits URLs
that actually changed, computed by diffing the two most recent snapshots written by
snapshot.py.

Usage:
  python3 hub/indexnow.py --delta         # submit only URLs changed since last snapshot
  python3 hub/indexnow.py --urls a/ b/    # submit specific paths (urgent code change)
  python3 hub/indexnow.py --test          # submit one URL to prove the pipeline works
"""
from __future__ import annotations
import argparse, json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
SNAPS = DATA / "snapshots"
HOST = "pixiespantryshop.com"
DOMAIN = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/IndexNow"
KEY = (DATA / "indexnow_key.txt").read_text().strip()
LOG = DATA / "indexnow_log.json"


def offer_sig(o: dict) -> tuple:
    """What counts as a material change for a single offer."""
    return (o.get("code"), o.get("title"), o.get("ends"), o.get("status"), o.get("kind"))


def changed_slugs() -> tuple[set[str], dict]:
    """Diff the two newest snapshots -> slugs whose page content materially changed."""
    snaps = sorted(SNAPS.glob("*.json"))
    if len(snaps) < 2:
        return set(), {"reason": "only one snapshot on disk; nothing to diff yet"}
    now, prev = json.load(open(snaps[-1])), json.load(open(snaps[-2]))

    def by_merchant(snap):
        out: dict[str, set] = {}
        for k, o in snap["live"].items():
            out.setdefault(o["merchant"], set()).add(offer_sig(o))
        for k in snap["expired"]:
            out.setdefault(k.split("|", 1)[0], set()).add(("EXPIRED", k))
        return out

    a, b = by_merchant(now), by_merchant(prev)
    reasons: dict[str, str] = {}
    for m in set(a) | set(b):
        if m not in b:
            reasons[m] = "new merchant"
        elif m not in a:
            reasons[m] = "merchant removed"
        elif a[m] != b[m]:
            gained, lost = len(a[m] - b[m]), len(b[m] - a[m])
            reasons[m] = f"offers changed (+{gained}/-{lost})"

    slug = {}
    for p in json.load(open(DATA / "partners.json")):
        slug[p["name"]] = p["slug"]
    new_pages = set(now["pages"]) - set(prev["pages"])
    urls = {slug[m] for m in reasons if m in slug} | new_pages
    return urls, {slug.get(m, m): r for m, r in reasons.items()}


def submit(paths: list[str]) -> dict:
    """POST a batch to IndexNow. Max 10,000 URLs per request."""
    if not paths:
        return {"submitted": 0, "status": None, "note": "nothing changed - no submission sent"}
    urls = [p if p.startswith("http") else f"{DOMAIN}{p}" for p in paths]
    payload = {"host": HOST, "key": KEY, "keyLocation": f"{DOMAIN}/{KEY}.txt",
               "urlList": urls[:10000]}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            code, body = r.status, r.read(600).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read(600).decode("utf-8", "replace")
    except Exception as e:
        return {"submitted": len(urls), "status": "ERROR", "error": str(e)[:200]}
    # 200 = accepted, 202 = accepted, key validation pending
    return {"submitted": len(urls), "status": code, "ok": code in (200, 202),
            "body": body.strip()[:300], "urls": urls[:20]}


def log(entry: dict) -> None:
    hist = json.loads(LOG.read_text()) if LOG.exists() else []
    hist.append(entry)
    LOG.write_text(json.dumps(hist[-200:], indent=1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--delta", action="store_true")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--urls", nargs="*", default=[])
    a = ap.parse_args()
    import datetime
    stamp = datetime.datetime.now().isoformat(timespec="seconds")

    if a.test:
        res = submit(["/promo-codes/dynavap/"])
        why = {"/promo-codes/dynavap/": "pipeline test"}
    elif a.delta:
        slugs, why = changed_slugs()
        res = submit(sorted(f"/promo-codes/{s}/" for s in slugs))
    else:
        res = submit(a.urls)
        why = {u: "manual" for u in a.urls}

    print(json.dumps({"when": stamp, "result": res, "reasons": why}, indent=1)[:3000])
    log({"when": stamp, "count": res.get("submitted"), "status": res.get("status"),
         "ok": res.get("ok"), "reasons": why})
    return 0 if res.get("ok") or res.get("submitted") == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
