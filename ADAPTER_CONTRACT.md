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
