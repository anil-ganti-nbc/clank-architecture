# GRAND CLANK BLOCKERS — ranked list of what makes unification unsafe today (2026-08-21 state)

Deliverable 9. Each blocker: affected Clanks · severity · why it blocks unification · fix locus · remediation order.

## B-1 · Deployment truth does not exist for the fleet
- **Affected:** all 13 (worst: oem-radar, smartwatch, KTW, tablet, SemInt)
- **Severity:** P0
- **Blocks unification because:** Grand Clank cannot manage runtimes it cannot identify. fleet.yaml deployments:[] is honest — nobody can currently prove which SHA runs on Hetzner/Windows for 9 of 10 domain repos. Unifying would encode repository-state-as-deployment-truth, the exact R-001 failure.
- **Fix locus:** deployment layer + shared control plane (host evidence bundles → fleet.yaml).
- **Order:** FIRST. Everything else assumes this.

## B-2 · Canonical fixes stranded on unmerged branches
- **Affected:** korean-tech-wire (stage4.1: promotions+due-gate fix), oem-radar (codex/bankai: availability events + benchmark), feature-phone (PR #6 Discord outbox), smartphone (phase0 tip), smartwatch/CTW/KTW (macOS bundle-id ×3)
- **Severity:** P0 (KTW/OEM) / P1-P2 rest
- **Blocks because:** adapters would read main and see EXP statuses for promoted sources, missing availability semantics, absent delivery paths — wiring the wrong reality into the fleet ledger permanently.
- **Fix locus:** inside individual Clanks (reviewed merges; no squash).
- **Order:** SECOND (pure git work, zero runtime risk).

## B-3 · Baseline/flood semantics diverge catastrophically
- **Affected:** free-game-tracker (floods by design [D-16]), tablet (fragile one-shot [D-23]), OEM Radar bankai blind-absorption [D-01], smartphone Samsung legacy absorption; counter-models exist in watch/smartphone-wave1/KTW
- **Severity:** P0 when a shared runtime inherits FGT's semantics; P1 otherwise
- **Blocks because:** "add collector" is Grand Clank's most common future operation; today three different answers exist (suppress-until-baseline / flood-Discord / silently absorb). A shared scheduler must not pick one at random.
- **Fix locus:** shared runtime contract + per-Clank conformance tests (port watch's freshness classifier concept; do NOT transplant code blindly).
- **Order:** THIRD.

## B-4 · Notification authority leakage paths remain open
- **Affected:** oem-radar dashboard auto-crawl→prod webhook [D-14]; FGT webhook-in-transcript rotation OPEN [D-25]; CTW rotation OPEN; SemInt wrong-app scheduled script could send under OEM Radar identity [D-02]
- **Severity:** P0 (rotation items are operator actions already overdue)
- **Blocks because:** v3's single-notification-authority invariant cannot hold while one repo lets a browser tab fire production webhooks and two repos have unrotated exposed credentials.
- **Fix locus:** inside individual Clanks (auto_crawl default-off; rotations now), enforced later by adapter capability flags.
- **Order:** THIRD (rotations are operator actions — do them immediately regardless).

## B-5 · Scheduler authority fragmentation with no live inventory
- **Affected:** all deployed Clanks; proven ghost-timer class (watch fcb5e91); SemInt registers wrong app [D-02]; Windows unreachable since ~08-14
- **Severity:** P0 risk / P1 current
- **Blocks because:** unified scheduling over per-Clank cron/systemd/Task-Scheduler sprawl without host inventory guarantees duplicate or dead execution — both already observed historically.
- **Fix locus:** deployment layer (host evidence pass) then shared fleet control plane owns registration going forward.
- **Order:** FOURTH (after B-1 evidence exists).

## B-6 · Source-health dishonesty patterns persist in three repos
- **Affected:** KTW dashboard HEALTHY-for-blocked [D-12]; FGT 200+0=ok [D-24]; smartphone maintenance-alerting never exercised [D-26]
- **Severity:** P1
- **Blocks because:** a fleet health roll-up built on these would show green during exactly the failures that matter (proven: SK hynix died day 1 and stayed green-looking all soak).
- **Fix locus:** inside individual Clanks; contracts/delivery.py already models correct vocabulary for the adapter layer.
- **Order:** FIFTH (parallel with B-3).

## B-7 · QC/human-feedback asymmetry means no learning corpus exists
- **Affected:** smartwatch, FGT, CTW, tablet effectively zero; oem-radar designed-never-operated [QC matrix]
- **Severity:** P1
- **Blocks because:** Phase 2+ intends human QC to become fleet-level learning data; four Clanks generate unlabeled-or-nothing, and FGT's lack of run-history makes retroactive labeling impossible.
- **Fix locus:** QC layer (fleet disposition vocabulary + per-event provenance prerequisites = B-8).
- **Order:** SIXTH.

## B-8 · Event/run history absence destroys provenance retroactively
- **Affected:** free-game-tracker (snapshot-sync deletes evidence [D-24]); partially tablet (no code-version in runs)
- **Severity:** P1
- **Blocks because:** telemetry envelopes require stable lead_id + run linkage; FGT literally cannot answer "which run produced this" about its own production DB.
- **Fix locus:** inside individual Clank (add runs table before unification; migration additive).
- **Order:** SIXTH (with B-7).

## B-9 · Control-plane engines do not exist yet
- **Affected:** diagnostic-clank Fleet API mutations 501/no-authn; fencing/offline-queue/machine-capability contract-only; adapters fixture-proven only [D-32]
- **Severity:** P1 (by design Stage 0.75, but it IS a blocker for actually controlling anything)
- **Blocks because:** Grand Clank needs at minimum: authenticated read surfaces, one safe write path (pause/run_now), real-DB adapter validation. Today it can observe two fixture files.
- **Fix locus:** shared runtime/control plane (diagnostic-clank itself).
- **Order:** SEVENTH — after B-1..B-4 make its inputs trustworthy.

## B-10 · Governance labels diverge between branches/repos
- **Affected:** clank-architecture ACTIVE vs PROPOSED; diagnostic-clank default branch vs containment branch authority.status; UCP disposition incomplete [D-31]
- **Severity:** P2
- **Blocks because:** automation reading fleet.yaml gets different answers depending on ref; the freeze itself has ambiguous enforcement state.
- **Fix locus:** governance repo + reviewed merge.
- **Order:** EIGHTH (trivial but must precede unfreeze).

## B-11 · Identity-normalization collision classes documented but unfixed
- **Affected:** smartphone suffix-strip collisions (SM-F7000 class); KTW Samsung filterless acceptance pending REWORK [D-13 resurrection defect]; CTW blocked sources reduce CN coverage
- **Severity:** P2
- **Blocks because:** cross-Clank identity joins (a stated Grand Clank goal) amplify normalization collisions from local annoyances into fleet-wide identity corruption.
- **Fix locus:** inside individual Clanks first; shared identity registry explicitly REJECTED by v3 non-goals (correctly).
- **Order:** NINTH.

## Suggested remediation sequence (summary)

1. Operator actions now: credential rotations (FGT, CTW) · decide stage4.1/codex-bankai/PR#6 merges.
2. Host evidence pass (B-1/B-5) — read-only SSH/inventory, feeding fleet.yaml deployments rows.
3. Branch convergence sprint (B-2) — reviewed merges, no squashes, CI green per PR_HEADS.md discipline.
4. Flood/baseline + health-semantics conformance suite (B-3/B-6) as *tests* against each Clank before any shared runtime exists.
5. Diagnostic-clank minimal engine work (B-9): authn, pause/run_now write path, real-DB adapter validation.
6. Then, and only then, adapter onboarding in readiness order (watch → smartphone → KTW → FPC observation plane).
