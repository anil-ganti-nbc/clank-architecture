# ADR-0012: Application-Result Attestation for Scheduler Traces

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0008 (liveness), ADR-0011 (no-work semantics), Canonical v0.2 §5

## Context

P-4.1 gave Motherclank full consumer semantics for `execution_result`
(`completed | no_work_due | failed`) but live verification found **0 of 19**
real scheduler traces carried one: the producer plane could not attest what
an application actually did. Meanwhile OEM Radar legitimately completes
hourly executions with zero due sources and writes no participant run
record - so without attestation those executions remain honestly UNKNOWN,
and inferring from DB absence would fabricate gaps.

## Decision

### 1. Extractors live in the adapter plane, never Motherclank core

```
scheduler trace collector (probe)
    ↓ invocation output (bounded excerpts only, never whole logs)
application-result extractor  (Diagnostic Clank; clank-specific)
    ↓ canonical execution_result + execution_detail + extractor provenance
scheduler trace JSONL
    ↓ generic P-4.1 consumer (Motherclank)
```

Motherclank contains zero participant-output vocabulary. An architecture
test enforces this at the source level.

### 2. Extraction requires a PROVEN participant contract

`oem-radar/done-line@1` is the first instance: canonical OEM Radar source
shows the `done:` line prints only after `execute_crawl` returns normally
(config loaded, lock acquired, due-gating executed, due sources attempted,
outbox drained), and `sources=len(stats)` counts only actually-run sources
(due-gated skips are excluded). Therefore:

- `done: N source(s) crawled, N=0` → `no_work_due`
- `done: N>0` → `completed` (cycle completion ONLY; per-source success
  stays operational-plane evidence in crawler_runs)
- exit code 2 = LockError = by-design contention → deliberately UNKNOWN,
  never failed
- anything else → UNKNOWN

No other Clank has a proven contract yet; none gets an extractor until its
code path is traced.

### 3. Invocation identity and append-only deduplication

`invocation_key = sha256(clank_id|instance_id|lane_id|scheduler_type|
unit_or_job|invoked_at)`. Probe reruns that re-observe the same fire are
collapsed in the CONSUMER view: richest evidence wins (attested result >
process facts > bare fire; newer discovery breaks ties), superseded trace
ids surface as loader warnings, and nothing on disk is rewritten.

### 4. Orthogonal dimensions restated

Scheduler observation, process-start observation, application-result
observation, participant persistence, operational health, and continuity
remain independent evidence planes. Attestation adds positive evidence to
one plane; it never upgrades or downgrades the others.

## Conformance

Goldens P42-G1..G10 (`motherclank` tests/test_p42_attestation.py) plus
extractor unit tests on the Diagnostic Clank side. The hot-swap guard now
also asserts Motherclank core contains no participant output vocabulary
(`source(s) crawled` etc.) anywhere executable.

## Non-decisions

No probe deployment (host-side work). No fleet-wide extractor rollout -
each Clank needs its own traced contract first. FGT needs NO extractor:
its materialization proof rests on persisted per-source health rows, not
log attestation.
