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
not by itself change operational authority boundaries.

ADR-0001 originally proposed that this repository govern the Clank fleet
without running it, that Diagnostic own control-plane/inventory contracts,
and that `unified-clank-platform` be superseded after a documented
unique-function disposition. Its text still says Proposed and refers to an
unmerged draft, although it is now in `main`. This dated historical wording
is not proof that the live Diagnostic service implements the fleet adapter
plane or that `unified-clank-platform` has been superseded.

[ADR-0016](adr/0016-nas-observer-plane-and-snapshot-contract.md), **only after
platform-owner review and merge**, is the current narrow observer-plane
decision: child state → governed read-only snapshot → versioned
Diagnostic-owned adapter package → Motherclank. It ratifies the precise
ADR-0001/0002 provisions listed there, supersedes the old unconditional
observer probe hypothesis, and leaves the live Diagnostic service parallel.
The adapter package Git SHA, artifact digest, observer surface version, and
snapshot contract version are separate facts. No Board admission or runtime
deployment follows from this authority pointer alone.

The Phase 0 trust boundary is deliberately narrow:

- repository state is not deployment truth;
- unauthenticated HTTP services are loopback-only and read-only by default;
- schedulers, notification senders, databases, and backups require named owners;
- missing evidence is `UNKNOWN`, never silently healthy;
- no artifact is promotable while the no-promotion policy is active.

See `adr/0001-authority-and-phase0-freeze.md` for the proposed authority decision
and `NO_PROMOTION_POLICY.md` for the proposed release gate.

Dated 2026-09-15 (ADR-0015): future implementation work follows
[DEVELOPMENT_CONTROL.md](DEVELOPMENT_CONTROL.md) and
[AGENT_RULES.md](AGENT_RULES.md) rule 16. That gate is development-state
control, not a change to the v0.2 integration gates or ADR-0001 authority
split.
