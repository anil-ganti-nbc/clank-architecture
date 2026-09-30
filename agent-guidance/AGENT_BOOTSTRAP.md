# Agent Bootstrap

`agent-guidance/PROMPT_OPTIMIZATION.md` is the canonical prompt-efficiency policy for every coding agent working in this repository.

- Reference durable repository context instead of repasting it.
- Structure briefs as: **Task / Context / Blocker / Reference / Evidence / Question**.
- When evidence is required, paste exact logs, errors, diffs, focused code, or query results.
- State the relevant branch, SHA, file, and deployment state.
- State explicit no-touch constraints.
- Separate architecture decisions from implementation work.
- Repository truth is not automatically deployment truth.
- Do not rediscover documented architecture; reference it.
- If instructions conflict, report the conflict instead of silently overriding canonical architecture.

Read [`PROMPT_OPTIMIZATION.md`](PROMPT_OPTIMIZATION.md) before starting work.
