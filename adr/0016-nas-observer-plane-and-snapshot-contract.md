# ADR-0016: Ratify the NAS observer plane and governed snapshot contract

Status: **PROPOSED — OWNER REVIEW REQUIRED** (not binding until reviewed and merged)
Date: 2026-09-29
Decision owner: Clank architecture/platform owner (`@anil-ganti-nbc`)
Development record: COPS-000083; blocking observer work: COPS-000081
Related: [Canonical v0.1](../CANONICAL_CLANK_ARCHITECTURE_v0.1.md),
[Canonical v0.2](../CANONICAL_CLANK_ARCHITECTURE_v0.2.md),
[Observer Adapter Surface Contract](../ADAPTER_CONTRACT.md), ADR-0001,
ADR-0002, ADR-0003, ADR-0005, ADR-0014, Fleet Laws 3, 5, 6, and 7

## Context and evidence boundary

The NAS has a healthy, separately deployed Diagnostic archivist/incident service
at Git SHA `2ab77d397b16f290c24361c8a5363d70fde477e0`. Its UI lists Clank
identities, but its image does not contain the `clank_fleet` adapter package and
does not prove observation of any child database. The existing NAS Motherclank
harvest instead packages Diagnostic-owned adapters from `3667af0`, reads four
SQLite-safe child snapshots, and truthfully reports six other lanes UNKNOWN.
These are dated deployment facts from COPS-000081, **not** an assertion that
either image is the current adapter-plane authority.

Canonical v0.1 permits batch adapters. ADR-0002 assigns the read-only adapter
plane to Diagnostic and Motherclank the consumer role. Neither requires a
live Diagnostic HTTP/service hop. Conversely, canonical v0.2 §5 names four
unconditional observer probes that the subsequently documented and implemented
Observer Adapter Surface Contract v0.2 expressly did not adopt. ADR-0001 and
ADR-0002 also retained Proposed status after entering `main`. This ADR makes
the current decision and its precedence explicit without rewriting those
historical files as though they had always said it.

## Decision 1 — topology and authority

The operational NAS observation path is:

```text
child canonical persistent state
  -> governed, integrity-checked, read-only snapshot
  -> versioned Diagnostic-owned observer adapter package
  -> adapter-produced structures
  -> Motherclank harvest and derived synthesis
```

The child's own state remains domain truth. A snapshot is an immutable
transport/evidence artifact, not another canonical writer. The adapter
package and registry are owned by the Diagnostic project, even when packaged
inside a pinned Motherclank image. Motherclank MUST consume adapter-produced
structures; it MUST NOT reimplement child-specific DB interpretation or infer
health, novelty, or deployment truth from missing fields. Observer adapters
MUST be read-only and MUST NOT trigger collection, feedback writes, delivery,
or scheduler changes. Motherclank outputs remain labeled DERIVED.

The live Diagnostic service is a **parallel** diagnostic, archivist, report,
incident, and optional presentation surface. A live service or HTTP hop is
neither required nor implied for harvest. Future service participation needs
a separate reviewed decision and versioned interface; an identity dropdown
alone is not observer proof. The adapter package and live service have
independent source/deployment revisions and may evolve independently under
explicit compatibility rules. In particular,
`LIVE_NAS_DIAGNOSTIC_SHA` MUST NOT be reported as
`VALIDATED_ADAPTER_PACKAGE_SHA`. The latter is the exact Git commit of the
Diagnostic-owned adapter package used in the validated harvest; the built
package/image SHA-256 is a separate executable-artifact identity and both
must be recorded.

Machine-readable fleet membership and adapter registration remain
Diagnostic-owned responsibilities. Their location may be a versioned
Diagnostic package artifact rather than the live service process. A deployment
is not declared converged merely because that responsibility is assigned:
the active package, inventory, child paths, and freshness require separate
host evidence.

## Decision 2 — binding observer surface and version separation

Upon acceptance, `OBSERVER_CONTRACT_VERSION = "0.2"` is the governance and
handoff name for the required Observer Adapter Surface Contract v0.2 in
[`ADAPTER_CONTRACT.md`](../ADAPTER_CONTRACT.md):

```text
identity()  capabilities()  status()  health()  last_run()
capability_states()
```

It maps to the implementation's `OBSERVER_SURFACE_SPEC_VERSION = "0.2"` in
Motherclank's consumer-side `contract.py`; that validator does not transfer
adapter implementation or registry ownership from Diagnostic to Motherclank.
ADR-0013 is listed as a proposal in the decision ledger but has no ADR file
in this repository. On acceptance, this ADR ratifies only the six-method v0.2 surface and
its stated fail-safe rules, not every historical ADR-0013 proposal.

`last_run()` MUST retain its honest supported/unsupported signal. Absent
participant evidence remains UNKNOWN, not a manufactured cursor or event.
The contract's fail-safe validation, unsupported-major isolation,
per-adapter exception isolation, duplicate-store rejection, and no-create/
no-migrate/no-mutate rules are binding. Optional, versioned extensions may
include `source_summary`, `diagnostic_summary`, `schema_revision`,
`code_revision`/`deployed_revision` evidence, `recent_runs`, and
`execution_evidence`; their absence MUST NOT be represented as a healthy
zero or used to weaken the required core.

This **supersedes the unconditional observer method requirement** in canonical
v0.2 §5 for `probe_identity`, `probe_health`, `fetch_baseline_cursor`, and
`fetch_candidates`, the unconditional queryable-baseline exposure in §4, and
the corresponding unconditional baseline/candidate pagination wording in §9,
**for current observer-tier adapters only**. It also narrows canonical v0.1
§5's generic minimum of `describe`, collection/subscription intake, and
normalization: those are intake/participant-adapter requirements, not an
instruction to give a passive Diagnostic observer a collection trigger.
Those four names remain historical design evidence, not a second required
interface. They MUST NOT be added as empty or dishonest compatibility stubs.
Durable baselines, identity handover, source health, scheduler corroboration,
read-only operation, freshness, authentication/integrity, and honest UNKNOWN
semantics in v0.1/v0.2 and ADR-0005 remain binding where the child actually
supports them. A child with a real baseline MUST preserve and expose its
evidence through a versioned capability/extension; a child without one MUST
declare unsupported or UNKNOWN and cannot pass a production gate that still
requires durable baseline evidence. No local crawl cursor becomes a canonical
baseline by declaration.
Queryable cursor/candidate extensions require a future versioned contract and
participant evidence; this ADR does not invent them for stores that lack them.

`ADAPTER_CONTRACT_VERSION = "0.1.0-v3"` continues to identify shared
descriptor/payload types in `clank_runtime`. It is **not** the observer method
surface version. The typed-evidence/lane-configuration v0.3 proposal and
ADR-0014 remain PROPOSED; ratifying surface v0.2 does not silently accept
v0.3 or its future extensions.

## Decision 3 — governed snapshot contract

`SNAPSHOT_CONTRACT_VERSION = "1.0"` names the NAS child-snapshot provenance
manifest defined here. Its required record is one per refresh attempt per
child **instance and lane**, not one per repository or a directory-wide
`*.sqlite` sweep. Every snapshot supplied to an adapter MUST carry:

| Field | Required meaning |
|---|---|
| `snapshot_contract_version` | Exactly `1.0` for this contract. |
| `clank_id`, `instance_id`, `lane_id` | Stable child and runtime-lane identities; never inferred from filename alone. |
| `source_host`, `source_path` | Host and canonical child DB/interface observed; must not point to a Motherclank cache. |
| `snapshot_created_at` | UTC time the immutable snapshot was completed. |
| `child_as_of`, `child_as_of_clock` | Native latest-run/as-of time where available, with its clock label; otherwise null with an explicit unavailable reason. |
| `schema_version` | Child schema/contract version, or explicit UNKNOWN reason. |
| `child_source_revision`, `child_deployed_revision` | Host-evidenced revisions where exposed; distinguish source from deployed, otherwise null with reason. |
| `snapshot_path`, `snapshot_sha256`, `snapshot_bytes` | Exact immutable artifact identity and size on SUCCESS; null with reason on an attempt that produced no snapshot. |
| `integrity_result` | SQLite integrity and foreign-key result (or equivalent source-native check); failures are explicit. |
| `adapter_package_sha`, `adapter_artifact_sha256`, `adapter_package_version`, `observer_contract_version` | Diagnostic-owned source Git commit, built executable package/image digest, package version, and method-surface contract used to interpret the snapshot. |
| `refresh_outcome`, `freshness_state`, `child_execution_freshness` | Separate copy outcome, snapshot usability, and child-run/source freshness as defined below. |
| `observed_at`, `freshness_horizon` | Observer clock and declared per-lane age policy, with clock/source labels. |
| `error_code`, `last_good_snapshot_ref` | Required when refresh fails or a prior snapshot is retained; error text must be secret-safe. |

`refresh_outcome` is `SUCCESS`, `FAILED`, or `UNAVAILABLE`.
`freshness_state` is `FRESH`, `STALE`, `REFRESH_FAILED`, or `UNAVAILABLE`.
The distinction is load-bearing: a failed refresh may retain a last-good
snapshot as historical evidence, but MUST NOT make that old artifact appear
current. `FRESH` describes **snapshot transport freshness**: a successful
integrity-checked refresh, verified hash, compatible adapter/schema, and a
copy age within the declared horizon. `child_execution_freshness` is a
separate adapter-derived state from the child's native or explicitly labeled
derived run/source clock; it is UNKNOWN if such evidence is unavailable.
A recent copy MUST NOT manufacture a recent child run. UNKNOWN/failed
integrity or incompatible major versions fail closed. Every attempted lane
has a manifest record even when no artifact was produced; in that case the
snapshot identity fields are null and the failure/unavailability reason is
required.

Snapshot creation MUST use the source's supported consistent-backup API or an
equivalent quiesced transaction; a raw copy of an actively written SQLite/WAL
DB is not acceptable. The snapshotter opens canonical child state read-only,
records the intended source path and result, verifies destination checksum and
integrity, and uses authenticated/integrity-protected transport when crossing
hosts. Source non-mutation is proven through read-only permissions/connections
and an appropriate before/after or writer-attributed check; changing bytes in
an independently active child writer is not, by itself, proof that the
observer wrote them. Secrets and payload contents are excluded from the
provenance record.

Motherclank MUST preserve the per-lane refresh and freshness states in its
adapter block, synthesis, and report. A missing snapshot, failed refresh,
stale source, failed adapter, or unsupported major version yields UNKNOWN or
an explicitly degraded/failed observation according to the adapter contract;
it never upgrades to HEALTHY. Derived records cite snapshot hash, adapter
package SHA/version, observed-at time, and raw field provenance. An old
last-good hash remains visible as history, not as a substitute for a current
successful observation.

The contract is major-versioned: incompatible major manifests are rejected
as current input; additive minor fields require a documented minor revision.
Changing required fields or freshness/failure semantics requires a new ADR
and major version. This ADR defines the contract but does **not** claim that
the existing four-child NAS manifest already conforms to it.

## Governance reconciliation and precedence

This ADR, **only after reviewed merge**, ratifies these earlier provisions:

| Prior text | Disposition |
|---|---|
| ADR-0001 governance repository ownership and Diagnostic project responsibility for machine-readable inventory/control-plane contracts | RATIFIED as ownership, not proof that today's live Diagnostic service implements fleet adapters or inventory. |
| ADR-0002 child domain truth, Diagnostic ownership of the read-only adapter plane, separate Motherclank derived supervision, UNKNOWN fail-closed behavior, M0–M4 read/reason/propose and M5 behind a future ADR | RATIFIED. The live service hop is not a requirement. |
| ADR-0002's initial four-child onboarding order, `--real-state DIR` example, and dated host assumptions | HISTORICAL implementation examples, not permanent fleet inventory or transport paths. |
| ADR-0001's proposed supersession of `unified-clank-platform` | STILL OPEN pending a reviewed unique-function disposition; not ratified by this ADR. |
| Canonical v0.1 §5 observer intake implication, v0.2 §4 unconditional baseline exposure, §5 four-probe methods, and §9 unconditional baseline/candidate pagination for observer-tier adapters | SUPERSEDED only as unconditional observer-interface requirements by the six-method surface above. Participant/intake contracts and other safety/integration gates remain. |
| Ledger-only proposed ADR-0013 and `ADAPTER_CONTRACT.md` v0.2 surface | Only the six-method observer surface and its fail-safe validation are RATIFIED by this ADR; no missing ADR file or broader proposal is implied accepted. |
| Observer surface v0.3 / ADR-0014 typed evidence | REMAINS PROPOSED; no implicit ratification. |

The historical `Status: Proposed` headings in ADR-0001/0002 and their
unmerged-draft wording are preserved as records of their authoring state.
On reviewed merge, this ADR becomes the dated activation decision for the
precise provisions listed above; it does not retroactively claim every clause
was accepted on its original date. The architecture README, authority index, and decision
ledger must point to this disposition **when this ADR is merged**. No ADR,
commit, or ledger entry is deployment proof.

## Alternatives rejected

1. **Mandatory live Diagnostic HTTP/service hop.** Rejected: v0.1 permits
   batch transport; ADR-0002 assigns code/adapter ownership, not a network
   topology; the current service lacks fleet adapters. It could be added only
   through a separate reviewed decision and conformance work.
2. **Direct Motherclank-specific SQLite interpretation or directory sweep.**
   Rejected: violates Diagnostic adapter ownership, identity, provenance,
   lane isolation, and UNKNOWN semantics.
3. **Implement both observer method sets with empty stubs.** Rejected: creates
   false baselines/candidates and violates health honesty.
4. **Reuse the last successful snapshot after a failed refresh as fresh.**
   Rejected: hides source outage and produces false current coverage.

## Compatibility, rollout, conformance, and rollback

Acceptance changes the *normative contract*, not a running service. Existing
adapters conforming to the six-method surface may remain; no four-probe shim
is required. Current NAS Motherclank's four-child, `3667af0`-based pipeline
remains a partial historical deployment until separately verified under
COPS-000081. No Board adapter or Board-inclusive Diagnostic deployment is
authorized by this ADR.

After reviewed merge, COPS-000081 may resume in a new Session and:

1. identify and pin the current Diagnostic-owned adapter source Git commit as
   `VALIDATED_ADAPTER_PACKAGE_SHA` **and** its separate built artifact/image
   SHA-256; register only compatible non-Board NAS children;
2. prove at least two structurally different NAS-canonical children through
   snapshot manifest v1.0 and the observer surface v0.2, including honest
   healthy/degraded source semantics and no child mutation;
3. add other migrated children deliberately, preserving absent/failed/stale
   distinctions; stage a complete Motherclank harvest in isolated state;
4. only after staging tests and rollback capture, update the NAS task-14
   candidate atomically under single scheduler authority and verify a natural
   harvest. Hetzner's Motherclank timer stays off unless a guarded rollback
   first proves NAS harvest off.

Only after those gates may a separate Board COPS-000074 handoff provide
`VALIDATED_ADAPTER_PACKAGE_SHA`, `OBSERVER_CONTRACT_VERSION`,
`SNAPSHOT_CONTRACT_VERSION`, `BOARD_REGISTRATION_MECHANISM`,
`SOURCE_SUMMARY_CONTRACT`, `DIAGNOSTIC_SUMMARY_CONTRACT`,
`DEPLOYED_REVISION_SEMANTICS`, and `MOTHERCLANK_HARVEST_MECHANISM`, each with
the exact tested artifact and evidence. No Board-inclusive live Diagnostic
service SHA is a prerequisite or a substitute for these fields.

Conformance work must cover method validation and major-version rejection;
missing/disabled lanes; successful and failed SQLite-safe refresh; hash and
integrity mismatch; stale native run versus recent copy time; adapter failure
isolation; source non-mutation; mixed healthy/degraded proof children;
derivation provenance; scheduler authority and natural-run evidence. The
current partial NAS output is not grandfathered as conformant. Protocol
tests must run in the supported Linux/NAS environment before promotion.

Rollback of a later runtime change restores the preserved previous NAS
adapter package/inventory and four-child partial state **after** disabling
the candidate scheduler invocation and verifying it is off; the old partial
task may then resume as the sole NAS harvest authority. A Hetzner restore is
not implied. Child canonical stores are never replaced by observer snapshots.

## Non-goals

No Board onboarding or modification; no child collector, DB, scheduler, or
delivery mutation; no live Diagnostic redeploy; no mandatory service hop; no
Motherclank M5 or autonomous action; no promotion-freeze lift; no assertion
that the current NAS partial harvest or live Diagnostic UI is converged.

## Review and activation gate

The platform owner must review this ADR, the exact supersession table, the
version separation, snapshot failure semantics, compatibility/rollback, and
the architecture authority-index changes. CI and link/conformance checks
must pass on the exact PR head. Before merge, set this ADR's status to
**ACCEPTED — effective on reviewed merge** and update the README/authority
index and decision ledger in the same reviewed change. Only a verified merge
activates this decision and permits COPS-000081 to resume.
