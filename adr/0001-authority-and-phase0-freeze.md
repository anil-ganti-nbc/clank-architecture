# ADR-0001: Separate governance and control-plane authority

Status: Accepted for Phase 0  
Date: 2026-08-21

## Decision

`clank-architecture` is the architecture and governance authority.
`diagnostic-clank` is the canonical fleet control-plane implementation and owns
the machine-readable inventory. `unified-clank-platform` is a superseded
prototype pending a migration review for unique functionality; it is not an
authority and must not be promoted independently.

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
| Promotion freeze and status labels | Platform maintainer | `NO_PROMOTION_POLICY.md` | governance review | Active |
| Loopback-only unauthenticated dashboards | Application maintainers | repository-specific bind guards | repository tests | Draft |
| Scheduler repair | SemInt maintainer | narrow remediation PR | unit tests plus two real Windows runs | Unverified |
| Secret-safe CTW logging | CTW maintainer | centralized redaction | sentinel-key tests plus history/artifact scan | Draft |
