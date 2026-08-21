# Architecture authority

This repository governs the Clank fleet; it does not run it. The canonical
control-plane implementation and deployment ledger live in `diagnostic-clank`.
`unified-clank-platform` is a superseded prototype pending migration review.

The Phase 0 trust boundary is deliberately narrow:

- repository state is not deployment truth;
- unauthenticated HTTP services are loopback-only and read-only by default;
- schedulers, notification senders, databases, and backups require named owners;
- missing evidence is `UNKNOWN`, never silently healthy;
- no artifact is promotable while the no-promotion policy is active.

See `adr/0001-authority-and-phase0-freeze.md` for the authority decision and
`NO_PROMOTION_POLICY.md` for the active release gate.
