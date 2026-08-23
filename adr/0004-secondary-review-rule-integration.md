# ADR-0004: Integrate the multi-model review as subordinate mandatory rules

Status: ACCEPTED
Date: 2026-08-24

## Context

The recent multi-model adversarial review identified important gaps around event
expressiveness, streaming, materiality, baseline ownership, identity handover,
cross-Clank overlap, health/coverage, ingest security, backfill, high-volume
triage, feedback loops, deployment divergence, and executable hot-swap evidence.
These observations are valuable constraints, but they are not a replacement
constitution.

The existing Clank architecture and its accepted governance remain primary.
Historical material is preserved: this ADR adds interpretation and does not
delete or relabel prior records.

## Decision

The review findings are adopted as **secondary mandatory rules**. They MUST be
implemented whenever congruent with the primary canonical standard. They MUST
NOT silently override, broaden, narrow, or reinterpret primary canon. A genuine
conflict requires a new ADR with affected clauses, alternatives, evidence,
compatibility impact, and migration plan.

`CANONICAL_CLANK_ARCHITECTURE_v0.1.md` records the congruent results now:

| Review concern | Reconciliation |
|---|---|
| Envelope cannot express mode, corrections, or time semantics | Add explicit mode, correction reference, structured time, subject-schema, and evidence requirements. |
| Materiality risks domain logic in Motherclank | Make materiality declarative/versioned adapter metadata; the core applies it mechanically. |
| Baseline resets on collector replacement | Canonical history/baseline is platform-owned; local cursors remain disposable. |
| Cross-Clank collisions | No guessed global merge. Use an explicit reviewed relationship/alias extension with provenance. |
| Foreign corrections | Advisory and linked; originator ownership is never silently overwritten. |
| Streaming, push, and interactive Clanks | Capability-gated profiles, virtual-run/subscription health, and typed assistance states. |
| Six health planes lack meaning | Independent conservative planes; failed critical planes block promotion; recorded policy determines remediation. |
| Backfill and source-return ambiguity | Explicit mode semantics, recovery scopes, and no automatic novelty flood. |
| High-volume triage | A declared aggregation/sampling/rate policy is required. |
| Wire protocol/authentication and version drift | Language-neutral protocol, handshake/rejection, authenticated integrity-protected ingest. |
| Feedback/suppression loop risk | Versioned, explainable, reversible shadow evaluation with an independent loop guard. |
| Hot-swap is prose only | Recurring end-to-end replacement drill with identity continuity and rollback evidence. |

## Explicit non-overrides

This ADR does not authorize automated promotion, mutation, fleet control-plane
ownership changes, or a new global entity-resolution authority. It does not
convert a review suggestion into an implementation mandate where doing so
contradicts an accepted ADR, Fleet Law, or safety control. In particular,
cross-Clank relationships preserve provenance rather than collapsing evidence,
and health aggregation does not infer permission to act.

## Consequences

- Future agents must use the primary/secondary precedence rule in
  `AGENT_RULES.md`.
- Unresolved tensions are visible decision work, not local exceptions.
- The conformance suite should grow the listed failure cases as executable
  fixtures before production use of the relevant capability.
