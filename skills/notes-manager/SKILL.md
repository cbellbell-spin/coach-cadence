---
name: notes-manager
description: >
  Apply this skill when reading or writing training history files, appending a session log entry,
  updating phase trends, or writing to the permanent record. Governs all reads and writes to
  the three-tier memory system. Trigger phrases: "log this", "update notes", "training history",
  "write to log", "save today's session", "flag this", "update my record".
---

# Notes Manager

Manages the three-tier memory system plus the two Mann-pattern artifacts. These files are
the plugin's persistent memory — they store what Whoop and Strava cannot give back: coaching
decisions made, the reasoning behind them, interpretations of patterns, and permanent history
that must survive across all training blocks.

**Core principle:** Whoop and Strava are live data sources. Pull them fresh. This system stores
only what those APIs cannot retrieve.

## Cowork Project folder

All files live in the Cowork Project folder for this athlete:

```
~/cowork/Projects/adaptive-training-coach/session-log.md         <- Tier 1: rolling session context
~/cowork/Projects/adaptive-training-coach/phase-trends.md        <- Tier 2: block-level trajectory
~/cowork/Projects/adaptive-training-coach/permanent-record.md    <- Tier 3: permanent history
~/cowork/Projects/adaptive-training-coach/user-profile.md        <- brief (onboarding profile)
~/cowork/Projects/adaptive-training-coach/source-of-truth.md     <- canonical training values
~/cowork/Projects/adaptive-training-coach/current-block-plan.md  <- draft (living training plan)
~/cowork/Projects/adaptive-training-coach/coaching-decisions.md  <- decisions (coaching rationale)
```

Create any file on first use if it does not exist.

---

## Tier 1: session-log.md

Rolling log of coaching sessions. Compact by design — no Whoop numbers, no Strava activity
stats. Those come from the live API. This file stores only what the APIs cannot give back.

### What goes in a session log entry

- The recommendation given and the key reasoning behind it
- Qualitative session notes: RPE, how it felt, physical flags, fueling adequacy
- Context that affects interpretation: "travel day", "work stress", "had a few drinks last
  night — explains the red recovery and not a fitness signal"
- Coach flags to carry forward: cardiac decoupling streak, HRV tripwire streak, sciatica
  watch, anything that will matter at the next session

### What does NOT go in the session log

- Raw Whoop recovery scores, HRV, RHR, sleep data — pull those fresh from the API
- Strava activity stats (duration, distance, power, elevation) — pull those fresh
- Intervals.icu zone distributions and TSS — pull fresh when needed

This keeps entries compact. A full training block fits comfortably without the file becoming
a liability to load.

### Entry format

Prepend new entries at the top.

```markdown
## [YYYY-MM-DD] - [Day of Week] - [WHOOP Color]
whoop_pulled: yes | no | manual
strava_last_pull: [ISO timestamp] | not pulled

**Recommendation:** [full narrative summary of what Coach recommended - enough context that
the next session understands the decision without re-deriving it from scratch]
**Key factors:** [what drove it - e.g., "Yellow recovery, 48-hr buffer clear, redirected to
Session B. Blocked intensity regardless of how legs feel."]
**Session notes:** [qualitative context that can't be retrieved - RPE, how session felt,
physical flags (back, L-side sciatica), fueling (adequate / skipped / partial), personal
context like travel or alcohol or illness]
**Coach flags:** [carry-forward observations - e.g., "Cardiac decoupling 11.3% - third time
above 10% this block. Durability ceiling may be approaching. Watch next two outdoor rides.",
"HRV tripwire 3 consecutive days. Not training load - travel pattern.", "Sciatica L-side
tightness after Session A today. Monitor."]

---
```

### Trimming the session log

Do NOT trim on a calendar schedule. The session log remains intact through a training block.
The right boundary is a training boundary: the end of a rest week, an event completion, a
phase transition - not an arbitrary seven days.

When a block transition is confirmed, verify that phase-trends.md has been updated to capture
the block's trajectory and flags, then trim the session log entries from the completed block.
Keep the current block's entries intact.

---

## Tier 2: phase-trends.md

Updated at meaningful training boundaries only - not at every weekly review. The right trigger
is a structural shift: a rest week concludes, a block ends, a fitness test produces a result,
an event completes.

This file captures trajectory and Coach's interpretations. Not raw data - patterns.

### When to write a new phase-trends entry

- A rest week concludes and a new build block starts
- An event completes (race, century, gran fondo)
- A fitness test produces a result (FTP, aerobic threshold)
- A pattern has solidified enough to name across multiple sessions
- A training block is classified complete

### Entry format

Prepend new entries at the top.

```markdown
## [Block Name] - [Date Range] - [Block Classification]
Written: [YYYY-MM-DD]

**Block summary:** [2-3 sentences: what this block accomplished, how it evolved, how it ended]
**Trajectory observations:**
- [Concrete patterns named across the block - not daily noise, but confirmed trends]
- E.g., "Cardiac decoupling improved from ~12% to ~4% over 8 outdoor rides. Durability
  building at current durations."
- E.g., "HRV tripwire triggered 4 times - all correlated with alcohol or travel, not load."
**Recovery patterns:** [HRV/RHR baseline shifts observed across the block, trend direction]
**Ongoing watches:** [flags still active carrying into the next block]
**Block outcome:** [fitness test result, event completed, FTP change, or "no formal test"]
**Carry-forward for next block:** [constraints, focus areas, warnings]

---
```

### When to read phase-trends.md

- Weekly review - provides block context for interpreting the week
- Morning check-in when a session-log pattern looks like it may be crossing to a trend
- Planning a new training phase - previous block's carry-forward is the starting point

---

## Tier 3: permanent-record.md

Append-only. Never trimmed, never deleted. Accumulates history that must survive all blocks.

### Structure

```markdown
# Permanent Record
> Append only. Never delete, never trim.

## DEXA Results
| Date | Body Fat % | Lean Mass (lbs) | Fat Mass (lbs) | Notes |
|------|-----------|-----------------|----------------|-------|

## FTP History
| Date | FTP (W) | Method | Notes |
|------|---------|--------|-------|

## Event Results
| Date | Event | Result / Notes |
|------|-------|----------------|

## Injury History
| Date | Injury | Status | Notes |
|------|--------|--------|-------|

## Strength Progression
### Session A
| Date | Step-up | RDL | Glute Bridge | Leg Curl | Calf Raise | Notes |
|------|---------|-----|-------------|---------|-----------|-------|

### Session B
| Date | Chest Press | Row | Shoulder Press | Notes |
|------|------------|-----|---------------|-------|

## Key Decisions
| Date | Decision | Reasoning |
|------|----------|-----------|
```

### What triggers a write to permanent-record.md

- DEXA scan results - always logged here immediately; ask for the date if not provided
- FTP update (via update-source-of-truth) - log old value, new value, date, and method
- Event result - after any event
- Injury flagged or resolved - date, description, status
- Strength loads changed - log-workout prompts for confirmation before writing here
- Key training decision worth preserving

### When to read permanent-record.md

- Planning a new training block - injury history and FTP trajectory set the starting point
- Evaluating strength progression over multiple blocks
- Any session where DEXA, long-term injury context, or FTP history is referenced

---

## Mann-pattern artifact: current-block-plan.md

The living training plan for the current block. Written and overwritten by weekly-review
each week. Read at session start by morning-check-in. This is the "draft" in Mann's
artifact-driven pattern — the document the coach and athlete are executing against.

### What it contains

- Block context (name, phase, weeks remaining, event countdown)
- Weekly structural targets (ride hours, strength sessions, intensity limit)
- This week's day-by-day plan
- Active constraints in effect
- Conservative tripwire
- Carry-forward from the previous block

### Read rules

- Read at every morning-check-in (steps 5)
- Read at weekly-review before delivering the assessment (step 4)

### Write rules

- Written by weekly-review at Step 2 (after the weekly assessment, before block boundary check)
- Overwritten entirely each week — it reflects the current plan, not a history
- Do not write to this file from other skills without explicit instruction
- History is preserved in phase-trends.md and session-log.md

---

## Mann-pattern artifact: coaching-decisions.md

The coaching rationale log. Written by session-close skill after confirmed coaching calls.
Read at session start by morning-check-in. This is the "decisions" file in Mann's pattern.

### What it contains

Non-obvious coaching calls and the reasoning behind them. Not activity summaries — those
belong in session-log.md. Not recovery stats — those come from the API. Only the reasoning
that the next session should not have to re-derive from scratch.

### Entry format

Prepend new entries at the top.

```markdown
## [YYYY-MM-DD] — [one-line call summary]
[2-3 sentences: what the coach called, and why — the reasoning that shouldn't be re-derived]

---
```

### Read rules

- Read 4 most recent entries at every morning-check-in (step 6)
- Load more entries when a session involves reviewing a pattern across multiple weeks

### Write rules

- Written by session-close skill only
- User must confirm each proposed entry before it is written
- Prepend new entries at the top
- Entries older than 6 weeks are pruned on confirmation during session-close

### What goes in coaching-decisions.md vs. session-log.md

| coaching-decisions.md | session-log.md |
|------------------------|----------------|
| Why the coach called it | What the coach called |
| Pattern interpretation applied | Active flags to carry forward |
| Conservative override reasoning | Qualitative session notes (RPE, physical) |
| Named constraint and what it guards against | Personal context (travel, alcohol, stress) |

---

## Write rules (all files)

- Always read the file before writing - never overwrite without intent. Tier 1 and 2: prepend.
  Tier 3: append. current-block-plan.md: overwrite. coaching-decisions.md: prepend.
- Write Whoop pull status to session-log immediately after pulling
- Update strava_last_pull immediately after every Strava pull
- Do not write to source-of-truth.md except via update-source-of-truth
- Do not auto-update permanent-record.md strength loads without confirmation
- Do not write to coaching-decisions.md without user confirmation (session-close handles this)
- If a file does not exist, create it with section headers and first entry

## Read rules

- Always load session-log.md before generating a daily recommendation
- Check whoop_pulled before any Whoop API call - skip if already pulled today
- Check strava_last_pull before any Strava API call - skip if pulled within last 4 hours
  unless user reports a completed activity
- Load phase-trends.md at weekly review and when a pattern may be crossing to a trend
- Load permanent-record.md when training history depth is relevant
- Read current-block-plan.md at every morning-check-in and weekly review
- Read last 4 entries of coaching-decisions.md at every morning-check-in
- If files are missing or empty, note this and proceed - do not fabricate history

## Migration from previous model

If daily-log.md and weekly-summary.md exist from the old model:
- Do not delete them. Preserve as-is.
- Begin writing new entries to session-log.md and phase-trends.md going forward.
- On the next rest week or block transition, migrate Coach interpretations into phase-trends.md
  and strength progression history into permanent-record.md.
- After migration confirmed, rename old files to daily-log-archived.md and
  weekly-summary-archived.md.

## User profile

user-profile.md is written by onboarding and read at every session start. Unchanged.
Read alongside session-log.md before generating any recommendation. [pending] fields have
not been answered - do not assume values. [declined] fields - do not re-ask unless directly
relevant.
