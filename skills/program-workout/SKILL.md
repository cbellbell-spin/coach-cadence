---
name: program-workout
description: Program the current athlete's next gym session from their own program and history and publish it to the gym app.
---

# Program Workout

Read `references/ATHLETE.md` and load `training-knowledge`. Stop if athlete identity,
routine mapping, or their current strength program is missing. Ask which of their
configured sessions to program and its scheduled date; do not assume A/B/C.
Validate `<user_id>` and `<routine_type_id>` from athlete-config.json as UUIDs.
Confirm the selected routine is assigned to them:

```sql
SELECT ur.routine_type_id, ur.name
FROM workout.user_routines ur
WHERE ur.user_id = '<user_id>'::uuid
  AND ur.routine_type_id = '<routine_type_id>'::uuid AND ur.is_active = true;
```

If no assignment exists, stop for routine setup. Never reuse someone else's routine
as a shortcut. Shared catalog routines can be assigned independently through user_routines.

## Recent history

```sql
SELECT exercise_name, variant, set_number, weight_lbs, reps, duration_secs, notes, date
FROM workout.workout_sets
WHERE user_id = '<user_id>'::uuid
  AND routine_type_id = '<routine_type_id>'::uuid
  AND deleted_at IS NULL AND date >= CURRENT_DATE - 30
ORDER BY date DESC, set_number ASC;
```

Use the athlete's existing program as the baseline. Recommend changes with reasons
and adopt accepted changes. Never derive their starting load from another athlete.
Ask for an unknown starting load; retain bodyweight, timed holds, and per-side work
accurately. Finish with manageable effort according to their program and constraints.

## Publish atomically

Use one `execute_sql` statement, not separate parent/child calls. Generate a new plan
UUID once and retain it across uncertain retries. Before retrying after a timeout,
read back that ID with the athlete filter; do not generate duplicate plans.
The following is a template: expand the VALUES list to include every programmed
movement. Validate a nonempty list, positive sets/reps/durations, nonnegative loads,
and app sections (`main`, `trunk`, `durability`) before executing. Include any
warm-up movements at the start of `main`, with clear coaching notes.
Timed work sets target_reps to NULL and target_duration_secs to seconds; rep work
sets target_duration_secs to NULL. is_per_side records unilateral instructions.
The app migration adding those optional columns must be installed first.

```sql
WITH plan AS (
  INSERT INTO workout.programmed_workouts
    (id, status, coach_notes, programmed_at, scheduled_for, routine_type_id, user_id)
  SELECT '<plan_id>'::uuid, 'pending', '<overall_notes>', NOW(), '<date>'::date,
         ur.routine_type_id, ur.user_id
  FROM workout.user_routines ur
  WHERE ur.user_id = '<user_id>'::uuid
    AND ur.routine_type_id = '<routine_type_id>'::uuid AND ur.is_active = true
  RETURNING id
), movements AS (
  INSERT INTO workout.programmed_workout_sets
    (programmed_workout_id, slot_label, position, exercise_name, selected_variant,
     target_sets, target_reps, target_weight_lbs, target_duration_secs, is_per_side, coach_notes)
  SELECT plan.id, v.slot_label, v.position, v.exercise_name, v.selected_variant,
         v.target_sets, v.target_reps, v.target_weight_lbs, v.target_duration_secs,
         v.is_per_side, v.coach_notes
  FROM plan CROSS JOIN (VALUES
    ('<section>'::text, <position>::int, '<exercise>'::text, '<variant>'::text,
     <sets>::int, <reps_or_null>::int, <weight_or_null>::numeric,
     <seconds_or_null>::int, <true_or_false>::boolean, '<notes>'::text)
  ) AS v(slot_label, position, exercise_name, selected_variant, target_sets,
         target_reps, target_weight_lbs, target_duration_secs, is_per_side, coach_notes)
  RETURNING programmed_workout_id
)
SELECT programmed_workout_id, COUNT(*) AS movement_count
FROM movements GROUP BY programmed_workout_id;
```

Require the returned count to equal the planned movement count. Read back before
claiming the app is ready:

```sql
SELECT pw.id, pw.scheduled_for, ps.*
FROM workout.programmed_workouts pw
JOIN workout.programmed_workout_sets ps ON ps.programmed_workout_id = pw.id
WHERE pw.user_id = '<user_id>'::uuid AND pw.id = '<plan_id>'::uuid
ORDER BY ps.slot_label, ps.position;
```

Summarize the session, date, movement targets, and coach notes. On errors, explain
that publishing is incomplete; never claim it is loaded. Refresh only this athlete's
explicitly associated HUD if available; absence of a HUD does not block programming.
