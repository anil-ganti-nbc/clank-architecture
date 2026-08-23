# Canonical Clank Architecture Standard v0.1

Status: **CANONICAL architecture standard**
Adopted: 2026-08-24
Scope: all future Clanks, adapters, and Motherclank integrations

## 1. Authority and interpretation

This document is the primary normative architecture authority for the Clank
fleet. A conforming implementation, proposal, or agent instruction MUST follow
it. Existing accepted ADRs, the Fleet Laws, and explicit safety controls remain
binding in their stated scope; where two primary sources genuinely conflict, an
ADR MUST reconcile them before an implementation selects a side.

The findings recorded in ADR-0004 are secondary mandatory rules. They MUST be
applied where congruent with this standard, but MUST NOT silently amend,
reinterpret, or override it. A conflict is a decision-record event, not a local
implementation choice.

MUST requirements need an objective conformance check, a recorded exception, or
an ADR explaining why a mechanical check is infeasible.

## 2. Objective and non-goals

The fleet is a stable, generic integration plane: a correctly built Clank is
attachable through its manifest, adapter, declared capabilities, and conformance
evidence, without Motherclank-specific domain logic. This is the hot-swap
objective.

The standard does not require simultaneous migration of legacy Clanks, force
unfinished Clanks into production, or authorize production mutation. Promotion
and mutation remain subject to the Fleet Laws, `NO_PROMOTION_POLICY.md`, and
the relevant accepted ADRs.

## 3. Ownership boundaries

| Boundary | Owner | Rule |
|---|---|---|
| Domain discovery, parsing, source-specific behavior | Individual Clank | Implement behind its adapter; do not leak local structures into the core. |
| Manifests, event envelopes, findings, provenance, feedback, canonical observation history | Platform contracts | Versioned, payload-opaque where valid, and preserved across collector replacement. |
| Crawl cursors, session tokens, cookies, transient caches | Individual Clank | Disposable operational state; never the sole copy of canonical history. |
| Architecture, governance, ADRs, laws, conformance rules | This repository | Governed here; runtime truth remains in the control plane under ADR-0001. |
| Promotion and material mutation | Human authority | Never automatic. |

`checkpoint` has two meanings that MUST NOT be conflated: a local collection
cursor is Clank-local, while a novelty baseline and observation history are
canonical platform state.

## 4. Identity, manifests, and capabilities

Every Clank MUST have a stable, globally unique `clank_id`; display names are
not identity. A manifest MUST be machine-validatable and declare architecture,
manifest, adapter, and supported-version range; ownership; maturity; expected
collection profile; output types; sources/regions where applicable; and
capabilities.

Capabilities are additive and negotiated, not inferred from a Clank name.
Examples include `discovery`, `change_detection`, `detail_fetch`,
`availability`, `historical_backfill`, `replay`, `live_probe`,
`streaming`, `batch`, `correction`, and `interactive_pause`. The base
protocol MUST allow a stateless Clank: persistence/checkpoint operations are
capability-gated.

Motherclank MUST NOT contain `if clank == ...` domain logic. It MAY branch on
a declared, versioned output type or renderer capability.

## 5. Adapter and transport contract

The adapter is the language-neutral hot-swap boundary. At minimum it provides
versioned `describe`, `health`, collection or subscription intake,
normalization, and any declared state operation. The canonical wire protocol,
schema registry, negotiation handshake, major-version rejection behavior, and
ingest authentication/integrity requirements are MUSTs, not SDK conventions.

An adapter MAY be pull, batch, push, or streaming. A streaming adapter MUST
declare a virtual-run or subscription profile and report connection, lag,
back-pressure, and acknowledgement health; it is not required to pretend every
event belongs to a polling interval. A Clank requiring human interaction MUST
expose a typed pause/assistance state; no agent may invent an untracked
out-of-band control path.

Ingest MUST authenticate the Clank identity and protect event integrity.
Unknown or incompatible major protocol/schema versions MUST be rejected loudly,
preserving raw evidence where safe to do so.

## 6. Event, observation, and finding contract

Every accepted event MUST use a versioned envelope containing at least:

```text
event_id, clank_id, run_or_subscription_id, source_id,
subject { entity_type, entity_key, subject_schema_version },
event_type, payload_schema_version, payload, provenance,
observation_mode, times, confidence, health_context,
novelty, correction_ref (when applicable), evidence reference/hash
```

`times` MUST distinguish event/observed, collected, received, persisted,
source-published (when known), effective interval (when applicable), and
corrected time (when applicable). Clock validity and uncertainty MUST be
represented or rejected according to the transport contract.

Observations are not findings. The canonical path is:

```text
source -> raw evidence -> normalized observation -> identity/materiality/baseline
       -> candidate finding (when eligible) -> human triage -> feedback/history
```

The canonical store MUST preserve unknown-but-valid payload schemas and their
provenance without a new typed core column. Invalid schemas are not valid merely
because their payload can be stored.

## 7. Identity and cross-Clank relationships

An entity key is deterministic within the emitting Clank and subject schema. It
is not automatically a fleet-global identity. The platform MUST NOT silently
merge two Clanks' entities or findings based on guessed domain equivalence.

Cross-Clank identity is an explicit, versioned relationship/alias extension
with provenance, confidence, and review state. Until such a relation is
accepted, findings retain independent origin and provenance. This preserves a
domain-generic core and prevents accidental evidence loss.

An originating Clank owns its own finding. A foreign Clank may emit an advisory
correction referencing it, but Motherclank MUST surface that relation and MUST
NOT silently rewrite or adjudicate the originator's finding.

## 8. Novelty, materiality, baseline, and modes

`first_seen` is not `novel`. Novelty is computed against canonical observation
history and an explicit baseline scope. Materiality MUST be a versioned,
declarative part of the adapter/output-schema contract: field metadata and
rules tell the generic platform what is material; Motherclank does not infer
domain meaning from arbitrary payloads. Materiality-rule changes are governed
configuration changes, requiring evidence, versioning, rollback, and review.

Every event declares exactly one `observation_mode`: `live`, `baseline`,
`replay`, `backfill`, or `correction`.

| Mode | Candidate-finding rule |
|---|---|
| baseline | Establishes known state; MUST NOT create live novelty candidates. |
| live | May create an eligible candidate after identity/materiality evaluation. |
| replay | Reprocesses known evidence; MUST be idempotent and not create duplicate candidates. |
| backfill | Persists historical observations; no live candidate. A retrospective candidate requires an explicit marked policy and review. |
| correction | Preserves the original and correction linkage; never mutates history in place. |

Absence is not deletion. Return after a source gap and baseline rebuild are
explicit recovery states with a reviewed scope; neither may silently create a
novelty flood or absorb post-baseline change. Adding a source expands baseline
scope explicitly. Collector replacement MUST include an identity-continuity or
versioned alias-mapping plan before novelty is enabled.

## 9. Health, coverage, and lifecycle axes

Health MUST report independent execution, source, collection, persistence,
delivery, semantic, and coverage planes. A production-capable Clank MUST expose
an independently executable semantic probe and coverage evidence sufficient to
detect green-process/dead-parser and source-gap failures. Coverage checks
compare declared source/region/category inventory, where available, with
harvested evidence; known-entity canaries alone are insufficient.

Health aggregation is conservative: an `UNKNOWN` plane never upgrades health;
failed integrity, authentication, persistence, or semantic checks block
promotion and may quarantine intake. Severity and remediation decisions MUST
be recorded rather than inferred from one dashboard color.

Finding lifecycle, queue membership, Clank maturity, operational
readiness/health, source enabled state, and adapter compatibility/deprecation
are independent axes and MUST NOT be conflated. A quarantined
production-maturity Clank is valid and must remain representable.

## 10. Triage, feedback, and high-volume outputs

The canonical triage record captures finding identity, provenance, human
classification, reason (when provided), actor, time, and policy/model version.
Dismissal alone MUST NOT imply a classification. The core classification schema
is versioned and supports `useful`, `not_useful`, `duplicate`,
`false_positive`, and `out_of_stock`; a surface exposes only applicable
actions declared by its output capability.

Queue eligibility and ordering are declarative policies with recorded version
and inputs. Streaming or high-volume Clanks MUST declare a pre-triage policy
(aggregation, sampling, rate limit, auto-archive, or another reviewed strategy),
so individual-event human triage is never presumed feasible.

Feedback or learned suppression MUST be explainable, versioned, auditable,
reversible, and initially evaluated in shadow mode against delayed independent
human labels. A loop-guard metric MUST not depend only on the component's own
surfaced outputs. Feedback never silently mutates collector logic or launders
cross-Clank duplicates.

## 11. Deployment truth, migration, and promotion

Every running component MUST report repository, branch, source SHA, deployed
SHA, build/config/manifest versions, and deployment time. An untraceable,
dirty, or divergent revision MUST block promotion until reconciled; it is not a
mere warning.

The integration path is: manifest validation -> protocol/conformance ->
authenticated registration -> baseline -> controlled live probe -> soak ->
evidence review -> human promotion. No automatic promotion is authorized.
Experimental systems MUST be structurally prevented from writing production
canonical state except through an approved, auditable boundary.

Collector hot-swap requires a manifest comparison, compatibility negotiation,
canonical-state preservation proof, identity handover/alias proof, rollback
plan, and conformance fixtures. Motherclank must run this end-to-end drill on a
recurring schedule; prose claims of replaceability are not evidence.

## 12. Executable canon and historical learning

Each material incident becomes: incident -> architectural rule -> regression
fixture -> conformance evidence. At minimum the golden suite covers baseline
flood, identity instability, replacement handover failure, source return after
gap, field-semantic drift, coverage narrowing, duplicate laundering,
materiality/config drift, deployment divergence, clock skew, delivery failure,
and a broken Clank's isolation from the fleet.

Documentation alone is not runtime evidence. A claim of implementation,
conformance, or promotion MUST identify the test/probe/evidence artifact and
the revision it covers.

## 13. Change control

Changes to primary architecture require an ADR, compatibility assessment,
versioning plan, conformance update, and preservation of prior material.
Secondary-review rules are applied through ADR-0004's precedence rule. Where
they reveal a gap, the response is an explicit ADR or versioned future
amendment—not an undocumented reinterpretation of this standard.
