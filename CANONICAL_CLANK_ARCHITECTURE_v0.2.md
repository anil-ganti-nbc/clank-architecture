# Canonical Clank Architecture Standard v0.2

Status: **CANONICAL integration amendment to v0.1**
Adopted: 2026-08-24
Authority: ADR-0005
Effective scope: every Clank instance registered with Motherclank

This document preserves v0.1 and adds the archaeology-derived integration gates.
Where a clause here differs from v0.1, this version governs the affected
integration boundary. Existing Fleet Laws, safety controls, and accepted ADRs
remain binding.

## 1. Adapter profiles and authority

Every adapter declares exactly one profile:

| Profile | Motherclank authority | Minimum permission |
|---|---|---|
| observer | Never schedules, triggers, mutates, or sends | Read-only identity, health, baseline cursor, and candidate/evidence reads |
| participant | May be invoked by a separately registered scheduler after approval | Explicitly scoped collection participation; no notification authority by implication |
| managed | May receive approved control actions | A separate accepted ADR, authentication, fencing, authorization, rollback, and soak evidence |

All current fleet members are observer-tier. Motherclank MUST remain a passive
listener until a future ADR explicitly authorizes participant capability. An
observer adapter MUST NOT expose collection triggers as an implied default.
A dashboard, health page, or evidence read MUST NOT start a crawl.

## 2. Instance and lane identity

clank_id identifies the logical Clank family. It is not sufficient to identify
what is running. Every runtime instance MUST also declare:

- instance_id and lane_id;
- environment and maturity;
- deployed source SHA and manifest/config revisions;
- data-store identity and location class;
- scheduler authority and notification authority;
- host/environment identity;
- adapter profile and version;
- evidence snapshot time and freshness horizon.

Production, staging, experimental, retired, and replacement lanes MUST be
separate instance records even when they share a repository. Motherclank MUST
not aggregate their health, baselines, locks, outboxes, or findings without an
explicit relationship.

## 3. Capability state is evidence-bearing

A capability is not a boolean. Each declared capability has a state:

- active;
- supported_unconfigured;
- supported_undeployed;
- unsupported_by_policy;
- unsupported;
- unknown_or_unverified.

Every state MUST carry an evidence reference and observed_at time. In particular,
KTW policy-disabled delivery, CTW code-capable-but-unconfigured delivery, and
Feature Phone code-capable-but-not-deployed delivery MUST remain distinguishable.

## 4. Baseline and identity handover

The authoritative local baseline remains authoritative during observer
onboarding. Motherclank MUST NOT replace or reinterpret it without a migration
ADR.

Every observer MUST expose a durable, queryable baseline checkpoint containing
at least: baseline_id, scope/source set, identity-key scheme and version,
observation-history high-water mark, source revision, schema/config revisions,
created_at, and content hash. A baseline is a mode/state record, not a guessed
timestamp.

A collector replacement or identity-key change MUST provide a versioned
identity-alias migration record mapping predecessor keys to successor keys,
with provenance, confidence, review status, and rollback behavior. No live
candidate generation is allowed until the handover record is accepted.

Historical feedback/QC import is a feedback_backfill mode. It preserves original
actor, time, source, local record ID, policy/model version, and import provenance.
Backfilled feedback MUST NOT be counted as new Motherclank signal or silently
retrained into a collector.

## 5. Health and required observer probes

Every observer-tier adapter MUST implement authenticated, non-mutating probes:

- probe_identity(): instance, lane, deployed SHA, clank_id, adapter/profile/version, host identity;
- probe_health(): execution, source, collection, semantic, coverage, persistence, delivery, and scheduler-authority planes;
- fetch_baseline_cursor(): durable baseline_id and high-water mark;
- fetch_candidates(cursor): canonical events/evidence newer than the supplied cursor, with idempotent pagination.

A semantic zero MUST state whether it means intentional no-result, source block,
empty source, parser/extraction failure, or unknown. A scheduler health claim is
invalid unless declared authority, invocation path, and observed evidence agree.
Motherclank MUST quarantine or leave UNKNOWN any instance whose declared
scheduler/notification authority cannot be corroborated by inventory plus a
live probe.

A disabled component MUST be provably inert: no scheduled fires, no writes, no
notifications, and no hidden retry loop.

## 6. Cross-Clank entity identity

Cross-Clank entity resolution is a blocking architecture decision before any
Clank reaches participant profile. Until a future ADR defines a global entity
key/alias authority, two Clanks retain separate entities and findings. An
optional relationship may link them with provenance, confidence, and review
state; Motherclank MUST NOT silently merge, deduplicate, or overwrite either
origin.

## 7. Delivery and feedback state

The canonical delivery vocabulary is generated, pending, sent, failed,
suppressed, unsupported, and unknown. Delivery state is orthogonal to finding
generation and source health.

Human QC/feedback writes MUST identify the owning authority, actor, source
record, policy/model version, and lock/append-only evidence. An adapter MUST
not imply that Motherclank may write simply because a local review writer exists.
Observer-tier feedback is read-only until an explicit write ADR.

## 8. Evidence horizons and security

Any inventory-derived directive MUST carry an as_of/evidence horizon. A
time-bounded snapshot cannot become an eternal scheduler or safety instruction
without refresh.

Adapters exposing data beyond loopback MUST use authenticated, integrity-
protected transport and least-privilege credentials. Open secret scanning,
credential rotation, or unknown host security status is a tracked blocking
action, not a footnote.

## 9. Conformance gates

The conformance corpus MUST include the DiagnosticBench seed cases, DB-001
through DB-008, and these named incidents:

- zombie authority: a disabled timer still fires;
- authority bypass: cron invokes the pipeline outside the registered scheduler;
- first fire mistaken for cadence proof;
- directory sweep mistaken for fleet inventory;
- stale data-store artifact mistaken for production truth;
- unstable ambient host identity creating false migrations;
- observability lost after database reinitialization;
- publication time ignored in novelty/freshness;
- baseline/identity handover failure;
- cross-lane evidence leakage;
- capability state collapsed into a false boolean;
- scheduler or notification authority mismatch.

A production-integrated instance MUST pass identity, health, baseline,
candidate pagination, authn/integrity, lane isolation, scheduler corroboration,
and replay/idempotency checks. It MUST also provide owner-accepted evidence of
backup/restore and a current deployed SHA.

## 10. Phase gates

Phase 1 is observer-only. No Motherclank scheduler registration, crawl
trigger, candidate write, feedback write, notification send, or promotion is
authorized by this amendment.

Participant/managed consideration is blocked until the adapter evidence matrix,
golden incident fixtures, fresh host verification, baseline handover record,
and cross-Clank identity ADR are accepted. The Phase 0 no-promotion freeze
continues to control all production decisions.
