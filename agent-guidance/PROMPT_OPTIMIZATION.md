# Coding-Agent Prompt Optimization Strategy

**Author:** Anil Ganti
**Purpose:** Token-efficient prompting for the Clank newsroom intelligence system
**Audience:** Development team, coding agents, future collaborators
**Status:** Canonical reference for all coding-agent work across the Clank ecosystem

> **Scope note:** This policy applies to Claude, Codex, Grok, Gemini, Luna/Terra/Sol, and future coding agents. The `.claude/` paths and `unified-clank-platform` examples below are retained as historical/current implementation details of the original strategy; use the equivalent durable guidance path and repository context when a repository defines different conventions.

---

## Executive Summary

The Clank ecosystem has accumulated substantial architectural knowledge, operational procedures, and domain-specific patterns. Naive prompting—pasting full specs, orientation documents, and operations manuals every session—wastes **90%+ of available tokens** on context re-establishment.

This document defines a systematic approach to coding-agent interaction that:

- Preserves architectural knowledge across sessions
- Minimizes context overhead
- Maximizes productive work per token
- Ensures consistent understanding across multiple agents
- Makes explicit what the coding agent should and should not be asked to do

**Key principle:** Architectural documents are written once, stored durably, referenced many times.

---

## Part 1: Repository Structure for Coding-Agent Efficiency

### 1.1 Create `.claude/` Directory

All coding-agent-related reference material lives here:

```
unified-clank-platform/
├── .claude/
│   ├── README.md                 # Start here for new agents
│   ├── CONTEXT.md                # Canonical orientation packet
│   ├── PRINCIPLES.md             # Architectural laws and constraints
│   ├── VOCABULARY.md             # Precise term definitions
│   ├── TASK_TEMPLATES.md         # Prompt structure examples
│   ├── ops/
│   │   ├── README.md             # Operations index
│   │   ├── clanklift.md          # CTW Hetzner → NAS migration
│   │   ├── diagnostic-surgery.md # Provenance reconciliation
│   │   ├── baseline-rebaseline.md
│   │   └── production-genesis.md
│   ├── anti-patterns.md          # Common mistakes to avoid
│   └── changelog.md              # When strategy changes
├── .claude-prompt                # Quick reference (see section 1.2)
├── README.md                     # Project README (existing)
└── [rest of repo]
```

### 1.2 Create `.claude-prompt` at Repo Root

This file is read automatically by coding-agent-aware workflows and contains standing instructions:

```
# Standing Instructions for Coding-Agent Work on unified-clank-platform

## BEFORE PASTING ANYTHING

1. Is this architectural/operational? Link it from .claude/ instead.
2. Is this implementation-specific? Specify: branch, file, Git SHA.
3. Is this a known operation? Reference .claude/ops/[operation].md.
4. Is this a recurring task? Use template from .claude/TASK_TEMPLATES.md.

## REFERENCE, DON'T PASTE

- Full orientation packet → Link .claude/CONTEXT.md
- Operations docs → Link .claude/ops/[name].md
- Architectural principles → Link .claude/PRINCIPLES.md
- Term definitions → Link .claude/VOCABULARY.md

## WHEN PASTING IS OK

- Specific error messages (paste the actual log)
- Code snippets under 50 lines (paste the relevant section)
- Exact Git diffs (paste the output of `git show`)
- A single failing test (paste the test + failure)

## EFFECTIVE PROMPT STRUCTURE

See .claude/TASK_TEMPLATES.md for full examples.

Minimum viable brief:
- Task/goal (1 sentence)
- Current state (Git branch, deployed revision, or file path)
- Specific blocker (what's failing/unclear)
- Constraints (what not to touch)

## DIAGNOSTIC CLANK INTEGRATION

Every migration/operation must report to Diagnostic Clank.
Every incident discovered must be logged.
See .claude/ops/README.md for submission process.

## DO NOT ASK A CODING AGENT TO

- Rewrite mature Clanks from scratch without strong reason
- Delete historical databases or state
- Enable experimental sources in production
- Trust product-page order as publication chronology
- Assume zero results means "nothing happened"
- Migrate another Clank while one is in flight
- Treat repository truth as deployment truth
- Add ML to deterministic problems
- Let a GUI secretly become an intelligence engine

See .claude/anti-patterns.md for the full list.
```

### 1.3 Move Existing Documents

**Day 1 action:** Copy these into `.claude/`:

1. **CONTEXT.md** ← Orientation packet (sections 1-35)
2. **PRINCIPLES.md** ← Architectural laws (sections 5, 7, 8, 24-25)
3. **VOCABULARY.md** ← Precise definitions (section 34)
4. **ops/clanklift.md** ← CLANKLIFT operation doc
5. **ops/diagnostic-surgery.md** ← Diagnostic Clank provenance doc

**Commit to main.** Do not wait.

This is foundational. Everything else flows from here.

---

## Part 2: Day-by-Day Prompt Evolution

### Session 1: Foundational Context

**Goal:** Establish shared understanding. This is the expensive session.

**What to include:**
- `.claude/CONTEXT.md` (may need to paste if large)
- `.claude/PRINCIPLES.md` (paste)
- Project link + Git SHA of current HEAD

**Example:**

```
I'm bringing you into the Clank newsroom intelligence system.

Repository: https://github.com/anil-ganti-nbc/unified-clank-platform
Current HEAD: a3d6969

Foundational context:
.claude/CONTEXT.md (orientation packet, ~7,500 words)
.claude/PRINCIPLES.md (architectural laws, ~2,000 words)
.claude/VOCABULARY.md (term definitions)

Initial task: [specific task]
```

**Token cost:** ~10,000 (acceptable, one-time investment)

**Expected outcome:** Shared understanding of Clank philosophy, architecture, and vocabulary.

---

### Sessions 2-10: Reference-Based Work

**Goal:** Maximize productive work, minimize context overhead.

**What to include:**
- Specific task (1-2 sentences)
- Current state (Git branch, deployed revision, file path)
- Blocker or question
- Link to relevant `.claude/` docs if specialized

**Example (Clank debugging):**

```
Task: Debug Smartphone Clank scheduler misfires on Hetzner

Current state:
- Branch: develop/smartphone-scheduler-fix
- Deployed SHA: 3c4f8a2
- Blocker: APScheduler producing ~10 misfires/week

See .claude/PRINCIPLES.md (section "Scheduling model") for context.
See .claude/ops/diagnostic-surgery.md (section "Scheduler") for related work.

Error log:
[paste actual error, 50-100 lines max]

What's the root cause?
```

**Token cost:** ~500-1,000 (productive work, not re-context)

**Expected outcome:** Focused solution without architectural re-explanation.

---

### Sessions 11+: Minimal Overhead

**Goal:** Single-sentence setup for focused tasks.

**What to include:**
- Task name (should reference a known operation or Clank)
- Immediate blocker
- Optional: link to relevant doc section if unclear

**Example (Migration follow-up):**

```
CLANKLIFT CTW migration: Soak day 2 comparison.

Hetzner articles: 5,704 | NAS articles: 5,702
Difference: 2 articles. Are these expected?

See .claude/ops/clanklift.md section 13 for parity expectations.
```

**Token cost:** ~200 (minimal overhead, maximum productivity)

**Expected outcome:** Targeted answer without architectural review.

---

## Part 3: How to Reference Without Pasting

### 3.1 Link Pattern for Architecture

**❌ Wrong:**
```
[pastes entire 47-section architecture spec]

"Implement feedback contract"
```

**✅ Right:**
```
Implement human feedback contract for Unified.

Reference: .claude/ops/feedback-contract.md
Repo: unified-clank-platform
Current file: schemas/feedback.py (doesn't exist yet)

Specific question: How should FeedbackRecord handle scope semantics?
```

### 3.2 Link Pattern for Operations

**❌ Wrong:**
```
[pastes 19-section CLANKLIFT document]

"Execute this"
```

**✅ Right:**
```
Operation: CLANKLIFT for Chinese Tech Wire

See .claude/ops/clanklift.md for full procedure.

Status: Live backup complete, now at restore rehearsal (step 4)
Current blocker: Restore script integrity check failing

Error:
[paste actual error, not the entire operation doc]
```

### 3.3 Link Pattern for Principles

**❌ Wrong:**
```
[pastes all architectural principles]

"Should we do X or Y?"
```

**✅ Right:**
```
Question: Should we enable experimental sources during baseline creation?

See .claude/PRINCIPLES.md "Baselines are explicit" for relevant principle.

Context: We're onboarding Lenovo as a new source for OEM Radar.
```

### 3.4 When to Actually Paste

Paste (and only paste) these:

1. **Actual error messages** (exact stack trace, 50-200 lines)
2. **Code snippets** (the failing function, not the whole file)
3. **Git diffs** (output of `git diff` or `git show`)
4. **Test failures** (test code + failure message)
5. **Database output** (query results, actual counts)
6. **Log excerpts** (relevant lines from a run log)

**Never paste:**
- Entire architectural documents
- Full operations manuals
- Complete module files (quote specific functions instead)
- Full config files (quote relevant sections)
- Database schema dumps (link to the schema file)
- Entire test suites (link to test file + quote failing test)

---

## Part 4: Language and Structure

### 4.1 Effective Prompt Structure (Universal)

**Regardless of task type, use this order:**

1. **Task** (1 sentence: what are you asking a coding agent to do?)
2. **Context** (current state: Git branch, deployed revision, file path, or operation name)
3. **Blocker** (what's not working or unclear?)
4. **Reference** (link to .claude/ docs if applicable)
5. **Evidence** (error message, code, log excerpt—only if relevant)
6. **Question** (what specifically do you want to know?)

**Example (debugging):**

```
Task: Fix Smartphone Clank's identity resolution for Samsung regional variants

Context:
- Branch: develop/samsung-identity-fix
- Current file: clanks/smartphone/samsung_identity.py
- Latest natural run failed: 3 hours ago

Blocker: Samsung India and Samsung US are merging into single identity

Reference:
.claude/PRINCIPLES.md ("Identity requires evidence")
.claude/VOCABULARY.md ("canonical identity")

Evidence:
Error log from 3-hour failure:
[paste actual error, 30-50 lines]

Question: What identity field (ASIN, PSREF, SKU, URL slug, H1) should be canonical for Samsung regional variants?
```

**Token cost breakdown:**
- Task + context + blocker: ~100 tokens
- Reference: 0 (it's a link)
- Evidence: ~200 tokens
- Question: ~30 tokens
- **Total: ~330 tokens**

Compare to: pasting the full Smartphone Clank orientation (~2,500 tokens). **87% savings.**

---

### 4.2 Language: Use This

**✅ Effective language patterns:**

- "Reference: [link]" (the coding agent knows to check the doc)
- "See .claude/PRINCIPLES.md (section 'name')" (precise navigation)
- "Current state: [branch] [file] [symptom]" (clear context)
- "Blocker: [what's not working]" (direct statement)
- "Error log: [actual output]" (evidence, not interpretation)
- "Should we X or Y?" (clear question)
- "Why is [specific observation] happening?" (diagnostic)

**✅ Effective structure words:**

- "Reference:" (this is external knowledge)
- "Context:" (current state)
- "Blocker:" (what's stuck)
- "Evidence:" (actual data)
- "Question:" (what we're solving)
- "Constraint:" (what not to do)
- "Expected:" (what should happen)

---

### 4.3 Language: Avoid This

**❌ Ineffective patterns (token waste):**

- Pasting entire documents when linking works
- "Can you explain [huge topic]?" when a link exists
- "Let me tell you about our entire system" before the actual question
- Burying the actual question in prose
- Asking the coding agent to rediscover information from multiple sessions ago
- "I'm not sure if this is important, but..." (be direct)

**❌ Avoid these structures:**

```
# Wrong: Narrative brain-dump
"So we've been working on this system for two months and there's this
thing with the scheduler and I'm not sure what's happening but it might
be related to the locking mechanism and also we updated the database
schema recently and I'm wondering if that could be causing issues..."

# Right: Structured problem
Task: Debug scheduler misfires in Smartphone Clank
Branch: develop/scheduler-fix
Deployed SHA: 3c4f8a2
Blocker: ~10 misfires/week, APScheduler lock behavior unclear
Evidence: [error log excerpt]
Question: Root cause?
```

---

### 4.4 Language: For Different Agent Types

**If you're a human:**

Use structured format above. You're paying attention and likely know what information is relevant.

**If you're an AI agent (like coding agent or future agents):**

Add these fields automatically:

```
Agent: [your name/model]
Task: [what you're doing]
Confidence: [high/medium/low on relevance]
Reference: [what .claude/ docs apply]
Fallback: [what to do if unclear]
```

Example:

```
Agent: coding agent (debugging task)
Task: Trace Smartphone Clank identity failures
Confidence: Medium (unsure if problem is identity resolution or discovery)
Reference: .claude/PRINCIPLES.md, .claude/ops/diagnostic-surgery.md
Fallback: Report to Diagnostic Clank with exact query

Error from latest run:
[paste error]

Root cause analysis?
```

---

## Part 5: Reference Semantics

### 5.1 What `.claude/` Docs Mean

When you link a document, you're saying:

- **"Read this for background"** — Document provides relevant context
- **"This is authoritative"** — Document is the source of truth
- **"Don't paste this again"** — Document is referenced, not repeated
- **"Future agents should know this"** — Document is canonical

**Therefore:**

When you link `.claude/PRINCIPLES.md`, the coding agent understands:
- Those principles are real constraints on the system
- Violating them requires strong justification
- The document is preserved across sessions
- Other agents will also reference it

### 5.2 How the coding agent Uses Links

When you say:

```
See .claude/PRINCIPLES.md (section "Baselines are explicit")
```

the coding agent will:
1. Note that a principle exists
2. Apply it to the current question
3. Not ask you to re-explain it in future sessions
4. Refer other agents to the same document

**You do not need to paste the content.**

the coding agent understands structural links. Use them.

### 5.3 Cross-Session Reference

**Session 1:**
```
CONTEXT: .claude/CONTEXT.md, .claude/PRINCIPLES.md

Task: Build OEM Radar source coverage
```

**Session 5:**
```
Task: Debug OEM Radar Lenovo discovery

Reference: .claude/ops/clanklift.md (related source work)

Blocker: Only 6/50 known stories discovered
```

**Session 12:**
```
OEM Radar source audit: Which sources are production-ready?

Reference: .claude/ops/baseline-rebaseline.md (baseline semantics)
```

**Notice:** No re-pasting. the coding agent can retrieve the principles. Other agents can reference them. Tokens stay in productive work.

---

## Part 6: Specific Patterns by Task Type

### 6.1 Implementation Tasks

**Template:**

```
Task: [What you're building]

Repo: unified-clank-platform
Branch: [feature branch name]
File: [file path or "new file"]

Current state:
- [What exists now]
- [Relevant test status]

Blocker:
[What's stuck]

Constraint:
Do not [what to avoid]

Reference:
.claude/PRINCIPLES.md (if architectural)
.claude/ops/[operation].md (if related to known operation)

Code context:
[Paste only the relevant function/class, 20-50 lines]

Question:
[Specific implementation question]
```

**Example:**

```
Task: Implement FeedbackRecord schema for Unified

Repo: unified-clank-platform
Branch: feature/human-feedback-contract
File: schemas/feedback.py (new)

Current state:
- Four dispositions defined (USEFUL, NOT_USEFUL, FALSE_POSITIVE, OUT_OF_STOCK)
- Feedback store separate from observation tables
- Tests don't exist yet

Blocker:
How should scope field work? (THIS_FINDING_ONLY vs THIS_SOURCE_PATTERN vs custom)

Constraint:
Do not implement ML during this task
Do not modify child Clank databases

Reference:
.claude/ops/feedback-contract.md (section 18 discusses scope)

Question:
Should scope be: enum, string, JSON, or relationship to a scopes table?
```

**Token cost:** ~400 (focused, not architectural)

---

### 6.2 Debugging Tasks

**Template:**

```
Task: Debug [Clank name] [what's broken]

Deployed revision: [Git SHA]
Branch: [if local work]

Symptom:
[What you observe]

Expected:
[What should happen]

Evidence:
[Error log, 50-100 lines max]

Reference:
.claude/PRINCIPLES.md (section if relevant)

Question:
Root cause?
```

**Example:**

```
Task: Debug Smartphone Clank scheduler misfires

Deployed revision: 3c4f8a2
Blocker: ~10 misfires/week on Hetzner

Symptom:
APScheduler fires late or not at all. Audit shows 226 recorded misfires.

Expected:
Hourly execution, every 60 minutes ±30 seconds

Evidence:
Scheduler log excerpt:
[paste relevant log lines, ~50 lines]

Reference:
.claude/PRINCIPLES.md (section "Scheduling model")
.claude/ops/diagnostic-surgery.md (section "Scheduler")

Question:
Why is APScheduler misaligned? Is it the single-lane architecture?
```

**Token cost:** ~600 (includes evidence)

---

### 6.3 Migration/Operation Tasks

**Template:**

```
Operation: [Operation name]

Reference: .claude/ops/[operation].md (full procedure)

Current status:
[Which step you're on]

Previous outcomes:
[What worked before]

Current blocker:
[What's stuck]

Evidence:
[Error, log excerpt, or count comparison]

Question:
[What specifically do you need help with]
```

**Example:**

```
Operation: CLANKLIFT CTW migration

Reference: .claude/ops/clanklift.md

Current status:
Live backup complete and verified
Now at: restore rehearsal (step 4)

Previous outcomes:
Backup: successful
Backup checksum: 3f4a8c2 (verified)
Backup size: 2.1 GB

Current blocker:
Restore script failing on schema validation

Error:
[paste actual error, 30-40 lines]

Question:
Is this a schema version mismatch or a restore script bug?
```

**Token cost:** ~500 (evidence-driven, minimal re-context)

---

### 6.4 Architecture/Design Tasks

**Template:**

```
Question: [Architectural decision needed]

Reference:
.claude/PRINCIPLES.md (relevant sections)
.claude/VOCABULARY.md (definitions)
.claude/ops/[operation].md (if related to known operation)

Context:
[Why you're asking]

Constraints:
[What must be true]

Options:
A) [Option A with tradeoffs]
B) [Option B with tradeoffs]

Evidence:
[Relevant data, metrics, or history]

Question:
Which approach and why?
```

**Example:**

```
Question: How should Diagnostic Clank report feedback-derived suppression decisions?

Reference:
.claude/PRINCIPLES.md (sections "Feedback must survive" and "Feedback-informed decision provenance")
.claude/ops/feedback-contract.md (section 36)

Context:
We're designing how to record why the system suppressed/prioritized a finding.
Other Clanks will query this later. Need to make reversibility auditable.

Constraints:
- Must record exact rule/model/feedback version
- Must be queryable by future Diagnostic Clank
- Must survive Production Genesis

Options:
A) Extra column in Feedback table: [suppression_reason, rule_version, timestamp]
B) Separate SuppressionDecision table linked to Feedback
C) JSONL event log alongside the feedback DB

Question:
Which design preserves auditability + allows future reversibility?
```

**Token cost:** ~600 (structured question, reference-based)

---

## Part 7: Anti-Patterns and What NOT to Do

### 7.1 Token Waste Patterns

**❌ Pattern: Pasting the entire orientation every session**

```
[pastes 7,500-word orientation packet]
[pastes 3,500-word architecture spec]
[pastes 2,000-word operation manual]

"Can you help?"
```

**Cost:** ~13,000 tokens wasted on re-context

**✅ Fix:** Link the document

```
See .claude/CONTEXT.md and .claude/PRINCIPLES.md

Can you help with [specific task]?
```

**Cost:** ~0 tokens for context (already established)

---

**❌ Pattern: Asking the coding agent to re-explain something it already knows**

```
Session 1: [pasts full orientation]
Session 2: "Can you remind me what a Clank is?"
Session 5: "What are the four dispositions again?"
Session 10: "How does baseline work?"
```

**Cost:** ~2,000-3,000 tokens per re-explanation × sessions = massive waste

**✅ Fix:** Use internal links

```
Session 2: See .claude/VOCABULARY.md (Clank definition)
Session 5: See .claude/VOCABULARY.md (dispositions)
Session 10: See .claude/PRINCIPLES.md (Baselines are explicit)
```

**Cost:** ~0 tokens (already stored)

---

### 7.2 Prompt Anti-Patterns

**❌ Brain-dump prompts:**

```
"So there's this Clank and it does things and sometimes it breaks and I'm
wondering if you can help me understand why. Also we have databases and
they have state and sometimes the state is wrong. Oh, and there's this
scheduler thing..."
```

**✅ Structured prompts:**

```
Task: Debug [Clank] [symptom]

Current state: [Git SHA]
Blocker: [what's not working]
Evidence: [error/log]
Question: [specific question]
```

---

**❌ Asking the coding agent to make foundational decisions during implementation:**

```
"I'm about to implement the feedback contract. Should it be in one table or
three? Should scope be enum or string? How should supersession work? What
about TTL? Should we do ML? How do we handle..."
```

**This is trying to do architecture + implementation in one expensive session.**

**✅ Separate concerns:**

```
# Session 1: Architecture decision
Question: Feedback schema design (scope, supersession, TTL)
See .claude/ops/feedback-contract.md
Options: [A, B, C]
Decision: [chosen approach]

# Session 2: Implementation
Task: Implement FeedbackRecord schema
Architecture decision: [link to session 1 decision]
File: schemas/feedback.py
Blocker: [specific implementation issue]
```

---

**❌ Treating operations docs as implementation input:**

```
[Pastes entire CLANKLIFT doc]
"Execute this"
```

**the coding agent does not need the full doc. It needs the current status.**

**✅ Operations with focus:**

```
Operation: CLANKLIFT CTW
Status: Step 4 (restore rehearsal), currently failing on schema check
Reference: .claude/ops/clanklift.md
Blocker: [specific error]
```

---

### 7.3 Communication Anti-Patterns

**❌ Ambiguous pronouns:**

```
"It broke when we tried to do that thing with the other system."
```

**✅ Explicit references:**

```
"Smartphone Clank's scheduler broke when we migrated to NAS."
```

---

**❌ Vague severity:**

```
"Something might be wrong with the database."
```

**✅ Specific observation:**

```
"OEM Radar went from 300 articles to 3 articles after the source refresh."
```

---

**❌ Hypothesis disguised as fact:**

```
"The identity resolution is broken."
```

**✅ Observation + hypothesis:**

```
"Samsung India and Samsung US merged into a single product.
Hypothesis: identity resolution is conflating regional variants."
```

---

## Part 8: Governance and Maintenance

### 8.1 Who Owns `.claude/` Docs?

**CONTEXT.md, PRINCIPLES.md, VOCABULARY.md:**
- Owner: Architecture lead (Anil)
- Update when: System behavior changes fundamentally
- Frequency: ~monthly

**ops/*.md (operations procedures):**
- Owner: Operations lead
- Update when: Procedure changes or new operation defined
- Frequency: ~per operation

**TASK_TEMPLATES.md:**
- Owner: Any agent
- Update when: New task type emerges or pattern changes
- Frequency: ~quarterly

**anti-patterns.md:**
- Owner: Any agent
- Update when: New anti-pattern discovered
- Frequency: ~as discovered

### 8.2 When to Update `.claude/` Docs

**Update immediately when:**
- A principle changes (architecture shift)
- An operation procedure changes (new step required)
- A term's meaning shifts (vocabulary change)
- A new operation is defined

**Update when convenient when:**
- New anti-patterns discovered
- Task templates prove ineffective
- Link targets move

**Do not update:**
- Because one session used different language
- Because a better organizing principle occurred to someone
- Preemptively "just in case"

**Change discipline:**
1. Update the doc
2. Commit to main
3. Reference the change in `.claude/changelog.md`

```
# .claude/changelog.md

## 2026-08-19

### ops/clanklift.md
- Added section on NAS backup verification
- Clarified restore isolation requirements
- Updated Diagnostic Clank reporting link

### PRINCIPLES.md
- Added "Deployed truth beats repository truth" (previously implied)
```

### 8.3 Onboarding New Agents

**For any new agent joining Clank work:**

1. Read `.claude/README.md` (5 minutes)
2. Read `.claude/CONTEXT.md` (30 minutes, one-time)
3. Read `.claude/TASK_TEMPLATES.md` (10 minutes)
4. Reference docs as needed for specific work

**Total onboarding cost:** ~5,000-7,000 tokens (acceptable investment)

**Every session after:** ~200-500 tokens (productive work)

### 8.4 Deprecating Old Documents

**When a `.claude/` doc becomes obsolete:**

1. Add a deprecation notice at the top:

```markdown
⚠️ **DEPRECATED** (2026-08-20)

This document describes [old approach].

See [NEW_DOCUMENT.md] for current procedure.

Preserved for historical reference only.
```

2. Keep it in the repo (historical record)
3. Update links in other docs
4. Reference the new document instead

**Never delete `.claude/` docs.** They're historical knowledge.

---

## Part 9: Token Budgeting and Accounting

### 9.1 Typical Token Costs (Per Session)

| Task Type | Cost | Notes |
|-----------|------|-------|
| Architecture decision | 800-1,200 | Structured question, reference-based |
| Implementation (focused) | 400-800 | Specific file, clear blocker |
| Debugging | 600-1,200 | Error logs + question |
| Migration step | 500-1,000 | Status + specific blocker |
| Code review | 300-600 | Context already known, focused feedback |
| Architecture re-explanation (❌) | 2,000-5,000 | Waste: use links instead |
| Full doc paste (❌) | 3,000-10,000 | Waste: link instead |

### 9.2 Sample Week Budget

**Scenario:** 10 work sessions, ~50k token budget

**Suboptimal approach (current):**
- Session 1: Paste orientation (7,500 tokens)
- Sessions 2-10: Each pastes ops docs (3,500 × 5 = 17,500)
- Actual work: 3,000 tokens
- **Total: 28,000 tokens | Productive: 3,000 (11%)**

**Optimized approach:**
- Session 1: Link orientation (7,500 tokens, necessary)
- Sessions 2-10: Reference links (200 × 9 = 1,800)
- Actual work: 40,000 tokens
- **Total: 49,300 tokens | Productive: 40,000 (81%)**

**Difference:** 37,000 additional tokens for productive work per week.

---

## Part 10: FAQ and Troubleshooting

### Q: What if the `.claude/` docs don't have exactly what I need?

**A:** That's a signal to update the docs.

1. Add the missing content to the appropriate `.claude/` file
2. Commit to main
3. Update `.claude/changelog.md`
4. Then reference it in your prompt

**Don't work around gaps.** Fill them.

---

### Q: What if a doc is very long and the coding agent still needs more context?

**A:** That's fine. Link the main doc + paste a specific section:

```
Reference: .claude/ops/clanklift.md

For detailed context on restore semantics:
[paste section 4 of the doc, 200-300 lines]

Current blocker: [specific issue]
```

**Cost: ~500 tokens + reference**

---

### Q: Should I paste an error log or just describe it?

**A:** Always paste actual errors and logs.

```
✅ Good:
Error:
```
ConnectionError: unable to connect to database
  File "clanks/smartphone/collector.py", line 42, in fetch
    db.query("SELECT * FROM articles")
  sqlite3.OperationalError: database is locked
```

❌ Bad:
"The database is locked for some reason."
```

**Pasting actual errors costs tokens but saves back-and-forth.**

---

### Q: Can I ask a coding agent to update `.claude/` docs?

**A:** Yes, but review the changes before committing.

**Process:**

1. Ask the coding agent to update `.claude/ops/[operation].md` with new step
2. the coding agent provides updated document
3. You review for accuracy
4. You commit to main
5. Reference updated doc in future prompts

**Don't commit coding-agent-generated docs without review.** The docs are authoritative.

---

### Q: What if an operation is in-flight and we discover a new issue mid-way?

**A:** Report it to Diagnostic Clank, update `.claude/ops/[operation].md` if the procedure needs to change, and continue.

```
Operation: CLANKLIFT CTW
Status: Step 6, discovered new issue
Diagnostic Clank report ID: [ID]
Issue: [description]
Updated procedure: [if relevant]
```

---

### Q: How do I know when to reference vs. paste?

**Simple rule:**

- **Reference** if it's in `.claude/` (always)
- **Paste** if it's an error, log, code snippet, or specific data (always)
- **Never paste** architectural docs, full operation manuals, or full specifications

---

## Part 11: Example Session Sequence

### Session 1: Onboarding

```
Welcome to the Clank newsroom intelligence system.

Repository: https://github.com/anil-ganti-nbc/unified-clank-platform
Current HEAD: a3d6969

Foundational reading:
- .claude/CONTEXT.md (orientation packet, ~7,500 words)
- .claude/PRINCIPLES.md (architectural laws, ~2,000 words)
- .claude/VOCABULARY.md (term definitions, ~1,000 words)

Start here: .claude/README.md

Immediate task: [task]
```

**the coding agent reads the docs, understands the system, proceeds with task.**

**Token cost: ~10,000**

---

### Session 2: Follow-up Implementation

```
Task: Implement FeedbackRecord schema

Repo: unified-clank-platform
Branch: feature/human-feedback
File: schemas/feedback.py (new)

Reference:
.claude/ops/feedback-contract.md (architecture decided in session 1)

Blocker:
How to handle scope field (THIS_FINDING_ONLY vs THIS_SOURCE_PATTERN)?

Code context:
[paste similar schema from adjacent file, 30 lines]

Question:
What's the right Python type for scope?
```

**The coding agent references session 1 context via `.claude/` links and answers the focused question.**

**Token cost: ~500**

---

### Session 3: Debugging

```
Task: Debug OEM Radar Lenovo discovery

Branch: develop/lenovo-investigation
Deployed SHA: 2f3c8a9

Symptom:
Only 6/50 known Lenovo stories discovered (BANKAI benchmark)
[see .claude/ops/oem-radar.md for context]

Evidence:
Latest run log:
[paste relevant 50 lines]

Question:
Source gap or classification bug?
```

**The coding agent knows the benchmark context from the `.claude/` reference and answers about this specific run.**

**Token cost: ~700**

---

### Session 4: Architecture Decision

```
Question: Should we enable experimental Smile sources in production?

Reference:
.claude/PRINCIPLES.md (Baselines are explicit, Production epochs)
.claude/ops/baseline-rebaseline.md (baseline semantics)

Context:
Smartwatch Clank has 5 experimental sources (Garmin, Amazfit, Coros, Samsung, Apple).
We want to start capturing Garmin data but aren't ready for all 5.

Options:
A) Enable Garmin + 4 others (complete baseline at once)
B) Enable Garmin only (staged production epoch)
C) Keep experimental, do soak without production authority (parallel)

Question:
What's the right approach per our baseline/epoch laws?
```

**the coding agent references principles, answers architectural question.**

**Token cost: ~600**

---

### Session 5: Operation Execution

```
Operation: CLANKLIFT Smartwatch → NAS

Reference: .claude/ops/clanklift.md (general procedure)

Current status:
Step 3 (live production backup drill) - complete
Now at: Step 4 (restore rehearsal)

Blocker:
Restore script failing on dedup key preservation

Error:
[paste error, 40 lines]

Question:
Is this a data issue or script bug?
```

**the coding agent knows the operation structure from `.claude/` reference, focuses on this specific step.**

**Token cost: ~600**

---

## Part 12: Final Principles

### The Core Philosophy

1. **Architectural knowledge is durable.** Store it once, reference it many times.

2. **Tokens are finite.** Use them for productive work, not re-context.

3. **Explicitness reduces ambiguity.** "See .claude/PRINCIPLES.md" is clearer than pasting the doc.

4. **Specificity saves tokens.** "Debug Smartphone Clank scheduler" is cheaper than "We have issues with our system."

5. **Evidence matters.** Paste actual errors, logs, counts. Don't interpret them.

6. **Operations are repeatable.** Store procedures in `.claude/ops/`, not in chat history.

7. **Future agents matter.** Treat your prompts as templates for others.

8. **Governance prevents chaos.** Update `.claude/` docs, don't work around them.

---

## Checklist: Before You Prompt a coding agent

- [ ] Is this a known operation? Link `.claude/ops/[name].md` instead of pasting.
- [ ] Is this asking about a principle? Link `.claude/PRINCIPLES.md` instead of explaining.
- [ ] Is this asking a term definition? Link `.claude/VOCABULARY.md` instead of defining.
- [ ] Do I have a specific blocker? State it directly instead of describing the whole system.
- [ ] Am I pasting something that lives in `.claude/`? Replace with a link.
- [ ] Do I have an error or log? Paste the actual output, not my interpretation.
- [ ] Is my prompt structured (task/context/blocker/question)? If not, restructure.
- [ ] Am I asking a coding agent to re-explain something from session 1? Reference `.claude/` instead.
- [ ] Did I use precise terms from `.claude/VOCABULARY.md`? Yes? Good. No? Fix it.
- [ ] Would another agent understand this prompt? If not, clarify.

---

## Final Summary

This optimization strategy transforms coding-agent interaction from expensive context re-establishment to focused, productive work.

**Key changes:**

1. Move architectural/operational knowledge into `.claude/` (one-time cost)
2. Reference docs instead of pasting them (90% token savings per session)
3. Structure prompts consistently (faster answers, less ambiguity)
4. Use precise language from `.claude/VOCABULARY.md` (clearer intent)
5. Separate architecture decisions from implementation work (cheaper sessions)

**Result:**

- **Session 1:** Expensive but necessary (10,000 tokens)
- **Sessions 2-10:** Cheap and focused (500-1,000 tokens each)
- **Total productive work:** 80%+ of budget instead of 10%

**Investment:** 30 minutes to set up `.claude/` once.
**Payoff:** 2-3x more capacity per token budget, every session after.

---

**Document version:** 1.0
**Last updated:** 2026-08-19
**Status:** Canonical reference, all agents follow this strategy
**Owner:** Anil Ganti
**Feedback:** Update `.claude/changelog.md` when this strategy changes
