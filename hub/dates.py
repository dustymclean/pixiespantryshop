"""One place for the two dates the site cares about.

TODAY      -- the real calendar day the build runs. Used only to drop offers whose end date
              has passed.
DATA_DATE  -- the day the affiliate-network data was exported (data/meta.json). Every
              "verified" / "last checked" claim on the site uses this, never the build day,
              so a rebuild without fresh data cannot quietly re-stamp old offers as new.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

TODAY = dt.date.today().isoformat()
DATA_DATE = json.loads((Path(__file__).parent / "data" / "meta.json").read_text())["data_date"]
_d = dt.date.fromisoformat(DATA_DATE)
NICE_DATA = _d.strftime("%B %-d, %Y")
DATA_MONTH = _d.strftime("%B %Y")
STALE_DAYS = (dt.date.fromisoformat(TODAY) - _d).days


def is_live(o: dict) -> bool:
    """Seen in the latest export and not past its end date."""
    return o.get("last_seen") == DATA_DATE and (not o.get("ends") or o["ends"] >= TODAY)
