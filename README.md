# Coach Cadence

A Cowork plugin for personal workout planning, gym programming, and review.
The coach starts with the athlete's existing routine and agrees improvements with
them. It publishes prescribed workouts to Workout Tracker and reviews the logged
results. Whoop, Strava, cycling, and HUD features are optional.

## Two-person setup

Use one maintained plugin and one separate Cowork folder per athlete. This is a
small household setup, not a multi-tenant service. The existing shared Supabase SQL
connector can access both accounts: identity checks and query filters prevent
ordinary mixups, but are not an access-control boundary. See
[ATHLETE.md](references/ATHLETE.md).

1. Each athlete signs into the gym app with their own email. Record their verified
   Supabase Auth UUID, not the shared connector operator's identity.
2. Connect an empty folder for the new athlete in Cowork. Copy
   [athlete-config.example.json](references/athlete-config.example.json) into it as
   `athlete-config.json`. Leave unknown IDs unset; do not copy Chris's workspace.
3. Run `/onboarding`. The interview starts with the current gym program, goals,
   equipment, time, and preferences. It creates fresh `user-profile.md`,
   `source-of-truth.md`, and `strength-template.md`. Unknowns remain explicit.
4. A setup operator assigns the agreed routine types in `workout.user_routines`
   to this athlete. Add those verified UUIDs to `routine_type_ids`. No admin UI or
   new authentication service is required. Use the Workout Tracker setup guide for
   the additive database update and assignment example.
5. Enable only integrations she actually has, using her own connections. Gym
   coaching does not require a wearable. The repository does not contain working
   connector credentials; connect Supabase separately in Cowork.
6. Ask the coach to program a session. It verifies the assignment, publishes the
   complete plan atomically, and reads it back before reporting success.
7. Refresh the native app online before the gym. Downloaded plans work offline;
   finished sessions retry on launch, foreground, or pull-to-refresh. After sync,
   ask the coach to review programmed vs actual work.

Until a verified account UUID and routine mapping exist, the coach permits the
interview and setup but does not query the database or recommend training. The
example config is intentionally incomplete. An empty folder alone is ignored by
the session hook; copying the config or explicitly running `/onboarding` bootstraps it.

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

## Verification

Run `python3 -m unittest discover -s tests -v`. SQL integration checks require a
disposable local PostgreSQL database named `cadence_contract_test`; instructions
are in `tests/test_sql_contract.py`. These tests never query the live project.
