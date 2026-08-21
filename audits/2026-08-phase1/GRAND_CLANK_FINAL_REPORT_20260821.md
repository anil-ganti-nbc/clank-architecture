# GRAND CLANK PHASE 1 — FINAL HOSTILE AUDIT REPORT (2026-08-21 state; audited 2026-08-22)

## A. Executive verdict

**NO, SYSTEMIC REMEDIATION REQUIRED.**

Not because the fleet is bad — individually, several Clanks are the best-engineered scraping/intelligence systems this operator has built, and Watch Clank's repair proved the organization can fix itself. Systemically unready because:

1. **Deployment truth does not exist** (9 of 10 domain repos cannot prove what runs where; fleet.yaml deployments is honestly empty).
2. **Canonical fixes are stranded on unmerged branches** in 5+ repos while main ships known defects.
3. **The three most important semantic laws (initialization/no-flood, observation≠novelty, health honesty) are each implemented correctly somewhere and violated somewhere else** — unification today would average the worst of all three.
4. **Human QC exists in exactly one repo**, so fleet-level learning data does not exist.

"YES WITH LOCAL REMEDIATIONS" would be defensible if the defects were local. They are not: every P0/P1 class in the ledger appears in ≥3 repositories wearing different domain costumes.

## B. Fleet discovered

- Repos under anil-ganti-nbc: **23**
- Clank-relevant: **13** (matches Phase 0 inventory exactly, independently verified)
- Domain intelligence systems: **10** (watch-exempt, smartphone, smartwatch, feature-phone, tablet, KTW, CTW, OEM Radar, FGT, SemInt)
- Architecture/control-plane/governance: **3** (diagnostic-clank, unified-clank-platform, clank-architecture)
- Production-authoritative by operational evidence: **4** (watch, smartphone, FGT, feature-phone) — all self-labeled UNVERIFIED_PRODUCTION
- Experimental/soak: **4** (smartwatch, KTW, CTW, SemInt)
- Retired/supersession-pending: **1** (unified-clank-platform); Orphaned/unclear: **1** (tablet)
- Motherclank repository: **does not exist** — identity inside diagnostic-clank (knowledge store + Agent Inbox)

## C. Highest-risk findings (top 12)

1. **OEM Radar editorial recall = 0/50** on a frozen benchmark corpus; 88% SOURCE/REGION GAP; fixes+benchmark stranded on codex/bankai branch [D-01,D-15].
2. **SemInt Windows task fired 30-minutely exiting result 1 before app launch** — manual GUI runs masked total absence of unattended collection; main still ships the regressed wrong-app installer script [D-02,D-28].
3. **Deployment truth gap fleet-wide**: every banner UNVERIFIED_PRODUCTION; only watch (three-way SHA match) and FGT (append-only ledger w/ OCI digests) have forward-verifiable provenance [D-03].
4. **KTW due-gating defect quadrupled publisher request rate for 8.5 days** (~403-410 runs vs ~100 intended) — plausibly contributed to the AWS ALB host-block of its flagship production source; fix stranded on stage4.1 [D-05,D-06].
5. **KTW dashboard renders blocked source HEALTHY forever** (health iff any historical success) while its canonical promotion state exists ONLY on an unmerged branch [D-12,B-2].
6. **FGT subscription blackout incident**: entire category silently withheld from Discord for product lifetime (35 PS+ events); fixed with category coverage invariant — but fresh-DB notification flood remains possible by design and /api/run bypasses the cross-process lock [D-07,D-16,D-17].
7. **Smartphone contamination incident**: 73 junk devices entered Samsung-only prod DB via marketing-prose regex; purged + release-blocking regression tests — best-practice response, but novelty≡first-sight remains structural (100% catalogue-inventory sources) [D-10,D-11].
8. **Tablet production theater**: 3 sources "production-approved," zero scheduled executions ever; launcher branch README contradicts code (claims allowlist-only, collects any experimental source live) [D-04,D-22].
9. **Credential exposure without rotation**: FGT webhook echoed into assistant session transcript 2026-08-09 ("rotation queued but not yet done"); CTW Phase 0 credential audit OPEN [D-25].
10. **Smartwatch experimental runs can write any DB** (only guard = filename contains "experimental"); notification transport NotImplementedError — all event capability latent [D-19,D-20].
11. **Ghost scheduler class proven**: watch's obsolete fcb5e91 cron entry ran a stale image for days post-migration; SemInt registers "OEM Radar Hourly Crawl" under wrong name with space-split bug — no live fleet timer inventory exists anywhere [D-18].
12. **Control plane can observe only fixtures**: Fleet API mutations 501, no authn, fencing/offline-queue/machine-capability contract-only; clank_runtime installed nowhere despite six optional bridges [D-32,D-33].

## D. Recurring failure classes (cross-fleet)

| Class | Instances |
|---|---|
| First observation mistaken for novelty | smartphone (structural), tablet (reappearance), OEM Radar (bankai absorption), FGT (expired-deal reappearance), watch-Timex historical |
| Baseline failure | watch-Timex (fixed properly), OEM bankai blind soak, tablet one-shot fragility, smartphone Samsung legacy rows, FGT flood-opposite-pole |
| Source-health dishonesty | KTW dashboard lie, FGT 200+0=ok, smartphone dormant maintenance alerts, tablet substring classifier |
| Silent event opt-out | watch casio_multi (fixed), smartwatch NotImplementedError, feature-phone/tablet none-at-all |
| Scheduler authority fragmentation | 4 mechanisms + ghost timers + wrong-app registration + retired daemon debris |
| Deployment drift | universal banners; smartphone bare-venn-vs-image; smartwatch 11-commit drift; KTW stage4.1; feature-phone README pin |
| Identity corruption | smartphone 73-junk purge, suffix collisions; KTW Samsung filterless corpus; tablet Apple IN false positives |
| Event taxonomy dishonesty | catalogue=new_model; support-page=appearance events; preorder→in-stock silent; subscription suppression incident |
| QC asymmetry | only watch durable; oem-radar designed-never-operated; semint entity-QC strong but different axis |
| Expansion without promotion gates | counter-example KTW (best); tablet promotes-without-scheduling; smartwatch expansion merged-but-undeployed |
| Notification authority leakage | oem-radar auto-crawl dashboard; FGT/CTW rotation debt |
| SQLite writer coordination | FGT /api/run bypass, KTW feedback bypass, smartphone dashboard path unverified |
| Provenance gaps | FGT pre-cec0346 snapshots; tablet no code-version in runs; KTW env-only revision |

## E. Strongest existing implementations

- **Source promotion protocol:** korean-tech-wire (written policy, per-source yield log, PROMOTE/CONTINUE/DEFER/REWORK outcomes, rollback tooling)
- **Baselining:** watch-clank epoch lifecycle + freshness classifier (72h window empirically chosen against real catalogue data); smartphone wave1 per-source epochs close second
- **Delivery accounting:** oem-radar outbox (dedup_key idempotency, retry<5, suppressed-at-insert) — the v3 reference, though v3 misquotes its vocabulary
- **Notification authority:** smartphone fail-closed eligibility allowlist + staging segregation; watch env-scoped split editorial/health channels
- **QC:** watch dispositions w/ preserved correction history; SemInt mandatory human entity resolution structurally
- **Deployment:** FGT append-only ledger w/ OCI digests + .deployed-id; watch three-way SHA verification ritual
- **Provenance:** smartwatch per-run columns (run_uuid/app_version/config_fingerprint/git_revision); SemInt invocation≠commit heartbeat
- **Tests:** smartphone pollution regression suite (release-blocking); tablet hermetic CI (bogus proxy) + roster-freeze drift refusal; watch Hall-of-Shame specimen runs through real entrypoint
- **Experiment isolation:** feature-phone five-layer model with SHA-256 proof
- **Secret hygiene:** CTW redaction module + sentinel tests + launcher env-stripping
- **Heartbeat/scheduler evidence:** semiconductor-intelligence windows_task.py + heartbeat separation

## F. Weakest architectural areas (fleet-wide)

1. Deployment/host evidence (nobody can see production)
2. Health semantics at presentation layer (dashboards lie in 2 repos)
3. Human QC loops (absent or never operated in 9 of 10)
4. Run/event history (FGT structurally incapable; several others thin)
5. Branch hygiene (squash-landed containment destroyed review history everywhere)
6. Windows runtime reachability + Task Scheduler correctness (R-003 confirmed twice)
7. Editorial-source diversity (smartphone 100% catalogue; OEM Radar regionally blinded)

## G. Deployment drift (GitHub ≠ production reality)

See GRAND_CLANK_DEPLOYMENT_RECONCILIATION_20260821.md. Summary: smartwatch (+11 commits incl ALL Phase 0 hardening not on host), KTW (promotions exist only on branch), feature-phone (main +4 past documented deploy; expansion branch missing loopback guard yet deployed), smartphone (hardened image ≠ bare-venv reality), SemInt (commit claims production repair; ledger says nothing deployed), oem-radar (authority UNKNOWN by own admission), tablet (three unreconciled hosts of gitignored state). Watch and FGT are the only reconciled systems.

## H. Source coverage reality (populated but editorially blind)

- **OEM Radar:** 21 enabled sources, large inventories (Lenovo sitemap 6,349 URLs) → **0/50 benchmark recall**. The defining case.
- **smartphone-clank:** 126-URL sitemap inventories + 7 OEM catalogues → all catalogue-inventory; launch-news detection impossible by construction.
- **smartwatch-clank:** Garmin 4,324-page catalogue baselined; UK Samsung support 162 pages → zero delivered value ever (no transport).
- **KTW samsung_newsroom_kr:** 19,344 articles accepted, filterless → PR/CSR noise dominates; REWORK pending.
- **SemInt:** 80 sources/5,211 items imported from legacy DB → collection itself almost entirely OFF; zero organic claims created outside walkthroughs.
- **tablet:** 225 products/108 runs recorded — all state gitignored, twice-run manually, invisible to any operator.
- Genuinely delivering editorial signal today: watch-clank (proven hits incl Luke Skywalker pre-press alert), FGT giveaways lane (post-fix).

## I. Test quality (repos genuinely testing historical failure classes)

- **Genuine failure-class regression testing:** smartphone (pollution-cannot-recur incl full pipeline integration; baseline suppression parametrized; scope fail-closed invariant), watch (WatchBench specimens through production entrypoint; freshness classifier empirical tests), FGT (category coverage invariant born from incident), KTW-stage4.1 (15 scheduling/due-gate tests incl restart survival — stranded on branch), SemInt (heartbeat separation).
- **Solid-but-narrow:** tablet (43 hermetic contract tests), feature-phone (isolation proofs), CTW (sentinel security tests), oem-radar (508 test functions but zero on the recall problem that matters).
- **Dangerous gaps fleet-wide:** no new-collector-in-existing-DB end-to-end test except smartphone/watch; no deployment-drift test anywhere (impossible without host evidence); ZERO_ITEMS-as-hazard untested in FGT; scheduler duplication tested only in-process.

## J. Unification readiness

See GRAND_CLANK_UNIFICATION_READINESS_20260821.md. Verdicts: READY_FOR_ADAPTER ×4 (watch, smartphone*, KTW*, feature-phone* observation-plane), REQUIRES_LOCAL_REMEDIATION ×3 (FGT, OEM Radar, smartwatch), EXPERIMENTAL_ONLY ×3 (SemInt gate-blocked, tablet, CTW), RETIRED ×1 (UCP), control plane itself needs engines. (*conditional)

## K. New discoveries (not in prior handoffs)

1. Motherclank = diagnostic-clank knowledge store/Agent Inbox identity, NOT a missing repository.
2. Six-repo `runtime_bridge.py` propagation — Stage-1a adoption is folklore-complete: zero hard dependencies anywhere; FGT's is the most honest ("ingestion_state=UNKNOWN always").
3. Semiconductor-intelligence contains a full vendored dead copy of OEM Radar scheduled under the wrong product name by its own scripts.
4. The due-gating defect mechanism (dead source keeps fleet-due → cadence amplification) is a NEW failure class not previously named in fleet lore.
5. Quarantine-resurrection defect pattern (KTW upsert flips legacy_unverified→valid on rediscovery).
6. phase0/containment squash-landing destroyed review history in ≥7 repos simultaneously.
7. Watch Clank's Phase 9 DUPLICATE disposition rationale documents the QC-vocabulary trap (duplicates force-filed as FALSE_POSITIVE) that other repos will hit.
8. OEM Radar alert_reviews subsystem complete and empty — designed-but-unoperated human loop.
9. diagnostic-clank default branch ≠ main (diagnostic-clank-2026-08) with authority.status ACTIVE there vs PROPOSED on containment.
10. BANKAI experimental Lenovo soak proves negative-capability honestly: 6,349 URLs → 0 deltas documented as a result, not hidden.

## L. Claims disproven

1. "Motherclank repository exists somewhere" — DISPROVEN (identity inside diagnostic-clank).
2. "Smartwatch production allowlist potentially empty" — DISPROVEN as current state (4 sources allowlisted).
3. "Tablet Huawei expansion experimentation (code)" — DISPROVEN as implementation; PROVEN as parked research.
4. "CTW secrets leaked into git history/artifacts" — DISPROVEN within git horizon (test sentinels only); pre-git-host exposure UNVERIFIED; rotation still OPEN.
5. "Field-test dashboard divergence in KTW" — DISPROVEN as divergence (fully merged, then deliberately disabled on main).
6. "Feature-phone itel/lava never reached Hetzner" — DISPROVEN (user crontab + pinned checkout + isolation proof documented).
7. "unified-clank-platform contains unique functionality worth preserving" — DISPROVEN by disposition analysis (strict subset fork).
8. "Phase 0 remediation commits preserve review history" — DISPROVEN (squash topology).
9. "SemInt d43481f 'deployed to production… heartbeat confirmed'" — UNVERIFIED and CONTRADICTED by fleet ledger + later containment docs.
10. "v3 quotes OEM Radar outbox statuses EVENT_CREATED/DELIVERY_PENDING" — vocabulary does not exist in oem-radar (pending/sent/failed/suppressed/demoted).

## M. Operator decisions required (policy only)

1. **Rotate credentials now** (FGT webhook, CTW audit closure) — already overdue; not an engineering question.
2. **Merge-or-reject decisions:** KTW stage4.1, OEM codex/bankai, feature-phone PR #6, UCP archival. Engineering recommends merge for all four; the decision is yours because each changes production semantics.
3. **auto_crawl_on_start policy** for OEM Radar dashboards (default-off recommended).
4. **Freeze exit criteria confirmation:** accept Phase 0 gate list (incl "two real unattended SemInt Windows runs") as-is or amend before unfreeze review.
5. **Windows host access restoration** — required for R-003-class evidence; sessions have been locked out since ~2026-08-14.

## N. Git/output state

- Repos cloned fresh (13): `/Users/anilganti/Documents/Default Project/grand-clank-audit/<repo>` — clean working trees, no modifications, no commits, no pushes, no branches created.
- Audit deliverables written (this directory): Fleet Inventory · Architecture Map · Hostile Defect Ledger · Invariant Matrix · Source/Collector Matrix · Deployment Reconciliation · QC Capability Matrix · Unification Readiness · Blockers · Phase 2 Recommendation · this Final Report. All uncommitted local files (audit workspace is not a git repo).
- No repository was modified. No audit branches were created (per branching policy: central documentation location preferred; other repos kept read-only).

## O. Deployment statement

**Touched Hetzner: NO. NAS: NO. Windows: NO. macOS production/field-test DBs: NO. Discord: NO. Production databases: NO. Scheduler state: NO.**

All inspection was read-only against GitHub remotes and fresh local clones. No collectors, schedulers, dashboards, or notifications were run. No test messages were sent. Live source probing was performed only via documented evidence already present in the audited repositories (e.g., KTW's curl reproduction records) — no new live probes were executed by this audit.

---

*Prepared as Phase 1 of Grand Clank Unification. Companion deliverables: GRAND_CLANK_FLEET_INVENTORY_20260821.md, GRAND_CLANK_ARCHITECTURE_MAP_20260821.md, GRAND_CLANK_HOSTILE_DEFECT_LEDGER_20260821.md, GRAND_CLANK_INVARIANT_MATRIX_20260821.md, GRAND_CLANK_SOURCE_COLLECTOR_MATRIX_20260821.md, GRAND_CLANK_DEPLOYMENT_RECONCILIATION_20260821.md, GRAND_CLANK_QC_CAPABILITY_MATRIX_20260821.md, GRAND_CLANK_UNIFICATION_READINESS_20260821.md, GRAND_CLANK_BLOCKERS_20260821.md, GRAND_CLANK_PHASE2_RECOMMENDATION_20260821.md.*
