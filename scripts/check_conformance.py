"""Machine-checkable Phase 0 governance invariants."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    policy = (ROOT / "NO_PROMOTION_POLICY.md").read_text(encoding="utf-8")
    adr = (ROOT / "adr/0001-authority-and-phase0-freeze.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    errors: list[str] = []
    allowed_policy_statuses = (
        "Status: **PROPOSED — ACTIVATES ON REVIEWED MERGE**",
        "Status: **ACTIVE — PROMOTION FROZEN**",
    )
    if not any(status in policy for status in allowed_policy_statuses):
        errors.append("policy must declare proposed activation or active promotion freeze")
    required_policy_terms = (
        "promotion_eligible: false",
        "UNKNOWN",
        "13 repositories",
        "two real unattended Windows runs",
    )
    for term in required_policy_terms:
        if term not in policy:
            errors.append(f"policy missing required term: {term}")
    if "Status: Proposed" not in adr:
        errors.append("ADR-0001 must remain Proposed until merged and accepted")
    if "https://github.com/anil-ganti-nbc/diagnostic-clank/" not in readme:
        errors.append("README must use a resolvable cross-repository ledger link")
    if errors:
        print("\n".join(errors))
        return 1
    print("Phase 0 governance documents conform to the proposed-or-active-freeze contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
