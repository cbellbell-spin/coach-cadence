---
name: log-workout
description: >
  Manually log a strength session, indoor ride, or any activity not captured by Whoop or
  Strava. Writes qualitative context to today's session log, and strength load changes to
  the permanent record. Trigger phrases: "log my workout", "log session", "log strength",
  "I finished a strength session", "log my ride".
---

# Log Workout

Use this to record what Whoop and Strava don't capture - how a session felt, the loads used,
and any physical flags. This is the primary way strength session context enters the memory system.

## Prompt Chris for

- Session type: Strength A / Strength B / Strength C / Indoor ride / Other
- Duration (minutes)
- For strength: any loads changed from source-of-truth.md?
- RPE (1-10)
- How did it feel: smooth / normal / heavy / grinding
- Any physical flags: back, sciatica, joints
- Fueling: adequate / skipped / partial
- Any notes worth carrying forward

## Write behavior

1. Read `~/cowork/Projects/adaptive-training-coach/session-log.md`
2. Find today's entry (if morning check-in was run, it exists)
3. Append to the Session notes field of today's entry:
   - Session type, duration, RPE, quality, physical flags, fueling
   - Any context worth noting for the next session
4. If no entry for today exists, create one with the logged data, mark `whoop_pulled: no`,
   and `strava_last_pull: not pulled`

## If loads changed vs source-of-truth.md

Loads belong in permanent-record.md, not just the session log. When logged loads differ
from source-of-truth.md:

1. Note the discrepancy in the session-log entry
2. Prompt: "These loads look different from your recorded working loads. Want me to add a
   progression entry to your permanent record and update source-of-truth.md?"
3. If yes:
   - Append a row to the relevant Session A or Session B table in `permanent-record.md`
     (create the file with full headers if it doesn't exist)
   - Then prompt the user to run update-source-of-truth to update working loads
4. Do not update source-of-truth.md automatically - that requires explicit confirmation

## Physical flags

If grinding reps or sciatic flags are mentioned:
- Log it clearly in session notes
- Add a Coach flag to the entry: "Sciatica L-side tightness during Session A - monitor.
  No grinding reps next session regardless of how it feels."
- Remind Chris of the red flag protocol: reduce load if symptoms recur; do not push through

## Tone

No commentary on the quality of the session unless Chris asks. Log the facts.

---

## Cadence HUD — update after logging the session

After writing the session log entry and confirming any progressions, update the Cadence HUD
artifact to switch Zone 4 to comparison view and Zone 5 to the confirmed progressions.

### Step 1 — Collect progressions

A progression occurs when a logged load is higher than the previous working load in
source-of-truth.md for that exercise. Ask if not already confirmed:
"Were any loads progressed today vs last session?"

For each progression, collect:
```javascript
{ exercise: 'Step-ups', from: '50 lbs', to: '55 lbs', rule: '2-week rule met' }
```

Common rule strings: `'2-week rule met'`, `'3 clean sets unlocked'`, `'Rep ceiling hit'`.

### Step 2 — Check whether the artifact exists

Call `mcp__cowork__list_artifacts`. If `cadence-hud` is not present, skip.

### Step 3 — Read current artifact HTML and inject updates

Read the artifact HTML. Find the `window.CADENCE_DATA = {` block (the one written by
morning-check-in). Update these fields:

```javascript
sessionPhase: 'complete',
progressions: [
  { exercise: '...', from: '...', to: '...', rule: '...' },
  // one entry per exercise progressed; empty array if none
]
```

Do not change any other CADENCE_DATA fields.

Write the modified HTML to the outputs directory (`cadence-hud-updated.html`), then call:

```
mcp__cowork__update_artifact(
  id = 'cadence-hud',
  html_path = '<path>',
  update_summary = 'Session complete: <N progressions or "no progressions">'
)
```

The artifact will:
- Zone 4 → switch to programmed vs actual comparison view (loads from Supabase)
- Zone 5 → display the progressions array (or "no progressions this session")

### If no progressions this session

Still update the artifact with `sessionPhase: 'complete'` and `progressions: []`.
Zone 5 will show "— no progressions this session —".

### If artifact update fails

Log `hud_update: failed` in today's session-log entry. Do not block the rest of the session.
