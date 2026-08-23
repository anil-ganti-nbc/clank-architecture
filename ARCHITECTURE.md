# Architecture authority

The archaeology audits are ratified by
[ADR-0005](adr/0005-archaeology-ratified-integration-gates.md). The v0.2
amendment is binding at the integration boundary: all current Clank adapters
are observer-tier, runtime identity is instance/lane scoped, and scheduler or
notification authority requires corroborated evidence.

The primary normative standard is
[CANONICAL_CLANK_ARCHITECTURE_v0.1.md](CANONICAL_CLANK_ARCHITECTURE_v0.1.md).
Its primary/secondary precedence rule is governed by
[ADR-0004](adr/0004-secondary-review-rule-integration.md). This pointer does
not change the proposed operational authority boundaries in ADR-0001.

ADR-0001 proposes that this repository govern the Clank fleet without running
it, that the control-plane implementation and deployment ledger live in
`diagnostic-clank`, and that `unified-clank-platform` be superseded after a
documented unique-function disposition. None of those roles is active while
ADR-0001 remains on an unmerged draft branch.

The Phase 0 trust boundary is deliberately narrow:

- repository state is not deployment truth;
- unauthenticated HTTP services are loopback-only and read-only by default;
- schedulers, notification senders, databases, and backups require named owners;
- missing evidence is `UNKNOWN`, never silently healthy;
- no artifact is promotable while the no-promotion policy is active.

See `adr/0001-authority-and-phase0-freeze.md` for the proposed authority decision
and `NO_PROMOTION_POLICY.md` for the proposed release gate.
