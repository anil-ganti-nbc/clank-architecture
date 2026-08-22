# ADR-0002: Motherclank — Supervisory Intelligence Architecture

Status: **PROPOSED — REVIEWED DRAFT** (activates on merge; supersedes nothing)
Date: 2026-08-22
Authority basis: Phase 1 hostile audit (11 deliverables), Phase 1.5 Truth Convergence (`PHASE1_ARCHITECTURE_AMENDMENT.md`), Phase 2A `FLEET_LAWS.md` v1, Phase 2B deployment convergence evidence, Phase 2C validated read-only adapter plane (`215dd7d`).
Related: ADR-0001 (governance/control-plane separation), unified-clank-architecture-v3 (contracts heritage), `PHASE1_ARCHITECTURE_AMENDMENT.md` (Diagnostic Clank ≠ future Motherclank control plane).

---

## 1. Ownership boundaries

| Concern | Owner | Hard rule |
|---|---|---|
| Domain truth, collection, domain semantics | each individual Clank | Motherclank never becomes the source of domain truth; Clank SQLite remains authoritative |
| Diagnosis, forensic inspection, report ingestion, diagnostic knowledge | Diagnostic Clank | stays strictly read-only toward other systems; hosts the **adapter plane** Motherclank consumes |
| Fleet-level supervision, reasoning, recommendations | **Motherclank (this ADR)** | a *separate* layer with its own runtime identity; never merged into diagnostic-clank |
| Governance, invariants, ADRs, freeze authority | clank-architecture | Motherclank obeys Fleet Laws like any component; cannot amend them by action |

The adapter plane (`clank_fleet.adapters.*`, validated in Phase 2C) remains owned by Diagnostic Clank as diagnostic infrastructure. Motherclank is a **consumer** of its outputs, not its owner or successor.

## 2. Capabilities by stage

| Stage | Capability | Allowed at introduction? |
|---|---|---|
| M0 | **Observation**: consume adapter snapshots; emit timestamped, hash-chained fleet-state records | YES (read-only end-to-end) |
| M1 | **Fleet health synthesis**: cross-Clank roll-ups with UNKNOWN-honest aggregation (Law 3) | YES |
| M2 | **Anomaly detection**: deviation from recorded baselines (e.g., scheduler silence, source-health regressions, delivery-accounting divergence); detections carry evidence references | YES (detection only) |
| M3 | **Operator recommendations**: written, ranked, evidence-linked proposals filed into the Agent Inbox / governance queue | YES (text only; no execution) |
| M4 | **QC/learning ingestion**: consume disposition corpora (Watch reviews, smartphone ledger/analytics actions, KTW feedback) for fleet-level learning datasets | YES (read + derived datasets) |
| M5 | **Controlled actions**: pause/run_now/deploy/scheduler registration | **NOT NOW.** Requires: new reviewed ADR + authentication + fencing + operator authorization per action class + rollback proof + single-authority enforcement (§4). Until then Motherclank has zero mutation capability by construction |

Stage transitions M4→M5 each require their own ADR; this ADR grants nothing beyond M0–M4 read/reason/propose.

## 3. Data contracts (minimum read-only inputs)

Motherclank consumes only adapter-produced structures (already contract-versioned, `ADAPTER_CONTRACT_VERSION`). Minimum field set per Clank:

1. **Identity/provenance**: `clank_id`, `clank_version`, schema revision (alembic/migration head), observed-at timestamp, deployment SHA/digest as recorded in `fleet.yaml` (source: inventory join, not the DB).
2. **Scheduler/run health**: last run id/status/started/finished; run-kind (normal/baseline); invocation vs successful-commit pair where the system evidences both (SemInt pattern is the reference semantic).
3. **Source health**: per-source declared lifecycle (e.g., KTW EXPERIMENTAL/PRODUCTION), mapped status (ok/degraded/failed/blocked_zero/**unknown**), last attempt, last success, recency window.
4. **Events/taxonomy**: event counts by type/status; novelty-class labels where the Clank declares them (Watch FIRST_SEEN_BY_CLANK vs NEW_REFERENCE); absent lanes are `unsupported`, not zero.
5. **Delivery**: generation vs delivery accounting where persisted (smartphone webhook_deliveries/alerts); otherwise capability=false → field is UNKNOWN.
6. **QC state**: dispositions with counts and correction history presence flag (Watch full; smartphone ledger/actions; KTW freeform; others unsupported).

**UNKNOWN semantics (binding):** missing table/column/lane ⇒ literal UNKNOWN/null propagates verbatim into every synthesis; aggregation may downgrade (healthy→unknown) but NEVER upgrade (unknown→healthy, null→0). Every synthesized claim must retain: source clank_id, adapter contract version, observed_at, and the raw field provenance path. Fabricating any of {health, novelty, deployment truth} from absence is a violation of Laws 3+6 and voids the record.

## 4. Authority model (for any FUTURE M5 capability)

1. **Authentication**: named operator identities; no shared credentials; secrets machine-local per Watch convention (`~/.config/...`), never in repos/logs.
2. **Fencing**: monotonic epoch + ownership token (v3 `fallback.py` contracts already model this); a Motherclank action token is valid only while it holds current epoch AND the target Clank lane reports no conflicting live owner.
3. **Explicit operator authorization**: every action class (pause, run-now, deploy, scheduler registration) requires a pre-registered, reviewed authorization entry in clank-architecture naming permitted targets and blast radius; ad-hoc actions are impossible by construction.
4. **Rollback**: every authorized action must ship with a pre-proven inverse (the Phase 2A/2B standard: archived state, documented enable/disable command, verified restore).
5. **Single-authority enforcement**: mechanically checked by the conformance suite (one enabled scheduler/notification authority per lane per environment); Motherclank actions appear in the same inventory so duplication is detectable.
6. **Audit**: every action appends to an immutable, hash-chained ledger before execution (same discipline as FGT's deployment ledger).

## 5. Failure containment

- Motherclank's own failure must be invisible to Clanks: it holds no locks, shares no databases, and sits on no notification path.
- Missing adapter input ⇒ UNKNOWN synthesis, never interpolation; a dead adapter yields "observation stale" flags with last-good hash retained.
- Motherclank crash-looping cannot mask fleet truth because the authoritative records remain the Clanks' own DBs + fleet.yaml; Motherclank outputs are explicitly labeled DERIVED.
- No auto-retry storms: observation cadence is fixed-clock with jitter; Law 3's invocation≠commit applies to Motherclank's own scheduler evidence.

## 6. Initial onboarding

Exactly the validated Phase 2C order: **watch-clank → smartphone-clank → korean-tech-wire → feature-phone-clank (observation plane)**. Each joins when its adapter real-state validation passes (all four already do). Additional Clanks onboard only after passing the same two-layer validation (hermetic fixtures + real DB copies).

## 7. Non-goals (initial implementation)

No shared identity registry · no collector rewrites · no shared/clank database (state = append-only local records) · no automatic source promotion (KTW policy remains the human gate) · no autonomous remediation · no notification sends · no deployment mutation · no Windows/NAS reachability assumptions.

---

## Carried-forward obligations (explicit)

1. **Smartphone Law 2 novelty debt** (catalogue-inventory sources fire first-sight novelty): remains OPEN; Motherclank M2 may *surface* it as anomaly metrics but remediation belongs to smartphone-clank itself.
2. **FGT Discord webhook rotation**: AUTHORIZED, BLOCKED-ON-OPERATOR minting replacement; procedure in `PHASE2B_ROTATION_RECORD.md`. Blocks M4-quality learning data for FGT's history.
3. **Windows UNKNOWN state**: all Windows scheduler/DB facts remain UNKNOWN; no Motherclank inference permitted; closes only via operator-restored reachability.
4. **Deferred Law 9** (repo default branch must not trail production checkout > one review cycle): proposed for codification at Phase 2B-exit review; Motherclank M1 must compute the trailing-delta metric so enforcement becomes mechanical.

## Implementation plan (staged)

| Slice | Delivers | Verification gate |
|---|---|---|
| M0 | New `motherclank` runtime (own repo): scheduled read-only harvest via adapters → append-only, hash-chained JSONL fleet snapshots + generated human report | conformance suite green; snapshots reproducible from same DB copies; zero writes outside its own store |
| M1 | Synthesis layer: fleet.yaml-aware roll-ups, UNKNOWN-honest aggregator, trailing-delta metric (Law 9 feed) | property tests: unknown-upgrade impossibility; golden-fixture synthesis |
| M2 | Anomaly detectors: scheduler-silence, source-regression, delivery-divergence, drift | each detector ships with its historical specimen as regression fixture (D-06, smartwatch timer, FGT blackout classes) |
| M3 | Recommendation documents into Agent Inbox (diagnostic surface) | recommendations are files, evidence-linked; no executable side effects |
| M4 | QC corpus ingestion + derived learning datasets | dataset manifests record provenance chain; dispositions-only, no raw-secret surfaces |

## Smallest safe first slice (recommendation)

**M0 exactly as above, nothing else**: one Python package in a new `motherclank` repository; entrypoint `motherclank harvest --inventory fleet.yaml --real-state DIR`; reuses the Phase 2C adapters unchanged; output = dated JSONL snapshot (hash-chained) + one Markdown fleet report; scheduled by a single systemd user timer following the smartwatch fixed-clock precedent; rollback = disable timer, delete directory. Estimated surface: <400 LOC excluding tests. It creates supervision value (first-ever fleet-wide single view) while being structurally incapable of violating any boundary in this ADR.
