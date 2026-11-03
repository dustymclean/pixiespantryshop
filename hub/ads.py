"""Sponsored banner rotation: equal exposure per advertiser, not per creative.

Rules (set by the site owner):
  * one ad slot per page, box shape (300x250 and squares) -- fits phone and desktop
  * every advertiser gets the same number of rotation slots: the MEDIAN number of
    usable box creatives per advertiser
  * an advertiser's best creatives fill its slots; an advertiser with fewer than the
    median repeats its own to fill them
  * a page about a specific brand shows that brand's own banner instead of the rotation

Best = TopSeller flag, then in-season, then exact 300x250, then newest.
Clicks go through the network tracking link; the impression pixel fires only once the
ad is actually on screen. Nothing is placed to be clicked by accident.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

ROOT = Path(__file__).parent

# Banners for storefronts that don't sell to US shoppers are useless here.
NON_US = ("Netherlands", "Germany", "France", "Italy", "Austria", "Czech", "India", "(UK)", "UK")
SEASON_RANK = {"BLACK_FRIDAY": 3, "CYBER_MONDAY": 3, "CHRISTMAS": 3, "WINTER": 2, "": 1, "FALL": 1}


def is_box(w: int, h: int) -> bool:
    return w >= 250 and 0.9 <= w / h <= 1.25


def score(b: dict) -> tuple:
    exact = 2 if (b["w"], b["h"]) == (300, 250) else (1 if (b["w"], b["h"]) == (336, 280) else 0)
    return (1 if b.get("top") else 0, SEASON_RANK.get(b.get("season", ""), 0), exact, b.get("start", ""))


def build(partners_by_name: dict, slugs: dict) -> tuple[dict, dict]:
    """Return (ads_json, stats). ads_json = {"rot": [advertiser slug, ...], "own": {slug: [median creatives]}}."""
    raw = json.loads((ROOT / "data" / "banners.json").read_text())
    by_partner: dict[str, list] = {}
    for b in raw:
        p = partners_by_name.get(b["partner"])
        if not p or not is_box(b["w"], b["h"]):
            continue
        label = f'{p.get("brand", "")} {p.get("cat", "")}'
        if any(x in label for x in NON_US):
            continue
        by_partner.setdefault(b["partner"], []).append(b)

    counts = sorted(len(v) for v in by_partner.values())
    median = int(statistics.median(counts)) if counts else 0
    rot, own = [], {}
    for name, items in sorted(by_partner.items()):
        best = sorted(items, key=score, reverse=True)[:median]
        slot = [{"i": b["img"], "h": b["href"], "p": b["pixel"], "w": b["w"], "ht": b["h"],
                 "a": (b.get("alt") or partners_by_name[name]["brand"])[:100],
                 "b": partners_by_name[name]["brand"]} for b in best]
        # every advertiser holds exactly one entry in the rotation (equal exposure); within it,
        # its `median` slots are its best creatives, repeated in order if it has fewer
        own[slugs[name]] = [slot[k % len(slot)] for k in range(median)]
        rot.append(slugs[name])
    stats = {"advertisers": len(rot), "median": median, "slots": len(rot) * median,
             "unique": sum(len({c["i"] for c in v}) for v in own.values()),
             "most": max(by_partner.items(), key=lambda kv: len(kv[1]))[0] if by_partner else "",
             "most_n": counts[-1] if counts else 0, "least_n": counts[0] if counts else 0}
    return {"rot": rot, "own": own}, stats


def slot_html(own_slug: str | None = None) -> str:
    """A reserved, labelled box. Fixed size so nothing jumps when the ad loads."""
    key = f' data-own="{own_slug}"' if own_slug else ""
    return (f'<aside class="spon"{key} aria-label="Sponsored"><span class="spon-l">Sponsored</span>'
            f'<div class="spon-b"></div></aside>')


ADS_CSS = """
aside.spon{max-width:336px;margin:34px auto;text-align:center}
aside.spon .spon-l{display:block;font-size:.58rem;letter-spacing:.24em;text-transform:uppercase;
 color:var(--muted);margin-bottom:6px}
aside.spon .spon-b{min-height:250px;display:flex;align-items:center;justify-content:center;
 border:1px solid rgba(212,175,55,.22);background:rgba(0,0,0,.25)}
aside.spon img.cr{display:block;width:300px;max-width:100%;height:auto}
aside.spon .spon-n{display:block;font-size:.66rem;color:var(--muted);margin-top:6px}
aside.spon:empty,aside.spon.off{display:none}
"""

ADS_JS = r"""<script>
(function(){
  var slots=document.querySelectorAll('aside.spon');
  if(!slots.length||!('IntersectionObserver' in window))return;
  var data=null,wait=[];
  function load(cb){
    if(data){cb(data);return;}
    wait.push(cb);
    if(wait.length>1)return;
    fetch('/ads.json').then(function(r){return r.json();}).then(function(d){
      data=d;wait.forEach(function(f){f(d);});wait=[];
    }).catch(function(){slots.forEach(function(s){s.classList.add('off');});});
  }
  function pick(d,slot){
    var own=slot.getAttribute('data-own');
    if(own&&d.own[own]&&d.own[own].length){var o=d.own[own];return o[Math.floor(Math.random()*o.length)];}
    // equal exposure: choose the advertiser uniformly first, then one of its slots
    var adv=d.own[d.rot[Math.floor(Math.random()*d.rot.length)]];
    return adv[Math.floor(Math.random()*adv.length)];
  }
  function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      io.unobserve(e.target);
      var slot=e.target;
      load(function(d){
        var c=pick(d,slot); if(!c){slot.classList.add('off');return;}
        slot.querySelector('.spon-b').innerHTML=
          '<a href="'+esc(c.h)+'" rel="sponsored nofollow noopener" target="_blank">'+
          '<img class="cr" src="'+esc(c.i)+'" alt="'+esc(c.a)+'" width="'+c.w+'" height="'+c.ht+'" loading="lazy" decoding="async"></a>'+
          '<img src="'+esc(c.p)+'" width="1" height="1" alt="" style="position:absolute;width:1px;height:1px;opacity:0">';
        var n=document.createElement('span');n.className='spon-n';n.textContent='Ad from '+c.b;slot.appendChild(n);
      });
    });
  },{rootMargin:'200px'});
  slots.forEach(function(s){io.observe(s);});
})();
</script>"""
