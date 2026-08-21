# PHASE 2 EXECUTION QUEUE — ordered by dependency, systemic risk, production blast radius (2026-08-22)

Deferred by explicit instruction (NOT in this queue): control-plane engines in diagnostic-clank, Motherclank implementation, adapter onboarding, fleet QC rollout, shared identity work. Phase 1.5 prohibition on diagnostic-clank mutation authority is honored throughout.

| # | Action | Why now (dependency / risk / blast radius) | Evidence anchor | Authorization needed |
|---|---|---|---|---|
| 1 | **Rotate FGT + CTW credentials; record scan artifacts** | Only overdue operator action from Phase 1; zero engineering dependency; closes R-004 path | D-25; CTW PHASE0_CREDENTIAL_AUDIT.md OPEN | Operator executes |
| 2 | **Merge KTW `stage4.1-reliability-repair`** (resolve one doc-prose conflict toward branch status) | GitHub main is BEHIND its own production checkout; branch carries the due-gate fix that stops a live 4×-publisher-load defect class + canonical promotion record | Manifest: /opt/korean-tech-wire @afe158e succeeding today | Operator merge authorization |
| 3 | **Merge OEM Radar `codex/bankai-config-availability`** (split-review: availability fix + benchmark + soak runner priority) | Branch already executes as enabled Hetzner infrastructure (6-hourly, succeeded 18:06 today); main without it misrepresents running code and hides the availability-transition fix | Manifest bankai timer; Ledger #2 | Operator merge authorization |
| 4 | **Merge Feature Phone PR #6 outbox** | Sole delivery path for a Clank with zero operator visibility; unblocks future deploy decision | Ledger #3 | Operator merge authorization |
| 5 | **Merge the three macOS bundle-ID one-liners** (+ CTW field-test-enablement after review) | Trivial, conflict-free, same-defect ×3; CTW restores function of already-merged launcher | Ledger #5–7,#12 | Operator merge authorization |
| 6 | **Populate fleet.yaml deployment rows** from DEPLOYMENT_TRUTH_MANIFEST.md (redacted evidence bundles: paths/SHAs/timer identities/presence flags — never secret values) | Converts 11 UNKNOWNs into reviewed facts; every later phase depends on it; write confined to diagnostic-clank inventory file (documentation, not engine work — permitted under amendment boundaries) | Manifest per-Clank table | Operator review of redactions |
| 7 | **Fix smartwatch dual-scheduler** (disable ONE lane — recommendation: keep cron lane that succeeds, disable failing system timer OR repair it first) | Live duplicate-execution hazard with a persistently-failing unit nobody can see; Law 5 specimen | Manifest smartwatch row; journal exit-code evidence | Operator host change (Phase 2, not 1.5) |
| 8 | **Delete stale smartphone second checkout** (`/home/deploy/staging/smartphone-clank` @1b0a183) after archiving its `.deployed-id` note | Provenance trap adjacent to live /opt checkout | Manifest smartphone row | Operator host change |
| 9 | **Codify Fleet Laws v1** in clank-architecture (8 laws w/ preflight amendments + deferred Law 9 note) + attach regression-fixture list | Laws are now evidence-complete; fixtures include three NEW specimens discovered by deployment truth | FLEET_LAWS_PREFLIGHT.md | Governance review/merge |
| 10 | **Conformance suite authoring** (hermetic, per-repo CI badges feeding fleet.yaml) | Only after laws merged; test-only, no runtime change | Preflight minimum-invariant column each | Engineering work, no host access |
| 11 | **SemInt heartbeat repair to deployed host** during next authorized deploy cycle (checkout @0538644 predates fix present in GitHub main) | Restores scheduler-evidence truth for an hourly-running system; small blast radius, scheduled-change discipline applies | Ledger #10 deployment-gap note | Operator deploy window |
| 12 | **Tablet launcher REWORK** (resolve D-04 README/code contradiction, then merge branch) | Unblocks field-test tooling; P0 contradiction currently blocks convergence | Ledger #11 | Engineering then merge |
| 13 | **Windows reachability restoration** → complete manifest UNKNOWNs (feature-phone task principal, oem-radar/SemInt/FGT Windows registrations) | Last unreconciled failure domain; required before any unified scheduling claims | Manifest Windows=UNKNOWN | Operator action |

## Explicitly blocked until later phases
Diagnostic-clank pause/run_now/deploy/scheduler engines · Motherclank ADR implementation · any adapter onboarding (order when unlocked: watch → smartphone → KTW → feature-phone observation plane) · QC vocabulary rollout beyond watch (blocked by FGT run-history prerequisite) · shared identity registry.

## Stop-state honored
This document is a queue, not an execution log. Nothing above has been performed in Phase 1.5.
