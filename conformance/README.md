# Fleet Laws conformance suite

Hermetic pytest suite encoding the mechanical invariants of `FLEET_LAWS.md` v1.
No network, no databases, no host access. Exercises real merged fleet code
where dependency-light (korean-tech-wire scheduling, smartphone-clank alert
eligibility) and verifies Law 5/6/8 structurally against the canonical fleet
inventory in diagnostic-clank.

Run: `pytest conformance/ -q` (requires pytest + pyyaml only; sibling-repo
tests skip gracefully when their checkouts are absent).

Adoption into each Clank's own CI is the Phase 2B exit criterion.
