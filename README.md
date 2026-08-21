# Clank Architecture

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

Current controls:

- [`NO_PROMOTION_POLICY.md`](NO_PROMOTION_POLICY.md) — proposed fleet freeze and labels
- [`adr/0001-authority-and-phase0-freeze.md`](adr/0001-authority-and-phase0-freeze.md) — authority decision
- [`diagnostic-clank/clank-fleet/inventories/fleet.yaml`](https://github.com/anil-ganti-nbc/diagnostic-clank/blob/phase0/containment/clank-fleet/inventories/fleet.yaml) — proposed canonical deployment ledger
