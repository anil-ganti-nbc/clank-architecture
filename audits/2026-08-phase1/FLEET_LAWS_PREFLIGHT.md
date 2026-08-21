# FLEET LAWS PREFLIGHT — Phase 1.5 (2026-08-22)

Re-evaluation of the eight proposed Fleet Laws against reconciled canonical + deployment evidence (DEPLOYMENT_TRUTH_MANIFEST.md, BRANCH_CONVERGENCE_LEDGER.md). No conformance suites implemented. For each law: best existing reference implementation · known violators · domain exceptions · minimum mechanically testable invariant · historical specimens that must become regression fixtures.

**Verdict up front: all eight laws survive re-evaluation. Two need wording amendments (Law 2 gains an evidence-dated rescue clause it already implied; Law 5 must distinguish scheduling authority from notification authority after the smartwatch double-scheduling discovery). One new law candidate is recorded but deferred (Law 9).**

---

## Law 1 — Initialization / no-flood
*A collector's first run against an existing DB cannot alert; genuine freshness survives initialization.*

- **Best existing reference:** watch-clank epoch lifecycle (`epoch.py` explicit start/complete_baseline) + smartphone per-source `wave1_baseline_state` epochs with parametrized zero-alert tests.
- **Known violators:** free-game-tracker (fresh DB notifies everything, retries 429 to preserve the burst — notify.py:390-393); tablet-clank (one-shot fragile baseline); oem-radar staging checkout runs pre-bankai main where baseline semantics are older.
- **Domain exceptions:** news Clanks (KTW/CTW) have no catalogue-baseline concept; their analog is "first crawl of a source ingests backlog silently" — KTW satisfies via reject-before-fetch + editorial filters; law applies to them as "first-seen ingest produces zero alerts," which they already honor (no alert path at all).
- **Minimum mechanically testable invariant:** seed store with N pre-existing entities → run collector returning those N plus 1 genuinely-new evidence-dated item → assert exactly 0 notifications for the N and ≥0 (per policy) for the new item.
- **Regression fixtures required:** FGT fresh-DB burst (notify.py 429-retry path) · watch Timex Weekender New England cluster (INCIDENT_TIMEX_BASELINE_ABSORPTION) · smartphone Samsung legacy pre-ledger rows · OEM bankai Lenovo 6,349-URL→0-delta blind soak.

## Law 2 — Observation ≠ novelty
*First local sighting is not novelty without source-dated evidence of recency.* **AMENDED WORDING:** first sighting may be labeled NEW only when (a) source-published timestamp exists within policy window, or (b) operator explicitly accepts UNCONFIRMED labeling. Ambiguity must surface, never suppress.

- **Best existing reference:** watch-clank `editorial.py` FIRST_SEEN_BY_CLANK inversion + `freshness.py::classify_baseline_product_freshness` (72h empirically-chosen window).
- **Known violators:** smartphone-clank structurally (100% catalogue-inventory sources fire `new_model` on first sight); tablet-clank (vanished-and-returned refires new_product @0.85); FGT (expired-deal reappearance = brand-new alert with erased history).
- **Domain exceptions:** KTW/CTW news domain — article published_at IS the recency evidence; law satisfied by preserving timestamps without fabrication (KTW architecture.md:32 refuses inference).
- **Minimum testable invariant:** feed a reference whose source-dated age > policy window as first-sighting → assert event class ∈ {UNCONFIRMED, BASELINE_CATCHUP} and never plain NEW.
- **Fixtures:** Timex 22-second launch cluster · Apple IN sitemap 48 false positives (tablet corrections corpus) · FGT expired-then-returning giveaway.

## Law 3 — Health honesty
*HTTP success without useful output is not healthy; blocked surfaces BLOCKED; scheduler invocation ≠ successful work.*

- **Best existing reference:** semiconductor-intelligence heartbeat separation (`last_scheduler_invocation` vs `last_successful_job_commit`, task_never_ran/heartbeat_stale states) + watch ZERO_ITEMS-degradation counter (health.py:139-153).
- **Known violators:** KTW dashboard HEALTHY-iff-ever-succeeded (dashboard.py:160 — SK hynix lie); FGT 200+0=ok forever (database.py:137-151); smartphone maintenance-alerting dormant (never exercised).
- **Deployment-truth amendment:** smartwatch systemd lane now provides a live specimen — timer fires hourly, exits 1, nobody notified because the repo has no notification authority: health dishonesty extends to *silent scheduler failure*, covered by this law's invocation clause.
- **Exceptions:** none. Sources legitimately empty by cadence (RSS gaps) map to ZERO_ITEMS-with-degradation, not healthy.
- **Minimum testable invariant:** (a) 200-response-empty-body ×N cycles → status becomes DEGRADED/BLOCKED, never HEALTHY; (b) registered task fires M times with zero successful commits → unhealthy state observable in one query.
- **Fixtures:** SK hynix HOST-BLOCKED diagnosis matrix · smartwatch-soak failing-timer journal pattern · Google consent-wall degraded state (smartphone).

## Law 4 — Explicit event capability
*emit_events/notify are explicit per-path contracts with fail-closed defaults.*

- **Best existing reference:** post-casio_multi watch contract (all pipelines accept emit_events explicitly) + smartphone eligibility allowlist fail-closed on unknown reasons.
- **Known violators:** smartwatch (transport NotImplementedError — latent capability), feature-phone (no delivery path at all), tablet (ALERTS_ENABLED=False constant — honest but absolute).
- **Exceptions:** repos with deliberately zero notification (KTW, CTW-staging, feature-phone today) satisfy trivially; law requires the *absence be explicit and documented*, which theirs is.
- **Minimum testable invariant:** for every pipeline entrypoint, assert a declared (emit_events, notify) signature exists and defaults fail-closed; unknown reason/category ⇒ no send.
- **Fixtures:** watch casio_multi silent-period incident · FGT subscription-category blackout (test_category_coverage invariant generalizes).

## Law 5 — Single environment authority *(AMENDED SCOPE)*
*Exactly one notification authority per environment AND one scheduling authority per Clank-lane; experimental runs structurally cannot reach production channels.*

Amendment reason: Phase 1.5 found smartwatch-clank under TWO schedulers for the same script (deploy-cron succeeding + system timer failing) while OEM Radar's bankai branch runs as enabled infrastructure despite being "unmerged workstream." Authority applies to schedulers, not just webhooks.

- **Best existing reference:** watch-clank (single Hetzner Discord authority, machine-local secrets, annotated-disabled legacy cron lines) + smartphone systemd-only cutover with retired daemon disabled.
- **Known violators:** smartwatch (dual live schedulers NOW); oem-radar dashboard auto_crawl sharing prod webhook authority; feature-phone three authorities (Windows task + root cron + user cron — documented but fragmented).
- **Exceptions:** deliberate multi-host isolation (feature-phone prod-vs-exp split) satisfies the law when lanes are disjoint by DB+lock+volume, as proven there.
- **Minimum testable invariant:** enumerate schedulable units per host → for each Clank-lane, assert exactly one enabled mechanism; experimental lanes reference non-production credentials set (presence-check only, never values).
- **Fixtures:** watch fcb5e91 ghost-cron incident · smartwatch 2026-08-21 dual-lane journal evidence · SemInt wrong-app installer registration.

## Law 6 — Provenance
*Every event carries run/source/deployment revision; deployments prove SHA via ledger or OCI revision.*

- **Best existing reference:** FGT deployment ledger (append-only, OCI digest, byte-identical reconciliation) + watch three-way SHA match ritual + smartwatch per-run columns.
- **Known violators:** tablet (no code-version in run rows), KTW deployed-SHA unrecorded (env-var fallback), CTW/oem-radar/SemInt staging checkouts pinned to SHAs absent from any GitHub branch tip until convergence lands.
- **Exceptions:** none.
- **Minimum testable invariant:** every persisted event row has non-null (run_id, source_id, code_revision); every deployment row in fleet.yaml carries artifact digest or exact SHA evidenced on host.
- **Fixtures:** FGT pre-cec0346 hashed-snapshot gap · SemInt d43481f claim-vs-ledger contradiction.

## Law 7 — Writer coordination
*All writers of one SQLite DB share one cross-process lock, dashboards included.*

- **Best existing reference:** watch run_lock (stale-reclaim, heartbeat) ; smartphone kernel-lock serializing systemd one-shots.
- **Known violators:** FGT `/api/run` threading.Lock bypass (webapp.py:36,212); KTW feedback POST bypasses RunLock (database.py:181-183); smartphone dashboard local_collection path unverified.
- **Exceptions:** single-writer-by-construction systems (oem-radar WAL discipline) satisfy trivially.
- **Minimum testable invariant:** static assertion that every write-path imports/acquires the canonical lock; dynamic test: concurrent writer + scheduled run → one blocks, neither corrupts.
- **Fixtures:** FGT DASHBOARD_REGRESSION "DB Eradication" purge incident.

## Law 8 — Promotion gates
*No source reaches production scheduling without soak evidence, explicit promotion record, and rollback state.*

- **Best existing reference:** korean-tech-wire written policy + per-source yield log + four dated decisions (now VERIFIED as the deployed standard too).
- **Known violators:** tablet (production-approved sources never scheduled — inverse failure: promotion without operation); smartwatch stage-c brands merged-but-undeployed with latent notify; OEM Radar staging running old main while bankai soaks operate outside any promotion record.
- **Exceptions:** operator-run diagnostic probes (tablet fixture-probes, SemInt discovery suggestions) remain outside promotion scope by design.
- **Minimum testable invariant:** every PRODUCTION-flagged source in config has (a) soak-evidence pointer, (b) promotion decision record (commit/doc), (c) rollback note; conversely every source scheduled in production appears in a promotion record.
- **Fixtures:** The Elec/ETNews promotions · LG Display CONTINUE-EXPERIMENTAL · Xiaomi KEEP_STAGING · Apple-IN retirement (fail-closed disable with history retained).

## Deferred Law 9 candidate — Deployment-convergence
*"A repository's default branch must never be behind its own production checkout for longer than one review cycle."*
Phase 1.5 made this concrete (KTW main behind production; SemInt host pre-heartbeat; CTW host 13 commits stale). Not proposed as a law yet because enforcement requires the fleet inventory machinery; recorded here so Phase 2 cannot forget it.

## Post-reconciliation changes to Phase 1 conclusions absorbed by this preflight

1. SemInt reclassified partially: Linux-unattended collection VERIFIED alive; laws apply to it as an operating system, not just a staging project.
2. OEM Radar bankai treated as operating infrastructure → Laws 1/5/8 fixtures include its live soak.
3. Smartwatch failing-timer specimen added to Law 3/5 (silent scheduler failure with zero authority to complain).
