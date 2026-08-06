---
name: review-program
description: >
  Compare a past programmed workout (from Supabase) against the actual workout
  that was logged (also in Supabase). Trigger phrases: "review programmed vs actual",
  "how did my program compare", "program vs actual", "did I hit the targets".
---

# Review Program vs Actuals

Compare what was programmed against what was actually logged, pulling from
`workout.programmed_workouts`, `workout.programmed_workout_sets`, and
`workout.workout_sets`.

## Step 1 — Identify the programmed workout to review

Ask Chris: "Which workout do you want to review — Session A or Session B?"
And "Approximately when was it programmed? (This week, last week, etc.)"

## Step 2 — Fetch the programmed workout from Supabase

Use `execute_sql`:

```
SELECT id, workout_type, status, coach_notes, programmed_at, completed_workout_session_id
FROM workout.programmed_workouts
WHERE workout_type = '<workout_type>' AND status = 'completed'
ORDER BY programmed_at DESC
LIMIT 5
```

Pick the most relevant entry based on Chris's answer.

## Step 3 — Fetch the programmed sets

Use `execute_sql`:

```
SELECT slot_label, position, exercise_name, selected_variant,
       target_sets, target_reps, target_weight_lbs, coach_notes
FROM workout.programmed_workout_sets
WHERE programmed_workout_id = '<id>'
ORDER BY slot_label, position
```

## Step 4 — Fetch the actual workout sets

Use the `completed_workout_session_id` from step 2 to query `workout_sets`:

```
SELECT exercise_name, variant, set_number, weight_lbs, reps, notes
FROM workout.workout_sets
WHERE session_id = '<completed_workout_session_id>'
ORDER BY exercise_name, set_number
```

## Step 5 — Compare and present

For each programmed exercise, show:

| Movement | Programmed | Actual | Delta |
|----------|------------|--------|-------|
| Step-up | 3×8 @ 40 lbs | 3×8 @ 40 lbs | ✓ on target |
| RDL | 3×8 @ 80 lbs | 3×7 @ 85 lbs | +5 lbs, -1 rep |

Then write a brief coaching summary (2–3 sentences):
- What was hit precisely
- What deviated and why (load change, rep drop, different variant, etc.)
- Any flags (grinding reps, sciatica notes in the actual workout, etc.)

Write in the same narrative voice used in daily-coaching — direct, specific,
grounded in the data.

## If no completed programmed workout exists yet

Tell Chris: "I don't have a completed programmed workout to compare against yet.
Program a workout first, complete it in the app, then come back to review."