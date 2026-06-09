---
name: morning-check-in
description: >
  Run at the start of every session. Load training history, pull prior day's Whoop data
  (once per day only), enrich outdoor rides via intervals.icu, and deliver a single decisive
  training recommendation for the day. Trigger phrases: "morning check-in", "start session",
  "what should I do today", "good morning".
---

# Morning Check-In

Run at the start of every session. Check session-log.md before touching any external service.
If today's Whoop pull is already cached, use the flag. Whoop and Strava are live sources;
the session log stores only what they cannot give back.

## Steps

1. Load `training-knowledge`, `daily-coaching`, `activity-sync`, and `notes-manager` skills
2. Read `user-profile.md` from the Cowork Project folder:
   - **File does not exist** - new user. Run onboarding before anything else.
   - **File exists but has `[pending]` sections** - returning user with incomplete profile.
     Proceed with check-in, but weave in one pending Tier 2 question if an opening presents.
   - **File exists and reasonably complete** - proceed.
3. Read `session-log.md` - provides coaching context: prior recommendations, Coach flags
   carried forward, qualitative session notes, personal context. Not a substitute for live
   data - it's what live data cannot tell you.
4. Read `phase-trends.md` - current block context. If a pattern in the session log looks
   like it may be crossing from one-off to trend, check here to confirm.
5. Read `current-block-plan.md` (if it exists) — the active training plan being executed.
   Provides block structure and weekly targets that Strava data is measured against. If the
   file does not exist, proceed — the weekly-review skill creates it.
6. Read the 4 most recent entries in `coaching-decisions.md` (if it exists) — recent coaching
   rationale. Prevents re-deriving the same reasoning the coach has already worked through.
   If the file is empty or does not exist, proceed.

### Whoop data - pull prior day, once per day only

Check session-log.md for an entry dated today:

- **Today's entry exists with `whoop_pulled: yes`** - skip all Whoop calls. Jump to Strava.
- **No entry for today, or `whoop_pulled: no`** - ask the user: "Want me to pull yesterday's
  Whoop data?"
  - If yes: pull prior day's completed data, write `whoop_pulled: yes` to today's log entry
    immediately, then proceed.
  - If no: ask the user to provide recovery color, HRV, RHR, and sleep hours manually. Write
    those to today's log entry with `whoop_pulled: manual`.

When pulling Whoop, use **prior day's completed data only** - not today's in-progress cycle:
- `whoop_get_latest_recovery` - yesterday's completed recovery score, HRV, RHR
- `whoop_get_latest_sleep` - last night's completed sleep session
- `whoop_get_strain_range` - yesterday's completed strain
- `whoop_get_training_summary` - coaching snapshot

Workouts and activities come from Strava, not Whoop. Whoop strain is context only.

Write `whoop_pulled: yes` to today's session-log entry immediately after pulling. Do not call
Whoop again for the same day.

7. Pull Strava recent activities and enrich outdoor rides per the `activity-sync` skill. That
   skill owns all sync logic, throttle rules, intervals.icu fetch method, and cardiac
   decoupling flagging. If decoupling is above 10% on any recent ride, carry the flag into
   the recommendation.

### Recent context - compile before recommending

Before generating the recommendation, synthesize what the session log, live Strava pull,
current-block-plan, and recent coaching decisions actually show. The session log provides the
coaching history Strava cannot; current-block-plan provides the structural context; coaching-
decisions provides the reasoning the coach has already worked through.

Identify only what is load-bearing for today's decision:

- When was the last Session A (lower body strength)? Is the 48-hour buffer clear?
- When was the last intensity ride? What was it?
- How many ride hours accumulated this week so far? How does that track against the block plan?
- Any cardiac decoupling flags from recent outdoor rides?
- Any active Coach flags from the session log - sciatica watch, HRV tripwire streak,
  decoupling trend, rationalization patterns observed?
- Any recent coaching-decisions entries that apply to today's call — constraints or
  pattern interpretations already in play?
- Any personal context from session notes that affects interpretation of today's data?

This context feeds directly into the narrative recommendation. Do not output it as a
separate section - weave it into the coaching response.

8. Apply daily coaching framework per `daily-coaching` skill:
   - Determine WHOOP color and intensity eligibility
   - Check 48-hour buffer against last Session A
   - Tally weekly load from Strava
   - Factor in cardiac decoupling flags from intervals.icu
   - Determine training phase and event countdown
   - Identify rationalization patterns to flag proactively
9. **Reschedule Supabase programmed workout if coaching shifts the date**

   Now that the session type is determined, check whether a pending programmed workout
   of that type exists in Supabase but is scheduled for a different date within the next
   3 days. If so, update `scheduled_for` to today before writing anything else — this
   ensures Zone 4 of the Cadence HUD finds the right workout on first load.

   Only run this check when today's coaching call is Session A, B, or C.

   **Step 9a — Detect the mismatch**

   ```sql
   SELECT pw.id, pw.scheduled_for::text, wrt.name as workout_type
   FROM workout.programmed_workouts pw
   JOIN workout.workout_routine_types wrt ON pw.routine_type_id = wrt.id
   WHERE pw.status = 'pending'
     AND pw.scheduled_for BETWEEN CURRENT_DATE AND CURRENT_DATE + 3
     AND wrt.name ILIKE '%<A|B|C>%'
   ORDER BY pw.scheduled_for ASC
   LIMIT 1;
   ```

   Use the session letter from the coaching call to fill `<A|B|C>`.

   **Step 9b — If scheduled_for ≠ today, reschedule**

   ```sql
   UPDATE workout.programmed_workouts
   SET scheduled_for = CURRENT_DATE,
       updated_at    = now()
   WHERE id = '<id from 9a>';
   ```

   **Step 9c — Log it**

   Add to today's session-log entry:
   `programmed_workout_rescheduled: <workout_type> moved from <original_date> to today`

   If no mismatch exists, skip silently. If the update fails, log
   `reschedule_failed: <error>` and continue — do not block step 10.

10. Generate recommendation in the narrative voice defined in `daily-coaching` skill
11. Write today's entry to session-log.md:
    - Full recommendation summary and key factors
    - Any Coach flags raised or carried forward in this session
    - Any session notes provided by the user (RPE, physical flags, personal context)
    - Do not write Whoop numbers or Strava stats - those come from the live API

## After delivering the coaching call

### Update the Cadence HUD — mandatory after every coaching call

After writing to session-log.md, update the Cadence HUD. This is not optional.

#### Step 1 — Confirm the artifact exists

Call `mcp__cowork__list_artifacts`. If `cadence-hud` is not present, skip. If it exists, proceed — `list_artifacts` returns a `path` for each artifact.

#### Step 2 — Read the current artifact HTML

Read the HTML file at the `path` returned by `list_artifacts`.

#### Step 3 — Build the injection block

Find the existing injection block — everything from the first line matching `// ─── .* injection .* ───` through `// ─── end injection ───` inclusive. Replace it entirely with the following (substitute real values):

```javascript
// ─── morning-check-in injection YYYY-MM-DD ───
D.coachingCall = {
  status: '<green|yellow|red>',
  session: '<Session A|Session B|Session C|Long Ride|Z2 Ride|Rest>',
  directive: '<one phrase: what to do>',
  note: '<one sentence: the single most important behavioral constraint today>'
};
D.sessionPhase = 'pre';
D.sessionMode  = <'strength'|'cycling'|'rest'|null>;
D.rideData     = null;
D.sessionFlags = [];
D.progressions = [];
D.nextRide = {
  date: '<YYYY-MM-DD>',
  type: '<ride type>',
  duration: '<target duration>',
  notes: '<recovery constraint · fueling protocol>'
};
D.nextSession = {
  date: '<YYYY-MM-DD>',
  type: '<Session A/B/C — Label>',
  notes: '<key loads for that session>'
};
D.weekPlan = {
  weekOf: '<YYYY-MM-DD of this Monday>',
  goals: ['<taper/block goal 1>', '<goal 2>', '<goal 3>'],
  schedule: {
    '<YYYY-MM-DD>': { type: 'strength|cycling|rest', label: '<A|B|C|Z2|REST>', note: '<...>' }
    // one entry per day Mon–Sun
  },
  actuals: {
    '<YYYY-MM-DD>': { completed: false, type: 'strength|cycling|rest' }
    // completed:true only for days with a confirmed session; today is always false
  }
};
// ─── end injection ───
```

**sessionMode mapping:** Session A/B/C → `'strength'` · any ride → `'cycling'` · rest → `'rest'` · pre-session → `null`

**weekPlan source:** read from `current-block-plan.md`. If that file doesn't exist, derive the week schedule from the coaching call and source-of-truth.md constraints.

**nextSession vs nextRide:** populate both. `nextSession` is the next strength session; `nextRide` is the next cycling session. Both dates come from current-block-plan.md.

#### Step 4 — Write and push

Write the modified HTML to the outputs directory as `cadence-hud-updated.html`, then call:

### Prompt session close

After completing all of the above, close with:

"Run `/session-close` when your session is done to log this coaching call."

Only prompt this when the coaching decision involved non-obvious reasoning (override,
pattern interpretation, constraint applied). Skip the prompt for routine calls.

## If Whoop pull fails

State that Whoop is not responding. Ask the user to provide: recovery color, HRV, RHR, sleep
hours manually. Write those inputs to the log with `whoop_pulled: manual`.

## If Strava is unavailable

Proceed without it. Note the gap. Rely on session-log.md for recent activity context.
