# Decision ledger

| ID | Date | Decision | Status |
|---|---|---|---|
| DEF-M1.5 | 2026-08-22 | Smartphone adapter ordered runs by UUID-string id (false-STALE; inverse false-HEALTHY risk); shared status mapper lacked fleet vocabularies (SUCCESS/PARTIAL/success/ZERO_ITEMS/BLOCKED). Fixed in diagnostic-clank 97b07ae with UUID-trap + never-upgrade regressions and real-state equality tests; discovered by Motherclank M1 first synthesis. | CLOSED |
| ADR-0002 | 2026-08-22 | Motherclank is a separate supervisory-intelligence layer (stages M0–M4 read/reason/propose; M5 actions require a future reviewed ADR with authn/fencing/authorization/rollback). Consumes the Diagnostic-Clank-owned read-only adapter plane. Initial slice M0 recommended. | Proposed — REVIEWED DRAFT |
| ADR-0001 | 2026-08-21 | Governance belongs here; the fleet control plane and inventory belong in `diagnostic-clank`; `unified-clank-platform` is proposed for supersession pending migration review. | Proposed |
| P0-FREEZE | 2026-08-21 | Freeze all production promotion until the Phase 0 exit gate is evidenced and reviewed. | Proposed; activates on merge |
