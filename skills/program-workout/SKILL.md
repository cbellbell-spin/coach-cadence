---
name: program-workout
description: >
  Program the next strength workout for Chris by reading recent history from Supabase,
  selecting exercises from the slot options, and writing a structured programmed workout
  to the Supabase database. Trigger phrases: "program my next workout",
  "what should I do next session", "plan my next strength session", "program the workout".
---

# Program Workout

Write a programmed workout to Supabase `workout.programmed_workouts` and
`workout.programmed_workout_sets` for the user's next strength session.

## Prerequisite

Load `training-knowledge` skill first — it contains the strength template and
source-of-truth values needed for load selection.

## Inputs

You need to know the next workout type. Ask Chris directly:
"What workout are you programming — Session A (lower body), Session B (upper body),
or Session C (lower accessory)?"

Until Chris answers, output nothing.

## Data gathering

### Step 1 — Pull recent workout history from Supabase

Use the `execute_sql` tool with this query:

```
SELECT
  workout_type,
  exercise_name,
  variant,
  set_number,
  weight_lbs,
  reps,
  notes,
  date
FROM workout.workout_sets
WHERE workout_type = '<workout_type>'
  AND date >= NOW() - INTERVAL '30 days'
ORDER BY date DESC, set_number ASC
```

Replace `<workout_type>` with `Monday Lower Body` for Session A or
`Friday Upper Body` for Session B.

### Step 2 — Select exercise per slot

From the strength-template.md and source-of-truth.md:

**Session A (lower body) slots:**
- Main: Step-up, RDL, Leg Press, Glute Bridge, Leg Curl, Calf Raise
- Trunk: Dead bug or Standing Pallof press, Side plank
- Durability: Step-downs slow eccentric, Half-kneeling Pallof press, Tibialis Raise

**Session B (upper body) slots:**
- Main: Push (DB bench or push-ups), Pull (row or lat pulldown), Overhead press
- Accessory: Face pulls or band pull-aparts
- Trunk: Anti-rotation or carry

### Step 3 — Set target weight/reps/sets per movement

Use recent history as the baseline. Adjust conservatively:
- If recent sessions show consistent reps with a given load → hold or add 2.5–5 lbs
- If there are notes about grinding or fatigue → reduce or hold
- No PR chasing; finish all sets with 1–2 reps in reserve

### Step 4 — Write coach notes per movement

Write 1–2 sentences per exercise noting any adjustments, cues, or things to watch.
Examples:
- "Slower eccentric on the descent — back felt good last session"
- "Push through heels, not toes — sciatica watch"
- "Hold at top for 2 seconds, no bounce"

## Writing to Supabase

### Step 1 — Insert programmed_workout

Use `execute_sql` with this query:

```
INSERT INTO workout.programmed_workouts
  (workout_type, status, coach_notes, programmed_at)
VALUES
  ('<workout_type>', 'pending', '<overall coach notes>', NOW())
RETURNING id
```

Capture the returned `id` (UUID) — use it in step 2.

### Step 2 — Insert programmed_workout_sets

For each movement, use `execute_sql` with this query:

```
INSERT INTO workout.programmed_workout_sets
  (programmed_workout_id, slot_label, position, exercise_name, selected_variant,
   target_sets, target_reps, target_weight_lbs, coach_notes)
VALUES
  ('<programmed_workout_id>', '<slot_label>', <position>, '<exercise_name>',
   '<variant>', <target_sets>, <target_reps>, <target_weight_lbs>, '<coach_notes>')
```

Use `mainExercises` for main slot, `trunkExercises` for trunk, `durabilityExercises` for durability.
Position: 1, 2, 3 within each slot (display order).

Repeat for all movements in the session.

## Output — Confirmation to Chris

After writing to Supabase, write a summary to the user in the narrative coaching voice:

```
**Programmed — [Session A / Session B / Session C]**
[Date programmed]

| Movement | Target |
|-----------|--------|
| Exercise 1 | 3×8 @ 185 lbs |
| ...

Coach notes:
- Exercise 1: [note]
- Exercise 2: [note]
```

Then confirm: "Your [Session A/B/C] workout has been programmed.
It's loaded in the app — you'll see it when you start the session."

---

## Cadence HUD — refresh Zone 6 after programming

After writing the programmed workout to Supabase and confirming to Chris, refresh the Cadence
HUD so Zone 6 shows the newly programmed session immediately.

### Step 1 — Check whether the artifact exists

Call `mcp__cowork__list_artifacts`. If `cadence-hud` is not present, skip.

### Step 2 — Clear the Zone 6 cache key in the artifact

Zone 6 caches results under `cadence_cache_next_{today}` in localStorage. The artifact will
auto-refresh Zone 6 on its next reload — no additional data injection is needed for Zone 6
since it fetches live from Supabase.

However, if the artifact is currently open, it will show stale data until the user reloads.
To trigger an immediate refresh, read the artifact HTML, find the `boot()` call at the bottom,
and do not change it — just call `update_artifact` with a trivial update_summary so the
artifact reloads in the user's view.

### Step 3 — Call update_artifact

Read the current artifact HTML (get path from `list_artifacts`). Write it to a temp file
unchanged (or with the date comment updated), then call:

```
mcp__cowork__update_artifact(
  id = 'cadence-hud',
  html_path = '<path to temp file>',
  update_summary = 'Zone 6 refresh: <Session type> programmed for <date>'
)
```

The artifact's `loadZ6()` function will fetch the new programmed workout from Supabase on
reload.

### If artifact update fails

Proceed normally. Zone 6 will update on the next manual artifact reload.
