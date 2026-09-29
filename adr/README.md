# Architecture Decision Records

ADRs record architecture and governance decisions without erasing the history
that led to them. The primary architecture standard is
[CANONICAL_CLANK_ARCHITECTURE_v0.1.md](../CANONICAL_CLANK_ARCHITECTURE_v0.1.md).

0004-secondary-review-rule-integration.md records the binding precedence rule
for recent multi-model review findings: apply them when congruent with primary
canon; reconcile conflicts explicitly in a new ADR.

0005-archaeology-ratified-integration-gates.md records the four audit reviews
of the Fleet Archaeology Report and adopts the v0.2 integration gates.

0015-clankops-mandatory-development-control.md (2026-09-15) makes ClankOps
the mandatory development-state plane for material future work. It does not
rewrite v0.1/v0.2 or absorb architecture/domain/runtime authority.

0016-nas-observer-plane-and-snapshot-contract.md (2026-09-29) records the
owner-reviewed ratification of the NAS snapshot → Diagnostic-owned adapter
package → Motherclank topology, the six-method Observer Adapter Surface Contract v0.2,
and governed snapshot manifest v1.0. It becomes binding **on the reviewed
merge**. Its disposition table identifies exactly which older
provisions are ratified, superseded, or retained as historical evidence;
the live Diagnostic service remains a separate parallel surface.

