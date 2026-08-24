# Onboarding Playbook — adding a Clank to Motherclank observation

Canonical procedure. Steps are ordered; prohibitions at the end are
absolute. Target property: **zero Motherclank-core edits**.

## Procedure

1. **Inspect participant schema/native semantics** from canonical source.
   Never from a single log sample. Record tables, run/persistence model,
   delivery substrate, QC substrate, schema-version mechanism.
2. **Identify scheduler authority** — positively (crontab, systemd unit,
   operator attestation). Record cadence/grace per lane; mark
   `verification_status` honestly.
3. **Identify execution/materialization semantics** — does every successful
   invocation persist participant evidence? Declare
   `materialization_policy` (ALWAYS / WHEN_WORK_ATTEMPTED / OPTIONAL /
   UNKNOWN) from code proof.
4. **Identify continuity/history semantics** — prior incidents, epochs,
   baseline behavior; register continuity events if real history demands.
5. **Declare capabilities** via `capability_states()` using the canonical
   CapabilityState enum with evidence refs. UNKNOWN where unproven.
6. **Implement the read-only adapter** in Diagnostic Clank against the
   observed schema only. No invented table/column names. Missing store →
   UNKNOWN blocks, never creation.
7. **Provide evidence provenance** for every non-null claim (row/query,
   trace, extractor id/version, continuity event, backup manifest,
   operator attestation).
8. **Register the lane**: registry entry (+ guarded refresh-real-state line
   with operator-confirmed paths) + expectations entry.
9. **Run contract conformance**: surface validation, capability vocabulary,
   read-only mutation proofs (`tests/test_adapter_contract_v02.py`,
   `test_fgt_onboarding.py` pattern).
10. **Run the Golden Incident Corpus** and add lane-relevant fixtures.
11. **Collect real-state evidence** (operator): deployed SHA, store
    identity, scheduler authority, backup posture — fresh as_of.
12. **Soak the observer**: harvest cycles with honest UNKNOWNs; no false
    gaps/anomalies across ≥ N natural executions including at least one
    legitimate zero-work if the domain allows it.
13. **Human review** of the observer evidence.
14. Only then consider deeper integration. Observer ≠ finished participant;
    maturity axes remain independent.

## Absolute prohibitions

- guessing DB filenames, Docker volume names, or inner paths
- guessing scheduler authority or cadence without live verification
- treating zero as healthy or missing rows as failure
- treating first observation as novelty
- treating deployment/CI success as promotion
- treating a source checkout as runtime state
- inferring execution outcomes from DB absence
- collapsing UNKNOWN into NO/FALSE/0
- Motherclank core edits for anything registry/adapter/config could carry

## Field trial note — Watch expansion

If Watch Clank adds six new collectors tomorrow, Motherclank requires ZERO
changes: collectors are participant-internal; the observer sees source/
collector health rows and run records through the same adapter methods.
Motherclank changes ONLY if Watch's *evidence model* changes (a genuinely
new evidence type), which is an explicit spec-bump event by design.

## v0.3 additions (ADR-0014) — explicit agent prohibitions

- DO NOT invent run rows; expose what the participant schema actually holds.
- DO NOT treat derived timestamps as native timestamps (label the clock).
- DO NOT infer execution from scheduler configuration, or scheduler
  configuration from observed execution.
- DO NOT collapse multi-cadence lanes into an invented single cadence.
- DO NOT add participant-specific evidence semantics to Motherclank core;
  new evidence = type declaration + validator + consumer + tests.
- DO NOT turn an unknown evidence type into a false boolean or a zero.
- DO NOT make collector-count changes require Motherclank changes.
