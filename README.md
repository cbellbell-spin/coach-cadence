# Coach Cadence

A Cowork plugin for data-driven endurance and strength training. Integrates Whoop recovery data with structured cycling and strength programming to deliver daily recommendations and weekly planning.

---

## What it does

- Runs a morning check-in automatically at session start — pulls Whoop, checks training history, delivers one decisive recommendation
- Tracks a rolling session log and block-level trajectory
- Enforces training rules: 48-hour buffer, yellow = no intensity, strength non-negotiable
- Flags rationalization patterns before they become bad decisions
- Manages a canonical Source of Truth file for training state
- Updates a Cadence HUD artifact with each coaching decision

---

## First-time setup

### 1. Create your project folder

```
mkdir -p ~/cowork/Projects/adaptive-training-coach
```

### 2. Copy the source of truth file

Copy `skills/training-knowledge/references/source-of-truth.md` to:
```
~/cowork/Projects/adaptive-training-coach/source-of-truth.md
```

Update it with your current values before the first session.

### 3. Configure MCP servers

Edit `.mcp.json` and replace the placeholder URLs:

- **Whoop:** Replace `REPLACE_WITH_YOUR_WHOOP_MCP_URL` with your deployed Whoop MCP endpoint
- **Strava:** Leave as placeholder until Strava MCP is built (see below)

### 4. Verify Whoop OAuth scopes

Ensure your Whoop OAuth app has `read:workout` scope enabled in addition to recovery, sleep, and strain. Without it, strength sessions won't appear in workout history.

---

## Commands

All commands are thin entry points that load the corresponding skill. The skill owns the workflow; the command just routes.

| Command | What it does |
|---------|-------------|
| `/morning-check-in` | Daily Whoop pull + recommendation (also runs automatically at session start) |
| `/weekly-review` | Week rollup, classification, upcoming week plan |
| `/log-workout` | Manual log for strength sessions or qualitative notes |
| `/onboarding` | First-session profile interview (new users) |
| `/update-profile` | Mid-session profile updates |
| `/update-source-of-truth` | Guided update of FTP, weight, strength loads, event info |

---

## Memory files

The plugin reads and writes the following files in your project folder. Files are created on first use.

**Live (canonical state):**
- `source-of-truth.md` — FTP, weight, strength loads, event info. Updated only via `/update-source-of-truth`.
- `user-profile.md` — onboarding profile (goals, schedule, health context). Updated via `/onboarding` and `/update-profile`.

**Three-tier memory** (managed by the `notes-manager` skill):
- `session-log.md` — rolling coaching context. Last 7 days, kept compact: recommendations, key factors, qualitative notes, Coach flags. No raw Whoop/Strava data.
- `phase-trends.md` — block-level trajectory. Written at meaningful training boundaries (rest week, event completion, fitness test), not on a calendar schedule.
- `permanent-record.md` — append-only. DEXA, FTP history, events, injuries, strength progression.

**Mann-pattern artifacts** (driven by `weekly-review`):
- `current-block-plan.md` — the living plan for the current week. Overwritten each weekly review.
- `coaching-decisions.md` — coaching rationale. Written by `/session-close` after confirmed calls. Pruned at 6 weeks.

Do not edit `session-log.md`, `phase-trends.md`, or `coaching-decisions.md` manually while the plugin is active — they're written by the plugin.

---

## Strava MCP (to be built)

Strava integration is planned but not yet implemented. When built, it will provide:
- Recent activities (last 7 days)
- Basic stats (duration, distance, elevation)

Until then, the plugin will note when Strava data is unavailable and rely on `session-log.md` for activity context.

---

## Training phase awareness

The plugin knows what phase you're in based on today's date:

| Phase | Dates | Behavior |
|-------|-------|----------|
| Event Prep | Now → May 3, 2026 | Durability ramp, countdown, maintenance inside 3 weeks |
| Post-Event Recovery | May 4–17, 2026 | Rest block, no training targets |
| New Block | May 18, 2026+ | Prompts for next goal before recommending |

---

## Canonical rules the plugin enforces

- Yellow WHOOP = no intensity, no exceptions
- 48-hour buffer: Session A → intensity cycling
- Green recovery ≠ bonus volume
- Fueling is mechanical — appetite suppression is active (GLP-1)
- Strength sessions are non-negotiable
- Cadence over torque (target 85–95 rpm)
- Sciatica is a chronic risk factor — flagged proactively
