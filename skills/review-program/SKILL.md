---
name: review-program
description: Compare this athlete's programmed session with their linked logged workout.
---

# Review Program vs Actuals

Read `references/ATHLETE.md` first. Stop without configured identity. Ask which
configured routine/date to review.

Call `list_programmed_workouts` with the configured routine and completed status:

```json
{"status":"completed","routine_type_id":"<routine_type_id>","limit":5}
```

Require the returned `athlete_id` to match `user_id` in athlete-config.json. If no
completed plan exists, report that accurately. Let the athlete select a result when
the date is ambiguous; do not fuzzy-match a logged session.

Call `get_programmed_workout` for the selected owned plan:

```json
{"workout_id":"<workout_id>","include_actuals":true}
```

Require the returned identity to match. Compare movements, targets, actuals, and
deviations. Preserve timed/per-side target meaning; do not label seconds as reps. If
logged data lacks duration or per-side detail, say that exact comparison is unavailable
and ask for context rather than inventing it. If the plan has no linked actuals, report
that accurately. Write coaching notes only in this athlete's workspace.
