# PHASE 2 RECOMMENDATION — Grand Clank Unification (2026-08-21 state)

Deliverable 10. Recommendation emerges from the evidence; deliberately NOT "rewrite everything" and equally NOT "build adapters now."

## Verdict

**Phase 2 should be a two-track sprint: (A) Fleet Laws + Conformance Tests, (B) Deployment-Truth and Branch-Convergence reconciliation — with control-plane engine work deferred until A+B complete.**

## Why not adapter-first

The unification architecture (diagnostic-clank) is real but can only observe fixtures; its inputs are untrustworthy until B-1/B-2 close. Wiring adapters now would encode repository-state-as-truth (R-001) and read main branches that contradict deployed reality (KTW promotions, OEM availability events). Evidence: fleet.yaml deployments:[] all UNKNOWN; five repos with stranded canonical fixes; every banner self-declaring UNVERIFIED_PRODUCTION.

## Why not remediate-everything-first

Remediation without codified laws repeats the pattern this audit found everywhere: good local fixes that don't propagate (watch's freshness classifier exists while three repos ship its failure class; oem-radar fixed install-hourly-task.cmd while SemInt regressed it byte-for-byte). The propagation graph proves laws must be written down and tested mechanically, not remembered.

## Track A — Codify the Fleet Laws (1 law-set + 1 conformance suite)

Write `FLEET_LAWS.md` in clank-architecture capturing the invariants the audit proved matter, each with a mechanical test template:

1. **Initialization law:** a collector's first run against an existing DB cannot alert (per-source baseline epochs or equivalent); genuine-freshness survives initialization (published_at/evidence-dated rescue window — watch's 72h model as reference semantics).
2. **Observation ≠ novelty law:** first local sighting labels itself UNCONFIRMED novelty unless source-dated evidence proves recency.
3. **Health honesty law:** HTTP success without useful items is not healthy after N cycles; blocked sources surface BLOCKED; scheduler invocation ≠ successful work (SemInt heartbeat separation).
4. **Explicit capability law:** emit_events/notify are explicit per-path contracts with fail-closed defaults (post-casio_multi rule).
5. **Single authority law:** exactly one notification authority per environment; experimental/field-test runs structurally cannot reach production channels; one deployment authority per Clank recorded in fleet.yaml.
6. **Provenance law:** every event carries run_id/source/deployment-revision; deployments prove SHA via ledger or OCI revision.
7. **Writer-coordination law:** all writers of a SQLite DB share one cross-process lock; dashboard paths included.
8. **Promotion-gate law:** no source reaches production scheduling without soak evidence + rollback state (KTW policy as written reference).

Deliverable: conformance test suite each repo runs in CI (hermetic, fixture-based — tablet/watch/CTW already have the blackhole-proxy pattern to copy), producing a per-repo PASS/FAIL badge consumed by fleet.yaml.

**Effort:** documentation + test templates; zero runtime changes. This directly serves Phase 1M's finding that historical failure classes are regression-tested in only 3 of 10 repos.

## Track B — Reconciliation sprints (operator-visible, mostly git/read-only-host work)

B1. **Branch convergence:** reviewed merges (no squashes) for stage4.1-reliability-repair (KTW), codex/bankai-config-availability (OEM Radar), PR #6 (feature-phone), smartphone phase0 tip, macOS bundle-id ×3; formal completion of UCP unique-function disposition → archive. 
B2. **Host evidence pass (read-only):** SSH inventory of Hetzner (+ Windows when reachable) recording: checkouts+SHAs, timers/cron entries, DB paths, webhook configs presence-not-values, backups. Writes results into fleet.yaml deployment rows. NO mutation. This is the single highest-leverage action available: converts 9 UNKNOWNs into facts and likely surfaces ghost timers (fcb5e91-class) elsewhere.
B3. **Operator actions:** credential rotations FGT+CTW (already overdue per D-25); decide auto_crawl_on_start default (oem-radar); reconcile SemInt d43481f production claim vs ledger.

## Deferred to Phase 3+ (explicitly)

- Adapter engines/authn in diagnostic-clank (after inputs trustworthy).
- Any Clank onboarding (order then: watch → smartphone → KTW → feature-phone observation plane).
- QC vocabulary rollout beyond watch (needs B8 run-history prerequisite in FGT first).
- Identity registry work (v3 non-goal correctly keeps identity domain-owned).

## Success criteria for Phase 2 exit

1. Every domain repo passes ≥Laws 1-7 conformance suite or carries an accepted, documented exception in clank-architecture.
2. fleet.yaml has ≥1 evidenced deployment row per live Clank with exact SHA/artifact digest.
3. Zero canonical fixes stranded on unmerged branches.
4. Both credential rotations recorded with scan artifacts (R-004 closure path).
5. UCP archived; ADR-0001 merged → freeze review becomes possible.

## Risk statement

If Phase 2 skips Track A and jumps to engines/adapters, the fleet will unify around smartphone-style catalogue-novelty, FGT-style flooding, and OEM-Radar-style silent absorption simultaneously — three proven failure modes — because those are today's loudest implementations. If it skips Track B, Grand Clank manages fiction. The audit shows both failure modes are one decision away; hence two tracks, one phase.
