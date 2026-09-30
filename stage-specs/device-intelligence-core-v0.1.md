# Device Intelligence Core (DIC) — unified discovery for Smartphone, Tablet, Smartwatch

- **Status:** PROPOSED v0.1 — REVIEW REQUIRED. This is a stage specification, **not** canonical
  architecture and not an ADR. Adoption requires operator review; implementation requires a
  ClankOps Mission per DEVELOPMENT_CONTROL.md / AGENT_RULES.md rule 16.
- **Date:** 2026-09-18
- **Author:** ZCode agent, commissioned architecture investigation
- **Evidence revision:** current-state facts verified against `origin/main` at:
  smartphone-clank `60bc5f5`, tablet-clank `c5d998d`, smartwatch-clank `5c2a816`,
  watch-clank `904e609`, oem-radar `90c8185`, clankops `main@2026-09-15`,
  standards-clank `master@2026-09-16`, clank-architecture `main@2026-09-15`,
  motherclank `main@2026-08-26`, unified-clank-platform `main@2026-08-21`.
- **Governing context:** Phase 0 no-promotion freeze is ACTIVE. Nothing in this document
  authorizes deployment, timers, or promotion. All Phase 1 execution is manual, local, staging-only.

---

## 0. Summary

The three device Clanks (smartphone-clank, tablet-clank, smartwatch-clank) each crawl OEM
first-party surfaces and classify URLs into editorial events. This works, but OEM pages are
among the *last* places a new device becomes observable. Regulatory databases, benchmarks,
retailers and support systems expose devices weeks earlier — and each of the three Clanks has
the regulatory/benchmark skeletons or the desire, but none has the plumbing: three different
stacks, three entity models, three baselining mechanisms, three alert policies.

This proposal creates one **Device Intelligence Core**: a single new Clank (`device-intel`) that
owns discovery planes (regulatory / runtime / commerce / OEM), a normalised evidence store, a
conservative entity resolver, a novelty firewall, targeted fan-out, INTEL/RELEASE alerts, and
source lead-time telemetry. Smartphone / Tablet / Smartwatch become **editorial profiles**
(data, not architecture) over the same core. The existing three Clanks are not merged or
rewritten; they remain authoritative for their own history and are progressively demoted to
enrichment sources plus linked editorial views (link-not-merge, per ADR-0005 v0.2 §6 and the
Standards Clank cross-Clank HOLD).

Phase 1 is a proving slice — KOMDIGI (or fallback regulator) + Geekbench + resolver + evidence +
fan-out + INTEL + strict baseline suppression — whose explicit success measure is that
evidence-centric discovery demonstrably beats OEM-page crawling (lead-time telemetry, not vibes).

---

## 1. Current-state assessment

### 1.1 The three device Clanks today

| | smartphone-clank | tablet-clank | smartwatch-clank |
|---|---|---|---|
| Stack | Python 3.11+, SQLAlchemy 2 + Alembic, httpx, Typer | **Zero-dependency** stdlib (sqlite3, urllib) | **Zero-dependency** stdlib; raw SQLite schema v4 |
| Store | SQLite; `devices` keyed `(manufacturer, model_number)`; evidence w/ decay; confidence ledger; aliases; timeline; families; regional sightings; device_relationships | SQLite; `products` keyed by compound `identity_key` (manufacturer+model/sku+**region**+connectivity+RAM+storage); `observations`; `change_events`; QC archive DB | SQLite; `observations` (collector-defined identity strings); `discoveries`; `evidence_records` UNIQUE `(source_class, identity)`; `prelaunch_candidates` (Samsung support-page pre-launch detection) |
| Discovery sources | Samsung support sitemap (production); Wave1/2 OEM sitemaps/storefronts (Google, Nothing, OnePlus, Motorola, Honor, Oppo, Realme); **skeleton FCC/BIS/TDRA/IMDA collectors returning `[]`; Bluetooth SIG collector disabled** | 8 OEM-only sources (Samsung sitemap, Apple Store US/IN, Honor CN/UK, TCL, Lenovo PSREF offline, Xiaomi offline). Dormant policy: Honor+TCL only are production-selected | Samsung catalogue + 3 regional support sitemaps, Google/Apple/Samsung/Garmin/Amazfit/COROS news, Garmin product sitemap, Amazfit Shopify, COROS Zendesk support, DC Rainmaker. 13-collector production allowlist |
| Alerting | Discord newsroom+maintenance; fail-closed reason allowlists; source-maturity gate; `webhook_deliveries` persistence; `backfill` firewall | **None** (`ALERTS_ENABLED=False`, grep-enforced); human QC queue instead | Persistence-first Discord outbox (origin/main `9d85f92`); editorial levels CRITICAL/NEWSWORTHY/MONITOR/NOISE; activation cutoff |
| Novelty control | `wave1_baseline_state` per-source epochs; backfill=True for the completing run; suppressed reason codes (`baseline_import`, `initial_backfill`) | `source_state.baseline_complete`; events only written when baseline already complete | First healthy run = silent baseline; qualification epochs; production allowlist |
| Entity resolution | Exact `(manufacturer, model)` + regional-suffix family key; alias table; **no fuzzy, no scoring** | Compound identity key; region is identity-splitting by design | Collector-defined identity strings; Samsung-specific reconciliation tables |
| Health | `collector_run_metrics` + deterministic health score + daily report | `source_state` + `classify_health` (NEVER_RUN…BLOCKED) | Per-collector `collector_health`; exception taxonomy (BLOCKED/RATE_LIMITED/PARSER) |

(watch-clank is out of scope — it covers *analog* watches — but is the fleet's best precedent for
evidence grades, release-lead telemetry (`lead_time_days`), specialist-vs-official two-lane
editorial, delivery receipts, editorial-freshness-vs-novelty separation, and bulk-touch noise
detection. This proposal reuses those patterns.)

### 1.2 Platform & governance facts this design must honour

- **Fleet Laws 1–8** (clank-architecture/FLEET_LAWS.md): no-flood init; observation ≠ novelty;
  health honesty; explicit event capability; single scheduler+notification authority per lane;
  provenance; writer coordination; promotion gates.
- **Canonical architecture v0.2 / ADR-0005:** observer-only adapters; instance/lane identity;
  baseline handover records; **cross-Clank entity resolution blocked until its own ADR** (§6);
  semantic zeros must be typed; capability states are evidence-bearing.
- **ADR-0014:** typed `EvidenceEnvelope` (evidence_type, evidence_version, subject, observed_at,
  occurred_at?, substrate, payload, provenance, content_hash) + semantic clocks.
- **Standards Clank (all RATIFIED MUST):** STD-DATA-COM-001 (continuity explicit), -002 (first-seen
  ≠ novelty; **read-side baseline exclusion built into every novelty path**), -003 (conservative,
  evidence-gated, auditable, reversible merges), -004 (observation / derived-canonical /
  operator-decision tiers separable and traceable); STD-OPS-COM-001/002 (execution recorded;
  dual-plane health); STD-UI-COM-002/003 (atomic QC, read-side queue exclusion) when a QC UI
  exists; STD-CUD-001 for any dashboard. **Cross-Clank entity identity is HELD/DO_NOT_STANDARDISE**
  (docs/data-ontology/constitution.md "Not a standard").
- **ClankOps / DEVELOPMENT_CONTROL:** new Clanks are registered at inception; every material
  tranche needs Mission + Session + checkpoint + handoff.
- **Phase 0:** promotion frozen; all current clanks `UNVERIFIED_PRODUCTION`; no timers from this
  work (fleet AGENTS.md rule 2: local collection is manually triggered).
- **UCP status:** frozen supersession candidate; the live shared-contract surfaces are
  `clank_runtime` (stage-0 contracts, evolved in diagnostic-clank) and the Motherclank observer
  adapter surface (`contract.py` v0.2 + EvidenceEnvelope v0.3.1). A new Clank should expose the
  observer surface method shapes from day one but onboarding order is operator-gated.

### 1.3 What already exists that this design reuses

| Pattern | Proven | Reused as |
|---|---|---|
| Persistence-first Discord outbox w/ dedup_key, attempts, 429 `not_before` | smartwatch-clank (origin/main), oem-radar | DIC alert outbox |
| Fail-closed alert reason allowlists + maturity gate + staging isolation | smartphone-clank `alerts/` | DIC alert eligibility |
| Per-source baseline epoch; backfill=True on the completing run; failed run never completes baseline | smartphone-clank `wave1_baseline_state`; watch-clank epochs | DIC epochs + novelty gate G0 |
| Evidence grades & "only official product page + freshness may claim release" | watch-clank WATCH_EVENT_SEMANTICS.md | DIC RELEASE gate |
| `lead_time_days` on correlated leads | watch-clank specialist_leads | DIC lead-time telemetry (generalised) |
| 72-hour freshness window; bulk-touch cluster detection | watch-clank freshness.py | DIC novelty freshness gate |
| Community evidence never alerts (confidence 0.0, delivery blocked, novelty unconfirmed) | oem-radar Reddit admission | DIC PRESS/COMMUNITY planes (deferred, designed-for) |
| Engines/collectors never write the DB; return typed results + metrics | watch-clank, smartwatch-clank, oem-radar | DIC SourceAdapter contract |
| Zero-dependency vs SQLAlchemy split | tablet/smartwatch vs smartphone/watch | DIC standardises on the smartphone/watch stack (donor) |
| QC archive DB + decisions vocabulary USEFUL/NOT_USEFUL/FALSE_POSITIVE/OUT_OF_STOCK | tablet-clank, watch-clank reviews | DIC QC + telemetry false-positive rates |
| Read-only cross-store adapters with `mode=ro` and integrity proof | Motherclank adapters | Phase 3+ linkage runner |

---

## 2. Problems in the present Smartphone/Tablet/Smartwatch design

1. **Discovery plane is inverted.** All three Clanks' *production* discovery sources are OEM
   surfaces (support sitemaps, product catalogues, storefronts). Regulatory collectors exist only
   as smartphone-clank skeletons that return `[]`. By construction, the fleet cannot see a device
   before its marketing machinery exists — which is the entire editorial point.
2. **Three entity models, none identifier-first.** smartphone-clank requires
   `(manufacturer, model_number)` at insert; tablet-clank splits identity by region+RAM+storage
   (so a certification sighting of `SM-X746B` and a retail sighting of the same board are
   different *products*); smartwatch-clank keys on collector-defined strings. None can represent
   "a model code with unknown marketing name accumulating evidence" as a first-class citizen.
3. **No fan-out.** When smartphone-clank sees a new model code there is no mechanism to ask
   Geekbench, Bluetooth SIG, or retailers "have you seen this?" Evidence that would corroborate or
   refute a candidate is never sought; it is only stumbled upon.
4. **No lead-time accountability.** No Clank can answer "which source actually finds devices
   earliest, and which is noise?" — so source budgets are vibes. watch-clank's `lead_time_days`
   exists only inside its specialist-lead lane.
5. **Triplicated hard problems.** Baselining, alert suppression, health, provenance, QC, and
   Discord delivery exist in three (really five, counting watch/oem-radar) slightly different
   implementations, each with its own incident corpus. Every new regulatory source would have to
   be integrated three (or four) times.
6. **Device class is baked in at the repo boundary.** smartphone-clank's validators *reject*
   tablet model codes (`REASON_TABLET_NOT_PHONE`); tablet-clank only accepts tablets. A
   certification record is inherently class-agnostic ("SM-X746B" is a tablet; "SM-S928B" is a
   phone; KOMDIGI lists both) — the current architecture throws the cross-class signal away.
7. **Editorial classes are architecture.** To cover a new device class well you must clone a
   repo. The marginal cost of "also cover tablets properly" in smartphone-clank is a fourth repo.

Non-problems deliberately *not* claimed: the existing Clanks are individually well-run — the
baselining, eligibility, and health discipline is genuinely good and is the donor material here.

---

## 3. Proposed target architecture

### 3.1 The mental-model shift

```
TODAY   OEM crawl → new URL → classify → alert
TARGET  external signal → candidate device → identity resolution → targeted enrichment/fan-out
        → novelty decision → editorial alert
```

OEM sources become **confirmation/enrichment** inputs (authority tier 1, discovery value lower),
except in the smartwatch profile where OEM retains a higher discovery weighting.

### 3.2 Shape of the solution

**One new Clank: `device-intel`** (Device Intelligence Core).

- **One repository, one package (`device_intel`), one SQLite store.** Single process, single
  writer lock, manual execution. Not a service mesh, not a message bus, not a second runtime.
- **Three editorial profiles** (`smartphone`, `tablet`, `smartwatch`) as *configuration*: signal
  weights, novelty windows, fan-out eligibility, alert floors and routing, OEM weighting.
  Device class is a **derived, evidence-based classification** on the entity, never a hard
  ingestion filter.
- **Evidence-centric:** collectors produce normalised `EvidenceDraft`s; the store's unit of truth
  is an *evidence row*, not a URL and not a lifecycle stage. Marketing names are optional
  everywhere; model codes, cert IDs and codenames are first-class indexed identifiers.
- **Conservative resolver:** exact-identifier first; auto-merge only on deterministic
  discriminators; everything else becomes an auditable, reversible claim (STD-DATA-COM-003).
- **Novelty firewall:** ordered deterministic gates (§10) between evidence and alerts; every
  decision appended to an inspectable ledger; baseline-era records excluded by construction in
  every novelty path (STD-DATA-COM-002).
- **Existing Clanks untouched in Phase 1.** From Phase 3 they become enrichment sources and
  *linked* editorial views (`external_links`, link-not-merge). Full convergence of their
  discovery roles is an operator decision per Clank, gated by the future cross-Clank identity ADR.

### 3.3 Architectural invariants (binding on any implementation)

1. Marketing name is nullable everywhere; no ingestion path may require it.
2. A collector never writes the DB and never raises past its adapter boundary (Law: typed
   results + metrics; failures are data).
3. Evidence is immutable once written; corrections are new evidence rows, not updates.
4. Derived tables (`entity_signals`, classifications, editorial stage, telemetry) are always
   recomputable from raw evidence + claims; each derived row cites its evidence ids.
5. Every novelty evaluation is appended to `novelty_decisions` before any alert intent is written.
6. Baseline/continuity state lives in `epochs` and is consulted by *every* novelty path's own
   WHERE/predicate (read-side exclusion, STD-DATA-COM-002).
7. One scheduler authority, one notification authority per lane; staging lanes can never load
   production webhook credentials (smartphone settings precedent).
8. Fan-out depth is hard-capped at 1: fan-out-triggered evidence never triggers new fan-out.
9. No LLM in ingestion, resolution, classification, or novelty. (LLM-assisted *rendering* of an
   already-decided alert, OEM-Radar ADR-5 style, is permitted later; it can never change a fact.)
10. Idempotency: replaying any run is a no-op at the evidence level (content-hash dedupe) and at
    the alert level (dedup keys).

---

## 4. Component diagram

```
                    ┌─────────────────────────────────────────────────────────────────────────────┐
   SOURCE PLANES    │                     device-intel  (one process, one SQLite store)           │
                    │                                                                             │
 KOMDIGI / FCC /    │  ┌──────────────┐   EvidenceDraft   ┌──────────────┐                        │
 BIS / BT SIG / WFA │  │ collectors / │ ────────────────► │  ingestion   │──► evidence (+ids)     │
 ──────────────────►│  │ adapters     │  + AdapterMetrics │ (dedupe,     │    evidence_identifiers│
                    │  └──────▲───────┘                   │  baseline    │                        │
 Geekbench / Google │         │ query_identifier()        │  epoch)      │                        │
 device catalog /   │         │ (fan-out, depth 1)        └──────┬───────┘                        │
 firmware DBs ─────►│         │                                  ▼                                │
                    │  ┌──────┴───────┐                   ┌──────────────┐                        │
 Retailers /        │  │ fanout       │ ◄── requests ──── │   entity     │──► device_entities     │
 carriers ─────────►│  │ planner +    │                   │   resolver   │    entity_identifiers  │
                    │  │ budgets      │                   │  (claims)    │    identity_claims     │
 OEM pages/feeds ──►│  └──────────────┘                   └──────┬───────┘    entity_signals(der.) │
 Support/companion  │                                            ▼                                │
 ──────────────────►│  epochs/baseline firewall ──► ┌────────────────────────┐                    │
                    │  run metrics / dual-plane     │   NOVELTY FIREWALL     │                    │
                    │  health ──► maintenance       │  G0 baseline · G1 known│                    │
                    │                               │  G2 freshness·G3 mat.  │                    │
                    │  confidence ledger · QC       │  G4 dedupe · G5 flood  │                    │
                    │                               └───────────┬────────────┘                    │
                    │                                           ▼                                 │
                    │                        ┌──────────────────────────────┐                     │
                    │                        │ alert intents (outbox)       │──► Discord drain    │
                    │                        │ channels: intel / release /  │   (staging first)   │
                    │                        │           maintenance        │                     │
                    │                        └──────────────────────────────┘                     │
                    │  lead-time telemetry · source report · observer adapter surface (later)    │
                    └─────────────────────────────────────────────────────────────────────────────┘
                                   │ Discord                          ▲ read-only / linkage (Phase 3+)
                                   ▼                                  │
                    Editorial profiles: smartphone.yaml / tablet.yaml / smartwatch.yaml
                    Views & dashboards (Phase 2+): candidate queue, entity timeline, source report
                    Existing clanks (Phase 3+): enrichment sources + external_links (link-not-merge)
```

---

## 5. Data models / schemas (exact)

SQLite dialect; SQLAlchemy 2.0 models + Alembic migration `0001_initial`. All timestamps are
ISO-8601 UTC strings; column names carry semantic clock roles per STD-UI-COM-010 and ADR-0014
(`observed_at` = we saw it; `occurred_at`/`published_at` = the world's claim). IDs are UUIDv7
strings (sortable; matches clankops practice).

```sql
-- 5.1 Source registry -------------------------------------------------------
CREATE TABLE sources (
  source_id        TEXT PRIMARY KEY,            -- e.g. 'komdigi', 'geekbench', 'samsung_oem'
  display_name     TEXT NOT NULL,
  plane            TEXT NOT NULL CHECK (plane IN
                     ('regulatory','runtime','commerce','oem','support','press','community')),
  authority_tier   INTEGER NOT NULL CHECK (authority_tier BETWEEN 1 AND 4),
                     -- 1 official/primary  2 structured-secondary (benchmark, big retail)
                     -- 3 specialist press  4 community
  capabilities     TEXT NOT NULL,               -- JSON list of discovery|enrichment|fanout_query|confirmation
  region           TEXT NOT NULL DEFAULT '*',   -- ISO code or '*'
  state            TEXT NOT NULL DEFAULT 'EXPERIMENTAL'
                     -- vocabulary from tablet-clank: PRODUCTION|EXPERIMENTAL|DISABLED|RETIRED
                     -- (STD-UI-COM-005: state changes are explicit config edits, never GUI/auto)
  ,
  adapter_class    TEXT NOT NULL,               -- import path, e.g. 'device_intel.collectors.komdigi.KomdigiAdapter'
  adapter_version  TEXT NOT NULL,
  config_json      TEXT NOT NULL DEFAULT '{}',  -- politeness: min_delay_seconds, jitter, max_bytes, fixtures...
  kill_switch      INTEGER NOT NULL DEFAULT 0,
  notes            TEXT,
  created_at       TEXT NOT NULL,
  updated_at       TEXT NOT NULL
);

-- 5.2 Continuity epochs (STD-DATA-COM-001; ADR-0006) ------------------------
CREATE TABLE epochs (
  epoch_id              TEXT PRIMARY KEY,
  scope                 TEXT NOT NULL CHECK (scope IN ('global','source')),
  source_id             TEXT REFERENCES sources(source_id),   -- NULL for global
  kind                  TEXT NOT NULL CHECK (kind IN ('BASELINE','CONTINUITY')),
  baseline_completed_at TEXT,                  -- NULL until a qualifying run completes it
  baseline_version      INTEGER NOT NULL DEFAULT 1,
  material_identity     TEXT,                  -- code revision + config fingerprint
  previous_epoch_id     TEXT REFERENCES epochs(epoch_id),
  reason                TEXT NOT NULL,
  started_at            TEXT NOT NULL,
  created_by_run_id     TEXT
);
CREATE INDEX ix_epochs_source ON epochs(source_id, started_at);

-- 5.3 Run provenance (Fleet Law 6; STD-OPS-COM-001) --------------------------
CREATE TABLE collector_runs (
  run_id                TEXT PRIMARY KEY,
  source_id             TEXT NOT NULL REFERENCES sources(source_id),
  started_at            TEXT NOT NULL,
  finished_at           TEXT,
  status                TEXT NOT NULL   -- SUCCESS|PARTIAL|ZERO_ITEMS|BLOCKED|FAILED|SKIPPED_OVERLAP
                        -- a ZERO_ITEMS row MUST carry zero_reason (v0.2 §5 semantic zeros)
  ,
  zero_reason           TEXT            -- intentional_empty|source_block|empty_source|parser_failure|unknown
  ,
  run_reason            TEXT NOT NULL,  -- manual|baseline|fanout|enrichment|validation|demo|test
  execution_provenance  TEXT NOT NULL CHECK (execution_provenance IN ('MANUAL','SCHEDULED','UNKNOWN')),
  code_revision         TEXT,           -- git SHA; literal 'UNKNOWN' allowed, never NULL
  config_fingerprint    TEXT,
  epoch_id              TEXT REFERENCES epochs(epoch_id),
  pages_requested       INTEGER NOT NULL DEFAULT 0,
  pages_fetched         INTEGER NOT NULL DEFAULT 0,
  bytes_downloaded      INTEGER NOT NULL DEFAULT 0,
  http_failures         INTEGER NOT NULL DEFAULT 0,
  drafts_total          INTEGER NOT NULL DEFAULT 0,
  drafts_accepted       INTEGER NOT NULL DEFAULT 0,
  drafts_rejected       INTEGER NOT NULL DEFAULT 0,
  evidence_new          INTEGER NOT NULL DEFAULT 0,
  evidence_resighted    INTEGER NOT NULL DEFAULT 0,
  entities_new          INTEGER NOT NULL DEFAULT 0,
  fanout_requests_made  INTEGER NOT NULL DEFAULT 0,
  silent_drop           INTEGER NOT NULL DEFAULT 0,  -- drafts validated but none accepted (regression signal)
  warnings_json         TEXT NOT NULL DEFAULT '[]',
  errors_json           TEXT NOT NULL DEFAULT '[]'
);
CREATE INDEX ix_runs_source_started ON collector_runs(source_id, started_at);

-- 5.4 Content-addressed raw capture (provenance; retention is per-source config)
CREATE TABLE snapshots (
  snapshot_id   TEXT PRIMARY KEY,
  content_hash  TEXT NOT NULL,                 -- sha256 hex
  byte_size     INTEGER NOT NULL,
  content_type  TEXT,
  compression   TEXT NOT NULL DEFAULT 'none',  -- none|gzip
  blob          BLOB,                          -- inline for Phase 1; disk-backed later (watch-clank pattern)
  fetched_at    TEXT NOT NULL
);
CREATE UNIQUE INDEX ux_snapshots_hash ON snapshots(content_hash);

-- 5.5 EVIDENCE — the central observation fact (STD-DATA-COM-004 tier: observation)
CREATE TABLE evidence (
  evidence_id        TEXT PRIMARY KEY,
  run_id             TEXT NOT NULL REFERENCES collector_runs(run_id),
  source_id          TEXT NOT NULL REFERENCES sources(source_id),
  signal_type        TEXT NOT NULL CHECK (signal_type IN (
                       'REGULATORY_SIGNAL','BENCHMARK_SIGNAL','RETAIL_SIGNAL','OEM_SIGNAL',
                       'SOFTWARE_SIGNAL','SUPPORT_SIGNAL','PRESS_SIGNAL','ACCESSORY_SIGNAL',
                       'COMMUNITY_SIGNAL')),
  authority_tier     INTEGER NOT NULL,
  manufacturer_raw   TEXT,                     -- verbatim from source; NULL when absent
  manufacturer       TEXT,                     -- normalized (e.g. 'samsung'); NULL when unknown
  marketing_name     TEXT,                     -- verbatim when the source states one; NULL otherwise
  device_class_hints TEXT NOT NULL DEFAULT '[]', -- JSON list, e.g. ["tablet","phone"]
  region             TEXT NOT NULL DEFAULT '*',
  attributes         TEXT NOT NULL DEFAULT '{}', -- normalized observed attrs (band, storage, price, SoC, os...)
  attributes_raw     TEXT NOT NULL DEFAULT '{}', -- verbatim extraction for audit
  url                TEXT,
  title              TEXT,
  published_at       TEXT,                     -- source-declared publication/issue date; NULL when absent
  observed_at        TEXT NOT NULL,            -- fetch time (UTC)
  reference_date     TEXT,                     -- DERIVED: COALESCE(published_at, observed_at); the date
                                               -- used for freshness/lead-time; labeled by construction
  content_hash       TEXT NOT NULL,            -- sha256 over canonicalised extraction
  snapshot_id        TEXT REFERENCES snapshots(snapshot_id),
  raw_ref            TEXT,                     -- pointer when blob is externalized
  collector_version  TEXT NOT NULL,
  extraction_version TEXT NOT NULL,            -- parser version: parser fixes create NEW evidence, never edits
  source_confidence  TEXT NOT NULL DEFAULT 'UNKNOWN', -- source-native confidence, preserved verbatim
  is_baseline        INTEGER NOT NULL DEFAULT 0,   -- baseline-era record (STD-DATA-COM-001 A2, read-time)
  fanout_request_id  TEXT                      -- set when this evidence arrived via fan-out (loop marking)
);
CREATE UNIQUE INDEX ux_evidence_source_hash ON evidence(source_id, content_hash);
CREATE INDEX ix_evidence_signal ON evidence(signal_type, observed_at);
CREATE INDEX ix_evidence_run ON evidence(run_id);

-- 5.6 Typed identifiers observed by an evidence row (queryable, indexed)
CREATE TABLE evidence_identifiers (
  evidence_id  TEXT NOT NULL REFERENCES evidence(evidence_id),
  id_kind      TEXT NOT NULL CHECK (id_kind IN (
                   'model_code','model_code_base','regional_sku','codename','marketing_name',
                   'benchmark_name','cert_id','fcc_id','sig_id','retail_sku','part_number')),
  id_raw       TEXT NOT NULL,                 -- exactly as the source printed it
  id_value     TEXT NOT NULL                  -- normalised (per-kind normaliser, §8.2)
);
CREATE INDEX ix_evid_id ON evidence_identifiers(id_kind, id_value);
CREATE INDEX ix_evid_eid ON evidence_identifiers(evidence_id);

-- 5.7 DEVICE ENTITY — the resolved candidate (STD-DATA-COM-004 tier: canonical)
CREATE TABLE device_entities (
  entity_id          TEXT PRIMARY KEY,
  manufacturer       TEXT,                     -- normalized; NULL until evidence supports one
  primary_model_code TEXT,                     -- display convenience; identity truth lives in
                                               -- entity_identifiers (never required at insert)
  marketing_name     TEXT,                     -- NULL until corroborated; display only
  device_class       TEXT NOT NULL DEFAULT 'unknown'
                       -- smartphone|tablet|wearable|unknown  (editorial classification)
  ,
  device_class_basis TEXT NOT NULL DEFAULT 'NONE'
                       -- NONE|HINT|DECLARED|CONFIRMED|OPERATOR (STD-DATA-COM-004 D3: derived values
                       -- are labeled as derived; OPERATOR = human decision)
  ,
  class_rule_version TEXT NOT NULL DEFAULT '0',
  identity_state     TEXT NOT NULL DEFAULT 'OPEN'
                       -- OPEN|RESOLVED|MERGED_INTO|SPLIT|REJECTED  (MERGED_INTO rows keep history;
                       -- canonical pointer = identity_claims)
  ,
  editorial_stage    TEXT NOT NULL DEFAULT 'candidate'
                       -- DERIVED projection: candidate|identified|announced|released|archived
                       -- recomputed from signals; explicitly NON-authoritative and NOT a required
                       -- linear lifecycle — stages are predicates over evidence, not gates evidence
                       -- must pass in order.
  ,
  stage_rule_version TEXT NOT NULL DEFAULT '0',
  identity_confidence TEXT NOT NULL DEFAULT 'LOW', -- LOW|MEDIUM|HIGH (§9.3)
  confidence         INTEGER NOT NULL DEFAULT 0,  -- 0..100 evidence-weight projection (§9.2)
  anchor_evidence_id TEXT REFERENCES evidence(evidence_id), -- first evidence satisfying RELEASE predicates
  first_seen         TEXT NOT NULL,           -- min(reference_date) over member evidence (back-datable)
  last_seen          TEXT NOT NULL,           -- max(observed_at); maintained on attach
  created_at         TEXT NOT NULL,
  notes              TEXT
);
CREATE INDEX ix_entities_class ON device_entities(device_class, identity_state);
CREATE INDEX ix_entities_stage ON device_entities(editorial_stage);

-- 5.8 Entity identifier membership
CREATE TABLE entity_identifiers (
  entity_id  TEXT NOT NULL REFERENCES device_entities(entity_id),
  id_kind    TEXT NOT NULL CHECK (id_kind IN (
                   'model_code','model_code_base','regional_sku','codename','marketing_name',
                   'benchmark_name','cert_id','fcc_id','sig_id','retail_sku','part_number')),
  id_value   TEXT NOT NULL,
  first_evidence_id TEXT NOT NULL REFERENCES evidence(evidence_id),
  first_seen TEXT NOT NULL,
  last_seen  TEXT NOT NULL,
  PRIMARY KEY (entity_id, id_kind, id_value)
);
CREATE INDEX ix_ent_id ON entity_identifiers(id_kind, id_value);

-- 5.9 Derived signal projection per entity (recomputable; §3.3-4)
CREATE TABLE entity_signals (
  entity_id               TEXT NOT NULL REFERENCES device_entities(entity_id),
  signal_type             TEXT NOT NULL,
  first_evidence_id       TEXT NOT NULL REFERENCES evidence(evidence_id),
  last_evidence_id        TEXT NOT NULL REFERENCES evidence(evidence_id),
  distinct_sources        INTEGER NOT NULL,
  distinct_planes         INTEGER NOT NULL,
  strongest_authority     INTEGER NOT NULL,    -- MIN(authority_tier) among member evidence
  observation_count       INTEGER NOT NULL,
  first_reference_date    TEXT NOT NULL,
  last_observed_at        TEXT NOT NULL,
  alerted_as_intel        INTEGER NOT NULL DEFAULT 0,  -- set by novelty engine, not recomputed away
  updated_at              TEXT NOT NULL,
  PRIMARY KEY (entity_id, signal_type)
);

-- 5.10 Identity decisions — append-only, auditable, reversible (STD-DATA-COM-003)
CREATE TABLE identity_claims (
  claim_id     TEXT PRIMARY KEY,
  kind         TEXT NOT NULL CHECK (kind IN ('MERGE','ALIAS','SPLIT','EXTERNAL_LINK')),
  subject_id   TEXT NOT NULL,          -- entity_id (or external ref for EXTERNAL_LINK)
  object_id    TEXT,                   -- second entity_id, or external (clank_id, table, id) JSON
  status       TEXT NOT NULL CHECK (status IN
                 ('PROPOSED','AUTO_APPLIED','OPERATOR_CONFIRMED','REJECTED','REVERSED')),
  rule_id      TEXT NOT NULL,          -- e.g. 'exact_model_code_hit', 'manufacturer_guarded_base_match'
  rule_version TEXT NOT NULL,
  evidence_ids TEXT NOT NULL,          -- JSON list; the discriminators that justify the claim
  detail_json  TEXT NOT NULL DEFAULT '{}',
  actor        TEXT NOT NULL,          -- 'auto' or operator label
  created_at   TEXT NOT NULL,
  reversed_by  TEXT REFERENCES identity_claims(claim_id)
);

-- 5.11 Novelty firewall ledger — every evaluation is recorded (§3.3-5)
CREATE TABLE novelty_decisions (
  decision_id   TEXT PRIMARY KEY,
  entity_id     TEXT NOT NULL REFERENCES device_entities(entity_id),
  trigger_evidence_id TEXT NOT NULL REFERENCES evidence(evidence_id),
  policy_version TEXT NOT NULL,
  gate_results  TEXT NOT NULL,          -- JSON: {"G0_baseline":"pass","G2_freshness":"fail:186d",...}
  outcome       TEXT NOT NULL CHECK (outcome IN
                  ('INTEL','RELEASE','BASELINE_SILENT','KNOWN_NO_MATERIAL_CHANGE','HISTORICAL_CATCHUP',
                   'BELOW_MATERIALITY','DUPLICATE_SUPPRESSED','FLOOD_SUPPRESSED','INSUFFICIENT_IDENTITY')),
  intent_id     TEXT,                   -- alert outbox row when outcome ∈ {INTEL, RELEASE}
  decided_at    TEXT NOT NULL
);
CREATE INDEX ix_novelty_entity ON novelty_decisions(entity_id, decided_at);

-- 5.12 Fan-out ledger
CREATE TABLE fanout_requests (
  request_id    TEXT PRIMARY KEY,
  entity_id     TEXT NOT NULL REFERENCES device_entities(entity_id),
  trigger_evidence_id TEXT NOT NULL REFERENCES evidence(evidence_id),
  target_source_id TEXT NOT NULL REFERENCES sources(source_id),
  query_identifier_kind TEXT NOT NULL,
  query_identifier_value TEXT NOT NULL,
  status        TEXT NOT NULL CHECK (status IN
                  ('PENDING','RUNNING','DONE','NO_RESULTS','SKIPPED_BUDGET','SKIPPED_DUPLICATE',
                   'SKIPPED_LOOP','SKIPPED_DISABLED','FAILED','EXPIRED')),
  executed_run_id TEXT REFERENCES collector_runs(run_id),
  reason        TEXT,                   -- why skipped/failed (budget window, loop rule id, ...)
  requested_at  TEXT NOT NULL,
  completed_at  TEXT
);
CREATE INDEX ix_fanout_entity ON fanout_requests(entity_id, target_source_id, requested_at);

-- 5.13 Alert outbox (persistence-first; smartwatch/oem-radar pattern)
CREATE TABLE alert_intents (
  intent_id    TEXT PRIMARY KEY,
  provider     TEXT NOT NULL DEFAULT 'discord',
  channel      TEXT NOT NULL CHECK (channel IN ('intel','release','maintenance')),
  dedup_key    TEXT NOT NULL,           -- §13.2; UNIQUE per channel
  entity_id    TEXT REFERENCES device_entities(entity_id),
  run_id       TEXT REFERENCES collector_runs(run_id),
  decision_id  TEXT REFERENCES novelty_decisions(decision_id),
  payload_json TEXT NOT NULL,           -- fully rendered at enqueue time (render-then-store)
  status       TEXT NOT NULL CHECK (status IN
                 ('pending','sent','failed','suppressed','held')),
  suppress_reason TEXT,                 -- baseline|staging|below_floor|maturity|flood|policy|test_mode
  attempts     INTEGER NOT NULL DEFAULT 0,
  not_before   TEXT,                    -- 429 backoff floor
  last_error_class TEXT,                -- bounded vocabulary; never raw transport text (secret hygiene)
  created_at   TEXT NOT NULL,
  sent_at      TEXT
);
CREATE UNIQUE INDEX ux_intents_dedup ON alert_intents(channel, dedup_key);
CREATE INDEX ix_intents_status ON alert_intents(status, not_before);

-- 5.14 Confidence ledger (every entity.confidence change is a row; smartphone-clank pattern)
CREATE TABLE confidence_ledger (
  entry_id          TEXT PRIMARY KEY,
  entity_id         TEXT NOT NULL REFERENCES device_entities(entity_id),
  evidence_id       TEXT REFERENCES evidence(evidence_id),
  rule_id           TEXT NOT NULL,
  rule_version      TEXT NOT NULL,
  points            INTEGER NOT NULL,
  previous_confidence INTEGER NOT NULL,
  new_confidence    INTEGER NOT NULL,
  duplicate_suppressed INTEGER NOT NULL DEFAULT 0,
  explanation       TEXT NOT NULL,
  created_at        TEXT NOT NULL
);
CREATE INDEX ix_ledger_entity ON confidence_ledger(entity_id, created_at);

-- 5.15 Source health — dual-plane (Fleet Law 3; STD-OPS-COM-002)
CREATE TABLE source_health (
  source_id            TEXT PRIMARY KEY REFERENCES sources(source_id),
  last_attempt_at      TEXT,            -- invocation plane
  last_success_commit  TEXT,            -- yield plane: last run with evidence_new + drafts_accepted > 0
  consecutive_failures INTEGER NOT NULL DEFAULT 0,
  consecutive_empty    INTEGER NOT NULL DEFAULT 0,
  blocked_reason       TEXT,            -- http_403|http_429|robots|parser|proxy|unknown
  backoff_until        TEXT,
  health_status        TEXT NOT NULL DEFAULT 'UNKNOWN',  -- HEALTHY|DEGRADED|ZERO_ITEMS|BLOCKED|FAILED|NEVER_RUN|UNKNOWN
  updated_at           TEXT NOT NULL
);

-- 5.16 Operator QC (STD-UI-COM-002 semantics; tablet/watch vocabulary)
CREATE TABLE qc_decisions (
  qc_id        TEXT PRIMARY KEY,
  target_type  TEXT NOT NULL CHECK (target_type IN ('entity','evidence','intent','identity_claim')),
  target_id    TEXT NOT NULL,
  decision     TEXT NOT NULL CHECK (decision IN
                 ('CONFIRM','REJECT','QUARANTINE','NOT_USEFUL','FALSE_POSITIVE','MERGE','SPLIT','NOTE')),
  actor        TEXT NOT NULL,
  reason       TEXT,
  before_json  TEXT NOT NULL DEFAULT '{}',
  after_json   TEXT NOT NULL DEFAULT '{}',
  created_at   TEXT NOT NULL
);

-- 5.17 Lead-time telemetry (materialised on RELEASE anchor; §19)
CREATE TABLE lead_time_observations (
  observation_id  TEXT PRIMARY KEY,
  entity_id       TEXT NOT NULL REFERENCES device_entities(entity_id),
  anchor_evidence_id TEXT NOT NULL REFERENCES evidence(evidence_id),
  evidence_id     TEXT NOT NULL REFERENCES evidence(evidence_id),
  source_id       TEXT NOT NULL REFERENCES sources(source_id),
  signal_type     TEXT NOT NULL,
  lead_seconds    INTEGER NOT NULL,     -- anchor.reference_date − evidence.reference_date (signed;
                                        -- negative = earlier than anchor = discovery credit)
  reference_date_kind TEXT NOT NULL CHECK (reference_date_kind IN ('published_at','observed_at'))
);
CREATE INDEX ix_leadtime_source ON lead_time_observations(source_id);
```

Notes:
- `alert_intents` *is* the delivery log (oem-radar pattern); the smartphone-style separate
  `webhook_deliveries` table is intentionally not duplicated. `qc_decisions` rows are the
  operator-decision tier (STD-DATA-COM-004).
- No `devices.lifecycle` enum exists; `editorial_stage` is a derived projection with
  `stage_rule_version`, recomputable, explicitly non-authoritative (§7).

---

## 6. Signal / evidence schema — semantics

`signal_type` is the evidence's *kind of claim about the world*, decoupled from the source that
carries it (a retailer page can carry an OEM_SIGNAL-free RETAIL_SIGNAL; a KOMDIGI cert is a
REGULATORY_SIGNAL; Geekbench rows are BENCHMARK_SIGNALs). One evidence row = one source
observation at one moment; multiple identifier observations inside one page are one evidence row
with multiple `evidence_identifiers`.

Required drafting rules (enforced in `ingest`):
- `content_hash` = sha256 over a canonical JSON of the *extraction* (signal_type, manufacturer,
  identifiers raw+kind, marketing_name, region, sorted attributes, published_at) — not over the
  raw HTML, so cosmetic page changes do not create evidence; a real field change does.
- Same `(source_id, content_hash)` seen again → refresh nothing except health; the row exists
  (idempotent replay, Law-1-safe).
- `published_at` is set only when the source itself declares a date. **Never infer or fabricate
  it** (watch-clank law: publisher-maintained timestamps are never populated from our crawl time
  in reverse). `reference_date` is always the label of which clock was used.
- `source_confidence` carries any source-native confidence verbatim (ADR-0014: participant-native
  confidence is never silently reinterpreted). For most Phase 1 sources it is `UNKNOWN`.
- Signals are never deleted. Disproof (e.g. cert cancelled) arrives as new evidence.

**Signal type → default weight / materiality** (profile-overridable; §14):

| signal_type | default authority | base weight | alone_material (default profile) |
|---|---|---|---|
| REGULATORY_SIGNAL | 1 | 30 | yes |
| BENCHMARK_SIGNAL | 2 | 20 | yes |
| OEM_SIGNAL | 1 | 40 | yes (RELEASE-capable) |
| RETAIL_SIGNAL | 2 | 25 | yes (RELEASE-capable when orderable) |
| SUPPORT_SIGNAL | 1–2 | 20 | yes |
| SOFTWARE_SIGNAL | 1–2 | 15 | no |
| ACCESSORY_SIGNAL | 2–3 | 8 | **never alone** (weak evidence per brief) |
| PRESS_SIGNAL | 3 | 10 | no |
| COMMUNITY_SIGNAL | 4 | 0 | **never** (oem-radar Reddit precedent) |

---

## 7. Device / entity schema — semantics

A `device_entities` row is created lazily: the resolver creates an entity the first time an
identifier cannot be attached to an existing one. Minimum viable insert is literally:

```
manufacturer=samsung  primary_model_code=NULL→'SM-X746B'  marketing_name=NULL
device_class='unknown'/basis=HINT  identity_state=OPEN  identity_confidence=LOW
first_seen=<evidence.reference_date>  editorial_stage='candidate'
```

- `editorial_stage` predicates (all must hold; evaluated in this order; a stage is *claimed* when
  its predicate holds even if a "later" stage's predicate also holds — no ordering enforcement):
  - `candidate`: ≥1 member evidence (always true).
  - `identified`: identity_confidence ≥ MEDIUM (§9.3).
  - `announced`: exists OEM_SIGNAL with tier-1 source, or PRESS_SIGNAL tier ≤3 naming the
    identifier set, and entity already `identified`.
  - `released`: RELEASE predicates of §10.5 hold (anchor set; `anchor_evidence_id` written).
  - `archived`: operator QC action only.
- `device_class` classification (deterministic, `class_rule_version`-stamped, append-derived rows
  may be added later if per-profile classification history is needed):
  1. OPERATOR if a QC MERGE/CONFIRM decision says so.
  2. DECLARED if a tier≤2 source states a category that maps cleanly (KOMDIGI certificate
     category / Geekbench platform metadata / Google device catalogue device type).
  3. CONFIRMED if ≥2 independent tier≤2 sources' hints agree.
  4. HINT if exactly one source hints, or manufacturer model-code grammar implies
     (Samsung `SM-X*` → tablet, `SM-S*` → phone — derived from the manufacturer rule files,
     smartphone-clank `knowledge/data/*.yaml` pattern).
  5. else `unknown` + `NONE`. **Class is never required to be known**; alerts render
     "Tablet candidate" / "Device class unknown" honestly.
- Cross-entity sets: regional variants, storage tiers and carrier variants are *identifiers and
  attributes on one entity* (`model_code` vs `regional_sku` kinds), NOT separate entities —
  reversing tablet-clank's region-splits. A genuinely different product sharing a marketing name
  is a separate entity; the marketing name is attached as `marketing_name` identifier to each,
  and the conflict is visible, never silently resolved (§8.5).

---

## 8. Identity-resolution strategy

### 8.1 Principles
Exact-first, conservative, evidence-gated, auditable, reversible (STD-DATA-COM-003). A key or
signal used to *propose* a match is never by itself sufficient to *commit* one (C1). Every
automatic merge carries an in-record discriminator and full evidence list (C2). Pre-merge
identities remain reconstructable (reversal splits re-write membership; `identity_claims` keeps
the lineage).

### 8.2 Identifier normalisers (per `id_kind`; registry module `resolution/normalize.py`)
- `model_code`: uppercase; strip spaces and dashes; keep alphanumerics. `SM-X746B` → `SMX746B`.
- `model_code_base`: derived **only** via evidence-backed per-manufacturer suffix rules
  (port of smartphone-clank `_extract_family_key` digit-guard logic): `SMX746B` → `SMX746`
  (suffix `B`, previous char digit). Unknown suffixes are preserved verbatim (watch-clank JDM
  rule: never strip what you can't justify).
- `codename`: lowercase alphanumeric.
- `marketing_name`: casefold; collapse whitespace; strip punctuation — used for *matching
  proposals only*, never for committing merges.
- `cert_id` / `fcc_id` / `sig_id`: uppercase, per-source grammar (e.g. FCC `FCC-XXXX`);
  malformed IDs are stored raw with kind `part_number`… no — malformed stays unparsed; the
  normaliser returns failure and the identifier is stored with `id_value = id_raw` and flagged in
  `detail_json`. Never guess.
- `retail_sku` / `part_number`: verbatim.

### 8.3 Resolution pipeline (per evidence, deterministic order)
1. **Extract** identifiers from the evidence draft; insert `evidence_identifiers`.
2. **Exact hit**: look up `entity_identifiers` on normalised `(id_kind, id_value)`.
   - One hit → attach evidence to that entity (no claim needed; record nothing).
   - Multiple hits → **no auto-merge**; create an `ALIAS` claim with status `PROPOSED` naming the
     entities; attach evidence to the *oldest* entity; the queue surfaces the proposal.
3. **Base-code hit** (only if no exact hit): match on `model_code_base` **plus manufacturer
   agreement (both non-null and equal) plus device_class-hint compatibility**. This is the one
   auto-merge rule (`rule_id='manufacturer_guarded_base_match'`); it commits as
   `MERGE/AUTO_APPLIED` citing the discriminating evidence. Region/storage/colour differences do
   **not** block it (they are variants, §7).
4. **No hit** → create a new entity; insert its identifiers; `identity_state=OPEN`.
5. **Manufacturer guard**: evidence with manufacturer X never attaches to an entity whose
   manufacturer is non-null and ≠ X. Manufacturer-unknown evidence may attach (and may fill the
   entity's manufacturer) but only via a `PROPOSED` alias claim when the identifier is
   `marketing_name`/`codename`; via exact `model_code` hit it attaches normally.
6. **Marketing-name never merges**: a marketing-name match at resolution time produces at most a
   `PROPOSED` claim (candidate for operator QC), regardless of confidence.
7. **Attachment effects** (in order): update `entity_identifiers.last_seen` / insert new
   membership; refresh `entity_signals`; recompute `identity_confidence`, `confidence` (ledger),
   `device_class`, `editorial_stage`, `first_seen` (min reference_date — may move backwards),
   `last_seen`.
8. **Recompute, then novelty.** Novelty evaluation always runs on the *post-resolution* entity.

### 8.4 Merges and splits (operator + auto)
- `MERGE` claims record both entity ids, rule, evidence; `object` entity gets
  `identity_state=MERGED_INTO`; a canonical pointer row (`kind='MERGE'`, `status` active) defines
  the survivor; reversal (`REVERSED`) restores both as OPEN. All writes via the same transaction
  path; dashboard shows merge lineage.
- `SPLIT` is operator-only in Phase 1–2.
- **Cross-Clank linkage is `EXTERNAL_LINK` claims only** — `(clank_id, table, row_id)` triples
  with evidence and confidence, never identity fusion (ADR v0.2 §6; Standards HOLD). The
  linkage runner (Phase 3) is read-only toward the sibling stores (Motherclank adapter pattern).

### 8.5 Known hard cases (must be tests)
- Same base code, different manufacturers (badge engineering) → manufacturer guard blocks.
- Samsung regional suffix collision (`SMX746B` vs `SMX7460`) → base normaliser digit-guard
  prevents collapse.
- Two unrelated products sharing a marketing name ("Galaxy Tab S11" Wi-Fi vs 5G *is one entity*;
  "Galaxy Tab S11" vs a hypothetical "S11 Ultra" is two) → marketing name proposes, never merges;
  DECLARED class + distinct model codes keep them apart.
- A cert for a cancelled/withdrawn product → evidence stays; novelty policy treats absence of
  further signals as below-materiality, no false RELEASE.
- Benchmark device strings containing marketing names but no model codes → entity matches by
  marketing-name proposal only; identity_confidence stays LOW until a code-bearing source agrees.

---

## 9. Confidence model

Three separate numbers, never conflated:

1. **Evidence confidence** (`evidence.source_confidence` + `authority_tier`): how much the source's
   claim is trusted. Deterministic from source registry; no decay of official evidence
   (smartphone rule: `official` never decays).
2. **Entity evidence-confidence** (`device_entities.confidence`, 0–100): bounded deterministic
   sum over member evidence — `Σ weight(e) × freshness(e)` over the strongest evidence per
   (source, signal_type), capped at 100, written only through `confidence_ledger`
   (smartphone enforcement pattern: tests forbid direct `confidence` writes).
   Freshness factor: 1.0 for tier-1 / official; otherwise `decay_schedule`
   `[(90d,1.0),(180d,0.75),(365d,0.5),(∞,0.25)]` (config).
3. **Identity confidence** (`identity_confidence`, LOW/MEDIUM/HIGH): *how sure we are the member
   evidence refers to one physical product*. Rule-based (config `identity_rules`):
   - HIGH: ≥2 independent tier≤2 sources, ≥2 distinct planes, agreeing on the same
     `model_code` or `model_code_base` (e.g. KOMDIGI + Geekbench).
   - MEDIUM: ≥2 independent tier≤2 sources, same plane; **or** 1 tier-1 source stating a full
     model code (a KOMDIGI certificate alone ⇒ MEDIUM).
   - LOW: single non-tier-1 source, or marketing-name-only evidence.
   Computed at attach time; stored on the entity; drives novelty gate G5/INTEL floors and the
   `identified` stage. This is the "Identity confidence: high" of the brief's INTEL template.

Weights per signal_type are §6; profile overlays adjust (e.g. smartwatch: OEM_SIGNAL 45,
SUPPORT_SIGNAL 25). All weight changes are config + `rule_version`, never inline magic numbers.

---

## 10. Novelty policy

### 10.1 Structure
Ordered gates; each returns pass/fail(+reason); evaluation recorded as one `novelty_decisions`
row per (entity, trigger evidence) *before* any alert intent exists (§3.3-5). Policy is versioned
(`policy_version`); re-evaluation of history never rewrites past decisions.

### 10.2 Gates
- **G0 baseline** (Law 1; STD-DATA-COM-002): the evidence's source has
  `epochs.baseline_completed_at IS NULL` (or evidence `is_baseline=1`) ⇒ outcome
  `BASELINE_SILENT`. This predicate is part of *every* novelty query path's definition
  (read-side exclusion, B2) — there is no "filter afterwards" code path.
- **G1 known-entity**: if the trigger evidence added no new `entity_signals` row, no new
  identifier kind, and no attribute material to the profile ⇒ `KNOWN_NO_MATERIAL_CHANGE`.
- **G2 freshness** (Law 2): `now − evidence.reference_date > novelty_window(signal_type)`
  ⇒ `HISTORICAL_CATCHUP` (evidence kept; entity may still alert later via accumulation — but the
  *first* sighting of an old-dated item is never plain NEW; the decision row says so).
  Defaults: regulatory 180d, benchmark 90d, retail/OEM 30d, support 45d. Future-dated beyond
  1-minute tolerance ⇒ treated as failure (`reference_date` rejected → `observed_at` used,
  labelled) — watch-clank precedent.
- **G3 materiality**: strongest new signal's `base_weight × profile multiplier ≥ floor` AND
  (`alone_material` OR the entity now has ≥2 distinct signal types). COMMUNITY/ACCESSORY never
  pass alone. Fails ⇒ `BELOW_MATERIALITY`.
- **G4 duplicate suppression**: an intent with the same channel `dedup_key` (§13.2) exists ⇒
  `DUPLICATE_SUPPRESSED` (the second source repeating a known fact does not re-alert;
  accumulation does — a digest re-alert is allowed after `digest_window` with ≥2 *new* signals,
  keyed on the window bucket).
- **G5 flood guards**: identity_confidence below profile INTEL floor ⇒ `INSUFFICIENT_IDENTITY`;
  bulk-touch detector (≥8 entities first-seen by one run within 90s — watch-clank constants)
  ⇒ `FLOOD_SUPPRESSED` + maintenance alert; per-profile daily INTEL cap (default 12) ⇒ excess
  held (status `held`, drained next day in FIFO).
- **G6 release separation**: if RELEASE predicates hold (§10.5), the decision is `RELEASE`
  (and INTEL for the same evidence is skipped — release supersedes intel for that trigger).

### 10.3 Outcomes → actions
| outcome | action |
|---|---|
| INTEL | enqueue `intel` intent (rendered payload, §13) |
| RELEASE | enqueue `release` intent; set anchor; write lead-time rows (§19) |
| BASELINE_SILENT / KNOWN… / HISTORICAL_CATCHUP / BELOW_MATERIALITY / DUPLICATE… / FLOOD… / INSUFFICIENT… | no intent; decision row is the audit trail |

### 10.4 INTEL template (from the brief; rendered at enqueue)
```
NEW DEVICE INTEL
Samsung SM-X746B — Tablet candidate
Signals: KOMDIGI (cert 2506xxxx) + Geekbench (MediaTek Dimensity 8300)
Marketing name: unknown
Identity confidence: high · Evidence confidence: 62
First seen (cert date): 2026-09-02 · Sources: komdigi, geekbench
https://... (primary evidence URL)
```

### 10.5 RELEASE predicates (all required)
1. Entity identity_confidence ≥ MEDIUM;
2. exists tier≤2 evidence with signal_type ∈ {OEM_SIGNAL, RETAIL_SIGNAL} whose observation is
   *new* (this run) and fresh (reference_date within 7d, or observed within this run when the
   source declares no dates);
3. the evidence contains release-shape attributes: product page (`/product|/buy|specs` class),
   price, or orderable/availability flag (per-source extractor declares which it can honestly
   provide);
4. stage `announced`-or-above predicate not already alerted (`(entity, stage)` dedup key).
Template:
```
DEVICE RELEASE
Samsung Galaxy Tab Foo — matches existing candidate SM-X746B
OEM product page now live (samsung.com) · Germany €699
Evidence: <url> · Stage: released
```

---

## 11. Fan-out / event architecture

### 11.1 Trigger rules (deterministic)
A fan-out request is created when, after ingestion+resolution of run R:
- entity has ≥1 `fanout_query`-capable identifier kind (`model_code` in Phase 1) AND
- entity entered this run as new OR gained a signal type it lacked AND
- for each eligible target T: no prior request `(entity, T)` within `fanout_dedup_days` (default
  21), T enabled with `fanout_query` capability, entity not fan-out-born (`fanout_request_id`
  lineage — **depth 1 hard cap**, §3.3-8), T not in backoff.

Requests are created as `PENDING` rows inside the ingestion transaction (crash-safe); execution
is a separate step (`fanout execute`) so planning is inspectable and skippable.

### 11.2 Budgets & burn accounting (per config, defaults shown)
- `max_requests_per_run`: 25 per target source; `max_per_entity`: 4 targets;
- `daily_cap_per_source`: 200; `max_concurrent`: 1 (single process, sequential);
- budget checks read `fanout_requests` counts; over-budget ⇒ `SKIPPED_BUDGET` with reason
  (visible, not silent);
- burn accounting = `collector_runs` counters on `run_reason='fanout'` (requests, bytes, wall
  time) — feeds §19 source report ("useful enrichment contribution vs cost").

### 11.3 Execution
`query_identifier(identifier, ctx) -> FanoutResult` on the target adapter (§12); results become
EvidenceDrafts with `fanout_request_id` set, entering the *normal* ingest→resolve→novelty path
(so fan-out evidence can raise identity_confidence and trigger INTEL — but never new fan-out).
Failures mark the request `FAILED` with bounded reason; source backoff via `source_health`.
`EXPIRED` after `fanout_ttl_days` (7). Retry policy: one retry on transient transport error per
request, then backoff (reuse smartphone tenacity profile at adapter level).

### 11.4 Loop prevention (hard rules)
depth cap (§11.1); `(entity, target)` dedup window; fan-out evidence can never create a request;
self-target exclusion (a source never fans out into itself); global kill switch
(`sources.kill_switch` checked at plan time).

---

## 12. Source adapter contract

```python
# device_intel/adapters/base.py
class SourcePlane(StrEnum):   REGULATORY="regulatory"; RUNTIME="runtime"; COMMERCE="commerce"
                              OEM="oem"; SUPPORT="support"; PRESS="press"; COMMUNITY="community"

@dataclass(frozen=True)
class Identifier:
    kind: str          # §5.6 vocabulary
    raw: str
    value: str         # normalised

@dataclass(frozen=True)
class EvidenceDraft:
    signal_type: str                 # §6 vocabulary
    manufacturer_raw: str | None
    marketing_name: str | None       # only when the source states it
    identifiers: tuple[Identifier, ...]
    device_class_hints: tuple[str, ...] = ()
    region: str = "*"
    attributes: Mapping[str, object] = field(default_factory=dict)     # normalised
    attributes_raw: Mapping[str, object] = field(default_factory=dict) # verbatim
    url: str | None = None
    title: str | None = None
    published_at: datetime | None = None      # ONLY if the source declares it
    source_confidence: str = "UNKNOWN"        # verbatim; usually "UNKNOWN"

@dataclass(frozen=True)
class AdapterMetrics:   # smartphone wave1 metrics, carried forward
    pages_requested: int; pages_fetched: int; bytes_downloaded: int
    http_failures: int; timeouts: int; redirects: int
    status_distribution: Mapping[int, int]
    drafts_emitted: int; drafts_rejected: int; rejection_reasons: Mapping[str, int]

@dataclass(frozen=True)
class ZeroReason:       # canonical v0.2 §5 semantic zeros — never a bare []
    kind: str   # intentional_empty|source_block|empty_source|parser_failure|unknown
    detail: str = ""

@dataclass(frozen=True)
class CollectorResult:  # adapters never touch the DB; never raise past run()
    drafts: tuple[EvidenceDraft, ...]
    metrics: AdapterMetrics
    zero: ZeroReason | None = None
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()     # bounded, classified; no raw exception text (secret hygiene)

class SourceAdapter(Protocol):
    source_id: str
    plane: SourcePlane
    authority_tier: int
    def capabilities(self) -> frozenset[str]: ...        # {"discovery"} | {"discovery","fanout_query"} | {"enrichment"}
    def collect(self, ctx: CollectionContext) -> CollectorResult: ...
    def query_identifier(self, identifier: Identifier, ctx: CollectionContext) -> CollectorResult:
        """Only when 'fanout_query' in capabilities(). MUST be a targeted lookup, not a crawl."""
```

- `CollectionContext`: `started_at`, `run_reason`, `code_revision`, `config_fingerprint`,
  `budget_remaining`, politeness config. Adapters get a pre-configured HTTP client (httpx,
  http2, UA `device-intel/0.1 (+source-research)`, per-source `min_delay` + jitter + `max_bytes`,
  robots respected) — smartphone-clank `BaseCollector.fetch` hardening, carried over.
- Registration: `adapters/registry.py` builds adapters from `sources` config; **fail-closed
  eligibility** (unknown config, disabled, kill_switch, state DISABLED/RETIRED ⇒ excluded with
  reason; smartphone `_eligible` pattern). A source's `state` transitions are explicit config
  edits (STD-UI-COM-005) recorded in git; no GUI promotion.
- Every adapter ships with **fixtures captured from the live source** (tablet/watch precedent;
  `fixtures/<source>/PROVENANCE.md` records capture date/URL). Tests are hermetic; live probes
  are opt-in (`-m live`).
- New source checklist (the "make adding collectors straightforward" contract): (1) adapter class
  + fixtures + parser tests; (2) one `sources` config block; (3) profile weight entries; (4)
  baseline epoch runs silently on first successful cycle. Nothing else — no touch-points in
  resolve/novelty/alerts.

---

## 13. Alert contract

### 13.1 Channels
`intel`, `release` (editorial), `maintenance` (health; Fleet Law 3; smartphone two-channel
precedent). Distinct Discord webhooks per channel; staging environment loads **only** staging
webhooks and overwrites all channels with the staging one (smartphone settings isolation, verbatim
pattern). Secrets from env only (`DEVICE_INTEL_DISCORD_WEBHOOK_URL__*`), never config files in
git; gitleaks contract test from day one.

### 13.2 Dedup keys
- `intel`: `intel:{entity_id}:{window_bucket}` where `window_bucket` = UTC day of the newest
  signal — materially new evidence on a later day may re-alert once per day max, and only when
  G4's accumulation rule (≥2 new signals since last intel for this entity) holds; otherwise
  suppressed silently.
- `release`: `release:{entity_id}:{stage}` — announced/orderable/shipping each alert once ever
  per entity.
- `maintenance`: `maint:{source_id}:{problem_class}` — re-open sends only on recovery→failure
  transition (smartphone MaintenanceAlerter semantics).

### 13.3 Delivery semantics
Persistence-first (smartwatch origin/main pattern): the intent row with fully rendered payload is
written **inside the ingest/novelty transaction**; `drain` performs POSTs; 429 → durable
`not_before` floor (cap 900s), attempt not burned, drain pauses; 5xx → retry ≤5 then `failed`;
4xx → terminal `failed` (except 429); never raises; errors recorded as bounded classes only.
`alerts sent` ≠ `decisions made` — every suppression keeps its intent row with `suppress_reason`
(inspectability). No claim of exactly-once; dedup_key UNIQUE + sent_at is the accounting.

### 13.4 Eligibility gates (fail-closed, layered; smartphone pattern)
1. reason-code allowlist per channel (unknown reason ⇒ never send);
2. source maturity: sources in EXPERIMENTAL state may contribute evidence but their *own*
   discoveries are suppressed from `intel` until PRODUCTION (watch delivery-gate precedent);
3. staging isolation + `test_mode` flag;
4. baseline (`suppress_reason='baseline'`), flood caps, per-profile floors.

---

## 14. Device-class policy profiles

`config/profiles/{smartphone,tablet,smartwatch}.yaml`; validated by a pydantic schema; effective
profile for an entity is chosen by its `device_class` (unknown ⇒ `default` profile: conservative
floors, INTEL only, no RELEASE until class ≥HINT). Profile keys:

```yaml
# tablet.yaml (illustrative)
weights:                       # overrides of §6 defaults
  REGULATORY_SIGNAL: 32
  BENCHMARK_SIGNAL: 22
  OEM_SIGNAL: 38
  ACCESSORY_SIGNAL: 8          # weak: never alone_material, floors untouched
novelty_windows_days: { REGULATORY_SIGNAL: 180, BENCHMARK_SIGNAL: 90, RETAIL_SIGNAL: 30, OEM_SIGNAL: 30 }
materiality_floor: 20
intel_min_identity: MEDIUM
intel_daily_cap: 12
release_enabled: true
fanout:
  enabled_targets: [geekbench, bluetooth_sig, google_device_catalog, retailer_search]
  dedup_days: 21
alert_routing: { intel: intel, release: release }   # per-profile override hooks (Phase 3)
oem_discovery_weight: 1.0      # smartwatch profile sets 1.5 + OEM in discovery scope (§14.1)
```

**14.1 Profile emphasis (per brief):**
- **smartphone:** discovery scope = regulatory + runtime first; fan-out priority
  `[bluetooth_sig, geekbench, carrier/retail]`; OEM as confirmation (weight on confirmation, not
  discovery). Radio certification is the highest-value early signal.
- **tablet:** discovery scope = regulatory + **Bluetooth/Wi-Fi certification** (Wi-Fi-only devices
  never touch radio-cert databases that require cellular) + runtime/ecosystem catalogues;
  fan-out adds accessories and retail; ACCESSORY_SIGNAL weak (never alone material).
- **smartwatch:** **hybrid** — OEM retained *in the discovery scope* (catalogues/support/news,
  smartwatch-clank's current collector set donates this plane), plus Bluetooth SIG,
  companion-software/support lists, retail. `oem_discovery_weight: 1.5`; SUPPORT_SIGNAL weight 25.
  Companion-app support records become SUPPORT_SIGNAL evidence (Phase 3 collectors).

Profile files are data; adding tuning does not require code. Profile *structure* changes are a
`policy_version` bump.

---

## 15. Persistence changes

- **device-intel (new):** the schema of §5 is created by Alembic `0001_initial` (+ later additive
  migrations). WAL mode; `PRAGMA foreign_keys=ON`; single writer via file lock (Fleet Law 7);
  `sqlite3.Connection.backup()` for every pre-migration backup (fleet rule 3).
- **smartphone-clank / tablet-clank / smartwatch-clank: ZERO schema changes in Phases 1–2.**
  Phase 3 linkage writes live **only in device-intel** (`identity_claims kind='EXTERNAL_LINK'` +
  `entity_id`); sibling stores are opened read-only (`file:...?mode=ro`) by the linkage runner —
  exactly the Motherclank adapter discipline (read-only, lock-free, integrity proof).
- Derived-table refresh is idempotent: `recompute_entity(entity_id)` rebuilds signals/stage/
  class/confidence from evidence+claims; nightly drift audit compares and reports (smartphone
  `recalculate(repair=...)` pattern).

---

## 16. Migration strategy (preserving history/baselines)

1. **Nothing is imported from the existing Clanks in Phase 1.** device-intel starts empty; each
   source baselines *itself* silently on first successful full enumeration (its own history, its
   own epoch) — this is the flood-proof path and needs no ETL.
2. **Historical backfill tool** (`cli backfill --source X --since <date>`): replays archived
   listings/feeds as baseline evidence (`is_baseline=1`, `run_reason='baseline'`, epoch open
   until the run succeeds). Completing run sets `baseline_completed_at` *before* novelty ever
   sees the rows (G0). **A failed or suspiciously-shrunken enumeration never completes a
   baseline** (smartphone rule, verbatim).
3. **Phase 3 linkage** (additive, reversible): match device-intel entities to sibling-Clank rows
   by exact normalised model code + manufacturer; results are PROPOSED EXTERNAL_LINK claims;
   operator confirms; nothing in the sibling stores changes.
4. **First-seen preservation:** when a source declares dates, entity `first_seen` back-dates to
   `min(reference_date)` — real history is preserved; when it doesn't, `first_seen` is honest
   (`observed_at`) and labeled as such. **Under no circumstance does an import produce an alert**
   (Law 1 invariant test).
5. **Existing Clank evolution** (Phase 4, per-Clank operator decisions): each Clank's OEM
   collectors may be *re-registered* as device-intel `oem`-plane sources (adapter wrapper over
   their collectors) so their proven value survives; their databases remain untouched archives.
   No `reset`, no re-baselining of their stores; any identity-key change would need the baseline
   handover record of v0.2 §4 — which is why we don't change their keys at all.

---

## 17. Testing strategy

- **Hermetic by default** (no network in CI; `live` marker opt-in). Fixture-first per source with
  provenance files (fleet precedent).
- **Law conformance tests** (named, one per invariant):
  - L1 no-flood: seed 500 baseline rows + 1 genuinely-new → exactly 1 intel intent, 0 for baseline.
  - L2 observation≠novelty: new entity whose only evidence carries 200-day-old published_at ⇒
    decision `HISTORICAL_CATCHUP`, no intel.
  - L3 health honesty: N empty-but-HTTP-200 runs ⇒ health DEGRADED/zero-reason surfaced.
  - L4 explicit event capability: every entrypoint declares (emit_events, notify); unknown reason
    ⇒ no send.
  - L5 authority: staging config cannot load production webhooks (negative test).
  - L6 provenance: every evidence row joins to run with code_revision; missing ⇒ 'UNKNOWN' literal.
  - L7 writer coordination: concurrent writer vs run serialized by the canonical lock.
  - L8 promotion: EXPERIMENTAL source cannot emit intel; bidirectional state↔config consistency.
- **Standards tests:** STD-DATA-COM-001 (epoch rows + read-time `is_baseline` flag), -002 (every
  novelty path's SQL carries the baseline predicate — tested by injecting baseline-era rows and
  asserting exclusion *through the path*, not via post-filter), -003 (auto-merge has in-record
  discriminator; reversal restores pre-merge members), -004 (tiers separable: evidence vs derived
  vs QC; derived rows cite evidence ids).
- **Resolution corpus:** §8.5 hard cases + golden fixtures (`SM-X746B` style end-to-end scenario:
  KOMDIGI cert → entity → fan-out Geekbench → identity HIGH → INTEL → OEM page → RELEASE →
  lead-time rows). Replaying the corpus twice is byte-identical at the DB-diff level except
  health/updated_at (idempotency proof).
- **Fan-out tests:** budget exhaustion, loop prevention (depth-2 attempt), 429 backoff, kill
  switch — all offline via a scripted transport.
- **CI:** sibling pattern — `phase0-ci.yml` (uv sync, ruff, compileall, pytest, gitleaks,
  pip-audit) + `fleet-laws.yml` (conformance suite from clank-architecture).

---

## 18. Observability / health requirements

- **Dual-plane source health** (`source_health`): invocation plane (`last_attempt_at`) is never
  conflated with yield plane (`last_success_commit`) — STD-OPS-COM-002. `zero_reason` typed on
  every ZERO_ITEMS run. Blocked sources surface BLOCKED with reason class.
- **Run report** (`report daily`): expected-vs-ran sources, per-source health score
  (smartphone `health_score` formula, carried over), silent-drop check, novelty outcome counts,
  intents sent/suppressed/held, fan-out burn. Markdown output; no new infra.
- **Alerts for the operator** go to `maintenance` only (config drift, parser collapse, failure
  streaks, scheduler stalls — vocabulary inherited from smartphone eligibility).
- **Observer adapter surface** (Motherclank): implement `identity/status/health/last_run/
  capability_states` shapes (v0.2 contract) + optional `evidence_envelopes` (ADR-0014 typed
  envelopes: subject=entity, evidence_type=`dic.evidence@1`) from Phase 2 so onboarding is a
  registry entry, not a project. Adapter profile: **observer** (no triggers exposed; dashboards
  never start collections — v0.2 §1, STD-UI-COM-001).
- **ClankOps:** Mission + Session per tranche; checkpoints at each phase boundary (this is
  binding, not optional).

---

## 19. Source lead-time telemetry design

- **Anchor:** the first evidence satisfying RELEASE predicates (`device_entities.anchor_evidence_id`).
  Anchor `reference_date` (labeled kind) is the market-availability moment for lead-time math.
- **Rows:** on anchor set, one `lead_time_observations` row per member evidence:
  `lead_seconds = anchor.reference_date − evidence.reference_date` (negative = source led the
  market; `reference_date_kind` records published vs observed honesty).
- **Source report** (`report source --days 90`), all derivable by SQL:
  - median / p10 lead time per source (e.g. `komdigi −47d · geekbench −31d · retailer −6d ·
    samsung_oem 0d`);
  - **unique discovery rate:** share of entities where this source's evidence was the first
    identifier introduction;
  - false-positive rate = QC `FALSE_POSITIVE`+`REJECT` decisions ÷ intents, per source;
  - duplicate rate = `DUPLICATE_SUPPRESSED` decisions naming the source ÷ its evidence;
  - availability = healthy-run share (health plane);
  - enrichment contribution = evidence that changed a derived value (new signal type, identifier
    kind, class, stage) ÷ total evidence;
  - signal→INTEL conversion and INTEL→(not suppressed) rate;
  - cost = fan-out + discovery bytes per useful discovery.
- **Governance hook:** the report is *advisory*; demotion/promotion of a source is an explicit
  `sources.state` config change with a git record (Fleet Law 8 symmetry: demotions are recorded
  like promotions). Quartermaster may later consume the report for budgets — no automatic action
  in any phase.

---

## 20. Security, rate-limit, failure considerations

- **Secrets:** env-only; staging/production isolation in settings; redaction in reprs/logs;
  gitleaks + contract test; transport errors logged as bounded classes, never raw bodies
  (webhook URL *is* the credential — smartwatch rule).
- **Politeness:** robots.txt respected; per-source `min_delay_seconds` + jitter + `max_bytes`;
  UA identifying the clank; no auth-bypass, no paywall circumvention, public surfaces only;
  Cloudflare-hostile sources get an explicit egress-relay decision (smartwatch Garmin precedent)
  recorded in source config — never an implicit proxy.
- **Failure containment:** adapter boundary never raises; semantic zeros; per-source circuit
  breaker (`consecutive_failures` → backoff_until, exponential, cap 24h); fan-out budgets;
  SQLite WAL + single-writer lock; pre-migration backup + `integrity_check` (fleet rule 3);
  crash between ingest and drain loses nothing (outbox rows persist).
- **Loop/cascade safety:** §11.4 rules are hard-coded, not config-tunable beyond caps.
- **Supply chain:** minimal deps (SQLAlchemy, alembic, httpx, pydantic, typer — the smartphone
  donor set), lockfile, pip-audit in CI.

---

## 21. Incremental implementation phases

Every phase: ClankOps Mission (per DEVELOPMENT_CONTROL) → branch → PR → review → merge. No phase
deploys, enables timers, or touches production hosts (Phase 0 freeze active throughout).

### Phase 0 — Governance & scaffolding (~small)
Register Clank identity `device-intel` in ClankOps; create repo; CI (pytest+ruff+gitleaks+fleet
laws); Alembic 0001 (§5); settings with staging isolation; adapter protocol + registry + fake
adapter; this spec's ADR-follow-up if the operator amends anything.

### Phase 1 — Proving slice (the milestone; detailed blueprint in Appendix B)
1. KOMDIGI regulatory collector (viability probe first, §21.1) producing REGULATORY_SIGNAL
   evidence with `cert_id` + `model_code` identifiers;
2. Geekbench collector: discovery (benchmark result listings) + `query_identifier` fan-out;
3. resolver v1 (exact + manufacturer-guarded base match + claims), evidence persistence, epochs,
   entity_signals;
4. targeted fan-out (KOMDIGI⇄Geekbench, depth 1, budgets);
5. INTEL alerts — staging webhook / dry-run drain only; RELEASE **not yet enabled** (no reliable
   anchor source in the slice; lands Phase 2 with the OEM/retail plane);
6. strict baseline suppression (full KOMDIGI history backfill silent);
7. lead-time observation rows (anchors only from Phase 2; Phase 1 records evidence, no anchors).
Explicitly *not* in Phase 1: commerce plane, smartwatch profile collectors, dashboards, RELEASE
channel, cross-Clank linkage.

**21.1 KOMDIGI viability gate (read-only, before any code):** confirm (a) a stable, paginated,
public listing of issued certificates exists; (b) per-certificate detail exposes holder, device
type/category, model name(s) and model code(s) without JS-only rendering or auth; (c) robots
policy permits. If any check fails: record the probe evidence and fall back in order →
**BIS (India CRS public search)** → **GCF certification DB** → **TENAA** — same adapter contract,
same Phase 1 scope; the doc's acceptance criteria are source-agnostic (`komdigi` = "primary
regulatory source actually implemented").

### Phase 2 — Second plane + RELEASE + profiles
Bluetooth SIG or Wi-Fi/equivalent second regulatory/runtime source; one retailer/commerce
targeted source (search-by-code only); RELEASE gate + anchor + lead-time report; profile split
(smartphone/tablet YAMLs live); maintenance channel on; QC queue CLI (+ dashboard only if
operator wants; STD-CUD-001 applies); daily report; observer adapter surface.

### Phase 3 — Smartwatch profile + linkage
Donate smartwatch-clank's collector patterns as the smartwatch profile's OEM/support plane
(companion-app support records as SUPPORT_SIGNAL); `smartwatch.yaml` live; EXTERNAL_LINK runner
over smartphone/tablet/smartwatch stores (read-only); first source-telemetry-driven demotion
proposal (operator decision).

### Phase 4 — Convergence (operator-gated, per-Clank)
Existing clanks' discovery roles progressively fold into device-intel sources; editorial
dashboards over device-intel with per-profile views; per-Clank ADRs for any store changes; the
cross-Clank identity ADR becomes prerequisite only if the operator wants *shared identity*
(rather than links) — otherwise links suffice indefinitely.

---

## 22. Acceptance criteria per phase

**Phase 0**
- ClankOps identity + Mission exist; repo CI green; Alembic 0001 applies to a fresh DB and
  `db check` passes; fake-adapter run produces evidence+run rows; no network in tests.

**Phase 1 (all must hold; measurable)**
1. Baseline: full historical import of the regulatory source (expected ≥1,000 certificates) and
   initial Geekbench enumeration complete with **zero** intents in channels intel/release
   (`SELECT COUNT(*) FROM alert_intents WHERE channel IN ('intel','release') = 0`), and ≥1
   novelty_decision row per baseline entity with outcome `BASELINE_SILENT`.
2. Synthetic new-certificate fixture (model code absent from store) → exactly 1 INTEL intent;
   replaying the same fixture changes nothing (idempotency).
3. Fan-out: the synthetic candidate generates Geekbench `query_identifier` request(s); a matching
   benchmark fixture raises identity_confidence to HIGH and `entity_signals` shows 2 distinct
   planes; no fan-out request is ever created from fan-out-born evidence (depth-1 test).
4. Re-sighting the same certificate (same content hash) ⇒ `KNOWN_NO_MATERIAL_CHANGE`, no new
   evidence row.
5. A 300-row bulk-touch fixture ⇒ `FLOOD_SUPPRESSED` + one maintenance intent.
6. All Fleet-Law and standards tests (§17) green; `git grep` for webhook URLs in fixtures clean.
7. Manual run end-to-end under 30 min wall-clock including polite delays; burn accounting visible
   in `collector_runs`.
8. A written comparison note: for ≥5 devices certified in the last 90 days, KOMDIGI evidence
   date vs the earliest OEM-page sighting known to smartphone-clank/tablet-clank — the "beats
   OEM crawling" hypothesis quantified (this is the phase's *purpose*).

**Phase 2**
- Second regulatory/runtime source baselined silently; RELEASE anchor + lead-time rows populated
  for ≥3 historic launches; profile split demonstrably changes weights/floors via config only;
  maintenance alerts fire on an injected parser failure; observer adapter passes Motherclank
  `validate_surface`.

**Phase 3**
- Smartwatch profile collectors baselined silently; EXTERNAL_LINKs PROPOSED for ≥80% of
  smartphone-clank devices from the last 12 months by exact code match; zero writes to sibling
  stores (verified by pre/post integrity + row-count checks).

**Phase 4** — per-Clank ADRs with their own criteria; nothing automatic.

---

## 23. Explicit non-goals — what NOT to build

1. **No cross-Clank entity merge / global entity-key authority** — blocked (v0.2 §6, Standards
   HOLD). Links only.
2. **No LLM anywhere in the core pipeline** (ingest, resolve, classify, novelty). Rendering-only
   LLM later, never decision-making.
3. **No new infrastructure**: no Redis/Kafka/message bus, no microservices, no Postgres migration,
   no containers beyond sibling-standard Dockerfiles, no scheduler daemon in Phase 1.
4. **No indiscriminate commerce crawling** — retailer search-by-identifier only.
5. **No mandatory linear lifecycle**; `editorial_stage` is a derived, orderless projection.
6. **No historical-import alerting path** — not even a debug flag.
7. **No speculative planes in Phase 1**: press/community/accessory collectors stay *designed-for*
   (schema + weights), unimplemented until a source justifies them.
8. **No dashboards before Phase 2**, no GUI promotion controls ever (STD-UI-COM-005).
9. **No modification of the three existing Clanks' schemas, DBs, or behavior in Phases 1–2**;
   their history is never rewritten; no baseline handover is triggered.
10. **No auto-demotion/auto-promotion of sources from telemetry** — reports advise; humans decide.
11. **No coverage of analog watches** (watch-clank's domain) — different Clank, out of scope.
12. **No authentication bypass, login-wall scraping, or TOS-hostile access on any source.**

---

## Appendix A — Conformance matrix (design → law/standard)

| Requirement | Mechanism |
|---|---|
| Fleet Law 1 (no-flood) | epochs + G0 + intent suppression with reasons; L1 test |
| Fleet Law 2 (obs ≠ novelty) | G2 freshness + HISTORICAL_CATCHUP outcome; reference_date labeling |
| Fleet Law 3 (health honesty) | dual-plane source_health + zero_reason; maintenance channel |
| Fleet Law 4 (explicit events) | reason-code allowlists; intents only from decisions |
| Fleet Law 5 (authorities) | one scheduler authority (manual runs in P1), one notification authority, staging isolation |
| Fleet Law 6 (provenance) | collector_runs (code_revision, config_fingerprint, run_reason); snapshots; extraction_version |
| Fleet Law 7 (writers) | single-store + canonical file lock; read-only sibling access later |
| Fleet Law 8 (promotion) | sources.state config changes; maturity eligibility gate; EXPERIMENTAL silent |
| STD-DATA-COM-001 | epochs + is_baseline read-time flag |
| STD-DATA-COM-002 | G0 predicate inside every novelty path; first-seen≠novelty outcomes |
| STD-DATA-COM-003 | resolver conservatism; identity_claims auditable/reversible |
| STD-DATA-COM-004 | evidence/derived/QC tier separation; derived rows cite evidence ids |
| STD-OPS-COM-001/002 | run rows + dual-plane health |
| STD-UI-COM-002/003 | qc_decisions semantics (when QC surface exists) |
| ADR-0014 envelopes | evidence fields align; `dic.evidence@1` envelope projection (P2+) |
| v0.2 §5 semantic zeros | ZeroReason on every adapter result |
| v0.2 §6 cross-Clank | EXTERNAL_LINK claims only; ADR prerequisite named for Phase 4 |

## Appendix B — Phase 1 implementation blueprint

Repository `device-intel` (provisional name; operator may rename):

```
device-intel/
  pyproject.toml                # deps: sqlalchemy>=2, alembic, httpx, pydantic>=2, typer; python>=3.11
  alembic/versions/0001_initial.py
  config/
    settings.py                 # DEVICE_INTEL_* env; staging loads staging webhooks only
    config.yaml  config.staging.yaml
    sources.yaml                # §5.1 registry as config (komdigi, geekbench, [fake])
    profiles/default.yaml  smartphone.yaml  tablet.yaml  smartwatch.yaml
  device_intel/
    models/            # ORM mirror of §5 DDL
    adapters/          # base.py (§12 types) registry.py eligibility.py http.py transport_fake.py
    collectors/komdigi/   adapter.py parser.py
    collectors/geekbench/ adapter.py parser.py
    resolution/        # normalize.py resolver.py claims.py confidence.py
    evidence/          # ingest.py projections.py
    novelty/           # gates.py policy.py stages.py
    fanout/            # planner.py budgets.py executor.py
    alerts/            # intents.py render.py discord.py drain.py eligibility.py
    telemetry/         # leadtime.py source_report.py
    observability/     # metrics.py health.py daily_report.py
    runtime/           # locks.py provenance.py paths.py     (smartphone-clank donor patterns)
    pipeline.py        # run_once(source) = collect→ingest→resolve→novelty→plan_fanout (tx per stage)
    cli.py             # init, collect, ingest, resolve, novelty-evaluate, fanout plan|execute,
                       # drain [--dry-run], report daily|source, backfill, qc, db, epoch, test-alert
  tests/               # law/standard suites (§17), resolution corpus, fixtures per source
  fixtures/komdigi/    fixtures/geekbench/      # + PROVENANCE.md each
```

Key signatures (beyond §12):

```python
# resolution/resolver.py
class EntityResolver:
    def attach(self, session, evidence: evidence_row) -> AttachResult:
        """AttachResult(entity, created: bool, claims: list[Claim], material_change: bool).
        Implements §8.3 steps 2–7 exactly; auto-merge only via
        rule_id='manufacturer_guarded_base_match'."""

# novelty/policy.py
class NoveltyPolicy:
    VERSION = "dic-policy-1"
    def evaluate(self, session, entity, trigger_evidence, profile) -> Decision:
        """Runs G0→G6 in order; writes novelty_decisions; returns outcome.
        Every early-exit writes its decision row too (audit completeness)."""

# alerts/intents.py
def enqueue_intel(session, entity, decision, profile, *, test_mode: bool) -> intent_row | None
def enqueue_release(session, entity, decision, profile, *, test_mode: bool) -> intent_row | None
    # render payload fully here (templates §10.4/§10.5); persist with dedup_key; never POST.

# fanout/planner.py
def plan(session, entities_changed_this_run, profile, *, now) -> list[FanoutRequest]
    # pure: creates PENDING rows or SKIPPED_* rows with reasons; no network.
```

Manual run loop (Phase 1 operator flow; no timers):
```
python -m device_intel collect --source komdigi      # or: --all (production-selected only)
python -m device_intel fanout execute --limit 25
python -m device_intel drain --dry-run               # inspect; then real drain against staging webhook
python -m device_intel report daily
```

## Appendix C — Open decisions for the operator

1. **Repo/name:** `device-intel` as proposed, or fold Phase 1 into an existing repo (rejected in
   §3.2 for identity/scope reasons; noted for completeness).
2. **Primary regulatory source:** KOMDIGI NextGen per the brief, with the §21.1 viability probe
   and BIS→GCF→TENAA fallback order.
3. **Phase 1 alert destination:** staging webhook vs `--dry-run` only (both compliant; staging
   webhook proves the full path).
4. **ADR follow-ups to schedule:** (a) accept/amend this spec (one ADR); (b) eventual
   cross-Clank identity ADR *only if* Phase 4 wants shared identity rather than links.
5. **Quartermaster consumption** of the source report for budgets — later, advisory.

---

*End of specification. Nothing in this document is authority until the operator accepts it via
review; implementation must not begin without the ClankOps Mission gate (AGENT_RULES.md rule 16).*
