# Golden Incident Corpus

Machine-readable source: `motherclank/src/motherclank/golden_corpus.py`
(CORPUS_SPEC_VERSION 1). This document is the human index; the corpus
module is normative for IDs/coverage, and `tests/test_golden_corpus.py`
enforces integrity + fixture existence.

Every entry carries: title · affected plane · evidence shape · required
derivations · forbidden derivations · provenance requirements · coverage ·
real origin. Status is either **executable** (fixtures run in CI) or
**registered_pending_fixture** (real origin documented; fixture requires
host evidence that does not exist — never faked).

| ID | Incident | Plane | Status |
|---|---|---|---|
| GIC-01 | first_seen != new reference | novelty | executable |
| GIC-02 | legitimate legitimate-zero source | collection health | executable |
| GIC-03 | ZERO vs STAGNANT | recency/freshness | executable |
| GIC-04 | scheduler fired, process never started | execution liveness | executable |
| GIC-05 | started, mandatory record absent past bound | execution liveness | executable |
| GIC-06 | legitimate NO_WORK_DUE | execution liveness | executable |
| GIC-07 | observer blindness | observer | executable |
| GIC-08 | restored DB keeps lineage | continuity | executable |
| GIC-09 | total loss -> explicit NEW_EPOCH | continuity/novelty | executable |
| GIC-10 | intentionally dormant lane | execution liveness | executable |
| GIC-11 | multi-cadence scheduler evidence | execution liveness | executable |
| GIC-12 | application failure after successful start | liveness/health | executable |
| GIC-13 | delivery independent of generation | delivery | executable |
| GIC-14 | schema drift / unsupported schema | persistence | executable |
| GIC-15 | duplicate/replayed evidence | observer ingestion | executable |
| GIC-16 | backup exists, integrity unverified | survivability | executable |
| GIC-17 | integrity verified, restore never tested | survivability | executable |
| GIC-18 | off-host copy in temporary scratch | survivability | executable |
| GIC-19 | qualification without rewriting history | epistemology | executable |
| GIC-20 | capability absent/unsupported/unknown tri-state | capability contract | executable |
| GIC-21 | directory sweep mistaken for inventory | membership | executable |
| GIC-22 | resource naming mistaken for identity | destructive safety | registered_pending_fixture |
| GIC-23 | runtime state consumed by tree-wide git ops | deployment safety | registered_pending_fixture |
| GIC-24 | dual scheduler authority per lane | scheduling | executable |
| GIC-25 | capability collapsed into false boolean | capability contract | executable |

Cross-plane invariants (dimensions never imply each other) are enforced by
`motherclank/tests/test_adapter_contract_v02.py::`
`test_three_dimensions_survive_every_combination` and the stage-implication
tests. Adding a new invariant = add an entry here conceptually + a test in
that file.

Promoting a new incident: real origin evidence -> corpus entry with status
registered_pending_fixture if host evidence is missing -> fixture when
evidence arrives -> flip status. Fabricating fixtures for incidents whose
root cause was UNKNOWN is prohibited.
