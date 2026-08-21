# PHASE 1 ARCHITECTURE AMENDMENT — Diagnostic Clank / Motherclank boundary correction

Status: **ACCEPTED CORRECTION to Phase 1 conclusions** (supersedes the affected Phase 1 statements; does not rewrite history — Phase 1 deliverables are preserved verbatim with SHA-256 in `audits/2026-08-phase1/`)
Date: 2026-08-22
Amends: GRAND_CLANK_FINAL_REPORT_20260821.md §J/§K, GRAND_CLANK_UNIFICATION_READINESS_20260821.md, GRAND_CLANK_BLOCKERS_20260821.md B-9, and any reading of ADR-0001 that treats diagnostic-clank as the future production control plane.

## Correction

Phase 1 observed that diagnostic-clank contains the fleet's only control-plane implementation (contracts, Fleet API shell, adapters) and its inventory declares itself `authority.control_plane_repository`. Phase 1 language occasionally collapsed **"current location of control-plane-shaped code"** into **"future Motherclank control plane."** That inference is rejected.

**Diagnostic Clank is not automatically the future Motherclank supervisory/control intelligence.**

## Preserved boundaries (until a reviewed ADR changes them)

| Concern | Owner | Notes |
|---|---|---|
| Domain truth, collection, domain semantics | each individual Clank | authoritative per-Clank SQLite/state stays domain-owned; v3 non-goals reaffirmed |
| Diagnosis, forensic inspection, report ingestion, diagnostic knowledge | Diagnostic Clank | its actual demonstrated competence in Phase 1 (report-ingestion API, diagnosticbench curriculum, Agent Inbox) |
| Fleet governance / invariants | clank-architecture | ADR process, laws, freeze authority |
| Supervisory/control intelligence ("Motherclank") | Motherclank — eventual, separate | NOT diagnostic-clank by default |

## Evidence status of Motherclank-named artifacts

`motherclank_knowledge.db`, the Agent Inbox GUI (`clank-desktop/src/clank_desktop/inbox/agent_inbox_gui.py`), and `launcher/common/preflight.py` inside diagnostic-clank prove **only the current location of Motherclank-named knowledge functionality**. They establish nothing about future production mutation authority. No artifact in the fleet grants diagnostic-clank write authority over any live Clank.

## Consequential prohibitions for Phase 1.5 (and until superseding ADR)

Diagnostic Clank must NOT receive, during Phase 1.5:
- pause / run_now / deployment mutation routes
- scheduler registration machinery
- autonomous remediation logic
- production writes of any kind
- control-plane engines beyond read-only diagnosis

This extends Phase 1 finding D-32 ("control plane can observe only") from an observation into a deliberate constraint.

## Disposition of affected Phase 1 text

- Blockers B-9 ("control-plane engines do not exist yet") is re-scoped: engine-building is no longer the default Phase 2 path for diagnostic-clank; it becomes one option before a Motherclank architecture ADR.
- Unification readiness row for diagnostic-clank ("READY_FOR_ADAPTER as the control plane itself") is amended to: READY_FOR_DIAGNOSTIC_INTEGRATION; control-role PENDING MOTHERCLANK ADR.
- All other Phase 1 findings are unaffected.

## Required follow-on (recorded, not scheduled)

A reviewed ADR (clank-architecture) must eventually define: Motherclank's runtime identity, its authority boundaries versus individual Clanks and Diagnostic Clank, and the migration path (if any) for existing `motherclank_knowledge.db`/Agent-Inbox artifacts. Until merged, every prohibition above stands.
