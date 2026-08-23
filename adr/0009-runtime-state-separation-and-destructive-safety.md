# ADR-0009: Runtime-State / Source-Tree Separation and Destructive Operation Safety

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0007 (survivability), ADR-0008 (liveness), Fleet Laws v1

## Context

Two operator-verified incident families share one root hazard: tooling and
operators could not tell what a resource WAS.

1. `git stash -u` run as root inside live checkouts consumed untracked
   runtime state (`logs/`) that lived accidentally inside source trees, then
   recreated it with wrong ownership (root:root vs deploy), silently killing
   three collectors for ~36 hours.
2. `docker volume rm` against pattern-inferred names destroyed two REAL
   production volumes ("staging" in a name provided zero evidence of
   disposability).

## Decision 1 — State-classification law

Every persistent resource path belongs to exactly one class:

```
SOURCE_TREE | RUNTIME_STATE | LOGS | DATABASES | BACKUPS | SECRETS
```

Rules (binding on deployment/coherence tooling and operators):

1. Runtime state MUST NOT be created as untracked content inside a source
   checkout where tree-wide git operations can consume or recreate it. Where
   legacy Clanks still do this, `git stash -u`, `git clean`, `git reset`,
   and checkout-replacement MUST NOT be executed against the checkout until
   the runtime paths are relocated or explicitly protected (.gitignore +
   ownership + path pinning).
2. Ownership continuity: files under runtime paths must keep their service
   identity across deployments. Interactive privileged redeploys MUST verify
   post-deploy ownership of runtime paths along the ACTUAL scheduled
   execution path (the incident's post-deploy check passed only because it
   did not reproduce cron's redirect).
3. Resource naming is NOT identity. The words "cleanup", "rebuild",
   "converge", "staging", "temporary", "old", "unused", "backup",
   "experimental" carry ZERO destructive authorization.

## Decision 2 — Destructive-operation contract (for future participant tooling)

Motherclank remains observer-only and implements NONE of this. Any future
tool with destructive capability MUST implement:

```
DISCOVER → RESOLVE ACTUAL IDENTITY → CLASSIFY (persistent?)
→ PROVE BACKUP/RECOVERY POINT → DISPLAY EXACT TARGET
→ EXPLICIT AUTHORISATION FOR THAT TARGET → MUTATE → VERIFY
```

Covered operations: volume/container/filesystem prune, `rm -rf` on state
paths, database replacement or DROP, volume deletion, backup deletion.
Pattern-derived target lists are forbidden; each target is resolved and
authorized individually. Guards implementing this law must NOT themselves
gain fleet write authority beyond reporting.

## Decision 3 — Violation reporting, not mass refactoring

Existing violations (runtime state inside checkouts, unnamed ownership,
label-less volumes) are IDENTIFIED AND REPORTED via the survivability
matrix and adapter evidence — remediation is per-lane reviewed work, never
an automated sweep.

## Conformance

Golden register: ROOT-STASH-RUNTIME-PATH. Mechanically checkable pieces
(backup-state vocabulary validation, expectations-registry validation) ship
with Motherclank's conformance suite. Label conventions
(`org.clank.clank_id|instance_id|lane_id|environment|data_role|epoch_id`)
are RECOMMENDED metadata, advisory to agents, authoritative to nothing.
