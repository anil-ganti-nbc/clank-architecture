# ADR-0005: Ratify archaeology findings as integration gates

Status: ACCEPTED
Date: 2026-08-24
Supersedes: none
Related: CANONICAL_CLANK_ARCHITECTURE_v0.1.md, ADR-0004, Fleet Laws

## Context

Four independent audit reviews examined the Fleet Archaeology Report against
Canonical Architecture v0.1. They ratified its evidence discipline and its
central conclusion—adapter-first preservation, not collector rewrite—while
identifying load-bearing mechanics that v0.1 did not yet make normative:

- the adapter contract must distinguish observer from scheduler/participant authority;
- repository identity is insufficient for split production/staging/experimental lanes;
- capability absence has policy, configuration, deployment, and verification causes;
- local baseline and feedback ownership require explicit migration semantics;
- semantic, coverage, delivery, and scheduler probes need durable contracts;
- cross-Clank entity identity remains an unresolved blocking design decision;
- the conformance corpus must promote DiagnosticBench and fleet incidents to fixtures;
- snapshot directives and open security debt need evidence horizons and owners.

The audits also noted that the archaeology report is a time-bounded inventory
assertion, not live-host proof. Its report is preserved as evidence.

## Decision

Adopt CANONICAL_CLANK_ARCHITECTURE_v0.2.md as a binding integration amendment
to v0.1. Adopt observer as the default and current profile for every Clank.
Keep Motherclank passive until a later reviewed ADR authorizes participant or
managed authority.

The adapter evidence matrix and golden-incident register are required
preconditions for any profile transition. The cross-Clank entity-resolution
design is a blocking ADR before participant tier. The Phase 0 no-promotion
freeze remains active.

## Reconciled findings

1. Instance/lane identity is added beside clank_id.
2. Scheduler and notification authority become registered, evidence-bearing
   instance facts.
3. Capability state is explicit and non-boolean.
4. Baseline and identity handover are durable, ADR-gated migration records.
5. Feedback backfill preserves provenance and cannot silently train collectors.
6. Observer probes are authenticated and non-mutating.
7. Delivery states are canonical and orthogonal to generation/health.
8. Coverage and scheduler authority are first-class health concerns.
9. Disabled components must be provably inert.
10. DiagnosticBench cases and named archaeology incidents become conformance
    fixtures.
11. Open security/deployment items require owner, status, evidence horizon, and
    refresh—not an unassigned note.

## Non-decisions

This ADR does not create a shared runtime, shared database, central entity
resolver, Motherclank scheduler, notification sender, or automatic promotion
path. It does not authorize changing any Clank collector or local database.
Those require their own reviewed decisions.

## Required follow-up

- refresh the adapter evidence matrix from live hosts;
- add golden incident fixtures to executable conformance tests;
- assign owners and horizons to credential rotation and scheduler residuals;
- file the cross-Clank entity identity ADR;
- preserve the archaeology report and its original evidence snapshot.

The owned control register is maintained in
AUDIT_ACTION_REGISTER.md. Snapshot-derived statuses are time-bounded and must
be refreshed rather than silently edited.
