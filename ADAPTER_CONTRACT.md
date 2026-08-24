# Observer Adapter Surface Contract v0.2

Status: **PROPOSED — REVIEWED DRAFT** (ADR-0013)
Machine-readable source of truth: `motherclank/src/motherclank/contract.py`
(`OBSERVER_SURFACE_SPEC_VERSION = "0.2"`)

## Terminology reconciliation

| Name | Governs | Version source |
|---|---|---|
| ADAPTER_CONTRACT_VERSION ("0.1.0-v3") | shared descriptor/payload types | clank_runtime |
| **Observer Adapter Surface Contract v0.2** | which methods an adapter exposes + fail-safe rules | `contract.py` |

## Required core (all seven real adapters already conform)

`identity()` · `capabilities()` · `status()` · `health()` ·
`last_run()` (with honest `supported` flag) · `capability_states()`
(canonical CapabilityState vocabulary, evidence refs mandatory)

## Optional extensions

Discovered via `hasattr`, consumed generically when present:
`event_summary, delivery_summary, qc_summary, qc_records, qc_summary,
source_lifecycle, timeline_taxonomy, schema_revision, current_epoch,
execution_evidence, generation_summary, recent_runs, store_inventory,
eligible_count, telemetry, source_summary`.

Adding an extension is ADDITIVE to the spec (minor bump). Adding required
methods or changing fail-safe semantics is a MAJOR bump and must define a
compatibility window.

## Fail-safe rules

1. Surface validated BEFORE any probing; violations → isolated
   `FAILED_ADAPTER` block carrying machine-readable `contract_violations`.
2. Unsupported runtime-contract major → same isolation (fail-safe UNKNOWN,
   never guesses).
3. Raising methods are runtime-isolated per evidence surface; sibling
   lanes unaffected; harvest always completes.
4. Duplicate store identity across registry entries fails registry load.
5. Participant stores are never created, migrated, or mutated; missing
   stores yield UNKNOWN blocks.

## Four-probe hypothesis verdict

The historical probe_identity/probe_health/fetch_baseline_cursor/
fetch_candidates hypothesis was NOT adopted verbatim: every real adapter
already implements identity/status/health natively, while cursor/candidate
fetching exists only where participants keep queryable history (none do
today - FGT has no run table, smartwatch runs are latest-only). Forcing
four methods would have created three dishonest implementations per lane.
v0.2 instead formalizes what exists and leaves cursor/candidates as future
OPTIONAL extensions for lanes that grow replayable history.

---

# Observer Adapter Surface Contract v0.3 (P-4.3)

Spec source: `motherclank/src/motherclank/evidence.py` +
`lane_config.py`. Status: PROPOSED via ADR-0014.

## Law 1 — Typed evidence envelopes

All new participant evidence travels as an EvidenceEnvelope:
`evidence_type · evidence_version · subject · observed_at · occurred_at? ·
substrate · payload · provenance · content_hash`. Compatibility classes:
KNOWN / KNOWN_PAYLOAD_INVALID / UNSUPPORTED_MAJOR / UNKNOWN_TYPE / MALFORMED.
Unknown types and invalid payloads stay visible and auditable and produce
ZERO derived claims. Consumers register per type through the public API;
Motherclank core never learns participant names.

## Law 2 — Semantic clocks

Timestamps carry a clock identity: native_run_row, DERIVED_ACTIVITY_MAX,
scheduler_invocation, application_execution, persistence_event,
observer_observation. Cross-clock comparisons are permitted for ordering
but MUST be annotated (`cross_clock_comparison`) wherever they drive a
verdict. A derived MAX() is never presented as a native run row.

## Law 3 — Declaration vs observation vs participant evidence

Lane configuration is DECLARATION. Traces/rows are OBSERVATION or
PARTICIPANT EVIDENCE. Derivations may combine them under their proven
contracts; declarations alone never manufacture observations, and
observations never rewrite declarations.

## Law 4 — Lane configuration contract

One validated schema per lane: clank/instance/lane identity,
execution_policy, materialization_policy, scheduler_type/authority/unit,
cadence (+ multi_cadence instead of invented single cadence), grace
(per-lane), verification_status, evidence_refs, active/effective window.
Contradictory identities and impossible declarations are load-time errors.
Runtime-derived facts are never written into configuration.

## Semantic audit matrix (condensed; full detail in ADR-0014 appendix)

| Field | Meaning | Native/Derived | Clock | Primary consumer |
|---|---|---|---|---|
| last_run.finished_at | run-row completion OR derived activity MAX | per clock label | varies | M1 recency |
| last_attempt_at | fetch attempt time | native | participant | FGT/watch health |
| trace.invoked_at | scheduler fire | probe-attested | scheduler | liveness stages |
| execution_result | application outcome | attested via extractor | application | liveness NO_WORK_DUE/GAP |
| observed_at | observer saw it | observer | observer | freshness |
| occurred_at | event happened | event | event/substrate | downstream analysis |
| cadence/multi_cadence/grace | declaration only | declaration | n/a | liveness windows |
| materialization_policy | declaration only | declaration | n/a | gap gating |

## last_run disposition

`last_run()` survives as a COMPATIBILITY PROJECTION with narrowed semantics:
payload must either be a native run row or a clearly labeled derivation
(`clock` + `derived_from`). New adapters should prefer emitting typed
evidence envelopes; unlabeled timestamps are treated as clock=UNKNOWN.
