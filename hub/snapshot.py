#!/usr/bin/env python3
"""Record a weekly state snapshot and report what changed since the previous one.

Run AFTER build_offers.py + build.py. Writes hub/data/snapshots/<date>.json and
prints a change report against the most recent earlier snapshot. The first
snapshot on disk is the baseline (2026-08-25); it is never overwritten.
"""
from __future__ import annotations
import json, re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
DATA, DIST = ROOT / "data", ROOT / "dist"
SNAPS = DATA / "snapshots"
SNAPS.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()


def words(html: str) -> int:
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    return len(re.sub(r"<[^>]+>", " ", t).split())


def capture() -> dict:
    partners = json.load(open(DATA / "partners.json"))
    offers = json.load(open(DATA / "offers.json"))
    offers = offers if isinstance(offers, list) else offers.get("offers", [])
    pages = {}
    for d in sorted((DIST / "promo-codes").iterdir()):
        if d.is_dir() and (d / "index.html").exists():
            pages[d.name] = words((d / "index.html").read_text())

    def key(o):
        return f'{o["merchant"]}|{o.get("code") or o.get("title","")}'

    live = {key(o): {"merchant": o["merchant"], "code": o.get("code"),
                     "title": o.get("title"), "kind": o.get("kind"),
                     "ends": o.get("ends"), "status": o.get("status")}
            for o in offers if o.get("status") != "EXPIRED"}
    dead = {key(o) for o in offers if o.get("status") == "EXPIRED"}
    excl = {key(o) for o in offers
            if o.get("exclusive") and o.get("personal") and o.get("status") != "EXPIRED"}
    return {"date": TODAY, "partners": sorted(p["name"] for p in partners),
            "pages": pages, "live": live, "expired": sorted(dead), "exclusive": sorted(excl)}


def fmt(items, limit=15):
    items = sorted(items)
    head = ", ".join(items[:limit])
    return (head + (f" (+{len(items)-limit} more)" if len(items) > limit else "")) if items else "none"


def report(now: dict, prev: dict) -> str:
    L = [f"CHANGE REPORT  {prev['date']} -> {now['date']}", "=" * 58]
    pa, pb = set(now["partners"]), set(prev["partners"])
    L += [f"Partners: {len(pa)} ({len(pa)-len(pb):+d})",
          f"  added:   {fmt(pa - pb)}",
          f"  removed: {fmt(pb - pa)}"]
    ga, gb = set(now["pages"]), set(prev["pages"])
    L += [f"Merchant pages: {len(ga)} ({len(ga)-len(gb):+d})",
          f"  added:   {fmt(ga - gb)}",
          f"  removed: {fmt(gb - ga)}"]

    la, lb = now["live"], prev["live"]
    added = set(la) - set(lb)
    gone = set(lb) - set(la)
    changed = [k for k in set(la) & set(lb)
               if (la[k]["title"], la[k]["ends"]) != (lb[k]["title"], lb[k]["ends"])]
    newly_expired = [k for k in gone if k in set(now["expired"])]
    L += [f"Offers live: {len(la)} ({len(la)-len(lb):+d})",
          f"  codes/deals added:   {len(added)}  {fmt([la[k]['merchant'] for k in added], 10)}",
          f"  newly expired:       {len(newly_expired)}  {fmt([lb[k]['merchant'] for k in newly_expired], 10)}",
          f"  disappeared (no expiry recorded): {len(gone)-len(newly_expired)}",
          f"  terms/end-date changed: {len(changed)}  {fmt([la[k]['merchant'] for k in changed], 10)}"]

    ea, eb = set(now["exclusive"]), set(prev["exclusive"])
    L += [f"Audience-exclusive codes: {len(ea)} ({len(ea)-len(eb):+d})",
          f"  gained:   {fmt(ea - eb)}",
          f"  LOST:     {fmt(eb - ea)}"]
    if eb - ea:
        L.append("  ** an exclusive code vanished from its feed - investigate before next run **")

    thin_now = {k for k, v in now["pages"].items() if v < 400}
    thin_prev = {k for k, v in prev["pages"].items() if v < 400}
    L += [f"Pages under 400 words: {len(thin_now)} ({len(thin_now)-len(thin_prev):+d})",
          f"  newly thin: {fmt(thin_now - thin_prev)}"]
    return "\n".join(L)


def main():
    now = capture()
    prior = sorted(p for p in SNAPS.glob("*.json") if p.stem != TODAY)
    (SNAPS / f"{TODAY}.json").write_text(json.dumps(now, indent=1, sort_keys=True))
    if not prior:
        print(f"BASELINE RECORDED {TODAY}: {len(now['partners'])} partners, "
              f"{len(now['pages'])} pages, {len(now['live'])} live offers, "
              f"{len(now['exclusive'])} exclusive codes.")
        return
    prev = json.load(open(prior[-1]))
    print(report(now, prev))
    base = json.load(open(prior[0]))
    if prior[0] != prior[-1]:
        print("\n" + report(now, base).replace("CHANGE REPORT", "VS BASELINE", 1))


if __name__ == "__main__":
    sys.exit(main())
