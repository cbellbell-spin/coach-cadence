---
name: review-program
description: Compare this athlete's programmed session with their linked logged workout.
---

# Review Program vs Actuals

Read `references/ATHLETE.md` first. Stop without configured identity.
Ask which configured routine/date to review. Validate all UUID placeholders.

```sql
SELECT pw.id, wrt.name AS workout_type, pw.status, pw.coach_notes,
       pw.programmed_at, pw.completed_workout_session_id
FROM workout.programmed_workouts pw
JOIN workout.workout_routine_types wrt ON wrt.id = pw.routine_type_id
WHERE pw.user_id = '<user_id>'::uuid
  AND pw.routine_type_id = '<routine_type_id>'::uuid AND pw.status = 'completed'
ORDER BY pw.programmed_at DESC LIMIT 5;
```

Use the selected plan ID to fetch targets and actuals, always retaining ownership:

```sql
SELECT ps.*
FROM workout.programmed_workout_sets ps
JOIN workout.programmed_workouts pw ON pw.id = ps.programmed_workout_id
WHERE pw.user_id = '<user_id>'::uuid AND pw.id = '<plan_id>'::uuid
ORDER BY ps.slot_label, ps.position;
```

```sql
SELECT ws.exercise_name, ws.variant, ws.set_number, ws.weight_lbs, ws.reps, ws.duration_secs, ws.notes
FROM workout.workout_sets ws
JOIN workout.programmed_workouts pw
  ON lower(pw.completed_workout_session_id::text) = lower(ws.session_id)
WHERE pw.user_id = '<user_id>'::uuid AND ws.user_id = '<user_id>'::uuid
  AND pw.id = '<plan_id>'::uuid AND ws.deleted_at IS NULL
ORDER BY ws.exercise_name, ws.set_number;
```

Compare movements, targets, actuals, and deviations. Preserve timed/per-side target
meaning; do not label seconds as reps. If logged data lacks duration or per-side detail,
say that exact comparison is unavailable and ask for context rather than invent it.
If no completed plan or linked actuals exist, report that accurately. Do not fuzzy-match
another athlete's sessions. Write coaching notes only in this athlete's workspace.
