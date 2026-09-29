# Clank Architecture

**Before beginning material Clank development:**

1. read [AGENT_RULES.md](AGENT_RULES.md)
2. follow [DEVELOPMENT_CONTROL.md](DEVELOPMENT_CONTROL.md)
3. establish a ClankOps Mission, then exactly one attributable Session for this actor/workstream

Primary law: **NO MATERIAL CLANK DEVELOPMENT EXISTS OUTSIDE CLANKOPS.**
ClankOps records development state; it does not replace architectural,
conformance, compute/resource, or domain authority. Dated 2026-09-15
([ADR-0015](adr/0015-clankops-mandatory-development-control.md)).

## Canonical architecture

[CANONICAL_CLANK_ARCHITECTURE_v0.2.md](CANONICAL_CLANK_ARCHITECTURE_v0.2.md)
is now the binding integration amendment to v0.1. ADR-0005 ratifies the
archaeology audits and makes observer-only adapters, instance/lane identity,
evidence-bearing capabilities, baseline handover, scheduler corroboration, and
golden incidents mandatory integration gates.

[CANONICAL_CLANK_ARCHITECTURE_v0.1.md](CANONICAL_CLANK_ARCHITECTURE_v0.1.md)
is the primary normative architecture authority for future Clanks, adapters, and
Motherclank integration. The review-derived rules in
[ADR-0004](adr/0004-secondary-review-rule-integration.md) are secondary
mandatory rules: follow them where congruent with primary canon, and reconcile
any conflict explicitly in a new ADR.

The observer-plane reconciliation is recorded in
[ADR-0016](adr/0016-nas-observer-plane-and-snapshot-contract.md). **It is not
binding before platform-owner review and merge.** On that reviewed merge,
ADR-0016 becomes the dated authority for the NAS snapshot → Diagnostic-owned
adapter package → Motherclank topology, the six-method observer surface, and
the governed snapshot manifest. The live Diagnostic service remains parallel;
its deployed SHA is not an adapter-package version.

> Historical status note: ADR-0001 and ADR-0002 retained `Proposed` headings
> after entering `main`; the earlier unmerged-draft wording is not a current
> Git-topology claim. ADR-0016, only if reviewed and merged, ratifies the
> specifically listed provisions without retroactively changing those files
> or lifting the Phase 0 no-promotion controls.

Historical and governance source for the Unified Clank ecosystem: architecture
principles, agent working rules, the decision ledger, risk register, roadmap,
architecture decision records, stage specifications, investigations, reviews, and
handoff documents.

- `ARCHITECTURE.md`, `ARCHITECTURE_PRINCIPLES.md` — governing architecture
- `AGENT_RULES.md` — rules for agents implementing against this architecture
- `DEVELOPMENT_CONTROL.md` — binding ClankOps development-state procedure
- `DECISION_LEDGER.md`, `RISK_REGISTER.md`, `ROADMAP.md`
- `adr/`, `investigations/`, `reviews/`, `stage-specs/`, `handoffs/` — historical record

This repository is documentation and governance, not application code. Where
architecture files have superseded versions, prior versions are preserved rather than
deleted — git history plus explicit documentation explains the evolution.

Supporting audit artifacts:

- [ADAPTER_EVIDENCE_MATRIX.md](ADAPTER_EVIDENCE_MATRIX.md) — instance-level registration and verification contract
- [conformance/GOLDEN_INCIDENTS.md](conformance/GOLDEN_INCIDENTS.md) — archaeology-derived regression register
- [AUDIT_ACTION_REGISTER.md](AUDIT_ACTION_REGISTER.md) — owned follow-up gates and evidence horizons
- [audits/CLANK_FLEET_ARCHAEOLOGY_REPORT_2026-08-24.md](audits/CLANK_FLEET_ARCHAEOLOGY_REPORT_2026-08-24.md) — preserved evidence report
- [audits/INCIDENT_IMPACT_MAP_2026-08-23.md](audits/INCIDENT_IMPACT_MAP_2026-08-23.md) — volume-loss incident impact analysis (partial; host artifacts pending)
- [DATA_SURVIVABILITY.md](DATA_SURVIVABILITY.md) — fleet data survivability architecture (DESIGNED; ADR-0007 draft)

Current controls:

- [`NO_PROMOTION_POLICY.md`](NO_PROMOTION_POLICY.md) — proposed fleet freeze and labels
- [`adr/0001-authority-and-phase0-freeze.md`](adr/0001-authority-and-phase0-freeze.md) — authority decision
- [`diagnostic-clank/clank-fleet/inventories/fleet.yaml`](https://github.com/anil-ganti-nbc/diagnostic-clank/blob/phase0/containment/clank-fleet/inventories/fleet.yaml) — proposed canonical deployment ledger

- [ADAPTER_CONTRACT.md](ADAPTER_CONTRACT.md) - Observer Adapter Surface Contract v0.2
- [GOLDEN_INCIDENT_CORPUS.md](GOLDEN_INCIDENT_CORPUS.md) - executable incident corpus index
- [ONBOARDING.md](ONBOARDING.md) - canonical add-a-Clank procedure
