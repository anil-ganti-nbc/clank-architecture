"""Grand Clank Fleet Laws conformance suite (Phase 2A).

Hermetic: no network, no databases, no host access. Tests exercise REAL merged
fleet code where that code is dependency-light (korean-tech-wire scheduling,
smartphone-clank alert eligibility) and mechanically verify Law 5/Law 6/Law 8
properties directly against the canonical fleet inventory
(diagnostic-clank/clank-fleet/inventories/fleet.yaml).

Sibling repos are located relative to THIS repository so the suite runs from
any checkout layout that keeps the Phase 1 workspace convention
(<workspace>/<repo>). Missing siblings or optional deps cause SKIP, never FAIL.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent          # .../grand-clank-audit
KTW_SRC = WORKSPACE / "korean-tech-wire" / "src"
SPHONE = WORKSPACE / "smartphone-clank"
FLEET_YAML = WORKSPACE / "diagnostic-clank" / "clank-fleet" / "inventories" / "fleet.yaml"

if str(KTW_SRC) not in sys.path and KTW_SRC.exists():
    sys.path.insert(0, str(KTW_SRC))
if str(SPHONE) not in sys.path and (SPHONE / "alerts").exists():
    sys.path.insert(0, str(SPHONE))


# ---------------------------------------------------------------------------
# Law 3 / Law 5 — scheduler honesty: per-source due-gating and bounded backoff
# (real module: korean_tech_wire.scheduling.py, merged to main in 45e6ec4)
# ---------------------------------------------------------------------------

def _scheduling():
    if not (KTW_SRC / "korean_tech_wire" / "scheduling.py").exists():
        pytest.skip("korean-tech-wire checkout not present")
    try:
        from korean_tech_wire import scheduling  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover
        pytest.skip(f"scheduling import failed: {exc}")
    return scheduling


def test_dead_source_does_not_hold_siblings_hostage():
    """Regression fixture: D-06 due-gating defect (2026-08-10..18, ~4x cadence).

    A permanently-failing source in its own backoff window must NOT drag healthy
    sources into 'due'; each source gates on its OWN cadence."""
    s = _scheduling()
    now = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)
    states = {
        # HOST-BLOCKED: attempted 5 min ago, failing for a long time -> deep backoff, NOT yet due
        "sk_hynix": s.SourceDueState(last_attempt_at=now - timedelta(seconds=300),
                                     last_success_at=None, consecutive_failures=50),
        # healthy and fresh: succeeded 1h ago (<2h cadence) -> asleep
        "the_elec": s.SourceDueState(last_attempt_at=now - timedelta(seconds=3600),
                                     last_success_at=now - timedelta(seconds=3600),
                                     consecutive_failures=0),
        # healthy but stale: last cycle >2h ago -> due
        "etnews": s.SourceDueState(last_attempt_at=now - timedelta(seconds=7300),
                                   last_success_at=now - timedelta(seconds=7300),
                                   consecutive_failures=0),
        # never attempted at all -> due immediately
        "lg_display": s.SourceDueState(last_attempt_at=None, last_success_at=None,
                                       consecutive_failures=0),
    }
    due = set(s.due_sources(states, base_interval_seconds=7200, now=now))
    assert "the_elec" not in due, "fresh source must stay asleep"
    assert "sk_hynix" not in due, "blocked source inside backoff window must wait its own interval"
    assert {"etnews", "lg_display"} <= due


def test_persistent_failure_backoff_is_bounded():
    """SK hynix HOST-BLOCKED specimen: retry interval must grow monotonically but
    stay capped, never resuming full-frequency polling against a blocking edge."""
    s = _scheduling()
    base = 7200
    prev = None
    for failures in range(0, 60):
        interval = s.retry_interval_seconds(base, failures)
        assert interval >= base, "backoff never polls faster than normal cadence"
        assert interval <= base * s.BACKOFF_CEILING_MULTIPLIER, \
            f"backoff exceeded ceiling at {failures} failures"
        if prev is not None:
            assert interval >= prev, "backoff must be monotonic in failure count"
        prev = interval
    assert s.retry_interval_seconds(base, s.TRANSIENT_FAILURE_THRESHOLD) == base


# ---------------------------------------------------------------------------
# Law 4 — explicit event capability: fail-closed eligibility
# (real module: smartphone-clank alerts/eligibility.py)
# ---------------------------------------------------------------------------

def _eligibility():
    mod = SPHONE / "alerts" / "eligibility.py"
    if not mod.exists():
        pytest.skip("smartphone-clank checkout not present")
    try:
        from alerts import eligibility  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover
        pytest.skip(f"eligibility import failed: {exc}")
    return eligibility


def test_unknown_reason_fails_closed():
    e = _eligibility()
    assert e.newsroom_eligible("totally_made_up_reason") is False


def test_baseline_and_backfill_reasons_are_suppressed():
    """Law 1/Law 4 specimen: the contamination/baseline era taught that init-time
    reasons must be explicitly suppressed, not merely unlisted."""
    e = _eligibility()
    for reason in ("baseline_import", "initial_backfill", "fixture", "demo", "quarantine"):
        assert e.newsroom_eligible(reason) is False, reason


def test_editorial_reasons_remain_eligible():
    e = _eligibility()
    assert e.newsroom_eligible("new_model") is True
    assert e.newsroom_eligible("support_page_change") is True


# ---------------------------------------------------------------------------
# Laws 5 / 6 / 8 — mechanical checks against the canonical fleet inventory
# ---------------------------------------------------------------------------

def _inventory():
    yaml = pytest.importorskip("yaml")
    if not FLEET_YAML.exists():
        pytest.skip("canonical fleet.yaml not present")
    return yaml.safe_load(FLEET_YAML.read_text())


def test_law5_each_repository_lane_has_exactly_one_enabled_scheduler():
    """The smartwatch dual-scheduler defect (retired 2026-08-21T21:06Z) must be
    structurally visible forever: two ENABLED scheduler mechanisms for one
    repository IN THE SAME ENVIRONMENT is a failure. Distinct environments
    (production vs experimental) are the Law 5 documented exception when they
    are disjoint by database, lock, and volume."""
    inv = _inventory()
    enabled_by_lane: dict[tuple[str, str], list[str]] = {}
    for dep in inv["deployments"]:
        if dep["scheduler"].get("enabled") is True:
            lane = (dep["repository"], dep["environment"])
            enabled_by_lane.setdefault(lane, []).append(dep["instance_id"])
    dupes = {lane: ids for lane, ids in enabled_by_lane.items() if len(ids) > 1}
    assert not dupes, f"multiple enabled scheduler lanes for one (repo, environment): {dupes}"


def test_law5_cross_environment_lanes_are_isolated():
    """Where multiple environments of one repo exist on one host, each must
    declare a distinct scheduler authority string and distinct instance."""
    inv = _inventory()
    by_repo: dict[str, set[str]] = {}
    for dep in inv["deployments"]:
        if dep["scheduler"].get("enabled") is True:
            by_repo.setdefault(dep["repository"], set()).add(dep["scheduler"]["authority"])
    for repo, authorities in by_repo.items():
        assert len(authorities) == len(
            [d for d in inv["deployments"]
             if d["repository"] == repo and d["scheduler"].get("enabled") is True]
        ), f"{repo}: scheduler authority strings must be unique per lane"


def test_law6_running_deployments_have_evidenced_shas():
    inv = _inventory()
    for dep in inv["deployments"]:
        if dep["deployment_state"] == "RUNNING":
            sha = dep.get("deployed_commit_sha", "UNKNOWN")
            assert sha != "UNKNOWN" and len(sha) >= 40, f"{dep['instance_id']} lacks evidenced SHA"
            assert dep.get("host") == "ubuntu-4gb-hel1-1"


def test_law8_promotion_freeze_holds_fleet_wide():
    inv = _inventory()
    for dep in inv["deployments"]:
        assert dep["promotion_eligible"] is False, dep["instance_id"]


def test_retired_smartwatch_lane_stays_disabled():
    """Preserved-evidence invariant: the retired failing lane must remain
    DISABLED and non-enabled until a reviewed governance change says otherwise."""
    inv = _inventory()
    retired = [d for d in inv["deployments"] if d["instance_id"] == "smartwatch-hetzner-soak-timer-retired"]
    assert len(retired) == 1
    row = retired[0]
    assert row["deployment_state"] == "DISABLED"
    assert row["scheduler"]["enabled"] is False
    assert "do NOT re-enable" in row["rollback_artifact"]
