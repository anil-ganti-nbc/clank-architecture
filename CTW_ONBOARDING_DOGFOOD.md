# CTW Onboarding Dogfood Scorecard

First real v0.3 onboarding. Scored strictly against
`clank-architecture/ONBOARDING.md`.

| Step | Verdict | Notes |
|---|---|---|
| 1 inspect participant schema | PASS | models.py/database.py fully mapped; no invented names needed |
| 2 identify scheduler authority | LIVE_EVIDENCE_REQUIRED | deploy-crontab hourly per prior convergence table; final live confirmation pending |
| 3 execution/materialization semantics | PASS_WITH_FRICTION | ALWAYS provable from source_runs; friction was realizing the policy is attempt-level, not cycle-level |
| 4 continuity/history semantics | PASS_WITH_FRICTION | CONTIGUOUS not provable from repo; correctly encoded unknown_or_unverified instead |
| 5 declare capabilities | PASS | canonical enum; delivery split (sent persisted vs suppressed log-only) expressed cleanly |
| 6 implement read-only adapter | PASS | ~230 LOC incl. docstring; layer-tagged health; native run rows labeled clock=native_run_row |
| 7 evidence provenance | PASS | every claim cites table/query; schema revision honestly None |
| 8 register lane | PASS | one registry data row + guarded refresh line |
| 9 contract conformance | PASS | surface validation, capability vocabulary, read-only proofs |
| 10 Golden Incident Corpus | PASS | all 38 green; zero corpus additions needed (SK hynix maps to existing classes) |
| 11 real-state evidence | LIVE_EVIDENCE_REQUIRED | operator discovery procedure issued |
| 12 soak observer | PENDING | begins after Claude deploys |
| 13 human review | PENDING | this transfer |

## Metrics

- Motherclank core files changed: **1** (`synthesis.py`, +4 generic lines:
  capability_states passthrough onto claims — participant-neutral)
- Motherclank core participant-specific lines: **0** (guard-scanned)
- Diagnostic Clank files: 1 adapter (~250 LOC)
- Registry/config/fixtures/tests: motherclank tests/test_ctw_onboarding.py;
  lane-config seed row; refresh line
- New evidence types: **0** — existing v0.3 types sufficient
- New GICs: **0**
- Bespoke vs generic LOC in adapter: ~30 bespoke mapping / ~200 shared
  contract surface

## Friction found

1. FGT registry db filename had drifted from the live-verified inner name
   (`newsroom.db`); caught during this pass because the refresh script and
   registry were cross-checked — playbook step 8 now implicitly requires
   that cross-check, worth making explicit next revision.
2. Layer-tagged health entries (`src[NEWS]`) are an adapter-side convention;
   a future spec minor may want a formal layer dimension on
   SourceHealthEntry.
