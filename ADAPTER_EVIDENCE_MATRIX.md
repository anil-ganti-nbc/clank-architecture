# Adapter Evidence Matrix — v0.2 registration contract

Status: **Schema and snapshot seed; not live verification**
Snapshot horizon: 2026-08-22 fleet inventory
Authority: ADR-0005

Motherclank must not treat a row as verified merely because a repository or
deployment row exists. Each row requires a live probe, evidence timestamp, and
operator/source reference before any profile transition.

| Logical Clank | Instance/lane from snapshot | Environment | Deployed SHA | Adapter/profile | Data-store identity | Scheduler authority | Notification authority | Verification |
|---|---|---|---|---|---|---|---|---|
| watch-clank | watch-hetzner-user-timers-01 | production | f0b327a | Phase 2C observer | host path UNKNOWN | watch-hetzner-scheduler-f0b327a | watch-discord-editorial-and-health | snapshot_only |
| smartphone-clank | smartphone-hetzner-opt-timers-01 | production | b8b8988 | Phase 2C observer | /opt/smartphone-clank/data | smartphone-hetzner-source-timers-b8b89885 | smartphone-discord-webhook | snapshot_only |
| smartwatch-clank | smartwatch-hetzner-cron-lane-01 | staging | d987b66 | observer required | /home/deploy/.../var | smartwatch-cron-lane-d987b66 | NONE implemented | snapshot_only |
| korean-tech-wire | ktw-hetzner-soak-timer-01 | staging | 262c36d | Phase 2C observer | /opt/korean-tech-wire/var | ktw-soak-timer-262c36d | NONE by policy | snapshot_only |
| feature-phone-clank | fpc-hetzner-prod-cron-01 | production | c749df3 | Phase 2C observer | Docker named volume | fpc-prod-cron-c749df3 | NONE on deployed revision | snapshot_only |
| feature-phone-clank | fpc-hetzner-experimental-cron-01 | experimental | 49eab25 | observer required | separate experimental volume | fpc-exp-cron-49eab25 | NONE | snapshot_only |
| tablet-clank | tablet-hetzner-idle-checkout-01 | experimental | 1d3509b | not onboarded | var/tablet_clank.db | NONE | NONE implemented | snapshot_only |
| chinese-tech-wire | ctw-hetzner-hourly-cron-01 | staging | c1b3a41 | observer required | data/ctw.db | ctw-hourly-cron-c1b3a41 | NONE/no host env | snapshot_only |
| oem-radar | oem-radar-hetzner-staging-cron-01 | staging | 410313b | Phase 2C observer | data/ WAL | oem-staging-cron-410313b | oem-discord-webhook | snapshot_only |
| oem-radar | oem-radar-hetzner-bankai-exp-timer-01 | experimental | 31fc46b | observer required | separate experimental store | oem-bankai-exp-timer-31fc46b | NONE experimental | snapshot_only |
| semiconductor-intelligence | semint-hetzner-hourly-cron-01 | staging | 9dbf06d | observer required | semintel_staging_data | semint-hourly-cron-0538644 | NONE found | snapshot_only |
| free-game-tracker | fgt-hetzner-hourly-cron-01 | production | cec0346 | observer required | container volume | fgt-hourly-cron-cec0346 | fgt-discord-webhook | snapshot_only |

Required additions for each refreshed row: lane_id, host identity, manifest/config
revision, adapter version, baseline_id, identity-key version, data-store hash or
stable path class, last successful semantic probe, last scheduler invocation,
last backup/restore proof, capability states with evidence refs, and evidence
expiry time.
