---
description: Review the past week's training and recovery data, classify the week, and plan the upcoming week with specific recommendations.
---

# /weekly-review

Run this at the start of each week (Sunday evening or Monday morning). Generates a structured assessment and forward plan.

## Steps

1. Load `training-knowledge` skill and `notes-manager` skill
2. Read `~/cowork/Projects/adaptive-training-coach/weekly-summary.md` (last 6 weeks of context)
3. Read `~/cowork/Projects/adaptive-training-coach/daily-log.md` (confirm this week's entries)
4. Pull Whoop data:
   - `whoop_get_recovery_range` (last 7 days)
   - `whoop_get_sleep_range` (last 7 days)
   - `whoop_get_strain_range` (last 7 days)
   - `whoop_get_training_summary`
5. Pull Strava activities (last 7 days)
6. Ask Chris for any context not captured in data: upcoming constraints (travel, work stress), any pain or niggles, Healthspan Age if visible in WHOOP app, how legs felt late in longer rides

## Assessment output

```
**WEEK OF [DATE] — [CLASSIFICATION]**
Event countdown: [X weeks to May 3]

**Last week (facts):**
- Riding: X hrs | X rides | X intensity sessions
- Strength: X/2 sessions
- Longest ride: X hrs
- WHOOP recovery trend: [mostly green / mixed / mostly yellow-red]
- Avg HRV: Xms | Avg RHR: X bpm | Avg sleep: Xh

**What worked:**
[2–3 sentences]

**What didn't / risks carried:**
[direct assessment — flag any constraint violations, missed sessions, rationalization patterns observed]

**Week classification:** [Base / Volume / Maintenance / Recovery]

---

**Upcoming week plan:**
- Ride days: [X] | Intensity: [day, session type] | Long ride: [day, target duration]
- Strength: Session A [day], Session B [day]
- Flags: [anything to watch — fueling, sciatica risk, scheduling conflicts]
- Conservative tripwire: [what would trigger stepping down next week]
```

## Classification logic

| Type | When |
|------|------|
| Volume Opportunity | Green trend, no upcoming stressors, event >3 weeks out |
| Base Consolidation | Mixed recovery, completing minimums, building consistency |
| Maintenance | Inside 3 weeks of event, or high life stress |
| Recovery | Red/yellow trend, illness, post-event |

## After delivering assessment

Append entry to `weekly-summary.md` with the week's facts, classification, summary, and next week plan.

## Tone

Honest and direct. Name what was missed. Flag rationalization patterns observed in the past week's notes. Do not soften the assessment to protect feelings.
