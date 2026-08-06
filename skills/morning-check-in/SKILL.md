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
9. Generate recommendation in the narrative voice defined in `daily-coaching` skill
10. Write today's entry to session-log.md:
    - Full recommendation summary and key factors
    - Any Coach flags raised or carried forward in this session
    - Any session notes provided by the user (RPE, physical flags, personal context)
    - Do not write Whoop numbers or Strava stats - those come from the live API

## After delivering the coaching call

### Update the Cadence HUD

After writing to session-log.md, update (or create) the Cadence HUD artifact so Zone 2
reflects today's coaching decision immediately — before the user opens the HUD.

#### Step 1 — Check whether the artifact exists

Call `mcp__cowork__list_artifacts`. Look for id `cadence-hud`.

- **Exists** → proceed to Step 2 with `mcp__cowork__update_artifact`.
- **Does not exist** → skip silently (artifact must be created separately).

#### Step 2 — Build the CADENCE_DATA patch

From the coaching decision you just made, populate these fields:

```javascript
{
  coachingCall: {
    status: '<green|yellow|red>',
    session: '<Session A|Session B|Session C|Long Ride|Z2 Ride|Rest>',
    directive: '<Strength only|Z2 target — Xh|Complete rest|Intensity allowed>',
    duration: '<45–50 min|3h|—>',
    note: '<one sentence: the single most important behavioral constraint today>'
  },
  sessionPhase: 'pre',
  sessionMode: '<strength|cycling|rest>',
  eventDate: '<YYYY-MM-DD from source-of-truth.md>',
  ftpWatts: <number from source-of-truth.md>,
  hrvLow: <HRV baseline low end>,
  hrvHigh: <HRV baseline high end>,
  cadenceFloor: 85,
  fuelCeiling: <GLP-1 ceiling from source-of-truth.md>,
  weeklyHrMin: <weekly cycling minimum hours from source-of-truth.md>
}
```

**sessionMode mapping:**
- Session A / B / C → `'strength'`
- Long Ride / Z2 Ride / Intensity ride → `'cycling'`
- Rest / Recovery only → `'rest'`

**coachingCall.note** — one sentence max. The single behavioral constraint.
Examples:
- `'Yellow blocks all intensity — strength only today.'`
- `'Red recovery — no training, full rest.'`
- `'Green but 48h buffer from Session A — Z2 only, no intensity.'`
- `'Green, all systems clear — session as programmed.'`

#### Step 3 — Read the current artifact HTML

Call `mcp__cowork__list_artifacts` to get the artifact path. Read the HTML file at that path.

#### Step 4 — Inject CADENCE_DATA and write updated artifact

In the HTML file, find the comment line:
```
// ═══════════════════════════════════════════════════════
//  CADENCE_DATA — written by skills via update_artifact
```

Immediately before that block (before `window.CADENCE_DATA = window.CADENCE_DATA || {};`),
insert a new `<script>` block that pre-populates CADENCE_DATA:

```html
<script>
// Written by morning-check-in — YYYY-MM-DD
window.CADENCE_DATA = {
  coachingCall: { status: '...', session: '...', directive: '...', duration: '...', note: '...' },
  sessionPhase: 'pre',
  sessionMode: '...',
  eventDate: '...',
  ftpWatts: ...,
  hrvLow: ...,
  hrvHigh: ...,
  cadenceFloor: 85,
  fuelCeiling: ...,
  weeklyHrMin: ...,
  rideData: null,
  sessionFlags: [],
  progressions: []
};
</script>
```

Write the modified HTML to the outputs directory (e.g. `cadence-hud-updated.html`), then call:

```
mcp__cowork__update_artifact(
  id = 'cadence-hud',
  html_path = '<path to cadence-hud-updated.html>',
  update_summary = 'Morning check-in: <one-line coaching summary>'
)
```

#### If artifact update fails

Log `hud_update: failed` in today's session-log entry. Do not block the rest of the session.

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
