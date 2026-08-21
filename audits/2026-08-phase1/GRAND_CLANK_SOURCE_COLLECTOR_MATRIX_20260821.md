# GRAND CLANK SOURCE & COLLECTOR MATRIX — 2026-08-21 (audited 2026-08-22)

Phase 1F/1G deliverable. Fleet-wide matrix making structural blindness visible. Event-capable = can produce editorial events; Baseline-safe = adding to live DB cannot flood alerts.

## watch-clank (EXEMPT reference — summary only)
17 registered collectors: Casio multi/news, Citizen news/products(+DE sitemap-delta), Seiko news/JP retail, Timex news/products, CASIOBLOG, G-Central, Plus9Time, Monochrome/Deployant/Fratello/WatchTime specialist RSS, Gear Patrol (local-only), G-Shock World. Editorial freshness classes FRESH/STALE_PUBLICATION/BASELINE/UNKNOWN_TIMESTAMP/MANUAL_UNDATED on every specialist lead.

## smartphone-clank — 8 production sources, ALL catalogue-inventory

| Collector | Source | Region | Type | Scheduled | Deployed | Event-capable | Baseline-safe | Freshness | Availability | Health | Known miss class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| samsung_us_support_sitemap | samsung.com/us support sitemap | US | official-support | systemd 3h | Hetzner b8b89885 | yes (multi-hash page change) | traversal-cursor legacy | weak (page dates) | no | degraded/unexpected_zero states exist | first-15-URL historical blindness FIXED; pre-ledger rows absorbed |
| google store phones | store.google.com category | **US only** | official-catalogue | systemd 45m | same | catalogue appearance incl teasers | single_full_enumeration + suppression | no | implicit in catalogue | consent-wall → degraded (fixed) | region gap: GB/IN/JP stores absent |
| nothing products | nothing.tech sitemaps | multi | official-catalogue | 90m | same | catalogue | per-source epoch | no | no | standard | marketing-slug identity only |
| oneplus regional sitemap | oneplus.com/{region} | US+ | official-catalogue | 90m | same | catalogue | same | no | no | standard | no CPH codes → identity ambiguity |
| motorola sitemaps | motorola.com {us,gb,de} | US/GB/DE | official-catalogue | 6h | same | catalogue | same | no | no | standard | 106/124 slugs AMBIGUOUS/cycle churn [D-27] |
| honor global sitemap | honor.com | Global | official-catalogue | 6h | same | catalogue | same | no | no | standard | — |
| oppo / realme global sitemaps | oppo.com, realme.com | Global | official-catalogue | 6h ×2 | same | catalogue | same | no | no | standard | — |
| xiaomi wave adapter | mi.com | — | official-catalogue | NOT scheduled | staging only | catalogue | KEEP_STAGING | no | no | 403 oscillation documented | Akamai adaptive blocking |

Dormant/disabled (13): certification bodies (BIS/BT-SIG/TDRA/IMDA/FCC), generic support collectors (contamination vector, disabled), OTA/firmware collectors, samsung IN/GB BLOCKED Akamai, samsung_us_owners_product LIVE_VALIDATED with NO wired collector. **Structural blindness: zero editorial sources enabled; launch-news detection impossible by construction.**

## smartwatch-clank — 4 PRODUCTION allowlisted, 10 EXPERIMENTAL

| Collector | Source | Region | Type | Scheduled | Deployed | Event-capable | Baseline-safe | Notes |
|---|---|---|---|---|---|---|---|---|
| samsung_product_catalogue | samsung.com {us,uk,in,de,sec}/watches | 5 regions | official-catalogue | soak timer | Hetzner d987b66 | NEW_DEVICE etc HIGH | silent first run | allowlisted |
| samsung_support_in/gb/de | support sitemaps SM-L filter | IN/GB/DE | official-support | same | same | SUPPORT_PAGE_APPEARED/SOURCE_LISTING_REMOVED | silent; whole-snapshot reject if ANY page fails | UK baseline 162 pages; high-volume low-yield |
| garmin_catalogue | garmin product-sitemap → 4324 pages | US | official-catalogue | experimental runs | not deployed as prod | catalogue changes | silent | EXPERIMENTAL tier |
| amazfit_catalogue/_official_news | Shopify products.json; news.atom | US | official+news | experimental | not deployed | NEWS_ITEM_APPEARED w/ title classifier | silent | — |
| coros_support/_updates/_official_news | Zendesk API; stories HTML | global | official-support+news | experimental | not deployed | updates w/ affected_devices | silent | — |
| apple/google official news feeds | RSS/Atom | global | official-news | experimental | not deployed | NEWS_ITEM_APPEARED | roll-off suppressed | Pixel Watch traffic value questioned in handoffs |

**Notifications NotImplementedError → all event capability latent.** Garmin/boutique expansion merged but undeployed.

## feature-phone-clank

| Collector | Source | Region | Type | Scheduled | Deployed | Event-capable | Baseline-safe | Notes |
|---|---|---|---|---|---|---|---|---|
| hmd-nokia | hmd.com/en_int listings + sitemap-dtc | global(en_int) | official-catalogue | Windows 4×d IST + Hetzner cron 4×d UTC | c749df3 prod | NEW_PRODUCT/FIELD_CHANGED/SPECS_BECAME_{AVAIL,UNAVAIL}/PRODUCT_REMOVED/IDENTITY_ANOMALY/CLASSIFICATION_CHANGED | catastrophic-zero gate + scope wall | allowlist-free discovery cuts both ways |
| itel-india | itel-india.com SPA | IN | official-catalogue | user crontab 3×d | 49eab25 exp checkout | via run-experimental | separate DB/lock/volume PROVEN SHA-256 | Playwright/Chromium; selector fragility; networkidle hang fixed |
| lava-india | lavamobiles.com __NEXT_DATA__ | IN | official-catalogue | user crontab 4×d | same | same | same | JSON transport robust |

**Zero notification path anywhere [D-21].**

## tablet-clank

| Collector | Source | Region | Type | Scheduled | Deployed | Event-capable | Baseline-safe | Notes |
|---|---|---|---|---|---|---|---|---|
| apple_us_ipad_pro_store | apple.com US store config | US | official-catalogue | NEVER | no | new_product + identity_correction | complete(48) baseline | healthy post-fix; 24 corrections retained |
| apple_in_ipad_pro_store | same IN | IN | official-catalogue | NEVER | no | same | complete(48) | regional part numbers unresolved SKU→A-model |
| honor_cn_tablets_catalogue/_comparison | honor.com/cn | CN | official-catalogue | 1 manual cycle ever | claimed Wave-1 "production-approved" | yes | completeness guards ≥20 slugs+4 anchors | production theater [D-22] |
| tcl_global_tablets | tcl.com/global | global | official-catalogue | 1 manual cycle ever | same | yes | guards ≥8 slugs+2 anchors | same |
| samsung_us_sitemap | top_sitemap.xml | US | official-catalogue | never | no | yes | complete(3) | tiny surface |
| lenovo_psref.py | PSREF | — | official-evidence | never | BLOCKED fixture-parser only | no | n/a | token-gated 403/405 JS shell |
| xiaomi_mimall.py | Mi Mall | CN | official-catalogue | never | XIAOMI_SOURCE_NOT_RELIABLE offline probe | no | n/a | IDs resolve to appliances (stale/reassigned) |

No Huawei collector exists (research PARKED). **All evidence gitignored; zero unattended execution in repo history [D-22].**

## korean-tech-wire — the promotion-methodology reference

| Source | Domain | Region | Type | Cadence | Scheduled | Deployed | Event-capable | Baseline-safe | Health truth | Known miss class |
|---|---|---|---|---|---|---|---|---|---|---|
| sk_hynix_newsroom | news.skhynix.co.kr/feed | KR | official-news RSS | 2h due-gated | systemd timer | Hetzner | no events by policy | n/a | **HOST-BLOCKED since day 1; dashboard says HEALTHY [D-05,D-12]** | entire soak produced 0 articles from flagship source |
| the_elec | thelec.kr indices | KR | specialist-news | 2h | shared timer | Hetzner | no (by policy) | signal-term allowlist filter | 403/403 early → recovered | broad-index leakage quarantined; resurrection defect [D-13]; promotion stranded on stage4.1 |
| etnews_hardware | etnews.com sections | KR | mainstream-tech-news | 2h | shared timer | Hetzner | no | low-value denylist | 99.3% run success | promotion stranded on stage4.1 |
| samsung_newsroom_kr | news.samsung.com/kr | KR | corporate-newsroom | 2h | shared timer | Hetzner | no | **NO FILTER AT ALL — 19,344/19,344 accepted [D-13 adjacent]** | REWORK decided, unfixed | Galaxy stunts/fashion/CSR dominate corpus |
| lg_display_newsroom | lgdisplay.com/kor | KR | corporate-newsroom | 2h | shared timer | Hetzner | no | employer/CSR denylist | connection resets ×18 mid-soak; 5 articles frozen since 08-10 | date-only timestamps (KST midnight floor) |

Deferred/rejected sources: DART/OpenDART (credential-blocked), ZDNet Korea, Digital Daily, Naver/Daum aggregators. **Due-gating defect quadrupled publisher load 8.5 days [D-6].**

## chinese-tech-wire — 14 sources, Tier B soak

| Layer | Sources | Region/Lang | Transport | Events | Baseline quality | Known status |
|---|---|---|---|---|---|---|
| NEWS | ithome 0.85, mydrivers 0.80, expreview(RSS) 0.90, zol 0.70, jiwei/laoyaoba 0.88, benchlife(TW) 0.88, technews(TW) 0.87, xfastest 0.82 **BLOCKED**, hkepc 0.85 **BLOCKED** | CN/TW/HK zh | HTML/RSS polls (~5m ithome) | cluster leads; article alerts OFF | per-source numeric baselines | 2 of 9 blocked |
| COMMUNITY | chiphell (Discuz), mobile01, coolaler (XenForo); ptt DISABLED (HTTP 500 gateway) | CN/TW | forum HTML | threshold 75 leads | — | anti-bot risk flagged |
| DOCUMENTARY | jd.com watchlist scrape PARTIAL; geekbench DISABLED permanently (anti-automation) | CN | retail scrape | snapshot→change events | — | partial coverage |
| Regulatory | SRRC/NCC researched, NOT implemented | CN/TW | — | — | — | future |

Credential posture: no leaks in git (DISPROVEN); rotation OPEN [D-25]. Field-test collection disabled on main; unmerged branch enables isolated local collection.

## oem-radar — 21 enabled of 28 descriptors

| Engine | OEMs | Region | Type | Scheduled | Deployed | Event-capable | Baseline-safe | Known miss class |
|---|---|---|---|---|---|---|---|---|
| shopify ×12 | acemagic, aoostar, beelink, bosgame, chuwi, gmktec, kamrui, minisforum, morefine, nipogi, starlabs, vaio | US/global | retailer-direct catalogue | hourly cmd (Windows) + dashboard auto-crawl | UNKNOWN authority [D-03] | restock/spec/new severity-scored → outbox | baseline ⇒ suppressed at insert | filtering gaps 6/50 bankai misses (Chuwi×3 GMK Minisforum Bosgame) |
| sitemap_jsonld ×4 | khadas, simplynuc, lg, medion@72h | global/regional | official sitemaps | same | same | yes | same | — |
| woocommerce ×3 | geekom, novacustom, pine64 | EU/US | retailer-direct | same | same | yes | same | — |
| category_jsonld ×1 | samsung.com | US | official-catalogue | same | same | yes | same | — |
| dell engine | dell.com | US | official-retailer | **disabled** since 2026-08-10 | persistent 403 | — | — | hard block |
| MISSING | **Lenovo (config exists, BLOCKED_BOT 403, refusal-to-spoof), ASUS (no descriptor — client-rendered Nuxt), Acer (timeouts), HP (timeouts), MSI (hard 403), Gigabyte/AORUS (never probed)** | — | — | — | — | — | — | **44/50 bankai misses = REGION_GAP concentrated here [D-01]** |
| evidence subsystem | Lenovo PSREF | — | official-evidence | NOT WIRED into runs | inert | evidence_items/links/events tables exist empty-ish | n/a | PSREF evidence exists separately from collectors [seed claim PROVEN] |

**Recall reality: 0/50 benchmark events alerted in useful time despite 21 enabled sources [D-01].**

## free-game-tracker

| Source | Domain | Type | Scheduled | Deployed | Event-capable | Baseline-safe | Health truth | Known miss class |
|---|---|---|---|---|---|---|---|---|
| epic | epicgames.com JSON | official-retailer promo | Hetzner cron hourly | hetzner ledger SHAs | GAME_PROMOTION alerts | **NO — fresh DB floods [D-16]** | 200+0=ok forever possible | JS-walled parsers read healthy at zero |
| ps_blog (PS Plus) | blog RSS + standalone articles | official-news | same | incident fix deployed 3546540f | SUBSCRIPTION alerts (post-fix) | same | same | subscription blackout historical [D-7] |
| xbox_game_pass | XGP catalog | subscription catalog | same | f6b4b77c→cec034695d52 | SUBSCRIPTION | same | successful_sources guard vs fake departures | global-region leakage fixed to US |
| geforce_now | GFN catalog | subscription catalog | same | same | SUBSCRIPTION | same | stable synthetic URLs | ElementTree falsy-element RSS bug class found; fleet audit recommended UNVERIFIED done |
| steam breakouts/deals | Steam API | storefront lanes | same | same | breakout/deal alerts bypass compare() | appid-not-in-previous keyed | — | side-lane semantics differ from main diff |
| prime_gaming | primegaming.blog | official-promo | **NOT REGISTERED anywhere** | never | module+tests exist | mock parser returns 0 items | React-rendered wall documented | dead code documented as feature [D-24 ledger #8] |
| amazon_luna | Luna channels | subscription | NOT REGISTERED | never | module exists | recon withdrew false claims post-June-2026 shutdown | frozen with conditions | dead code |

Webhook echoed into assistant transcript 2026-08-09; rotation UNCONFIRMED [D-25].

## semiconductor-intelligence

| Collector | Domain | Transport | Default | Event-capable | Notes |
|---|---|---|---|---|---|
| radar rss provider | tech media global | RSS/Atom cursor | OFF after import | SignalItems→candidates | 80 sources imported from legacy signal_radar.db (5211 items) — not collected by this codebase |
| radar x provider | X leaks community | Playwright + human cookie session | OFF; not in container | same | no automated login (deliberate) |
| google news discovery | global news ring ≤3 queries/story | RSS budgeted ≤5 cycles/hr | OFF until enabled | DiscoveryResults, never auto-evidence | relevance ≥0.45 gate |
| editorial feed discovery | alternate-link sniffing | HTTPS | on-demand | SourceSuggestions → human accept | — |
| rss_plugin / pci_ids_plugin | canonical evidence feeds; hardware registry | HTTPS/dataset | manual/pipeline | Evidence immutable content-hash | — |
| legacy_importer | old signal_radar.db | SQLite read-only | one-shot idempotent | bulk derived | rejected tables excluded |
| DEAD vendored src/oem_radar engines ×18 OEMs | mini-PC retail | HTML/JSON | manual only | restock/spec diffs | wrong-app scheduled script hazard [D-02] |

**Scheduler-heartbeat is its strongest subsystem; collection itself is almost entirely off.**
