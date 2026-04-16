---
description: >
  Run at the start of every session. Load training history, pull Whoop data
  (once per day only), and deliver a single decisive training recommendation.
  Trigger phrases: "morning check-in", "start session", "what should I do today", "good morning".
---

# Morning Check-In

Run at the start of every session. Check the daily log before touching any external service — if today's data is already cached, use it.

## Steps

1. Load `training-knowledge`, `daily-coaching`, `activity-sync`, and `notes-manager` skills
2. Read the daily log

### Whoop — once per day only

Check the daily log for today's entry:

- **Entry exists with Whoop data** — skip all Whoop calls. Use cached data. Jump to Strava.
- **No entry for today** — ask: "Want me to pull yesterday's Whoop data?"
  - If yes: pull and write to today's log immediately, then proceed.
  - If no: ask for recovery color, HRV, RHR, and sleep hours manually. Write those to today's log.

When pulling Whoop, use **two calls only**:
- `whoop_get_training_summary` — recovery score, HRV, RHR, prior day strain, sleep summary, coaching snapshot
- `whoop_get_latest_sleep` — sleep stage breakdown (light, SWS, REM, awake cycles)

Write Whoop data to today's log immediately after pulling. Never call Whoop again for the same day.

### Strava

Pull recent activities (last 7 days basic stats) — skip if `strava_last_pull` in today's log is less than 4 hours ago. Update `strava_last_pull` timestamp after every pull.

### Intervals.icu — on demand only

After the Strava pull, check whether any outdoor rides in the last 7 days are missing intervals.icu data in the log. If any are unenriched, offer: "I can pull intervals.icu data for [ride name / date] — want me to do that now?" Do not enrich automatically. If the user confirms, use the `activity-sync` skill to fetch and write the data.

### Compile context and recommend

3. Before generating the recommendation, identify only what is load-bearing for today's decision from the last 7 days of log and Strava data:
   - Last Session A — when, is the 48-hour buffer clear?
   - Last intensity ride — when, what was it?
   - Ride hours accumulated this week
   - Any cardiac decoupling flags from enriched outdoor rides
   - Any pattern worth naming — missed sessions, consecutive hard days, underfueling notes

4. Apply daily coaching framework per `daily-coaching` skill
5. Generate recommendation in the narrative voice defined in `daily-coaching`
6. Write recommendation summary to today's entry in `daily-log.md`

## If Whoop fails

Note it. Ask for recovery color, HRV, RHR, and sleep hours manually. Write those to today's log so the rest of the session has context.

## If Strava is unavailable

Proceed without it. Note the gap. Rely on daily-log.md for recent activity context.
