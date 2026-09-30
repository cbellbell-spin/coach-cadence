# Coach Cadence

A Cowork plugin for personal workout planning, gym programming, and review.
The coach starts with the athlete's existing routine and agrees improvements with
them. It publishes prescribed workouts to Workout Tracker and reviews the logged
results. Whoop, Strava, cycling, and HUD features are optional.

## Two-person setup

Use one maintained plugin and one separate Cowork folder per athlete. Connect each
athlete to the Coach Cadence remote connector with the same account they use in
Workout Tracker. The connector exposes narrow workout tools, derives identity from
OAuth, and relies on Supabase Row Level Security for account separation. It never
accepts an athlete ID as authorization input. See [ATHLETE.md](references/ATHLETE.md).

1. Each athlete signs into the gym app with their own email.
2. Connect an empty folder for the new athlete in Cowork. Copy
   [athlete-config.example.json](references/athlete-config.example.json) into it as
   `athlete-config.json`. Leave unknown IDs unset; do not copy Chris's workspace.
3. Run `/onboarding`. The interview starts with the current gym program, goals,
   equipment, time, and preferences. It creates fresh `user-profile.md`,
   `source-of-truth.md`, and `strength-template.md`. Unknowns remain explicit.
4. Add the Coach Cadence remote connector in Cowork and authenticate with the same
   account used in the app. Call `get_athlete_context`, confirm the identity and
   assigned routines with the athlete, then record the returned account UUID and
   agreed routine UUIDs in athlete-config.json. The connector is the only supported
   Workout Tracker data path; do not connect a generic Supabase SQL tool.
5. Enable only integrations the athlete actually has, using their own connections.
   Gym coaching does not require a wearable. Connector credentials and tokens are
   managed by Cowork and must not be copied into the workspace.
6. Ask the coach to program a session. It verifies the assignment, publishes the
   complete plan atomically, and reads it back before reporting success.
7. Refresh the native app online before the gym. Downloaded plans work offline;
   finished sessions retry on launch, foreground, or pull-to-refresh. After sync,
   ask the coach to review programmed vs actual work.

Until a verified account UUID and routine mapping exist, the coach permits the
interview and the single identity-bootstrap call `get_athlete_context`, but no other
Workout Tracker operation or training recommendation. The example config is
intentionally incomplete. An empty folder alone is ignored by the session hook;
copying the config or explicitly running `/onboarding` bootstraps it.

## Preserve Chris's existing setup

Keep Chris's existing workspace and history. Add his own athlete config, verified
account ID, assigned routine IDs, and enabled integrations. His live profile and
strength template take precedence. Historical bundled references are loaded only
with explicit `legacy_chris_profile: true` and confirmation that this is his folder.
They are never defaults for another athlete. Do not replace current goals with old
event dates or bundled loads.

## Commands and memory

- `/onboarding`, `/update-profile`: build and maintain the personal profile.
- `/morning-check-in`, `/weekly-review`: readiness, recent work, and next steps.
- `/log-workout`: qualitative or manual workout notes.
- `/update-source-of-truth`: confirmed updates to canonical training values.
- Ask naturally to program a workout or review a programmed session.

Each workspace owns `session-log.md`, `phase-trends.md`, `permanent-record.md`,
`current-block-plan.md`, and `coaching-decisions.md`. Do not share these files across
athletes. Connect the same folder across devices if continuity is needed.

## Connector operations

The plugin uses `get_athlete_context`, `get_workout_history`, `publish_workout`,
`list_programmed_workouts`, `get_programmed_workout`, and
`reschedule_programmed_workout`. Each response includes the authenticated
`athlete_id`, which must match the workspace binding. Publishing is atomic and
idempotent: retries reuse the original request UUID and cannot create a second plan.

## Verification

Run `python3 -m unittest discover -s tests -v`. These tests verify workspace isolation
and the named-tool contract without contacting the live project. The connector's
database and authorization tests live with its server implementation.
