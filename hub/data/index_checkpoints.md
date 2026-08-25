# Index-state checkpoint protocol (frozen 2026-08-25)

Baseline: hub/data/t0_baseline.json — FROZEN. Never overwrite; append snapshots.

## Report format — ONLY this table, nothing else
| URL | T0 state | T+Nh state | Transition | Last crawl | Google canonical | Action needed |

Do NOT re-run the 455-page audit, link reconciliation or page counts unless an
inspection exposes a systemic issue. Dusty has accepted those as closed.

## T+24h scope: exactly two URLs
- /promo-codes/dynavap/  (T0: UNKNOWN)
- /promo-codes/efe/      (T0: not yet tested — corrected URL)

Rules:
- DynaVap UNKNOWN -> DISCOVERED/CRAWLED/INDEXED: record transition, leave page unchanged.
- EFE discovered/indexed normally: close the phantom-404 issue permanently.
- Either still UNKNOWN: verify ONLY sitemap presence, internal linking, HTTP 200,
  self-canonical, indexability. Then leave it alone unless one of those fails.

## Checkpoints: T+24h, T+48h, T+72h, T+7d. State transitions only.

## Permanent rules
- Resolve merchant slugs from partners.json BEFORE any URL Inspection.
- Classify Impact by tracking-path structure `/c/<pub>/<campaign>/<ad>`, never hostname text.
- Dusty20 stays withheld until current merchant/network confirmation.
- WITHHELD codes never appear publicly.
- No network rerouting without proven attribution failure.
- Historical codes remain historical until reverified.
- UNKNOWN != failed and != zero.

## The funnel being measured
UNKNOWN -> DISCOVERED -> CRAWLED -> INDEXED -> IMPRESSIONS -> CLICKS -> AFFILIATE CONVERSIONS
