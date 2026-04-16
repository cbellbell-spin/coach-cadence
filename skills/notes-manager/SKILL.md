---
name: notes-manager
description: >
  Apply this skill when reading or writing training history files, appending a daily log entry,
  updating the weekly summary, or when context about past training days is needed. Trigger phrases:
  "log this", "update notes", "what happened last week", "training history", "write to log",
  "save today's session". This skill governs all reads and writes to rolling history files.
---

# Notes Manager

Manages two rolling history files. These are the plugin's memory — they provide the context that makes daily and weekly recommendations accurate over time.

## File locations

```
~/cowork/Projects/[coach-folder]/daily-log.md       ← 7-day rolling
~/cowork/Projects/[coach-folder]/weekly-summary.md  ← 6-week rolling
~/cowork/Projects/[coach-folder]/user-profile.md    ← onboarding profile
~/cowork/Projects/[coach-folder]/source-of-truth.md ← canonical training state
```

Create daily-log.md and weekly-summary.md on first use if they do not exist.

## Daily log format

Prepend new entries at the top. Trim entries older than 7 days from the bottom.

```markdown
## [YYYY-MM-DD] — [Day of Week] — [WHOOP Color]
whoop_pulled: yes | no | manual
strava_last_pull: [ISO timestamp] | not pulled

**Recovery:** [score]% | HRV: [X]ms | RHR: [X] bpm | Sleep: [X]h ([X]% perf)
**Strain (prior day):** [X.X]
**Activities:**
- [activity name] — [type] — [duration] — [distance] — [elevation]
  [Intervals.icu if outdoor ride:]
  HR zones: Z1 X% | Z2 X% | Z3 X% | Z4 X% | Z5 X%
  Power zones: Z1 X% | Z2 X% | Z3 X% | Z4 X% | Z5 X%
  Cardiac decoupling: X.X% [excellent / acceptable / concern]
  NP: XW | IF: X.XX | TSS: XXX
**Recommendation given:** [one-line summary]
**Notes:** [manual context — RPE, how session felt, physical flags, fueling]

---
```

**Flag meanings:**
- `whoop_pulled: yes` — Whoop data pulled from API today, do not pull again
- `whoop_pulled: no` — not yet pulled
- `whoop_pulled: manual` — user provided values manually
- `strava_last_pull` — ISO timestamp of last Strava API call; used to determine if 4-hour refresh is due

## Weekly summary format

Prepend new entries at the top. Trim entries older than 6 weeks from the bottom.

```markdown
## Week of [YYYY-MM-DD] — [Week Classification]

**Riding:** [X] hrs | [X] rides | [X] intensity sessions
**Strength:** [X]/2 sessions completed
**WHOOP trend:** [mostly green / mixed / mostly yellow-red]
**Avg HRV:** [X]ms | **Avg RHR:** [X] bpm | **Avg Sleep:** [X]h
**Longest ride:** [X] hrs | Cardiac decoupling: [X.X%] (if captured)
**Event countdown:** [X weeks to May 3] (or post-event phase)
**Healthspan Age:** [X] (if captured)

**Summary:** [2–3 sentences: what went well, what didn't, what to carry forward]
**Next week plan:** [week type + key recommendations]

---
```

## Write rules

- Always read the file before writing — never overwrite, always prepend
- Only append to monthly notes in source-of-truth.md — never edit existing entries
- Do not write to source-of-truth.md except via `/update-source-of-truth`
- Write Whoop data to the log immediately after pulling — before generating any recommendation
- Update `strava_last_pull` timestamp immediately after every Strava pull
- If a file doesn't exist, create it with a header comment and the first entry

## Read rules

- Always load daily-log.md before generating a daily recommendation
- Always load weekly-summary.md before generating a weekly review
- Check `whoop_pulled` flag before any Whoop API call
- Check `strava_last_pull` before any Strava API call — skip if pulled within last 4 hours unless user reports a completed activity
- If files are missing or empty, note this and proceed without historical context — do not fabricate history

## User profile

`user-profile.md` — written by /onboarding, read at every session start.

- Read alongside daily-log.md before generating any recommendation
- Use to personalize tone, explanation depth, and directness per user preferences
- [pending] fields have not been answered — do not assume or invent values
- [declined] fields — do not re-ask unless directly relevant to a specific recommendation
- When new profile information is gathered mid-session, write it to the file immediately
