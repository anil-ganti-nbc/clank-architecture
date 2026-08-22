# ADR-0003: Ratification of the Motherclank Triage Layer and Bridging M3 Recommendations into the Agent Inbox

Status: **ACCEPTED** (merged to governance after adversarial contract reconciliation and merge review; supersedes nothing)
Date: 2026-08-22
Authority basis: ADR-0001 (governance/control-plane separation), ADR-0002 (Motherclank supervisory architecture, stages M0–M4), FLEET_LAWS.md v1 (Laws 2, 3, 6; Law 9 deferred candidate), `NO_PROMOTION_POLICY.md` (ACTIVE freeze), DECISION_LEDGER entries DEF-M1.5 / M4.5-ACT / QC-SOAK-OPEN.
Evidence basis: repositories inspected 2026-08-22 at `clank-architecture@69468c3`, `diagnostic-clank@6363263`, `motherclank@7274fd3`. Implementation candidates reviewed at `diagnostic-clank@d20070c`, `motherclank@f2fdd83`.

---

## 1. Purpose — ratify existing implementation, close one gap

Motherclank M0–M4 **already exist** as a separate repository implementing ADR-0002: read-only harvesting and UNKNOWN-honest snapshot synthesis (`snapshot.py`), a deterministic versioned anomaly ledger (`anomalies.py`, `DETECTION_RULES_VERSION m2-r1`), deterministic text-only recommendations (`recommendations.py`, `RULES_VERSION m3-r1`), the Law 9 drift indicator (`drift.py`), and QC-corpus ingestion activated per ledger entry M4.5-ACT (`qc_corpus.py`, `soak.py`).

This ADR therefore **ratifies M2–M3 under formal governance review rather than authorising them from scratch**. It authorises exactly one new capability: the bridge that delivers M3 recommendations into the Agent Inbox named by ADR-0002 §2 M3. Prior to this ADR, M3 wrote only Motherclank-local Markdown reports; the Inbox delivery is the missing piece.

Ownership is unchanged from ADR-0002 §1 and is restated here as binding:

| Concern | Owner |
|---|---|
| Read-only adapter plane | Diagnostic Clank — consumed unchanged by Motherclank, never modified or owned by it |
| Snapshot synthesis, anomaly detection, recommendation generation, M4 QC ingestion | Motherclank |
| Domain truth for every Clank | each individual Clank's own SQLite store — Motherclank outputs are DERIVED, never authoritative |
| Agent Inbox storage, incidents, claims | Diagnostic Clank (`clank_runtime.knowledge.*`) |
| Disposition of recommendations | Operator, exclusively |

## 2. The Agent Inbox bridge (the one authorised addition)

M3 recommendations SHALL be ingested into the Diagnostic Clank Agent Inbox through the existing public contract (`clank_runtime.knowledge.inbox.AgentOutputInbox.save`), with exactly three enumerated contract extensions:

1. **`OutputType.RECOMMENDATION`** is added to the output-type enum. No existing type fits; `GENERAL_NOTE` would destroy filterability.
2. **Producer identity is `AgentFamily.MISC`.** No new `AgentFamily` value is added. `AgentFamily` means model/vendor family of the authoring agent; Motherclank is a deterministic in-house runtime, not a vendor family. Provenance is carried by the existing field: **`misc_source = "motherclank-m3/<RULES_VERSION>"`** — machine-parseable, satisfying Law 6 provenance for derived artifacts.
3. **A nullable `external_ref TEXT` column** is added to `agent_outputs` (schema_version '1' → '2', purely additive; v1 rows read as NULL). The bridge sets **`external_ref = recommendation_id`**, Motherclank's stable logical identity — the SHA-256 of `(rule_key, clank_id, subject_group)`, which deliberately excludes evidence content, severity, lifecycle, and rule version.

All other Inbox invariants apply unchanged and remain load-bearing: `extra="forbid"` record shape; registry validation of `primary_clank_id`; automatic git-SHA extraction into `related_git_revision`; immutability of stored raw text.

### 2.1 Dedup is content dedup, not identity

The Inbox's SHA-256 `raw_text_hash` mechanism remains **content deduplication only**: identical rendered text resolves to the canonical row. It is explicitly **not logical recommendation identity**. Logical identity across emissions is `external_ref`.

### 2.2 Version history semantics

Changed content under one `external_ref` forms an **immutable version history**: each changed emission inserts a new permanent row carrying the same `external_ref`; nothing is mutated or deleted. Canonical-version selection uses the latest persisted record under the deterministic order `(created_at ASC, output_id ASC)`; the Inbox has no monotonic insertion identity, `created_at` remains provenance metadata, and adding sequencing machinery is deliberately out of scope.

### 2.3 Identity stability invariant

`recommendation_id` stability across rule-version bumps (`m3-rN` → `m3-r(N+1)` with unchanged `rule_key`, `clank_id`, `subject_group`) is binding and enforced by test.

## 3. Governance of detectors and thresholds (ratifying what exists)

- Detection and recommendation rules are code-owned constants under explicit versions (`m2-r1`, `m3-r1`). Thresholds (e.g. `STREAK_THRESHOLD`) are not runtime-configurable and MUST NOT become so; changing a threshold means a reviewed PR bumping the rules version.
- Deterministic replay is binding: same ordered snapshots ⇒ same anomaly ledger. Wall-clock consultation in detection is prohibited.
- Every new detector type requires a historical regression specimen at introduction.
- **No detector rewrite is authorised by this ADR.**
- UNKNOWN propagation inherits ADR-0002 §3 verbatim and stays **fail-closed**: UNKNOWN evidence never proves failure; aggregation may downgrade, never upgrade.

## 4. Deployment-trail indicator status (advisory only)

The Law 9 drift indicator operates in **advisory-only mode** until deployment identity becomes mechanically authoritative. Because `NO_PROMOTION_POLICY.md` renders all deployments `UNVERIFIED_PRODUCTION` and `fleet.yaml` declares `inventory_status: INVENTORY_INCOMPLETE`, its comparisons are not authoritative deployment truth and shall not be promoted to alert-grade severity until Phase 0 exit establishes host-evidenced SHAs.

## 5. Verification and disposition — two independent dimensions

**Verification** uses the existing claims model (`ClaimVerification`, `verification_source_output_id`). Self-verification refusal is enforced on **canonical producer identity**: `AgentFamily` plus `misc_source` for MISC outputs — never AgentFamily alone. This enforcement is new implementation work shipped with this ADR; no claim-status transition API existed before it.

**Operator disposition** (ACT / DISMISS / DEFER) is a separate dimension, never mapped onto claim-verification states or `IncidentStatus`. It lives in an append-only, operator-owned disposition record keyed by `external_ref`, with UPDATE/DELETE rejected at the SQLite level by triggers; a revised decision inserts another row. Known limitation, documented honestly: operator verification provenance is not first-class representable in the current schema; operator transitions cite a source output like any other verifier.

**M4 learning join:** corpora join both dimensions so the fleet distinguishes *whether a recommendation was diagnostically correct* from *what the operator chose*. No component may mark its own recommendation verified or resolved.

## 6. Registry membership

The bridging registry seed is derived at runtime from the canonical machine-readable inventory (`fleet.yaml`, owned by diagnostic-clank per ADR-0001), selecting `classification: CLANK` rows only. Motherclank owns no fleet-membership truth; unparseable/unusable inventory fails loudly before any Inbox write; there is no fallback list.

Delivery outcome semantics: local recommendation artifacts and Agent Inbox delivery are independent outcomes; bridge failure produces an explicit stderr failure marker and nonzero exit, and must never be reported as successful delivery.

## 7. Non-goals (binding)

No fleet mutation · no notification sends · no scheduler registration or mutation · no deployment mutation · no promotion activity (the Phase 0 freeze remains ACTIVE) · no domain-Clank mutation · no automatic promotion · no auto-dispatch of repair agents · no threshold auto-tuning outside reviewed rule-version bumps · no detector rewrites · no M5 capability of any kind — M5 execution authority remains behind `M5_ENTRY_CRITERIA.md` and a future reviewed ADR per ADR-0002 §4 · no new runtime/repository boundary is asserted by this document.

## 8. Verification gates (evidenced at merge)

1. Conformance suites green at reviewed SHAs; full suites re-run post-merge (diagnostic-clank 111 passed; motherclank 103 passed, 4 skipped).
2. Round-trip property test: emitted recommendation survives Inbox save with dedup-on-identical-text, provenance intact, `external_ref` carried.
3. Schema tests: v1→v2 migration, NULL compatibility, external_ref version series, disposition append-only (SQLite-level trigger rejection), cross-producer transition enforcement.
4. Identity-stability test across `RULES_VERSION` bump.
5. Drift indicator advisory-severity-capped pending Phase 0 exit.
6. Bridge `--dry-run` writes nothing anywhere.

---

*Review trail: three adversarial passes (reconciliation against implementation reality, final contract reconciliation, merge review with live failure-mode probes) preceded this text. Candidate branches pushed and SHA-verified before governance merge.*
