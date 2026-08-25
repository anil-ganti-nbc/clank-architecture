# Semiconductor Intelligence Onboarding Dogfood Scorecard

First hard v0.3 extension test: claims-and-evidence subject model.

| Step | Verdict | Notes |
|---|---|---|
| 1 participant schema inspection | PASS | claims/claim_events/provider_runs/sources/source_reputation mapped from domain/models.py |
| 2 scheduler authority | LIVE_EVIDENCE_REQUIRED | deploy-crontab + OperationalScheduler; ACT-003 invocation-path proof still OPEN -> verification_status=unverified, scheduler health UNKNOWN |
| 3 execution/materialization semantics | PASS | provider_runs persist every pass incl. zero-collection maintenance passes -> ALWAYS at pass level |
| 4 continuity semantics | PASS_WITH_FRICTION | no destructive incidents recorded; encoded unknown_or_unverified rather than presuming CONTIGUOUS |
| 5 capability declaration | PASS | canonical enum only; delivery unsupported_by_policy (no substrate mapped) |
| 6 read-only adapter | PASS | ~250 LOC; native run rows labeled clock=native_run_row |
| 7 typed evidence | ARCHITECTURE_GAP -> EXTENDED | first genuine fleet-wide extension: intelligence_assertion@1 (generic; not SI-named); ADR-0014 envelope path absorbed it with zero core branching |
| 8 register lane | PASS | registry row + lane-config seed (verification_status=unverified per ACT-003) |
| 9 conformance | PASS | surface/capability/read-only tests green |
| 10 corpus | PASS | GIC-39 added (participant-native confidence != observer truth); all 38 prior cases green |
| 11 real-state evidence | LIVE_EVIDENCE_REQUIRED | operator discovery package issued |
| 12-14 soak/review/integration | PENDING | post-deployment |

## Metrics vs CTW baseline

- Participant-specific adapter LOC: ~260 (CTW ~230)
- Motherclank core files changed: **1** (`evidence.py` seed section —
  generic type+consumer, zero participant tokens; guard-tested)
- New evidence types: **1** (`intelligence_assertion@1`, generic)
- New GICs: **1** (GIC-39)
- Motherclank participant-name occurrences in executable core: **0**
- Live-only unknowns: deployed SHA, real DB inner path, OperationalScheduler
  invocation-path proof (ACT-003), continuity verification, backup posture

## Comparison verdict

SI was harder exactly where predicted — the subject model forced the first
genuine typed-evidence extension — and the difficulty stayed contained
inside the v0.3 extension architecture. No semiconductor vocabulary entered
Motherclank core.
