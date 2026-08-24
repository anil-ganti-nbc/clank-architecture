# Clank Architecture

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

> Status: **PROPOSED governance authority.** The Phase 0 promotion freeze and
> authority decision become active only if this draft is reviewed and merged.

Historical and governance source for the Unified Clank ecosystem: architecture
principles, agent working rules, the decision ledger, risk register, roadmap,
architecture decision records, stage specifications, investigations, reviews, and
handoff documents.

- `ARCHITECTURE.md`, `ARCHITECTURE_PRINCIPLES.md` — governing architecture
- `AGENT_RULES.md` — rules for agents implementing against this architecture
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
