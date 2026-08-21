# Phase 0 no-promotion policy

Status: **ACTIVE — PROMOTION FROZEN**
Proposed: 2026-08-21
Scope: the 13 repositories in the canonical `diagnostic-clank` fleet inventory

No default-branch commit, local build, container tag, executable, database, or
scheduler definition may be promoted to a production host while this policy is
active. Existing deployments are `UNVERIFIED_PRODUCTION` until host evidence
identifies their exact repository SHA or artifact digest, dependency state,
scheduler owner, database, credentials owner, notification authority, backup,
and rollback target.

This freeze does not prohibit local development, tests, draft pull requests, or
read-only host inspection. It prohibits deployment, task repair on a live host,
secret rotation that changes a live consumer, release publication, merging a
remediation PR as a deployment shortcut, and claims that an uninspected runtime
is healthy or current.

## Required labels

- `PROTOTYPE`: no verified production deployment is asserted.
- `UNVERIFIED_PRODUCTION`: production is claimed or plausible, but exact runtime
  evidence is incomplete.
- `VERIFIED_PRODUCTION`: all inventory evidence is complete and independently
  checked. This label cannot be used while the fleet release gate is closed.
- `QUARANTINED`: a deployment exists but is isolated from scheduling, mutation,
  notification, or promotion pending investigation.

Unknown facts remain the literal value `UNKNOWN`; they must never be omitted or
inferred from repository documentation.

## Unfreeze authority and gate

The platform maintainer may lift the freeze only through a reviewed governance
change linking evidence that every Phase 0 exit criterion is met. At minimum:

1. all 13 repositories are present in the canonical inventory;
2. every active deployment has an owner and exact SHA or artifact digest;
3. unknown deployments are disabled or explicitly quarantined;
4. unauthenticated dashboards fail closed on non-loopback binds and mutations;
5. Semiconductor Intelligence completes two real unattended Windows runs;
6. Chinese Tech Wire secret rotation and history/artifact scanning are recorded;
7. rollback targets and verified backups exist for every active deployment.

After this policy activates and until an unfreeze review merges, all inventory entries remain
`promotion_eligible: false`.
