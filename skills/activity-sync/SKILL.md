---
name: activity-sync
description: >
  Apply this skill when pulling activity data from Strava or intervals.icu, checking
  whether a sync is due, or processing a completed activity. Trigger phrases: "I finished
  a ride", "just got back", "completed a workout", "sync activities", "check Strava",
  "pull my ride data". Governs all activity data refresh logic and intervals.icu enrichment.
---

# Activity Sync

Governs when and how activity data is pulled from Strava and enriched via intervals.icu.
Strava is a live data source - pull it fresh. The session log stores only what Strava cannot
give back (qualitative notes, Coach flags, recommendation context).

## Strava pull logic

Pull Strava activity data when ANY of the following are true:

- **First conversation of the day** - no Strava pull recorded in today's session-log entry
- **4+ hours since last pull** - check `strava_last_pull` timestamp in today's session-log
- **User reports completing an activity** - any phrase indicating a session just finished

Never pull Strava more than needed. Check the log timestamp before calling the API.

After every Strava pull: update `strava_last_pull` timestamp in today's session-log entry.

## What to pull from Strava

Recent activities - last 7 days, basic stats:
- Activity name, type, date
- Duration, distance, elevation gain
- Average HR, average power (if available)
- Activity type flag: outdoor ride / indoor ride / strength / run / other

## Intervals.icu enrichment

Trigger automatically when a Strava pull returns an outdoor ride not already enriched in the
session log (check today's entry for an existing intervals.icu block for that ride date).

**Outdoor ride definition:** activity type is "Ride" - not "VirtualRide", not "EBikeRide",
not sport types indicating Peloton or spin bike.

**Do not enrich:** VirtualRide, indoor trainer sessions, Peloton rides, strength sessions, runs.

### How to pull intervals.icu data

Use Claude in Chrome (browser) as the primary method - the VM proxy blocks direct API calls
(403). Navigate to https://intervals.icu/activities/{athlete_id}, match by date, and extract
data from the activity detail page. Fall back to direct API only if browser is unavailable,
and expect it to fail from the VM. Credentials are stored as environment variables in .mcp.json:
- Athlete ID: `INTERVALS_ATHLETE_ID`
- API key: `INTERVALS_API_KEY`

Base URL: `https://intervals.icu/api/v1/athlete/{INTERVALS_ATHLETE_ID}/`

Authentication: HTTP Basic Auth - username `API_KEY`, password is the value of `INTERVALS_API_KEY`.

Match the activity to intervals.icu by date. Then fetch:
- `/activities` filtered by date to get the activity ID
- `/activities/{id}` for full detail including zone distributions and decoupling

Pull these fields:
1. **HR zone distribution** - time in each zone as % of ride time
2. **Power zone distribution** - time in each zone as % of ride time (zones from source-of-truth.md)
3. **Cardiac decoupling** - aerobic decoupling % (Pa:Hr ratio)
4. **NP, IF, TSS** - normalized power, intensity factor, training stress score

### Writing intervals.icu data to the session log

Add a Coach flag to today's session-log entry when cardiac decoupling is above threshold.
The raw zone data does not need to be stored in the session log - it can always be pulled
fresh. What matters is the interpretation.

Write the decoupling result to Coach flags like this:

```
Cardiac decoupling [X.X%] on [ride name] - [excellent / acceptable / concern].
[If concern: "Second/third time above 10% this block. Watch durability on next outdoor ride."]
```

For reference during the current session, display the full zone breakdown inline in the
conversation - but do not write all zone data to the session log.

Cardiac decoupling thresholds:
- Under 5%: excellent - no flag needed
- 5-10%: acceptable - note it in conversation, flag only if it is a repeated pattern
- Above 10%: concern - flag explicitly in Coach flags, factor into current and next recommendation

### If intervals.icu data is unavailable

Note the failure in the session. Do not block the rest of the session. Prompt the user to
check if the activity has synced yet - intervals.icu can lag 10-15 minutes after a ride.

## Session log timestamp field

The `strava_last_pull` field in today's session-log entry governs API throttling:

```
strava_last_pull: [ISO timestamp or "not pulled"]
```

Read this before any Strava API call. Update it immediately after every pull.

---

## Cadence HUD — update after intervals.icu enrichment

After enriching an outdoor ride with intervals.icu data, update the Cadence HUD artifact
to switch it to cycling mode and populate Zones 4 and 5 with the ride data.

### Step 1 — Compute session flags

Evaluate these four flags using the enriched ride data and thresholds from source-of-truth.md:

**1. Cardiac Decoupling**
- severity: `'red'` if > 10%, `'yellow'` if 5–10%, omit if ≤ 5% (unless repeated pattern)
- label: `'Cardiac Decoupling'`
- value: e.g. `'11.3%'`
- detail: one sentence (e.g. `'Third time above 10% this block — durability ceiling watch.'`)
- trend: array of recent decoupling values if available (e.g. `['4.2', '10.4', '11.3']`)

**2. Fueling Rate**
- severity: `'blue'` if rate is above previous ceiling (new ceiling update), `'yellow'` if
  significantly under ceiling (> 15g/hr below), omit if within normal range
- label: `'Fueling Rate'`
- value: e.g. `'72.6 g/hr'`
- detail: one sentence comparing to ceiling

**3. Cadence**
- severity: `'yellow'` if average cadence below 85 rpm floor
- label: `'Cadence'`
- value: e.g. `'82 rpm'`
- detail: `'Below 85 rpm floor — torque over spin increases sciatica risk.'`

**4. Recovery Compliance**
- severity: `'yellow'` if today's WHOOP recovery was yellow or red and this was an outdoor ride
- label: `'Recovery Compliance'`
- value: e.g. `'Yellow recovery'`
- detail: `'Ride executed on yellow recovery — document for pattern tracking.'`

Only include flags where the condition is met. Empty array is valid.

### Step 2 — Build the rideData object

```javascript
{
  distance_mi: <number, 1 decimal>,
  duration_str: '<Xh Ym>',
  elevation_ft: <number, 0 decimals>,
  avg_power: <number>,
  norm_power: <number>,
  intensity_factor: <number, 2 decimals>,
  avg_hr: <number>,
  max_hr: <number>,
  max_hr_pct: <number>,            // max_hr / max_hr_from_profile * 100
  cadence_avg: <number>,
  cardiac_decoupling_pct: <number, 1 decimal>,
  fueling_in_g: <number>,          // carbs consumed (from session log / user input)
  fueling_rate_ghr: <number, 1 decimal>,
  fueling_used_g: <number>,        // estimated from power/duration (optional, 0 if unknown)
  fueling_deficit_g: <number>,     // fueling_used_g - fueling_in_g (0 if unknown)
  zones: [
    { zone: 'Z1', minutes: <number>, pct: <number> },
    { zone: 'Z2', minutes: <number>, pct: <number> },
    { zone: 'Z3', minutes: <number>, pct: <number> },
    { zone: 'Z4', minutes: <number>, pct: <number> },
    { zone: 'Z5', minutes: <number>, pct: <number> },
    { zone: 'Z6', minutes: <number>, pct: <number> }
  ]
}
```

### Step 3 — Check whether the artifact exists

Call `mcp__cowork__list_artifacts`. If `cadence-hud` is not present, skip.

### Step 4 — Read current artifact HTML and inject updates

Read the artifact HTML. Find the `window.CADENCE_DATA = {` block written by morning-check-in.
Update these fields:

```javascript
sessionMode: 'cycling',
sessionPhase: 'complete',
rideData: { /* rideData object from Step 2 */ },
sessionFlags: [ /* flags array from Step 1 */ ]
```

Do not change coachingCall, eventDate, ftpWatts, or other constants.

Write the modified HTML to the outputs directory (`cadence-hud-updated.html`), then call:

```
mcp__cowork__update_artifact(
  id = 'cadence-hud',
  html_path = '<path>',
  update_summary = 'Ride synced: <distance>mi, <duration>, DC <X.X%>'
)
```

The artifact will:
- Zone 4 → switch to cycling mode, show ride stats panel
- Zone 5 → show session flags (or empty if none)

### If artifact update fails

Log `hud_update: failed` in today's session-log entry. Do not block the rest of the session.
