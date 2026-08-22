# QC SOAK — pre-soak maturity/promotion verification (addendum compliance)

Date: 2026-08-22 · Method: read-only repo + host evidence. **No host, schedule, database, collector, promotion or soak configuration was changed.**

## Two-axes declaration (binding for the entire soak)

- **Axis A — Clank maturity/soak state:** owned by each Clank's own promotion/validation process. Motherclank observes and reports only.
- **Axis B — Motherclank QC/M5 readiness:** measures ONLY whether sufficient trustworthy human-QC evidence exists for a future learning experiment.
- Axis B passing **never** promotes a Clank, ends a development soak, or alters deployment status. Soak completion is an evidence checkpoint, not a promotion gate. No Clank has a terminal DEVELOPED/COMPLETE state; PRODUCTION means a defined deployment is authorized for its documented role with applicable promotion evidence — never "feature-complete".

## Per-Clank maturity/promotion state (Axis A, verified)

| Clank | Authoritative state (evidence) | Live soak activity (Hetzner, read-only) |
|---|---|---|
| korean-tech-wire | Development/validation soak. Sources.yaml: SK hynix + The Elec + ETNews **PRODUCTION** (on soak evidence, per promotion-policy.md); Samsung Newsroom KR + LG Display **EXPERIMENTAL**; repo banner: promotion frozen / UNVERIFIED_PRODUCTION | soak timer firing (DB mtime 09:07:59 UTC today); stage4.1 deployed checkout converged to main 262c36d |
| smartphone-clank | UNVERIFIED_PRODUCTION banner; wave-1 scope gates active (WAVE1_PRODUCTION_SCOPE; KEEP_STAGING policy for uncanaried OEMs); Xiaomi held in staging | 8 systemd timers firing today (google/nothing/oneplus/samsung last fires 09:06–09:12 UTC); 181+ metric rows since Aug-19; last metric 09:12 UTC |
| smartwatch-clank | **Phase 0: UNVERIFIED_PRODUCTION — promotion frozen** (README banner); Experimental/under-construction; production allowlist exists (4 Samsung lanes) but notifications unimplemented; deployed d987b66 detached | deploy-cron lane every 2h at :50 (succeeding; systemd twin retired in Phase 2A) |
| feature-phone-clank | hmd-nokia promoted 2026-08-09 after Stage-2.1 hardening (8/8 criteria, documented); itel/lava explicitly experimental on separate checkout/DB/crontab; Phase 0 banner UNVERIFIED_PRODUCTION | prod cron 4×daily + experimental user-cron lanes (lava log for 2026-08-22 present) |

**Conclusion:** all four remain **development/soak systems**. None is promoted to production-complete by this verification; their present status is preserved. Watch-clank remains the exempt control specimen (production-authoritative per its own HANDOFF evidence, outside this addendum's four).

## Soak lifecycle note (adopted)

Each Clank's soak ends in an evidence-backed decision made by its own process: continue unchanged / remediate / extend / new development iteration / consider promotion. Motherclank may observe and report this lifecycle; it does not own or influence it.
