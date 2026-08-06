---
description: Load training history, pull prior day's Whoop data (once per day only), and deliver a single decisive training recommendation for the day.
---

# /morning-check-in

Run this at the start of every session. Check the daily log before touching any external service — if today's data is already cached, use it.

## Steps

1. Load `training-knowledge` skill, `daily-coaching` skill, and `activity-sync` skill
2. Load `notes-manager` skill
3. Read `~/cowork/Projects/adaptive-training-coach/daily-log.md`

### Whoop data — pull prior day, once per day only

Check the daily log for an entry dated today:

- **Today's entry exists and contains Whoop data** — skip all Whoop calls. Use cached data from the log. Jump to step 4.
- **No entry for today** — ask the user: "Want me to pull yesterday's Whoop data?"
  - If yes: pull prior day's completed data (see below), write it to today's log entry immediately, then proceed.
  - If no: ask the user to provide recovery color, HRV, RHR, and sleep hours manually. Write those to today's log entry.

When pulling Whoop, use **prior day's completed data only** — not today's in-progress cycle:
- `whoop_get_latest_recovery` — yesterday's completed recovery score, HRV, RHR
- `whoop_get_latest_sleep` — last night's completed sleep session
- `whoop_get_strain_range` — yesterday's completed strain
- `whoop_get_training_summary` — coaching snapshot
- `whoop_get_workouts` — last 7 days

Write Whoop data to today's log entry immediately after pulling. Every interaction for the rest of the day reads from the log — never call Whoop again for the same day.

4. Pull Strava recent activities (last 7 days basic stats) — skip if `strava_last_pull` in today's log entry is less than 4 hours ago. Update `strava_last_pull` timestamp after pulling.

### Intervals.icu enrichment — runs after Strava pull

For each outdoor ride returned by Strava that is not already enriched in today's log:

- Outdoor ride = Strava activity type "Ride" (exclude VirtualRide, EBikeRide, Peloton, spin bike)
- Fetch the matching activity from intervals.icu using the athlete ID and API key from env vars (`INTERVALS_ATHLETE_ID`, `INTERVALS_API_KEY`)
- Match by date; use Basic Auth (username: `API_KEY`, password: value of `INTERVALS_API_KEY`)
- Pull: HR zone distribution, power zone distribution, cardiac decoupling, NP/IF/TSS
- Write to the activity's entry in today's log immediately
- If cardiac decoupling > 10%: flag it explicitly and factor it into today's recommendation
- If intervals.icu is unavailable or the activity hasn't synced yet: note it in the log, do not block the session

5. Apply daily coaching framework:
   - Determine WHOOP color and whether intensity is eligible today
   - Check 48-hour buffer against last Session A
   - Tally weekly load from notes + Strava
   - Factor in any cardiac decoupling flags from intervals.icu
   - Determine current training phase and event countdown
   - Identify any anti-rationalization patterns to preemptively flag
6. Generate recommendation using the format defined in `daily-coaching` skill
7. Update today's entry in `daily-log.md` with recommendation summary

## Tone

Direct and prescriptive. No hedging. One recommendation — not a menu. If signals are mixed, state that clearly and give the conservative option.

## If Whoop pull fails

State that Whoop is not responding. Ask the user to provide: recovery color, HRV, RHR, sleep hours manually. Write those inputs to the log so the rest of the day's interactions have context without needing Whoop.

## If Strava is unavailable

Proceed without it. Note the gap. Rely on daily-log.md for recent activity context.
