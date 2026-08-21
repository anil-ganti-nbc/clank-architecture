# ADR-0001: Separate governance and control-plane authority

Status: Proposed
Date: 2026-08-21

## Decision

On reviewed merge, `clank-architecture` becomes the architecture and governance
authority and `diagnostic-clank` becomes the canonical fleet control-plane
implementation and machine-readable inventory owner. `unified-clank-platform`
is proposed for supersession, subject to a reviewed unique-function
disposition; it must not be promoted independently during the freeze.

## Consequences

- Governance decisions, risks, release gates, and conformance rules live here.
- Deployment truth and fleet runtime evidence live in `diagnostic-clank`.
- Duplicate control-plane code is not extended during Phase 0.
- Production promotion is frozen by `NO_PROMOTION_POLICY.md` until the Phase 0
  gate is explicitly lifted.

## Evidence and conformance

| Requirement | Owner | Implementation | Verification | Release state |
|---|---|---|---|---|
| Complete 13-repository inventory | Control-plane maintainer | `diagnostic-clank/clank-fleet/inventories/fleet.yaml` | inventory completeness tests | Draft |
| Promotion freeze and status labels | Platform maintainer | `NO_PROMOTION_POLICY.md` | governance review | Proposed |
| Loopback-only unauthenticated dashboards | Application maintainers | repository-specific bind guards | repository tests | Draft |
| Scheduler repair | SemInt maintainer | narrow remediation PR | unit tests plus two real Windows runs | Unverified |
| Secret-safe CTW logging | CTW maintainer | centralized redaction | sentinel-key tests plus history/artifact scan | Draft |
