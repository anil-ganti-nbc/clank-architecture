# AGENT_RULES

These rules bind agents working on a Clank, Motherclank, adapter, schema,
conformance suite, or related governance artifact.

1. Read `CANONICAL_CLANK_ARCHITECTURE_v0.1.md`, applicable Fleet Laws, and
   accepted ADRs before proposing or implementing architectural work.
2. Treat the canonical architecture and accepted governance as primary
   authority. Treat ADR-0004's multi-model review findings as secondary,
   mandatory rules only where congruent with that primary authority.
3. Never silently resolve a conflict by changing code, schemas, documentation,
   or wording. Record it in an ADR/decision note with the conflict, evidence,
   alternatives, compatibility impact, and migration/rollback plan.
4. Preserve historical material. Add a versioned successor, pointer, or ADR;
   do not erase earlier architecture evidence to make a new rule appear older.
5. Keep Motherclank generic: use manifests, versioned adapters, capabilities,
   schemas, and declared policies—not Clank-name conditionals or leaked domain
   structures.
6. Preserve canonical observation history and provenance through collector
   replacement. Baselines are not local crawl cursors; first seen is not novel.
7. Require authenticated, integrity-protected ingestion; explicit observation
   modes; version negotiation; and conformance evidence for a changed contract.
8. Do not infer health, maturity, triage classification, promotion permission,
   or cross-Clank identity from a convenient proxy. UNKNOWN is not healthy;
   dismissal is not classification; guessed entity equivalence is not a merge.
9. Do not auto-promote or introduce unreviewed mutation authority. Follow the
   no-promotion policy, Fleet Laws, and applicable ADR gates.
10. Turn material failures into regression fixtures and cite the evidence
    revision. Documentation-only claims of conformance or deployment are not
    sufficient.

