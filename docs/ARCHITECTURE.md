# Cadence — Integrations & Data Flow

How Coach Cadence connects to external systems, and where each piece of data lives. This
reflects what the plugin's skills/commands actually call, verified against the source in this
repo — not an aspirational design.

## At a glance

| System | Type | Status | Used for |
|---|---|---|---|
| Whoop | MCP server | Working, concrete tool calls | Recovery, sleep, strain, workouts |
| Strava | MCP server | **Not wired in** — referenced in prose only | Recent activity list (duration, distance, power, HR) |
| intervals.icu | Direct REST API (no MCP) | Working, browser-first | HR/power zones, cardiac decoupling, NP/IF/TSS |
| Cowork artifact (`cadence-hud`) | `mcp__cowork__*` tools | Working | Live HUD showing today's session state |
| Local project files | Filesystem | Working | All persistent memory (7 files, no database) |
| `workout-tracker` (iOS/Supabase repo) | — | **No integration exists** | N/A |

## Whoop

Cadence calls a dedicated Whoop MCP server with named tools — this is the most concretely
wired integration in the plugin:

- `whoop_get_latest_recovery`, `whoop_get_latest_sleep`, `whoop_get_strain_range`,
  `whoop_get_training_summary`, `whoop_get_workouts` (daily pulls — see
  [`skills/morning-check-in/SKILL.md`](../skills/morning-check-in/SKILL.md) and
  [`skills/daily-coaching/SKILL.md`](../skills/daily-coaching/SKILL.md))
- `whoop_get_recovery_range`, `whoop_get_sleep_range`, `whoop_get_strain_range` (7-day range
  pulls — see [`commands/weekly-review.md`](../commands/weekly-review.md))

Configured via `.mcp.json` at the plugin root (`REPLACE_WITH_YOUR_WHOOP_MCP_URL` placeholder —
**this file is currently missing from the repo**, see Known Gaps below). The Whoop OAuth app
needs `read:workout` scope in addition to recovery/sleep/strain, or strength sessions won't
appear in workout history.

Pulled once per day and cached: `whoop_pulled: yes | no | manual` is written to today's
`session-log.md` entry, and every later interaction in the day reads the cached value instead
of calling Whoop again.

The backing MCP server is most likely the one hosted from the `claude_coach` repo
(described in this account's repo notes as "cloud-hosted MCP server for Strava and Whoop").

## Strava — referenced but not wired in

`activity-sync`, `morning-check-in`, `daily-coaching`, `weekly-review`, and `notes-manager` all
talk about Strava as a live data source — pull throttling (`strava_last_pull`, 4-hour window),
what fields to extract (duration, distance, elevation, HR, power, activity type) — but **none
of them name an actual Strava MCP tool call**, unlike the Whoop integration above.

The README says this directly: *"Strava integration is planned but not yet implemented... Leave
[.mcp.json] as placeholder until Strava MCP is built."* The skill files were written ahead of
that wiring, assuming it would land later. As of this repo's initial commit, that wiring has not
happened — treat every "pull Strava activities" step in the skills as a no-op until an actual
Strava MCP server is configured in `.mcp.json`.

## intervals.icu — direct API, not MCP

Not an MCP server. `skills/activity-sync/SKILL.md` calls the intervals.icu REST API directly:

- **Primary path:** Claude in Chrome browser automation — navigate to
  `https://intervals.icu/activities/{athlete_id}`, match by date, scrape the detail page. The
  VM's network proxy blocks the direct API call (403), so this is the path that actually works.
- **Fallback:** direct HTTP with Basic Auth (`username=API_KEY`, `password=$INTERVALS_API_KEY`)
  against `https://intervals.icu/api/v1/athlete/{INTERVALS_ATHLETE_ID}/` — documented as
  expected to fail from the VM, kept as a fallback for environments without browser access.
- Credentials: `INTERVALS_ATHLETE_ID`, `INTERVALS_API_KEY` env vars, meant to live in
  `.mcp.json` (again, that file is currently missing — see Known Gaps).

Only triggers for outdoor rides (Strava activity type `Ride`, excluding `VirtualRide`,
`EBikeRide`, Peloton/spin). Pulls zone distributions and cardiac decoupling, writes only the
*interpretation* (a Coach flag) to `session-log.md` — raw zone data is never persisted, it's
re-pulled fresh each time it's needed.

## Cowork artifact — Cadence HUD

A separate integration from data pulls: after Whoop/Strava/intervals.icu data is gathered,
`morning-check-in`, `log-workout`, `program-workout`, and `activity-sync` all update a live
Cowork artifact (`mcp__cowork__list_artifacts`, `mcp__cowork__update_artifact`, artifact id
`cadence-hud`) — an HTML dashboard showing today's session mode, recovery flags, and (after a
ride) power/HR zones and cardiac decoupling. If the artifact doesn't exist yet, these steps are
skipped rather than blocking the rest of the session; if an update fails, it's logged as
`hud_update: failed` in the session log and the session continues.

## Local storage — the actual persistent memory

There is no database. Everything durable lives as markdown files in one Cowork project folder,
managed by `skills/notes-manager/SKILL.md`:

```
~/cowork/Projects/adaptive-training-coach/
├── session-log.md          Tier 1: rolling session context (whoop_pulled, strava_last_pull, notes)
├── phase-trends.md         Tier 2: block-level trajectory
├── permanent-record.md     Tier 3: permanent history
├── user-profile.md         Onboarding profile
├── source-of-truth.md      Canonical training values (FTP, weight, zones, event dates)
├── current-block-plan.md   Living training plan
└── coaching-decisions.md   Coaching rationale log
```

The rule throughout: **live APIs (Whoop, Strava, intervals.icu) are never re-stored** — only
their interpretation (a flag, a recommendation, a decision) gets written here. Raw numbers are
always re-pulled.

## Known gaps

- **`.mcp.json` is missing from this repo.** The README and two skills reference it (Whoop URL
  placeholder, `INTERVALS_ATHLETE_ID`/`INTERVALS_API_KEY` env vars, a Strava placeholder), but
  it was not present in the 0.5.0 build this repo was recovered from. It needs to be recreated
  before the plugin can actually reach Whoop or intervals.icu from a fresh install.
- **Strava has no real backing MCP call** despite being referenced throughout the skills as if
  it were live (see above).

## `workout-tracker` — no integration

The `workout-tracker` repo (SwiftUI iOS app + Supabase backend, at
`~/projects/workout-tracker`) has **no code-level connection to Cadence** — no shared API calls,
no shared Supabase schema, no data exchange in either direction. They are separate, parallel
projects that happen to cover related domains (strength/cardio logging). If a Cadence ↔
workout-tracker integration is wanted, it doesn't exist yet and would need to be designed and
built — this doc reflects current state only.
