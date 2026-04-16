---
name: activity-sync
description: >
  Apply this skill when pulling activity data from Strava, checking whether a sync is due,
  or fetching intervals.icu data for a specific ride. Trigger phrases: "I finished a ride",
  "just got back", "completed a workout", "sync activities", "check Strava", "pull my ride data",
  "pull intervals.icu", "enrich this ride". Governs all activity data refresh logic and
  intervals.icu enrichment.
---

# Activity Sync

Governs when and how activity data is pulled from Strava and enriched via intervals.icu.

## Strava pull logic

Pull Strava activity data when ANY of the following are true:

- **First conversation of the day** — no Strava pull recorded in today's daily log entry
- **4+ hours since last pull** — check `strava_last_pull` timestamp in today's daily log
- **User reports completing an activity** — any phrase indicating a session just finished

Never pull Strava more than needed. Check the log timestamp before calling the API.

After every Strava pull: update `strava_last_pull` timestamp in today's daily log.

## What to pull from Strava

Recent activities — last 7 days, basic stats:
- Activity name, type, date
- Duration, distance, elevation gain
- Average HR, average power (if available)
- Activity type flag: outdoor ride / indoor ride / strength / run / other

## Intervals.icu enrichment — on demand only

Enrichment runs when the user confirms they want it. Never auto-trigger at session start.

After a Strava pull, `morning-check-in` checks for unenriched outdoor rides and offers enrichment. If the user confirms, execute this section.

**Outdoor ride definition:** activity type is "Ride" — not "VirtualRide", not "EBikeRide", not sport types indicating Peloton or spin bike.

**Do not enrich:** VirtualRide, indoor trainer sessions, Peloton rides, strength sessions, runs.

### How to pull intervals.icu data

The VM proxy blocks direct API calls (returns 403). Use Claude in Chrome as the primary method.

**Browser (primary):** Navigate to `https://intervals.icu/activities/{athlete_id}`. Match by date. Open the activity detail page. Extract HR zones, power zones, cardiac decoupling, NP/IF/TSS.

**Direct API (fallback):** If browser is unavailable, attempt with env vars (`INTERVALS_ATHLETE_ID`, `INTERVALS_API_KEY`). Basic Auth — username `API_KEY`, password is the value of `INTERVALS_API_KEY`. Expect this to fail from the VM.

Base URL: `https://intervals.icu/api/v1/athlete/{INTERVALS_ATHLETE_ID}/`

Match the activity by date, then fetch:
- `/activities` filtered by date to get the activity ID
- `/activities/{id}` for full detail

Pull these fields:
1. HR zone distribution — time in each zone as % of ride time
2. Power zone distribution — time in each zone as % of ride time
3. Cardiac decoupling — aerobic decoupling % (Pa:Hr ratio)
4. NP, IF, TSS

### Writing intervals.icu data to the log

Append to the ride's entry in daily-log.md:

```
**Intervals.icu:**
HR zones: Z1 X% | Z2 X% | Z3 X% | Z4 X% | Z5 X%
Power zones: Z1 X% | Z2 X% | Z3 X% | Z4 X% | Z5 X%
Cardiac decoupling: X.X% [excellent / acceptable / concern]
NP: XW | IF: X.XX | TSS: XXX
```

Cardiac decoupling thresholds: under 5% excellent, 5–10% acceptable, above 10% is a concern — flag explicitly and carry into the next recommendation.

### If intervals.icu is unavailable

Note the failure in the log. Do not block the rest of the session. Prompt the user to check if the activity has synced — intervals.icu can lag 10–15 minutes after a ride.

## Daily log timestamp field

```
strava_last_pull: [ISO timestamp or "not pulled"]
```

The coach reads this to determine whether a 4-hour refresh is due.
