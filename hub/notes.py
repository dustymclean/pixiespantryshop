"""Per-partner editorial notes (data/notes/*.json), written for each partner individually.

Each entry: name -> [category, take, sells?]. Product lines can also live in
data/notes/sells_*.json (name -> [product, ...]). Edit the JSON to change a partner's copy.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_DIR = Path(__file__).parent / "data" / "notes"
NOTES: dict[str, dict] = {}
for _f in sorted(_DIR.glob("[0-9]*.json")):
    for _name, _v in json.loads(_f.read_text()).items():
        NOTES[_name] = {"cat": _v[0], "take": _v[1], "sells": list(_v[2]) if len(_v) > 2 else []}
for _f in sorted(_DIR.glob("sells_*.json")):
    for _name, _v in json.loads(_f.read_text()).items():
        NOTES.setdefault(_name, {"cat": "", "take": "", "sells": []})
        if _v and not NOTES[_name]["sells"]:
            NOTES[_name]["sells"] = list(_v)

BRANDS = {k: v for k, v in json.loads((_DIR / "brands.json").read_text()).items() if not k.startswith("_")}


def brand(name: str) -> str:
    """The name shoppers search for: explicit override, else the network name minus region tags."""
    return BRANDS.get(name) or re.sub(r"\s*\((US|USA|UK)\)$|\s+(US|USA|UK)$", "", name).strip()


# Programmes that exist on the network but sell nothing to shoppers.
HIDDEN = {"Awin (USD)"}


def apply(partners: list[dict]) -> list[dict]:
    """Attach notes to registry records; drop hidden ones. Missing notes fail loudly."""
    out, missing = [], []
    for p in partners:
        if p["name"] in HIDDEN:
            continue
        n = NOTES.get(p["name"])
        if not n or not n["take"]:
            missing.append(p["name"])
            continue
        p.update(cat=n["cat"], take=n["take"], sells=n["sells"], brand=brand(p["name"]))
        out.append(p)
    if missing:
        raise SystemExit("No editorial note for: " + ", ".join(missing)
                         + "\nAdd them to hub/data/notes/ before building.")
    return out
