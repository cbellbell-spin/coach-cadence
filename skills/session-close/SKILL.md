---
name: session-close
description: >
  Reflector skill run at the end of any coaching session. Scans the conversation for
  non-obvious coaching calls, proposes entries for coaching-decisions.md, waits for
  confirmation before writing. Prunes decisions older than 6 weeks. Trigger phrases:
  "session close", "close session", "log this call", "save coaching decisions", "end session".
---

# Session Close

Captures the coaching rationale from this session into coaching-decisions.md. Runs
after the coaching call has been delivered and any post-session notes have been provided.

coaching-decisions.md is NOT a session log. The session log records what happened.
This file records *why the coach called it that way* — the reasoning behind non-obvious
decisions that the next session should not have to re-derive from scratch.

Not every session warrants an entry. Skip if the call was routine and the reasoning
is obvious from the data. Write when the decision involved nuance, an override, a
pattern interpretation, or a constraint the session log alone wouldn't preserve.

---

## Steps

### Step 1 — Scan the conversation for decision-worthy calls

Look for any coaching decision that meets one or more of these criteria:

- Conservative override: coach stepped down from what recovery data would suggest
- Pattern interpretation: a one-day signal was read as part of a trend
- Explicit constraint applied: 48-hour buffer, decoupling flag, HRV tripwire, GLP-1 ceiling
- Rationalization flagged: coach named a pattern and held the call despite pushback
- Block-level context applied: decision driven by where we are in the block, not just today's data
- Non-obvious tradeoff: chose X over Y for a reason worth preserving

Routine calls (green recovery → recommended training, red → rest) do not need entries
unless something about the reasoning was notable.

### Step 2 — Propose entries

Present proposed entries to Chris before writing. Format each as:

```
[YYYY-MM-DD] — [one-line call summary]
[2-3 sentences: what the coach called, and why — the reasoning that shouldn't be re-derived]
```

Example:
```
2026-06-04 — Rest day despite 74% green recovery
Three consecutive high-strain days pushed cumulative load beyond what the single-day
score reflected. Holding rest here rather than banking another session — risk of
short-term fitness loss is lower than risk of digging a hole that takes a week to climb out of.
```

Say: "Here's what I'd log to coaching-decisions.md — confirm to write, or edit before I save:"

Present all proposed entries. Wait for explicit confirmation or edits before writing.

### Step 3 — Write confirmed entries

Load `notes-manager` skill.

Write confirmed entries to coaching-decisions.md per the format in notes-manager.
Prepend new entries at the top.

### Step 4 — Prune stale entries

After writing, check coaching-decisions.md for entries older than 6 weeks from today.

If stale entries exist, ask: "There are [N] entries older than 6 weeks. Prune them?"

If confirmed: remove entries older than 6 weeks. Never prune entries within the 6-week
window, regardless of count.

If not confirmed: leave as-is and note in session summary.

### Step 5 — Session summary

Confirm to Chris:
- How many entries were written to coaching-decisions.md
- Whether any entries were pruned
- One-line reminder: "coaching-decisions.md = coaching logic. session-log.md = what happened."

---

## What goes in an entry vs. what doesn't

**Write to coaching-decisions.md:**
- Reasoning behind a conservative override
- A pattern interpretation applied across multiple data points
- Why a specific constraint was applied today and what it's guarding against
- A named rationalization pattern and why the coach held firm

**Do NOT write to coaching-decisions.md:**
- Activity stats (power, duration, distance) — those live in Strava
- Recovery scores (HRV, RHR, WHOOP color) — those come from WHOOP API
- Routine call summaries — those belong in session-log.md
- Personal notes (RPE, how session felt) — those belong in session-log.md

---

## Triggering

This skill is prompted automatically at the end of daily-coaching and morning-check-in
sessions. It can also be invoked directly. The user must confirm before any write occurs.
