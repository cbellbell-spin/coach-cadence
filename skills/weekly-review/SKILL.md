---
name: weekly-review
description: >
  Review the past week's training and recovery data, classify the week, plan the upcoming
  week, and - when at a block boundary - write a phase-trends entry capturing the block's
  trajectory. Trigger phrases: "weekly review", "week review", "how was my week",
  "plan next week", "end of week".
---

# Weekly Review

Run at the start of each week (Sunday evening or Monday morning). Generates a structured
assessment and forward plan. Also determines whether this week represents a training block
boundary, and if so, writes to phase-trends.md.

## Steps

1. Load `training-knowledge` skill and `notes-manager` skill
2. Read `session-log.md` - recent coaching context, active flags, qualitative session notes
3. Read `phase-trends.md` - current block context and classification
4. Read `current-block-plan.md` (if it exists) - compare last week's execution against the plan
5. Pull Whoop data:
   - `whoop_get_recovery_range` (last 7 days)
   - `whoop_get_sleep_range` (last 7 days)
   - `whoop_get_strain_range` (last 7 days)
   - `whoop_get_training_summary`
6. Pull Strava activities (last 7 days)
7. Ask Chris for any context not captured in data: upcoming constraints (travel, work stress),
   any pain or niggles, Healthspan Age if visible in WHOOP app, how legs felt late in longer
   rides

## Assessment output

```
**WEEK OF [DATE] - [CLASSIFICATION]**
Event countdown: [X days to May 3]

**Last week (facts from Strava + Whoop):**
- Riding: X hrs | X rides | X intensity sessions
- Strength: X/2 sessions
- Longest ride: X hrs
- WHOOP recovery trend: [mostly green / mixed / mostly yellow-red]
- Avg HRV: Xms | Avg RHR: X bpm | Avg sleep: Xh

**What worked:**
[2-3 sentences]

**What didn't / risks carried:**
[direct assessment - flag constraint violations, missed sessions, rationalization patterns
observed in the session log this week]

**Week classification:** [Base / Volume / Maintenance / Recovery]

---

**Upcoming week plan:**
- Ride days: [X] | Intensity: [day, session type] | Long ride: [day, target duration]
- Strength: Session A [day], Session B [day]
- Flags: [anything to watch - fueling, sciatica risk, scheduling conflicts]
- Conservative tripwire: [what would trigger stepping down next week]
```

## Classification logic

| Type | When |
|------|------|
| Volume Opportunity | Green trend, no upcoming stressors, event >3 weeks out |
| Base Consolidation | Mixed recovery, completing minimums, building consistency |
| Maintenance | Inside 3 weeks of event, or high life stress |
| Recovery | Red/yellow trend, illness, post-event |

## After delivering the weekly assessment

### Step 1: Write a brief entry to session-log.md

Add a log entry summarizing the weekly review - week classification, key flags surfaced,
and the upcoming week's plan. This is the Coach's weekly checkpoint note, not a data dump.

### Step 2: Write or update current-block-plan.md

Write a fresh current-block-plan.md reflecting the upcoming week's structure and the
block's remaining trajectory. This is Mann's "draft" — the living plan Coach executes
against session-to-session.

```markdown
# Current Block Plan
Updated: [YYYY-MM-DD]

## Block context
[Block name, phase, weeks remaining, event countdown]

## Weekly structure
- Minimum ride hours: [X]
- Strength sessions: [2/week — Session A + Session B]
- Intensity: [X session/week, green recovery only]
- Long ride target: [duration, day preference]

## This week's plan
| Day | Session | Target | Constraints |
|-----|---------|--------|-------------|
| [Mon] | [Session A] | [45 min] | [48h buffer before next ride] |
| ... | ... | ... | ... |

## Active constraints
[List any constraints in effect this week: 48h buffer, decoupling watch, HRV tripwire,
sciatica monitor, GLP-1 ceiling. One line each.]

## Conservative tripwire
[What would trigger stepping the week down from this plan]

## Block carry-forward
[1-2 sentences: what the previous block's phase-trends entry says to watch for]
```

Overwrite the previous current-block-plan.md entirely — it reflects the current week,
not a history. History is preserved in phase-trends.md and session-log.md.

### Step 3: Determine if this is a block boundary

A block boundary has occurred when ANY of the following is true:
- This is a Recovery week following a multi-week build
- The event has completed
- A fitness test was run this week
- A significant shift in training phase is starting (entering taper, starting a new build)
- Chris explicitly signals a phase transition

If this is NOT a block boundary, stop here. No write to phase-trends.md.

### Step 4: If block boundary - write to phase-trends.md

Compile the block's trajectory from session-log entries and weekly Strava/Whoop data,
then write a new entry to phase-trends.md per the format in the `notes-manager` skill.

The entry captures:
- What this training block was and what it accomplished
- Patterns that solidified across the block - not daily noise, confirmed trends
- Recovery baseline shifts observed
- Flags still active that carry into the next block
- What the next block starts with

After writing, confirm to Chris: "I've written a block summary to phase-trends.md. The
session log from this block can be trimmed - want me to do that now, or leave it a bit
longer?"

Do not trim the session log without explicit confirmation.

## Tone

Honest and direct. Name what was missed. Flag rationalization patterns observed in the
session-log notes from this week. Do not soften the assessment.
