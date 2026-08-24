# ADR-0010: Least-Privilege Operational Identities

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0007 (survivability), ADR-0009 (destructive-operation safety),
Fleet Laws v1 (Law 5 lane isolation)
Evidence basis: operator-verified host findings, 2026-08-24 convergence pass

## Context

Both operational identities on the Hetzner host (`anilganti`, `deploy`)
currently hold unrestricted `NOPASSWD: ALL` sudo. This is the standing
enabler for incident family A (root `git stash -u` inside live checkouts)
and family B (pattern-matched `docker volume rm` of two real production
volumes): any process running as either identity — including an automated
agent following a plausible-looking plan — can destroy any state without
friction. ADR-0009 defines what must happen before destructive action;
this ADR defines who should possess the privilege in the first place.

## Decision

### 1. Identity classes (not one Unix-user model for all Clanks)

| Class | Purpose | May mutate production state? | Example |
|---|---|---|---|
| service identity | one per Clank/lane runtime | only its own store, via scoped commands | smartphone-clank's dedicated `/opt` user |
| deploy identity | checkout/image convergence | source trees; never DBs/volumes/backups directly | `deploy`, post-scoping |
| observer identity | Diagnostic Clank probes, Motherclank harvest | nothing (read-only paths only) | new dedicated reader |
| backup identity | backup jobs | create copies; never delete primaries | Clank-side or shared backup runner |
| operator (human) | break-glass | everything, interactively, logged | `anilganti` |

The smartphone-clank / korean-tech-wire dedicated-service-user + `/opt`
pattern is the fleet's existing strongest isolation example and is the
recommended target model for future lanes; retrofitting existing lanes is
per-lane reviewed work, not a sweep.

### 2. Scoped sudo via Cmnd_Alias (replaces NOPASSWD: ALL)

Each non-operator identity receives an explicit command allowlist:

```
Cmnd_Alias REFRESH_REAL_STATE = /path/to/refresh-real-state.sh *
Cmnd_Alias OBSERVER_READS    = /usr/bin/sqlite3 * .backup *, \
                               /usr/bin/journalctl -u clank-*, ...
deploy   ALL=(root) NOPASSWD: REFRESH_REAL_STATE
observer ALL=(root) NOPASSWD: OBSERVER_READS
```

Forbidden by construction for non-operator identities: `rm`, `docker
volume rm/prune`, `container prune`, `chown/chmod` outside their tree,
`git` against other identities' checkouts, sudoers editing, and any shell
wrapper (`sh -c`, `bash`) that would defeat the allowlist.

### 3. Mutation separation (complements ADR-0009 sequence)

Deployment tooling may converge SOURCE TREES. It may not touch DATABASES,
VOLUMES, BACKUPS, or SECRETS-class resources even where it holds nominal
permission — those require either a scoped backup identity or interactive
operator execution under the ADR-0009 checkpoint contract.

### 4. Break-glass path

Emergencies use the human operator identity interactively, with the action
recorded afterward into the continuity/incident evidence plane. There is no
automated break-glass.

### 5. Motherclank posture role

Motherclank observes and reports privilege posture as evidence (e.g.,
"identity X holds unrestricted NOPASSWD" recorded as a survivability/
security finding with as_of). It enforces nothing. Participant-tier
tooling, when it ever exists, inherits this ADR's allowlist requirements
as a precondition.

## Conformance additions

Golden register cross-reference: ROOT-STASH-RUNTIME-PATH and
DB-LOSS-* fixtures assume destructive capability was reachable from an
automation context; least-privilege scoping shrinks that reach. The
sudoers inventory itself is an ACT-001-style host fact to be re-collected
with fresh as_of after any remediation.

## Non-decisions

No sudoers file is changed by this ADR. No remediation timeline is set.
The audit finding remains OPEN until an operator applies scoped aliases at
a maintenance window and records fresh evidence.
