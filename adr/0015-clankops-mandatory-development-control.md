# ADR-0015: ClankOps as mandatory development-state control plane

Status: **ACCEPTED**
Effective: on merge of reviewed PR #5
Date: 2026-09-15
Supersedes: none
Related: [DEVELOPMENT_CONTROL.md](../DEVELOPMENT_CONTROL.md),
[AGENT_RULES.md](../AGENT_RULES.md) rule 16,
CANONICAL_CLANK_ARCHITECTURE_v0.2.md (dated pointer only)

## Context

Git history begins too late. Chat transcripts disappear. Agents change.
Abandoned work can exist before the first commit. Automatic Git observation
(Fleet Harvest / Fleet Pulse) can report branch, HEAD, and dirty state, but
lacks intent, decision, blocker, and next-action semantics. Wayward
development is currently possible: a Clank can be created or materially
changed without a ClankOps Mission.

Canonical architecture v0.1/v0.2 and AGENT_RULES 1–15 govern architecture,
observation, and conformance. They do not yet bind development-state
reporting. This ADR does not rewrite those historical texts to imply prior
adoption.

## Decision

All material future Clank development requires ClankOps reporting.

> **NO MATERIAL CLANK DEVELOPMENT EXISTS OUTSIDE CLANKOPS.**

Every new Clank and every material development tranche MUST have a ClankOps
Mission before implementation begins. Binding procedure:
[DEVELOPMENT_CONTROL.md](../DEVELOPMENT_CONTROL.md). Binding agent rule:
AGENT_RULES #16.

Tiny editorial/documentation corrections may remain outside a dedicated
Mission unless they alter architecture, runtime behaviour, or governance.

## Consequences

- Slight process overhead at the start and stop of material work.
- Dramatically improved resumability and auditability across agent switches.
- Local-only and prototype work becomes recoverable once registered.
- ClankOps remains non-authoritative over architecture, domain, conformance,
  compute/resource allocation, Git, GitHub, CI, and deployment truth.
- Automatic Harvest observations do not replace Mission / checkpoint / handoff.
- PROCESS EXIT IS NOT HANDOFF.
- Wayward work is recovered honestly (`RECONSTRUCTED` where needed), never by
  fabricating historical live observation.

## Non-decisions

This ADR does not change Motherclank observer onboarding, Fleet Laws,
canonical integration gates in v0.2 §§1–10, promotion policy, or runtime
authority. It does not complete any Mission on PR merge or CI success.
