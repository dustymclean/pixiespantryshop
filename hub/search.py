#!/usr/bin/env python3
"""Visitor search for pixiespantryshop.com.

Builds /search-index.json from the SAME canonical registry the merchant pages are
generated from, so search can never drift away from the published offers, and emits
the CSS/HTML/JS for the search box that is dropped into the homepage, /promo-codes/
and the three persona hubs.

Search is a visitor feature, not an SEO surface: results are rendered client-side,
never change the URL, and create no crawlable query pages.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re

TODAY_S = dt.date.today().isoformat()

# Endpoint that receives private on-site search telemetry (query, result count,
# zero-result flag, merchant clicked). No cookies, no identifiers, no PII.
TELEMETRY = "https://pixies-pantry.com/wp-json/pp-search/v1/log"

STOP = {"the", "and", "for", "with", "shop", "store", "official", "inc", "llc",
        "ltd", "co", "usa", "us", "uk", "com"}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9%]+", "", (s or "").lower())


def _pct(s: str) -> float:
    """Largest percentage mentioned in an offer, used to pick the best code."""
    m = re.findall(r"(\d{1,2})\s*%", s or "")
    return max((float(x) for x in m), default=0.0)


def _amount(s: str) -> float:
    m = re.findall(r"\$\s*(\d{1,4})", s or "")
    return max((float(x) for x in m), default=0.0)


def _live(o: dict) -> bool:
    return not o.get("ends") or o["ends"] >= TODAY_S


def _strength(o: dict) -> tuple:
    """Rank offers so the single 'best current offer' shown in search is defensible."""
    t = f'{o.get("title", "")} {o.get("description", "")}'
    return (1 if o.get("exclusive") else 0,
            1 if o.get("code") else 0,
            _pct(t),
            _amount(t) / 100.0)


# Sector words a shopper is likely to type but that the network feed does not use.
SECTOR_SYNONYMS = {
    "vaporizer": "vaporizers vape vaping dry herb", "glass": "glass bong pipe water pipe",
    "accessor": "accessories papers grinder tray", "hemp": "hemp cbd flower",
    "travel": "travel esim flights hotel", "camera": "camera photography capture video",
    "software": "software ai app saas tool", "home": "home garden household kitchen",
    "wellness": "wellness recovery health", "style": "style fashion jewelry gifts",
    "pet": "pets dog cat", "electronic": "electronics gadgets tech",
}


def hub_keywords(hubs) -> dict[str, list[str]]:
    """Merchant -> persona hub + curated section it appears in, so 'vaporizer' or
    'reviewed by dusty' finds the brands actually filed under that heading."""
    import html as _h
    out: dict[str, list[str]] = {}
    for h in hubs.values():
        title = h.get("title", "")
        for sec in h.get("sections", []):
            name = _h.unescape(sec.get("name", ""))
            for item in sec.get("items", []):
                pname = item[0]
                if not pname:
                    continue
                bucket = out.setdefault(pname, [])
                for w in (title, name):
                    if w and w not in bucket:
                        bucket.append(w)
    return out


def build_index(partners, promos, offers_by_merchant, slugs, personal, hubs=None) -> list[dict]:
    """One record per merchant page. Compact keys keep the payload small."""
    personal_by = {}
    for c in personal:
        if c.get("publish"):
            personal_by.setdefault(c.get("registry_name") or c["merchant"], []).append(c)

    promos_by: dict[str, list] = {}
    for p in promos:
        promos_by.setdefault(p.get("registry_name") or p["merchant"], []).append(p)

    hubkw = hub_keywords(hubs) if hubs else {}

    out = []
    for p in sorted(partners, key=lambda x: x["name"].lower()):
        name = p["name"]
        slug = slugs.get(name)
        if not slug:
            continue

        mine = personal_by.get(name, [])
        feed = [o for o in offers_by_merchant.get(name, []) if _live(o)]
        listed = [o for o in promos_by.get(name, []) if _live(o)]

        # Every code a visitor could plausibly type, deduped, exclusives first.
        codes, seen = [], set()
        for src in (mine, listed, feed):
            for o in sorted(src, key=_strength, reverse=True):
                c = (o.get("code") or "").strip()
                if c and c.upper() not in seen:
                    seen.add(c.upper())
                    codes.append(c)

        # Best current offer: a personal/exclusive code always wins.
        best = None
        if mine:
            b = sorted(mine, key=lambda c: _pct(c.get("discount", "")), reverse=True)[0]
            best = {"code": b["code"], "title": b.get("discount", ""), "excl": True,
                    "ends": "" if b.get("no_expiry") else b.get("ends", ""),
                    "st": b.get("public_label") or "Verified"}
        else:
            pool = listed + feed
            if pool:
                b = sorted(pool, key=_strength, reverse=True)[0]
                best = {"code": b.get("code", ""), "title": b.get("title", ""),
                        "excl": bool(b.get("exclusive")), "ends": b.get("ends", ""),
                        "st": "Exclusive" if b.get("exclusive") else "Live"}

        # Free-text bucket: sector, offer wording, and meaningful description words.
        hk = hubkw.get(name, [])
        syn = ""
        for stem, words in SECTOR_SYNONYMS.items():
            if any(stem in x.lower() for x in hk + [p.get("sector") or ""]):
                syn += " " + words
        blob = " ".join([(p.get("sector") or ""), " ".join(hk), syn]
                        + [(o.get("title") or "") for o in (listed + feed)[:6]]
                        + [re.sub(r"\s+", " ", (p.get("desc") or ""))[:180]])
        words, wseen = [], set()
        for w in re.findall(r"[a-z0-9%$]{2,}", blob.lower()):
            if w in STOP or w in wseen:
                continue
            wseen.add(w)
            words.append(w)
            if len(words) >= 34:
                break

        out.append({
            "n": name,
            "s": slug,
            "c": (p.get("sector") or "").strip(),
            "w": p.get("network", ""),
            "cd": codes[:8],
            "b": best,
            "x": 1 if mine or any(o.get("exclusive") for o in listed) else 0,
            "h": " ".join(hk),
            "t": " ".join(words),
        })
    return out


# --------------------------------------------------------------------------- UI

SEARCH_CSS = """
.ppsearch{position:relative;max-width:720px;margin:30px auto 0;text-align:left}
.ppsearch .fieldwrap{position:relative}
.ppsearch input{width:100%;padding:16px 46px 16px 48px;font-family:'Josefin Sans',sans-serif;
  font-size:1rem;color:var(--champagne);background:rgba(8,7,12,.82);
  border:1px solid rgba(212,175,55,.55);outline:none;transition:border-color .18s,box-shadow .18s}
.ppsearch input::placeholder{color:var(--muted);opacity:.85}
.ppsearch input:focus{border-color:var(--pink);box-shadow:0 0 0 3px rgba(255,79,163,.22)}
.ppsearch .ico{position:absolute;left:17px;top:50%;transform:translateY(-50%);
  color:var(--gold);font-size:1rem;pointer-events:none}
.ppsearch .clear{position:absolute;right:8px;top:50%;transform:translateY(-50%);
  background:none;border:0;color:var(--muted);font-size:1.35rem;line-height:1;cursor:pointer;
  padding:6px 10px;display:none}
.ppsearch .clear:focus-visible{outline:2px solid var(--pink)}
.ppsearch .hint{margin:9px 2px 0;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);opacity:.8}
.ppres{position:absolute;z-index:60;left:0;right:0;margin-top:8px;max-height:66vh;overflow-y:auto;
  background:#0B0912;border:1px solid rgba(212,175,55,.5);box-shadow:0 24px 60px rgba(0,0,0,.62);
  display:none;-webkit-overflow-scrolling:touch}
.ppres.open{display:block}
.ppres .cnt{padding:11px 18px;font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);border-bottom:1px solid rgba(212,175,55,.2)}
.ppres a.r{display:block;padding:14px 18px;text-decoration:none;color:var(--champagne);
  border-bottom:1px solid rgba(212,175,55,.14)}
.ppres a.r:last-child{border-bottom:0}
.ppres a.r:hover,.ppres a.r.sel{background:linear-gradient(90deg,rgba(255,79,163,.16),rgba(212,175,55,.06))}
.ppres a.r:focus-visible{outline:2px solid var(--pink);outline-offset:-2px}
.ppres .bn{font-family:'Cinzel',Georgia,serif;font-size:1.02rem;letter-spacing:.05em;
  display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.ppres .of{color:var(--muted);font-size:.87rem;margin-top:3px}
.ppres .of code{color:var(--gold-2);background:rgba(212,175,55,.12);
  border:1px solid rgba(212,175,55,.3);padding:1px 7px;font-size:.83rem;letter-spacing:.06em}
.ppres .go{margin-top:6px;font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--pink-2)}
.ppres .badge{font-family:'Josefin Sans',sans-serif;font-size:.58rem;letter-spacing:.18em;
  text-transform:uppercase;padding:3px 8px;border:1px solid var(--gold);color:#0A0710;
  background:linear-gradient(120deg,var(--pink-2),var(--gold-2))}
.ppres .st{font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);
  border:1px solid rgba(212,175,55,.35);padding:3px 8px}
.ppres .zero{padding:22px 18px}
.ppres .zero h3{margin:0 0 6px;font-size:1.05rem;letter-spacing:.06em;color:var(--champagne)}
.ppres .zero p{margin:0 0 14px;color:var(--muted);font-size:.88rem}
.ppres .zero .opts{display:flex;flex-wrap:wrap;gap:9px}
.ppres .zero .opts a{display:inline-block;padding:9px 15px;font-size:.66rem;letter-spacing:.18em;
  text-transform:uppercase;text-decoration:none;color:var(--champagne);
  border:1px solid rgba(212,175,55,.55)}
.ppres .zero .opts a:hover{border-color:var(--pink);color:var(--gold-2)}
@media(max-width:640px){
  .ppsearch{margin-top:22px}
  .ppsearch input{font-size:16px;padding:14px 42px 14px 44px}
  .ppres{max-height:60vh}
  .ppres .bn{font-size:.95rem}
}
"""


def search_html(where: str = "page") -> str:
    """The search box itself. `where` is only used for private telemetry context."""
    return f"""
<div class="ppsearch" data-ctx="{html.escape(where)}">
  <div class="fieldwrap">
    <span class="ico" aria-hidden="true">&#9906;</span>
    <label for="ppq" class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Search brands, promo codes and deals</label>
    <input id="ppq" type="search" autocomplete="off" autocorrect="off" spellcheck="false"
      role="combobox" aria-expanded="false" aria-controls="ppres" aria-autocomplete="list"
      placeholder="Search brands, promo codes &amp; deals&hellip;">
    <button class="clear" type="button" aria-label="Clear search">&times;</button>
  </div>
  <p class="hint">455 brands &middot; every active code &middot; start typing</p>
  <div class="ppres" id="ppres" role="listbox" aria-label="Search results"></div>
</div>
"""


SEARCH_JS = """
<script>
(function(){
  var box=document.querySelector('.ppsearch'); if(!box) return;
  var inp=box.querySelector('#ppq'), out=box.querySelector('#ppres'),
      clr=box.querySelector('.clear'), ctx=box.getAttribute('data-ctx')||'page';
  var DATA=null, loading=false, sel=-1, rows=[], lastQ='', logTimer=null;

  var PCT=/^\d{1,3}\s*%$/;
  function norm(s){return (s||'').toLowerCase().replace(/[^a-z0-9%]+/g,'');}
  function esc(s){return (s||'').replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  /* bounded edit distance - enough for dynvap/lumry, cheap over 455 records */
  function ed(a,b,max){
    if(Math.abs(a.length-b.length)>max) return max+1;
    var prev=[],cur=[],i,j;
    for(j=0;j<=b.length;j++) prev[j]=j;
    for(i=1;i<=a.length;i++){
      cur[0]=i; var best=i;
      for(j=1;j<=b.length;j++){
        cur[j]=Math.min(prev[j]+1,cur[j-1]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1));
        if(cur[j]<best) best=cur[j];
      }
      if(best>max) return max+1;
      prev=cur.slice();
    }
    return prev[b.length];
  }

  function load(){
    if(DATA||loading) return; loading=true;
    fetch('/search-index.json').then(function(r){return r.json();}).then(function(d){
      DATA=d.map(function(m){
        m._n=norm(m.n);
        m._tok=(m.n||'').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
        m._cd=(m.cd||[]).map(function(c){return norm(c);});
        m._all=(m.n+' '+(m.c||'')+' '+(m.h||'')+' '+(m.t||'')+' '+(m.cd||[]).join(' ')+' '+
                ((m.b&&m.b.title)||'')).toLowerCase();
        return m;
      });
      loading=false; if(inp.value.trim()) run();
    }).catch(function(){loading=false;});
  }

  /* Ranking, highest first:
     100 exact merchant | 90 exact code | 80 merchant prefix | 70 exclusive-code hit
     62 token prefix | 60 merchant/category contains | 50 fuzzy merchant | 40 offer text */
  function score(m,q,qn){
    if(m._n===qn) return 100;
    if(m._cd.indexOf(qn)>-1) return m.x?92:90;
    if(m._n.indexOf(qn)===0) return 80;
    if(m.x && m._cd.some(function(c){return c.indexOf(qn)===0;})) return 70;
    for(var i=0;i<m._tok.length;i++) if(m._tok[i].indexOf(q)===0) return 62;
    if(m._n.indexOf(qn)>-1) return 60;
    if((m.c||'').toLowerCase().indexOf(q)>-1) return 58;
    if((m.h||'').toLowerCase().indexOf(q)>-1) return 57;
    if(PCT.test(q)){
      var bt=((m.b&&m.b.title)||'').toLowerCase();
      if(bt.indexOf(qn)>-1) return 56;
      if((m.t||'').indexOf(qn)>-1) return 44;
      return 0;
    }
    if(qn.length>=4){
      var max=qn.length<=6?1:2;
      if(ed(qn,m._n,max)<=max) return 50;
      for(var k=0;k<m._tok.length;k++){
        var t=norm(m._tok[k]);
        if(t.length>=4 && ed(qn,t,max)<=max) return 48;
      }
    }
    if(m._all.indexOf(q)>-1) return 40;
    return 0;
  }

  function card(m){
    var b=m.b||{}, bits='';
    if(b.code) bits+='<code>'+esc(b.code)+'</code> ';
    if(b.title) bits+=esc(b.title);
    if(!bits) bits='Deals and current offers';
    var badge=m.x?'<span class="badge">Exclusive</span>':'';
    var st=b.st?'<span class="st">'+esc(b.st)+'</span>':'';
    return '<a class="r" role="option" href="/promo-codes/'+esc(m.s)+'/" data-m="'+esc(m.n)+'">'+
      '<span class="bn">'+esc(m.n)+badge+st+'</span>'+
      '<span class="of">'+bits+'</span>'+
      '<span class="go">View Codes &amp; Deals &rarr;</span></a>';
  }

  function zero(q){
    return '<div class="zero"><h3>We couldn\\u2019t find that brand or code yet.</h3>'+
      '<p>Nothing here matches &ldquo;'+esc(q)+'&rdquo;. Try a shorter spelling, or start here:</p>'+
      '<div class="opts">'+
      '<a href="/promo-codes/">Browse all promo codes</a>'+
      '<a href="/promo-codes/#merchants">Browse A&ndash;Z brands</a>'+
      '<a href="/promo-codes/#exclusive">My exclusive codes</a>'+
      '<a href="/promo-codes/#all">Popular &amp; current deals</a>'+
      '<a href="https://pixies-pantry.com/shop/">Shop Pixie\\u2019s Pantry</a>'+
      '</div></div>';
  }

  function log(q,n){
    if(!q||q===lastQ) return; lastQ=q;
    try{
      var body=JSON.stringify({q:q.slice(0,80),n:n,z:n?0:1,c:ctx});
      if(navigator.sendBeacon) navigator.sendBeacon(TELEMETRY_URL,new Blob([body],{type:'text/plain'}));
    }catch(e){}
  }

  function run(){
    var q=inp.value.trim().toLowerCase();
    clr.style.display=q?'block':'none';
    if(!q){close(); return;}
    if(!DATA){load(); return;}
    var qn=norm(q), scored=[];
    for(var i=0;i<DATA.length;i++){
      var s=score(DATA[i],q,qn);
      if(s>0) scored.push([s,DATA[i]]);
    }
    scored.sort(function(a,b){
      if(b[0]!==a[0]) return b[0]-a[0];
      if((b[1].x||0)!==(a[1].x||0)) return (b[1].x||0)-(a[1].x||0);
      return a[1].n.toLowerCase()<b[1].n.toLowerCase()?-1:1;
    });
    rows=scored.slice(0,25).map(function(x){return x[1];});
    sel=-1;
    if(!rows.length){ out.innerHTML=zero(inp.value.trim()); }
    else{
      out.innerHTML='<div class="cnt">'+scored.length+' match'+(scored.length===1?'':'es')+
        (scored.length>25?' &middot; showing 25':'')+'</div>'+rows.map(card).join('');
    }
    out.classList.add('open'); inp.setAttribute('aria-expanded','true');
    clearTimeout(logTimer);
    var n=scored.length;
    logTimer=setTimeout(function(){log(q,n);},1300);
  }

  function close(){out.classList.remove('open');out.innerHTML='';inp.setAttribute('aria-expanded','false');sel=-1;}

  function move(d){
    var els=out.querySelectorAll('a.r'); if(!els.length) return;
    if(sel>-1&&els[sel]) els[sel].classList.remove('sel');
    sel=(sel+d+els.length)%els.length;
    els[sel].classList.add('sel'); els[sel].scrollIntoView({block:'nearest'});
  }

  inp.addEventListener('input',run);
  inp.addEventListener('focus',load);
  box.addEventListener('mouseenter',load);
  inp.addEventListener('keydown',function(e){
    if(e.key==='ArrowDown'){e.preventDefault();move(1);}
    else if(e.key==='ArrowUp'){e.preventDefault();move(-1);}
    else if(e.key==='Enter'){
      var els=out.querySelectorAll('a.r');
      var t=sel>-1?els[sel]:els[0];
      if(t){e.preventDefault();t.click();}
    }
    else if(e.key==='Escape'){close();inp.blur();}
  });
  out.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a.r'); if(!a) return;
    try{
      var body=JSON.stringify({q:inp.value.trim().slice(0,80),n:rows.length,z:0,
                               m:a.getAttribute('data-m'),c:ctx});
      if(navigator.sendBeacon) navigator.sendBeacon(TELEMETRY_URL,new Blob([body],{type:'text/plain'}));
    }catch(err){}
  });
  clr.addEventListener('click',function(){inp.value='';close();inp.focus();});
  document.addEventListener('click',function(e){if(!box.contains(e.target)) close();});
  load();
})();
</script>
"""


def search_js() -> str:
    return f'<script>var TELEMETRY_URL="{TELEMETRY}";</script>' + SEARCH_JS
