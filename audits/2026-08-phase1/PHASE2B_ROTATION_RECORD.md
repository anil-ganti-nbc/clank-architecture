# PHASE 2B CREDENTIAL ROTATION RECORD — FGT / CTW

Status: **AUTHORIZED (operator, Phase 2B mandate) — EXECUTION PARTIALLY BLOCKED ON OPERATOR-MINTED REPLACEMENT VALUES**
Date: 2026-08-22 · Executor: Phase 2B session · Secret values read or recorded: **NONE**

## Findings that shape execution

1. **CTW has no credentials on Hetzner at all** (`/home/deploy/staging/chinese-tech-wire` contains only `.env.example`; staging webhook env defaults empty; Gemini/translation keys exist only in local macOS dev contexts). Nothing on the deployed host requires rotation for CTW.
2. **FGT's live webhook lives in `/home/deploy/free-game-tracker/.env`** (presence verified Phase 1.5/2A; value never read). The exposed value (assistant transcript echo, 2026-08-09) is a Discord webhook URL. Discord webhooks can only be *minted* from inside the Discord client by someone with channel manage rights — not executable from any fleet session.

## Executed in this phase

- Verified CTW host surface credential-free (Phase 1.5 manifest + 2A re-checks).
- Confirmed FGT `.env` untouched and its value never captured into any audit artifact (all Phase 1/1.5/2A deliverables secrets-scanned clean).
- Recorded this status block in the governance audit archive.

## Operator steps to close D-25 (est. 10 minutes)

1. Discord → target channels → create replacement webhooks (editorial lane for FGT).
2. `ssh hetzner`; `sudo -n nano /home/deploy/free-game-tracker/.env` → replace webhook value only.
3. Delete the old webhook URL in Discord (revocation = the actual rotation event).
4. Trigger one run: `sudo -n -u deploy /home/deploy/free-game-tracker/deploy/run.sh` → confirm delivery row/log success.
5. Record completion: append one line to `ai/handoff/DEPLOYMENT_LEDGER.md` ("webhook rotated, old revoked") — no values.

## Verification checklist (post-rotation)

- Old URL returns 404 from Discord ✓ revoked
- New deliveries land in expected channel
- No secret value appears in logs, ledger, or git
- CTW local dev keys (Gemini/translation), if ever used against shared limits, rotated separately by operator on device.
