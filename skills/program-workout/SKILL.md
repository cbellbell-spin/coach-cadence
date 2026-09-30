---
name: program-workout
description: Program the current athlete's next gym session from their own program and history and publish it to the gym app.
---

# Program Workout

Read `references/ATHLETE.md` and load `training-knowledge`. Stop if athlete identity,
routine mapping, or their current strength program is missing. Ask which configured
session to program and its scheduled date; do not assume A/B/C.

Call `get_athlete_context` and require its `athlete_id` to match `user_id` in
athlete-config.json. Confirm that the selected `routine_type_id` appears as an active
routine in the result. If it does not, stop for routine setup. Never reuse another
athlete's routine as a shortcut.

## Recent history

Call `get_workout_history` with:

```json
{"routine_type_id":"<routine_type_id>","days":30}
```

Require the returned `athlete_id` to match the workspace identity. Use the athlete's
existing program as the baseline. Recommend changes with reasons and adopt accepted
changes. Never derive their starting load from another athlete. Ask for an unknown
starting load; retain bodyweight, timed holds, and per-side work accurately. Finish
with manageable effort according to their program and constraints.

## Publish atomically

Generate one UUID as `request_id` and retain it across uncertain retries. Call
`publish_workout` once with the complete plan:

```json
{
  "request_id":"<request_id>",
  "routine_type_id":"<routine_type_id>",
  "scheduled_for":"<YYYY-MM-DD>",
  "coach_notes":"<overall notes or null>",
  "movements":[{
    "section":"<main|trunk|durability>",
    "position":1,
    "exercise_name":"<exercise>",
    "selected_variant":"<variant or null>",
    "target_sets":2,
    "target_reps":null,
    "target_weight_lbs":null,
    "target_duration_secs":30,
    "is_per_side":true,
    "coach_notes":"<movement notes or null>"
  }]
}
```

Validate a nonempty movement list, positive sets/reps/durations, nonnegative loads,
unique positive positions within each section, and allowed sections before calling.
Exactly one of `target_reps` or `target_duration_secs` must be non-null. Include warm-up
movements at the start of `main`, with clear coaching notes.

The connector verifies the authenticated athlete's active routine assignment and
inserts the parent plus every movement in one transaction. A repeated `request_id`
returns the same plan; do not generate a new ID after a timeout. Require the returned
`athlete_id` to match the workspace and the returned movement count and contents to
match the requested plan.

Then call `get_programmed_workout` with:

```json
{"workout_id":"<returned plan id>","include_actuals":false}
```

Require the identity, date, routine, movement count, and movement targets to match
before claiming the app is ready. Summarize the session, date, movement targets, and
coach notes. On errors, explain that publishing is incomplete; never claim it is
loaded. Refresh only this athlete's explicitly associated HUD if available; absence
of a HUD does not block programming.
