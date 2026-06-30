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

Replace `<workout_type>` with the correct value for each session:
- Session A: `A (Lower Body)`
- Session B: `B (Upper Body)`
- Session C: `C (Lower Accessory)`

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
  (status, coach_notes, programmed_at, scheduled_for, routine_type_id, user_id)
VALUES
  ('pending', '<overall coach notes>', NOW(), '<scheduled_for_date>',
   '<routine_type_id>', 'd11e8eea-7aab-4d6c-85ad-0079243bdbca')
RETURNING id
```

`scheduled_for` is the date the session is planned (YYYY-MM-DD).

`routine_type_id` values:
- Session A: `11111111-1111-1111-1111-111111111111`
- Session B: `22222222-2222-2222-2222-222222222222`
- Session C: `44444444-4444-4444-4444-444444444444`

`user_id` is always `d11e8eea-7aab-4d6c-85ad-0079243bdbca`.

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

## Update the Cadence HUD

After writing to Supabase, update the Cadence HUD per the standard protocol in `notes-manager`.

Zone 6 fetches live from Supabase on reload — no data injection is needed. To trigger an
immediate reload of Zone 6, read the artifact HTML (get path from `list_artifacts`), write
it unchanged to a temp file, then call `update_artifact`:

**update_summary:** `'Zone 6 refresh: <Session type> programmed for <date>'`

If the artifact update fails, Zone 6 will update on the next manual artifact reload. Do not
block the rest of the session.
