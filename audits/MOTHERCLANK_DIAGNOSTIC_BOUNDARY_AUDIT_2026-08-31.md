# Motherclank / Diagnostic Clank Boundary Audit

Status: **Audit draft — evidence-led, not a promotion decision**
Prepared: 2026-08-31
Scope: `anil-ganti-nbc/motherclank` and `anil-ganti-nbc/diagnostic-clank`, with governance from this repository.
Authority citations: ADR-0002 (PROPOSED reviewed draft), ADR-0003 (ACCEPTED inbox bridge), Fleet Laws 1–8 ACTIVE, Law 9 deferred, `NO_PROMOTION_POLICY.md` ACTIVE, `M5_ENTRY_CRITERIA.md` (pre-conditions only; does not authorize M5).
Live runtime: **UNKNOWN**. Git HEAD is not a deployed SHA. Timer templates are not scheduler-fire proof. Absence of incidents is not “no problem.”

This document is the durable artefact for Mission 3. It records what the trees contain at the inspected SHAs. It does not claim any of it ran on a host.

---

## Executive finding

The working hypothesis is **mostly confirmed as intended, leaky in implementation**.

- **Motherclank** answers: what is the fleet doing, what state can I observe, what deserves operator attention? Stages M0 harvest / M1 synthesize / M2 detect / M3 recommend / M4 QC ingest exist in Git. Outputs are DERIVED JSONL. M5 mutation is not present and is not authorized.
- **Diagnostic Clank** answers two historically fused jobs: (1) Archivist — what failed or was missed, what evidence explains it, how should that failure be classified; (2) observer-plane host — `clank-fleet` adapters + `fleet.yaml` inventory that Motherclank consumes unchanged.

That fusion is **intentional historical evolution**, not a clean diagram. ADR-0002 says Diagnostic hosts the adapter plane and Motherclank consumes it; ADR-0003 ratifies M0–M4 and authorizes one write: M3 recommendations into Diagnostic’s Agent Inbox. The split is coherent if operators keep:

1. observation (Motherclank DERIVED) distinct from diagnosis (Diagnostic engine / Archivist incidents);
2. collector HEALTHY distinct from recall / delivery / intelligence;
3. checkout HEAD distinct from `deployed_commit_sha`;
4. `SCHEDULE_EXPECTED ≠ SCHEDULER_FIRED ≠ PROCESS_STARTED ≠ RUN_MATERIALIZED`.

Leaks found in Git (not live-proven):

- M2 emitted `STALE_RUN` while M3 keyed `STALE_RUN_ACTIVE` — active stale-run produced **no recommendation**. Repaired in motherclank this audit (rule key aligned; tests now fire).
- Inbox regex treated `rec-<16hex>` and `sha256:<64hex>` as a git revision. Repaired in diagnostic-clank this audit (40-char SHA only; `sha256:` skipped).
- Operator sanity check labelled checkout HEAD as “deployed SHA”. Repaired (wording).
- `FINITE_SOAK` policy short-circuited `liveness_state=CURRENT` with no run evidence. Repaired to remain UNKNOWN.
- Continuity default `CONTINUOUS` on empty applicable events still names absence as proven continuity. **Documented, not renamed** (vocabulary cascade).
- v0.1 Diagnostic GUI/CLI never call `diagnose()`. The engine is a latent classifier.
- `host-harvest.sh` does **not** pass `--inbox-db`. Inbox bridge is implemented and tested; timer artefact does not fire it. Runtime of the timer remains UNKNOWN.
- Two “ADR-0003” identities. Two default knowledge DB names. Two BANKAI meanings.

No P0 found on harvest isolation, UNKNOWN→HEALTHY in M0/M1/M2 core, or Motherclank mutation of Clank DBs.

**Verdict: BOUNDARY HEALTHY WITH MINOR REPAIRS.**

CVC integration PRs (`motherclank#1`, `diagnostic-clank#9`) exist and were **not** treated as current architecture and were **not** merged.

---

## Method and limits

Inspected:

- motherclank `@7cee2f89c4e84fdad3eb337a7eb4cbcc5dce8e04` on `main` (then P1 branch)
- diagnostic-clank `@3667af02c8dd33503ce75461ec2974d42f2f1d4c` on `diagnostic-clank-2026-08` (then P1 branch)
- clank-architecture `@e9c4a2b77f0a484171b01980469eee34971f8ee5` on `main`

Method: read README/ADRs/CLI/schemas/persistence/tests; grep epistemic traps; run existing suites in a sandbox Python 3.11 venv. Did **not** operate collectors, inspect production databases, send notifications, access Hetzner, or treat systemd unit files as fire proof.

Standards Clank, CVC Clank, Clank Systems Handbook, DAU, and live hosts were out of scope.

---

## 1. Takeover

### motherclank (`anil-ganti-nbc/motherclank`)

| Item | Value |
|---|---|
| Default branch | `main` |
| Inspected HEAD | `7cee2f89c4e84fdad3eb337a7eb4cbcc5dce8e04` — “closure hygiene: operator sanity check script” |
| Package | `motherclank` 0.1.0, `requires-python >=3.11` |
| Open PRs (ignored as architecture) | [#1](https://github.com/anil-ganti-nbc/motherclank/pull/1) Wire CVC into registry-driven observation (`integrate-cvc-clank`) |
| Test baseline (this audit, Python 3.11) | **448 passed, 4 skipped** |
| Runtime | UNKNOWN |

Recent subjects (HEAD backwards): sanity-check script, Tablet RETIRED onboarding, fleet closeout, scheduler-fire attestation, SI/CTW onboarding, observer contract v0.2/v0.3.

CLI subcommands in Git: `harvest`, `synthesize`, `detect`, `recommend` (`--inbox-db` opt-in), `ingest-qc`, `soak-report`, `validate-continuity`, `closeout`. README still titled “Motherclank M0” and does not document M3/M4/inbox.

### diagnostic-clank (`anil-ganti-nbc/diagnostic-clank`)

| Item | Value |
|---|---|
| Default branch | `diagnostic-clank-2026-08` |
| Inspected HEAD | `3667af02c8dd33503ce75461ec2974d42f2f1d4c` — “P-4.6: Tablet Clank observer adapter” |
| Open PRs | [#9](https://github.com/anil-ganti-nbc/diagnostic-clank/pull/9) CVC observer (ignore as architecture); [#8](https://github.com/anil-ganti-nbc/diagnostic-clank/pull/8) draft Phase 0 closeout; [#3](https://github.com/anil-ganti-nbc/diagnostic-clank/pull/3) bench exact-SKU false negative |
| Test baseline (this audit, Python 3.11, pytest-qt autoload disabled) | clank-runtime **114 passed**; clank-fleet **72 passed, 6 skipped**; diagnostic-clank app **62 passed, 2 skipped**; diagnosticbench **1 passed**; repo-root tests **6 passed**. Desktop shell test **not run** (missing `libEGL.so.1` in sandbox). |
| Runtime | UNKNOWN. `fleet.yaml` diagnostic-clank `deployment_state: UNKNOWN`. CLI identity defaults to `"unknown"`. |

README still describes Stage 1A prototype control plane. v0.1 GUI is “Local Archivist / field test” with **no autonomous diagnosis**.

### clank-architecture (this repo — canonical home for this document)

| Item | Value |
|---|---|
| Default branch | `main` |
| Inspected HEAD | `e9c4a2b77f0a484171b01980469eee34971f8ee5` |
| Open PRs | [#1](https://github.com/anil-ganti-nbc/clank-architecture/pull/1) draft coding-agent prompt guidance (unrelated) |

ADR-0002 remains **PROPOSED — REVIEWED DRAFT**. ADR-0003 (inbox bridge) is **ACCEPTED** and is the only accepted Motherclank-specific ADR. ADR-0003 is **missing from `DECISION_LEDGER.md`**.

---

## 2. Responsibility matrix

Mark: **C** canonical owner · **R** read-only consumer · **S** shared intentionally · **A** accidental overlap · **N** no owner.

| Capability | Motherclank | Diagnostic | Neither/external |
|---|---|---|---|
| Fleet inventory (`fleet.yaml`) | R (registry seed, ledger SHAs) | **C** | |
| Collector / adapter inventory | R (BUILTIN_REGISTRY mirrors adapters) | **C** (`clank_fleet.adapters.*`) | |
| Source inventory | R (adapter health sources) | **C** (adapters + per-Clank DBs) | each Clank is domain truth |
| Scheduler observation | **C** (liveness + traces consume) | S (probe plane / `execution_results`) | timer templates are Git artefacts only |
| Deployed SHA observation | R (`fleet.yaml` `deployed_commit_sha`; Law 9 `checkout_head` vs ledger) | **C** of inventory text | live host SHA UNKNOWN |
| Process observation | **C** (liveness stages) | R (adapter `last_run`) | |
| Quota / capacity observation | N | N | **N — no owner** |
| Health observation (ops) | **C** of fleet rollup (DERIVED, downgrade-only) | **C** of adapter `status()`/`health()` | dual-domain HEALTHY (ADR-0007) is not what adapters emit |
| Recommendation | **C** M3 text-only | R Inbox storage | operator disposition |
| Mutation / remediation | N (forbidden; M5 not authorized) | N (Fleet POST /actions = 501) | operator / each Clank |
| Incident creation | N | **C** Archivist (manual) | |
| Incident classification | N (M2 types are anomalies, not incidents) | **C** (`IncidentClassification`, engine `failure_class`) | |
| Miss classification | N | **C** (engine + bench) | |
| Source-gap classification | N (may *surface* blocked sources as anomalies) | **C** | |
| Region-gap classification | N | **C** (engine keeps distinct; first-FAIL can mask) | |
| Root-cause evidence | N | **C** (`RootCauseCertainty`, never forced CONFIRMED) | |
| Evidence preservation | own JSONL hashes | **C** knowledge store + file-inbox content-hash | |
| Source admission / promotion | N | N | operator; freeze ACTIVE |
| Soak decision | Axis-B M5 *gate scoring only* (read-only) | N | operator; two “M5” meanings |
| Promotion decision | N | inventory records `promotion_eligible` | **C** operator + freeze |
| Operator notification | N (forbidden) | N (adapters do not send) | each Clank’s own notify path |
| Runtime-state ownership | own `var/` DERIVED | own `diagnostic.db` | Clank SQLite authoritative |
| Fleet policy | obeys | hosts inventory | **C** clank-architecture (laws/ADRs) |
| Standards / governance | N | N | **C** clank-architecture; Standards/CVC out of scope |
| Historical institutional memory | GIC / closeout JSONL | DiagnosticBench + incidents + reports | architecture `audits/` |

**Accepted intentional overlap:** adapter plane owned by Diagnostic, consumed by Motherclank; Inbox owned by Diagnostic, written by Motherclank only via public `save` when `--inbox-db` is passed.

**Harmful / leaky overlap:** Diagnostic desktop GUI titled “Motherclank — Agent Inbox”; default `data/motherclank_knowledge.db` vs Archivist `diagnostic.db`; Diagnostic `clank-fleet` is a generic fleet observer living inside the diagnostic repo; two ADR-0003 documents.

---

## 3. Data ownership map

| Object | Canonical owner | Writer(s) | Reader(s) | Lifecycle | Provenance | Copied? | Drift risk | Can be mistaken for live? |
|---|---|---|---|---|---|---|---|---|
| `fleet.yaml` deployments | Diagnostic | humans in diagnostic-clank | Motherclank harvest/registry; Fleet API | file in Git; `inventory_status: INVENTORY_INCOMPLETE`; as_of 2026-08-22 | inventory rows | snapshot `inventory_ledger` copies 40-char SHAs | stale inventory presented as current | **YES** if treated as live host |
| Clank identity | each Clank + inventory `instance_id` | Clank / inventory authors | adapters, Motherclank, Inbox registry | | `clank_id` | adapter identity() | two registries (adapter builtin vs fleet.yaml CLANK rows) | |
| Source / region identity | each Clank | Clank collectors | adapters `health().sources`; engine facts | | source_id | Motherclank source rollup | | |
| Adapter `status()` HEALTHY | Diagnostic adapters | none (computed) | Motherclank snapshot; Fleet API | ephemeral | last_run timestamp often sufficient | snapshot JSON | Watch/Smartphone/KTW HEALTHY ≠ dual-domain HEALTHY | **YES** |
| Observed SHA (`checkout_head`) | Motherclank drift.py | file-read `.git/HEAD` | M1/M2 REVISION_DRIFT | per harvest | labelled checkout, not deployed | | Law 9 advisory-only | if labelled deployed |
| Ledger SHA (`deployed_commit_sha`) | Diagnostic inventory | inventory authors | Motherclank `_inventory_ledger` (skips UNKNOWN) | Git text | 40-hex only | | inventory != host | **YES** |
| M0 snapshot JSONL | Motherclank | `append_snapshot` | M1/M2 | append-only `var/snapshots/` | `content_hash`, `derived_label` | no | | **YES** if not labelled DERIVED |
| M1 synthesis | Motherclank | `append_synthesis` | M2, reports | append-only | snapshot_hash | | fleet_state omits UNKNOWN members | |
| M2 anomaly | Motherclank | `append_batch` | M3 | NEW/ONGOING/RECOVERED retained | snapshot hashes | | unmapped types vanish at M3 | |
| M3 recommendation | Motherclank | JSONL + optional Inbox | operator; Diagnostic Inbox | ACTIVE/CLOSED retained | `recommendation_id`, `advisory_only` | Inbox row if bridged | STALE_RUN key mismatch (repaired) | rec text as observation |
| Inbox `agent_outputs` | Diagnostic | Motherclank bridge; GUI paste; CLI scan | dashboard | immutable raw_text; content-hash dedup | `misc_source`, `external_ref` | | SHA regex (repaired) | “Detected git revision” |
| Archivist incident | Diagnostic | dashboard/CLI (token) | dashboard | OPEN/…; claims never deleted | | | GUI root_cause string → HYPOTHESIS | |
| DiagnosticCase / engine result | Diagnostic (latent) | nobody in v0.1 GUI | tests only | ephemeral | facts dict | | first-FAIL dual-gap mask | HIGH confidence on first FAIL |
| DiagnosticBench case | Diagnostic | YAML authors | bench tests | fixtures | HISTORICAL_L_INCOMPLETE_EVIDENCE | | BANKAI name collision | |
| Continuity events | Motherclank registry file | operator append | M1 annotate | append-only JSONL | | | empty → CONTINUOUS | **YES** |
| Liveness expectations | Motherclank registry file | operator append | derive_liveness | append-only | | | FINITE_SOAK CURRENT (repaired) | |
| Scheduler traces | Diagnostic probe plane / operator JSONL | not Motherclank | liveness | | invoked_at / process_started | | timer unit ≠ fired | |
| QC corpus | Motherclank M4 | ingest-qc | soak-report | append-only | adapter version + snapshot hash | | soak PASS ≠ Clank promotion | |
| `diagnostic.db` | Diagnostic Archivist | store writers | dashboard | WAL-ish | | backup copies | vs `motherclank_knowledge.db` | two files look like one truth |
| Desktop cache schema | Diagnostic contracts | none (not wired) | n/a | DDL only | | | | |
| Quota/capacity snapshot | **no owner** | none | none | n/a | n/a | n/a | n/a | n/a |

Motherclank and Diagnostic independently author **fleet health-shaped objects** (adapter HEALTHY vs M1 fleet_state). They are not the same canonical truth: one is per-Clank ops signal, one is DERIVED rollup. Collapse is the defect.

---

## 4. Handoff traces (five scenarios)

### Scenario 1 — green machinery, failed mission (BANKAI-like)

**Do not collapse two BANKAI meanings:**

| Sense | Evidence | Owner |
|---|---|---|
| A. Named OEM experimental soak instance | `fleet.yaml:597-625` `oem-radar-hetzner-bankai-exp-timer-01`; last_job_status SUCCESSFUL; source_freshness UNKNOWN | inventory text (Diagnostic) |
| B. DiagnosticBench recall gap | `diagnosticbench/cases/DB-003.yaml` “BANKAI benchmark — 0/50 qualifying-story recall”; `incident_family: source_gap_recall`; `root_cause: UNKNOWN`; lesson: green collectors ≠ qualifying-story recall | Diagnostic bench (historical, incomplete evidence) |

**What Motherclank sees:** OEM adapter `status()` HEALTHY if a `crawler_runs` row is `ok` (`oem_radar.py`). Collection health does not consult recall gold-sets. A FINITE_SOAK / MANUAL BANKAI lane is a **liveness expectation**, orthogonal to ops health. Motherclank may emit source-health anomalies; it does not classify SOURCE_GAP recall.

**What Diagnostic sees:** DB-003 expects classification `[SOURCE_GAP, INTELLIGENCE_FAILURE]` and forbids inventing root cause. v0.1 GUI does not call `diagnose()`. An operator can file a manual incident with both SOURCE_GAP and INTELLIGENCE_FAILURE tags. `INTELLIGENCE_FAILURE` is **not** in `IncidentClassification` enum — bench expected class can fail to round-trip.

**Incident/miss:** only if an operator (or a future engine caller) creates one. Nothing automatic from adapter HEALTHY.

**Recommendation:** Motherclank will not recommend “fix the parser” from green crawlers. M3 maps blocked-source streaks to UPSTREAM_CLANK_REMEDIATION, first-observation degraded to NO_ACTION_WATCH. Recall-benchmark failure is Diagnostic’s job.

**Remains UNKNOWN:** whether any host still runs the bankai timer; whether the 0/50 set was ever remediated; live recall.

This is the **intended split**. Adapter HEALTHY ≠ intel health (engine law `OPS_HEALTH_NOT_INTEL_HEALTH`; ADR-0007; DB-003 lesson).

### Scenario 2 — scheduler fired, process did not materialize

Motherclank `liveness.py` states:

```
SCHEDULE_EXPECTED != SCHEDULER_FIRED != PROCESS_STARTED
    != RUN_MATERIALIZED != RUN_COMPLETED != OUTCOME_RECORDED
```

Absence of evidence is UNKNOWN, never NO — except a **positive** trace with `process_started=false`, which proves MATERIALIZATION_GAP (pre-exec failure). M2 emits `MATERIALIZATION_GAP`; M3 maps it to DEPLOYMENT_SCHEDULER_INSPECTION with explicit “Do NOT diagnose collector regression from this record alone.”

Diagnostic adapters: Watch `status()` HEALTHY if `last_run.started_at` exists — that is PROCESS_STARTED-ish, not SCHEDULER_FIRED. A timer unit file in Git is not SCHEDULER_FIRED.

`scripts/install-user-timer.sh` / host unit templates prove **intent to schedule**, not that a timer fired.

### Scenario 3 — source/region gap

Engine (`engine.py:32-43,133`): missing `source_capable` → INSUFFICIENT_EVIDENCE (honest). `source_capable=False` → source_gap. `region_monitored=False` → region_gap. Tests keep them distinct.

**Collapse:** first FAIL in pipeline order wins. SOURCE_CAPABILITY precedes REGION_COVERAGE, so dual FAIL becomes primary `source_gap` with region_gap downstream. Report ingestion string-scan also prefers SOURCE_GAP over REGION_GAP. Incident records **can** hold both tags; auto-extract and engine primary class cannot.

Motherclank does not emit source_gap/region_gap. It emits SOURCE_HEALTH_TRANSITION / PERSISTENT_BLOCKED_STREAK / SOURCE_DEGRADED_AT_FIRST_OBSERVATION from adapter source statuses. Those are observation-plane, not gap classification.

GUI unused: `source_capable` path is latent.

### Scenario 4 — deployed SHA unknown

Honest paths:

- `fleet.yaml` may contain `UNKNOWN` or a 40-char pin. Motherclank `_inventory_ledger` **drops** UNKNOWN pins (does not invent).
- `drift.py` reads checkout `.git/HEAD` as `checkout_head`, ledger as `ledger_sha`; relationship CONVERGED / DIVERGED / UNKNOWN. Advisory-only (ADR-0003 §4).
- Diagnostic CLI identity: env or `"unknown"`. Dockerfile `GIT_REVISION` bake-time, default unknown. `/healthz` has no revision.

False-certainty (repaired): `scripts/sanity_check.py` printed `deployed SHA: {git rev-parse HEAD}` of the **motherclank checkout**.

Repo HEAD must not become deployed SHA. After the wording fix, remaining risk is operator UX treating Law 9 `checkout_head` as host-deployed.

### Scenario 5 — quota/capacity constraint

Neither repo owns scheduling policy or quota/capacity observation. Grep for quota/capacity as a fleet concept is empty. Size caps exist only as local upload limits (attachments 25 MiB, file-inbox 2 MiB).

**Boundary:** Motherclank should not invent scheduling policy; Diagnostic should not either. Capacity failure, if it occurs, is an incident for Diagnostic to classify once evidence exists, and an observation/recommendation for Motherclank only if adapters expose a signal. Today that signal does not exist. **No owner — do not fill with Standards/CVC.**

---

## 5. Provenance audit

### Motherclank M0 snapshot preserves

`clank_id` (block key), `clank_version`, harvested_at, inventory_revision (`git:{sha}` of inventory repo **or** content hash), adapter contract version, previous_snapshot_hash, content_hash, per-method FAILED_ADAPTER isolation, source health entries as adapter emitted them.

### Dropped / narrowed

- Adapter `identity()` besides `clank_version` (contract_version used for validation then dropped from block).
- Capabilities reduced to three booleans.
- Undeclared optional methods never invoked (honest skip, not fabricated zeros).

### Inbox bridge (when `--inbox-db` used)

Preserved: `primary_clank_id`, `output_type=recommendation`, `agent_family=misc`, `misc_source=motherclank-m3/<RULES_VERSION>`, `external_ref=recommendation_id`, rendered text (title/action/citations/hashes), `advisory_only` in body.

Fail-closed: blank `clank_id` aborts; never rewritten to `fleet-wide`.

Lost before repair: true git SHA (none in typical rec text) while a **content-hash fragment** was stored as `related_git_revision`. After repair: stays None unless a standalone 40-char SHA appears.

Host-harvest **does not invoke the bridge**. Local JSONL recommendations still exist.

### Diagnostic engine

Preserves clank_id, facts keys, first_failed_gate, failure_class, evidence_missing. Drops dual-primary class. `diagnose()` does not write Inbox or Clank DBs (`test_no_child_mutation`).

### UNKNOWN / missing-evidence

M0/M1/M2 core: missing → UNKNOWN; aggregation may downgrade never upgrade. Continuity/liveness defaults that name absence as CONTINUOUS/CURRENT are the remaining epistemic leaks (CURRENT repaired for FINITE_SOAK).

---

## 6. UNKNOWN audit (false-certainty risks)

| Risk | Where | Severity | This audit |
|---|---|---|---|
| Git HEAD labelled deployed SHA | `motherclank/scripts/sanity_check.py` | P1 | **Fixed** wording |
| Timer template as scheduler-fire proof | `install-user-timer.sh`, fleet.yaml `scheduler.enabled` | P2 | Document only |
| No error / timestamp → HEALTHY | Watch/Smartphone `status()` if `started_at`; KTW if any `finished_at` | P1 (adapter, historical) | Document; dual-domain ADR-0007 already forbids collapse |
| Stale inventory as current | `fleet.yaml` as_of 2026-08-22, INVENTORY_INCOMPLETE | P2 | Document; live refresh is ACT-001 class |
| Absence of incident → no problem | continuity empty → `CONTINUOUS`; GUI empty incident list | P1 naming / P2 UX | Continuity **documented**; not renamed |
| Missing source auto source_gap | engine only if `source_capable is False`; absent key → INSUFFICIENT_EVIDENCE | honest | no change |
| Recommendation as observation | M3 text is advisory; dashboard stores as RECOMMENDATION | OK if type shown | |
| Inference persisted as fact | FINITE_SOAK → CURRENT | P1 | **Fixed** remain UNKNOWN |
| Fallback invents identity | inbox_bridge refuses blank clank_id | OK | |
| Content-hash as git SHA | inbox `_SHA_RE` 7–40 hex | P1 | **Fixed** 40-char, skip sha256: |
| First-FAIL HIGH confidence with missing later stages | engine.py:133,184 | P2 | Document |
| GUI root_cause string → HYPOTHESIS | dashboard.py:918-921 | P2 | Document |
| host-harvest inbox assumed | script omits `--inbox-db` | P2 | Document |

Silent UNKNOWN→concrete in **core harvest isolation** was not found. That remains the load-bearing invariant.

---

## 7. Motherclank M0–M4 (Git vs runtime)

Runtime status for all rows: **UNKNOWN** (not proven on a host).

| Stage | Intended | Code present? | Tests | Inputs | Outputs | Persistence | Operator surface | Git status | Current? |
|---|---|---|---|---|---|---|---|---|---|
| M0 | Observation | `snapshot.py`, `adapters.py`, `cli harvest` | `test_m0.py` + contract v0.2 | fleet.yaml, real-state DB copies, adapters | JSONL snapshot + Markdown | `var/snapshots/`, `var/reports/fleet-*` | harvest CLI; host-harvest.sh artefact | IMPLEMENTED IN GIT | current |
| M1 | Synthesis, Law 9 metric | `synthesis.py`, `drift.py`, `liveness.py`, `continuity.py` | `test_m1.py`, continuity, p4 goldens | latest snapshot, optional checkouts/traces | synthesis JSONL | `var/syntheses/` | synthesize CLI | IMPLEMENTED IN GIT | current |
| M2 | Anomaly ledger | `anomalies.py` m2-r1 | `test_m2.py` | snapshot+synthesis history | anomaly JSONL | `var/anomalies/` | detect CLI | IMPLEMENTED IN GIT | current (STALE_RUN type) |
| M3 | Advisory recs + Inbox bridge | `recommendations.py` m3-r1, `inbox_bridge.py` | `test_m3.py`, `test_adr0003_bridge.py` | anomaly batch | rec JSONL; Inbox **opt-in** | `var/recommendations/`; Inbox if `--inbox-db` | recommend CLI | IMPLEMENTED IN GIT; **timer path does not bridge** | current |
| M4 | QC corpus ingest | `qc_corpus.py`, `soak.py` | `test_m4.py`, `test_soak.py` | QC adapters (watch/smartphone/ktw) | qc JSONL; soak gates | `var/qc_corpus/`, `var/soak/` | ingest-qc, soak-report | IMPLEMENTED IN GIT | current; soak is Axis-B scoring not M5 execution |
| M5 | Controlled actions **or** QC learning (two docs) | soak-report scores gates only | soak tests | M4 corpus | gate PASS/NOT-YET-MATURE | soak JSONL | soak-report “M5 gate scoring” | **NOT AUTHORIZED**. No mutation path. `M5_ENTRY_CRITERIA.md` is pre-conditions. Two unreconciled M5 meanings. | forbidden |

`host-harvest.sh` chains M0→M1→M2→M3(no inbox)→M4→soak-report. Presence of the script is not proof it runs.

---

## 8. Diagnostic pipeline (actual)

```
fleet.yaml inventory
    → clank_fleet.adapters (read-only SQLite)
        → Fleet API GET /clanks|/health (Stage 1A)
        → Motherclank harvest (consumer)
evidence ingestion
    → file inbox + AgentOutputInbox + report_ingestion (AUTO_EXTRACTED findings, not incidents)
benchmark / miss intake
    → diagnosticbench YAML (DB-003 BANKAI, etc.) — fixtures, not a live runner in this audit
incident records
    → IncidentStore (manual, v0.1; independent of diagnose())
source_gap / region_gap
    → engine failure_class + incident tags; engine unused by GUI
failure taxonomy
    → IncidentClassification vs engine FailureClass vs bench expected lists (not 1:1)
confidence / UNKNOWN
    → RootCauseCertainty default UNKNOWN; engine UNRESOLVED if no FAIL
operator workflow
    → dashboard Archivist + optional Tk “Motherclank — Agent Inbox”
emitted packages
    → backup of diagnostic.db; no Motherclank mutation
```

**Has Diagnostic drifted into generic fleet supervision?** Partially, by construction: `clank-fleet` (adapters, inventory, Fleet API) lives in this monorepo because ADR-0002 put the adapter plane here. That is **intentional overlap**, not a secret Motherclank. Drift risk is UX: Fleet API `safe_status` HEALTHY and Archivist incidents share a product name. Files: `clank-fleet/src/clank_fleet/adapters/*`, `fleet_api/routes/__init__.py`, `inventories/fleet.yaml`. Do not rewrite for symmetry.

v0.1 Archivist explicitly **refuses** to call `diagnose()` (`incidents.py:1-8`, `dashboard.py:1-7`).

---

## 9. Overlaps

### Intentional

- Adapter plane Diagnostic-owned, Motherclank-consumed.
- Inbox Diagnostic-owned, Motherclank may `save` RECOMMENDATION rows.
- Dual-domain health law shared conceptually (ADR-0007 in Diagnostic; ops vs intel in DB-003; Motherclank liveness orthogonal to operational health).
- Law 9: Motherclank computes advisory drift; Diagnostic inventory holds ledger SHAs.

### Harmful

- Two ADR-0003 documents (architecture inbox bridge vs Diagnostic desktop cache). Code comments “ADR-0003 §2” mean architecture-repo. Operators grepping the Diagnostic tree hit the wrong file.
- Broader ADR-number collision (0001, 0002, 0005, 0006, 0007) across the two repos.
- Tk GUI title “Motherclank — Agent Inbox” and default `motherclank_knowledge.db` inside Diagnostic.
- `STALE_RUN` vs `STALE_RUN_ACTIVE` (repaired).
- Inbox SHA extraction (repaired).

### Historical

- Diagnostic repo grew as “Unified Clank Platform” (v3 desktop/NAS HQ) then gained Archivist + adapter plane + Motherclank-adjacent Inbox. Motherclank was extracted as a separate runtime (ADR-0002) but README/pyproject still say “M0”.
- BANKAI as soak instance vs BANKAI as 0/50 recall case.
- Two M5 meanings (mutation vs QC learning experiment).

---

## 10. Findings

### P0

None in core harvest isolation or UNKNOWN→HEALTHY of M0/M1/M2. No Motherclank write to Clank DBs. No M5 mutation path.

### P1 (behaviour incorrect; small repairs applied or documented)

| ID | Finding | Repair |
|---|---|---|
| P1-1 | M2 `STALE_RUN` unmapped in M3 (`STALE_RUN_ACTIVE`). Active stale-run yielded no recommendation. `test_m3.py` had a no-op loop over the wrong key. | **Fixed** in motherclank: rule key `STALE_RUN`; tests assert ACTIVE inspection rec. Recovered `watch:STALE_RUN` unchanged. |
| P1-2 | Inbox first 7–40 hex → `related_git_revision`; Motherclank rec text contains `rec-<16hex>` and `sha256:<64hex>`. Dashboard labelled “Detected git revision”. | **Fixed** in diagnostic-clank: 40-char only, skip `sha256:`; dashboard label “Related git SHA (40-char only)”; tests added. |
| P1-3 | `sanity_check.py` “deployed SHA: HEAD”. | **Fixed** wording: checkout HEAD (not a deployed SHA). |
| P1-4 | `FINITE_SOAK` → `liveness_state=CURRENT` with no run evidence. | **Fixed**: remain UNKNOWN; note explains cadence not applied; test added. |
| P1-5 | `continuity_state=CONTINUOUS` when no applicable events. Names absence as proven continuity. | **Documented**. Rename to `NO_REGISTERED_DISCONTINUITY` would cascade closeout/tests/reports. |
| P1-6 | Adapter `status() HEALTHY` from a timestamp (Watch/Smartphone/KTW). Dual-domain HEALTHY (ADR-0007) is not this signal. | **Documented**. Changing adapter HEALTHY is not a small isolated patch; it is fleet-wide contract. |

### P2 (architecture; document only)

- host-harvest does not pass `--inbox-db` while ADR-0003 presents Inbox as the M3 delivery path.
- ADR-0002 still PROPOSED while ADR-0003 ACCEPTED ratifies the implementation; ADR-0003 missing from decision ledger.
- Two ADR namespaces; two knowledge DB filenames; Tk vs HTTP product names.
- Engine first-FAIL masks dual source+region gap; unused `diagnose()`; unreachable all-pass LOW branch (unevaluated stages always INSUFFICIENT_EVIDENCE).
- Bench expected `INTELLIGENCE_FAILURE` not in `IncidentClassification`.
- Quota/capacity has no owner.
- Law 9 DIVERGED cannot state direction without fetch (honest); inventory as_of 2026-08-22.
- `make test` does not run diagnostic-clank app or diagnosticbench tests.
- CTW probe helper imports `motherclank.scheduler_traces` (Diagnostic → Motherclank package dependency).
- README/pyproject still describe Motherclank as M0-only.

### P3 (ideas; do not implement)

- Shared ADR numbering scheme across repos.
- Wire `diagnose()` into Archivist with an explicit “latent engine” flag.
- Quota/capacity observation plane.
- Unify BANKAI naming.
- Enable Inbox on the harvest timer (would be a deployment decision, not this audit).
- Rename CONTINUOUS / product strings.

---

## 11. Fixes applied this audit

Only P1 correctness/epistemic defects, small and tested.

**motherclank** (branch `audit/m3-p1-stale-run-liveness-wording`):

- `recommendations.py`: `_RULES` key `STALE_RUN_ACTIVE` → `STALE_RUN`.
- `tests/test_m3.py`: scheduler mapping actually asserts active `STALE_RUN`.
- `tests/test_adr0003_bridge.py`: fixtures use `STALE_RUN`.
- `scripts/sanity_check.py`: HEAD not labelled deployed SHA.
- `liveness.py`: FINITE_SOAK does not persist CURRENT.
- `tests/test_observer_expansion.py`: FINITE_SOAK remains UNKNOWN.

**diagnostic-clank** (branch `audit/m3-p1-inbox-sha-extraction`):

- `inbox.py`: `extract_related_git_revision` — exact 40-char, skip sha256 prefixes.
- `tests/test_adr0003_contract.py`: Motherclank-shaped rec text must not set git revision; 40-char accepted; short hex rejected.
- `dashboard.py`: label “Related git SHA (40-char only)”.

**clank-architecture** (this file, branch `audit/motherclank-diagnostic-boundary-2026-08-31`).

No M5, no CVC/Standards, no harvest-timer enablement, no continuity rename.

---

## 12. Tests

Sandbox Python 3.11 venvs. pytest-qt autoload disabled for Diagnostic because `libEGL.so.1` is absent (desktop shell test not run).

| Suite | Result |
|---|---|
| motherclank `pytest` | **448 passed, 4 skipped** |
| diagnostic clank-runtime | **114 passed** |
| diagnostic clank-fleet | **72 passed, 6 skipped** (2 warnings, pre-existing) |
| diagnostic-clank app | **62 passed, 2 skipped** |
| diagnosticbench | **1 passed** |
| diagnostic repo-root `tests/` | **6 passed** |
| clank-desktop | **not run** (missing libEGL) |
| ruff/typecheck | Diagnostic ruff on inbox.py reports many **pre-existing** E702/E501 style issues; no new failures attributed to the SHA helper. Motherclank has no ruff config. pyright not run. |

Do not treat these counts as CI on GitHub. They are this sandbox’s existing suites plus the new P1 tests.

---

## 13. Git

PRs opened by this audit are listed in the chat report after push. Default branches were not merged. CVC PRs were not merged.

Inspected bases:

- motherclank `main` @ `7cee2f89`
- diagnostic-clank `diagnostic-clank-2026-08` @ `3667af02`
- clank-architecture `main` @ `e9c4a2b`

---

## 14. Durable boundary statement (≤10 lines)

Motherclank observes, synthesizes, detects, and recommends; it does not diagnose incidents, mutate Clanks, or own inventory truth. Diagnostic owns inventory, adapters, Inbox storage, Archivist incidents, and (latently) gap classification; it does not generate M3 recommendations or become the Clank domain store. Adapter HEALTHY is machinery, not recall. Checkout HEAD is not deployed SHA. Timer files are not scheduler fire. MATERIALIZATION_GAP is execution-plane, not collector regression. Source-gap and region-gap stay distinct even when first-FAIL ranks them. UNKNOWN stays UNKNOWN. M5 stays closed. Inbox write is opt-in (`--inbox-db`), not implied by host-harvest. Operator owns every action.

---

## 15. Deferred live-evidence items

These remain UNKNOWN until a host-evidenced inspection (not this audit):

1. Whether `motherclank-harvest.timer` is enabled on any host, last fire time, exit status.
2. Whether any `--inbox-db` path is actually used in operations.
3. Deployed SHA of Diagnostic, Motherclank, and each Clank vs Git HEAD vs `fleet.yaml` pins.
4. Whether OEM BANKAI timer `oem-radar-hetzner-bankai-exp-timer-01` still exists and what it last committed.
5. Whether DB-003 0/50 recall was ever closed.
6. Whether `diagnostic.db` and `motherclank_knowledge.db` both exist on a host and diverge.
7. Quota/capacity pressure on Hetzner (neither repo observes it).
8. Windows unreachable lanes (ADR-0002 carried obligation; no inference permitted).
9. ACT-001 live inventory refresh vs 2026-08-22 snapshot.
10. Whether CVC PRs #1/#9 were intended to land after this boundary freeze (out of scope).

---

## 16. Verdict

**BOUNDARY HEALTHY WITH MINOR REPAIRS**

The division of responsibility in ADR-0002/0003 is still the right split. Git implements M0–M4 as read/reason/propose. Diagnostic remains the adapter and evidence host. The leaks were naming, an unmapped anomaly key, SHA extraction, and one liveness short-circuit — not a collapse of Motherclank into Diagnostic or the reverse.

Do not open M5. Do not merge CVC. Do not treat this document as live-host truth.

---

## Appendix A — prohibited couplings (restated)

- Motherclank must not write Clank DBs, send notifications, register schedulers, or deploy.
- Diagnostic `diagnose()` must not mutate fleet state (currently does not).
- Adapters must not fabricate delivery counts or upgrade UNKNOWN capability to active.
- Inventory row existence is not verification (`ADAPTER_EVIDENCE_MATRIX.md`).
- Standards/CVC must not be assigned to fill quota/capacity or promotion blanks.
- Repo HEAD must not be persisted as deployed SHA.

## Appendix B — accepted intentional overlaps (restated)

- Diagnostic owns adapters; Motherclank consumes them unchanged.
- Diagnostic owns Inbox; Motherclank may append RECOMMENDATION rows through `save`.
- Both may *display* health-shaped data if labels keep DERIVED vs adapter vs dual-domain distinct.

## Appendix C — evidence index (inspected SHAs)

| Repo | SHA | Note |
|---|---|---|
| motherclank | `7cee2f89c4e84fdad3eb337a7eb4cbcc5dce8e04` | pre-P1 HEAD |
| diagnostic-clank | `3667af02c8dd33503ce75461ec2974d42f2f1d4c` | pre-P1 HEAD |
| clank-architecture | `e9c4a2b77f0a484171b01980469eee34971f8ee5` | audit parent |
