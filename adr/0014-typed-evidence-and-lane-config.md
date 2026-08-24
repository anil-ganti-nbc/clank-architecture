# ADR-0014: Typed Evidence, Semantic Clocks, and the Lane Config Contract

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-25
Related: ADR-0008/0011/0012, Observer Adapter Surface Contract v0.2/v0.3,
FLEET_CAPABILITY_MATRIX

## Context

v0.2 proved hot-swappable onboarding but exposed three scaling limits:
(a) `last_run` semantically overloaded native run rows, derived MAX()
timestamps, scheduler invocations and observer times behind one name;
(b) genuinely new evidence primitives still required Motherclank core
edits (`execution_result` being the latest); (c) lane expectation
configuration sprawled across ad-hoc fields without validation or
provenance discipline.

## Decision

1. **Typed EvidenceEnvelope** (motherclank `evidence.py`): participant-
   neutral, versioned, content-hashed envelopes with mandatory provenance.
   Compatibility classification: KNOWN / KNOWN_PAYLOAD_INVALID /
   UNSUPPORTED_MAJOR / UNKNOWN_TYPE / MALFORMED. Unknown types and invalid
   payloads stay visible and auditable and produce ZERO derived claims.
2. **Consumer registry**: derivation semantics register per evidence type
   through the public API. Adding a new evidence type requires: a type
   declaration, a validator, a consumer, tests - NOT edits to synthesis/
   anomalies/recommendations or participant-specific branches.
3. **Semantic clocks**: every timestamp carries its clock identity
   (native_run_row / DERIVED_ACTIVITY_MAX / scheduler_invocation /
   application_execution / persistence_event / observer_observation).
   Cross-clock comparisons that drive verdicts must be visibly annotated.
4. **`last_run` disposition**: retained as a compatibility projection with
   narrowed semantics; payloads must label their clock (`clock`,
   `derived_from`). New adapters prefer typed envelopes. Unlabeled
   timestamps are treated as clock=UNKNOWN.
5. **Lane Config contract** (`lane_config.py`): single validated schema for
   identity, execution policy, materialization policy, scheduler type/
   authority/cadence/multi-cadence/grace, verification status, evidence
   refs, active window. Contradictory identities and impossible
   declarations are load-time errors. Migration from the expectations
   registry is lossless (verified against all 10 canonical seed rows).
6. **Declaration/observation separation**: configuration can never
   manufacture observations; observations can never rewrite declarations;
   participant evidence qualifies derivations only under proven contracts.

## Conformance

GIC-26..38 in the Golden Incident Corpus (38 total entries) plus property
grids: 120-combination plane independence, scheduler×cadence×policy grid,
unknown-evidence claim-freedom, malformed-sibling isolation, collector-count
scaling, read-only mutation proofs per registered lane.

## Non-decisions

No probe deployment changes. No participant mutation. No retrofit of the
four legacy adapters beyond what already exists. Historical v0.2 evidence
remains readable; unlabeled timestamps are clock=UNKNOWN by policy, not
guessed.
