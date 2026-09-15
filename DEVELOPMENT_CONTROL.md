# Development Control — ClankOps reporting

Status: **binding development procedure** (this amendment; not a historical
architecture gate)

Opening principle:

> ClankOps is the fleet's institutional-memory plane.
> It records development state; it does not replace architectural,
> conformance, compute/resource or domain authority.

Primary law:

> **NO MATERIAL CLANK DEVELOPMENT EXISTS OUTSIDE CLANKOPS.**

Every new Clank and every material development tranche involving an existing
Clank MUST have a ClankOps Mission before implementation begins. There is no
code-first / ledger-later workflow.

This procedure is dated **2026-09-15** (ADR-0015). It does not rewrite
canonical architecture v0.1/v0.2 or imply that earlier work was already
under this gate.

Related: [AGENT_RULES.md](AGENT_RULES.md) rule 16,
[adr/0015-clankops-mandatory-development-control.md](adr/0015-clankops-mandatory-development-control.md).
Operational contract for Cursor: `clankops/docs/CURSOR_AGENT_CONTRACT.md`.

## What is material

Material development includes at minimum:

- a new Clank/project
- a substantial feature
- an architecture change
- a cross-cutting refactor
- a production repair
- a migration
- a deployment/runtime authority change
- a substantial investigation likely to produce code/config changes
- standards/conformance remediation
- a new collector/source family
- major integration work

Tiny editorial/documentation corrections may remain outside a dedicated
Mission unless they alter architecture, runtime behaviour, or governance.

## Mandatory lifecycle

### A. Before implementation

Required:

- Clank identity exists in ClankOps
- a coherent Mission exists
- the agent prepare / resume packet has been reviewed
- exactly one Session is active for the work
- actor / launcher / context provenance is recorded where supported

Do not begin implementation, then invent the Mission afterwards.

### B. During implementation

ClankOps MUST preserve enough state for another agent to resume without the
originating chat transcript.

Record a checkpoint when materially useful:

- current objective
- completed work
- decisions and rationale
- blockers
- exact branch
- exact HEAD
- working-tree state
- next action

Do not spam checkpoints for every edit. Use them at meaningful resumability
boundaries.

### C. Agent switch / interruption

Before another agent takes over, or work stops for a meaningful period:

- checkpoint
- explicit handoff
- next action
- Mission `PAUSED` or `BLOCKED` where applicable
- Session closed truthfully

**PROCESS EXIT IS NOT HANDOFF.** A crashed or killed agent is not a recorded
handoff. Only canonical `handoff` writes the handoff record.

### D. PR / CI

Record exact branch, HEAD, PR, and CI result. Preserve existing ClankOps laws:

- local HEAD ≠ Mission completion
- CI success ≠ deployment success
- PR merge ≠ automatic Mission completion

Git, GitHub, CI, deployment evidence, and automatic Harvest observations do
not replace the Mission / Session / handoff record.

### E. Deployment

If deployment occurs, capture deployment/runtime evidence separately.

Source HEAD and deployed HEAD remain separate facts.

Deployment does not silently complete the Mission.

### F. Completion

A Mission may be completed only after:

- implementation state is known
- a final checkpoint exists
- required tests/evidence are recorded
- an explicit handoff exists
- remaining next action is genuinely none, or post-Mission work is
  represented elsewhere
- the lifecycle transition is explicit

Do not leave `COMPLETED` Missions with an open development Session.

## Harvest relationship

Fleet Harvest / Fleet Pulse automatically observes local Git state.

That observation is **not** a replacement for development reporting.

Harvest can answer:

- what branch / HEAD / dirty state exists?

It cannot answer:

- why are we here?
- what objective are we pursuing?
- what decision was made?
- what remains?
- where should the next agent continue?

Automatic Git evidence reduces clerical reporting. It never removes
Mission / checkpoint / handoff obligations.

## New Clank creation

A new Clank MUST be registered with ClankOps at project inception, not after
it becomes production-worthy.

This includes prototypes, experiments, personal Clanks, local-only Clanks,
support tooling, and architecture/governance Clanks, provided the work is
material and is intended to persist beyond a trivial scratch experiment.

Do not wait for GitHub repo creation, first PR, deployment, Standards
admission, or Motherclank onboarding.

ClankOps identity precedes those milestones where practical.

## Wayward-work recovery

If material work is discovered without a ClankOps Mission:

- do **not** fabricate historical live observation

Instead:

- register or recover identity
- create or reconstruct the Mission honestly
- mark historical facts `RECONSTRUCTED` where applicable
- capture current code state independently
- record the exact current stop point and next action

Then continue under normal ClankOps control.

## Authority boundary

ClankOps owns:

- development chronology
- Mission intent/state
- Session attribution
- checkpoints
- handoffs
- blockers
- next action
- development evidence presentation

ClankOps does **not** own:

| Plane | Authority |
| --- | --- |
| foundational architecture | Motherclank / architecture authority |
| conformance | Standards Clank |
| compute/resource allocation | Quartermaster |
| domain semantics | participant Clank |
| Git truth | Git |
| GitHub truth | GitHub |
| CI truth | CI |
| deployment truth | deployment observer |

It records and surfaces those facts without absorbing their authority.
This procedure does not supersede Fleet Laws, canonical architecture v0.1/v0.2,
the no-promotion policy, or Motherclank observer onboarding
([ONBOARDING.md](ONBOARDING.md)).
