# Athlete identity and workspace

Read this before any coaching skill, Workout Tracker operation, or external data
pull. Use only the session-connected athlete folder. Read its athlete-config.json.
If absent or invalid, stop coaching and run onboarding/setup. Never search another
athlete's folder, fall back to Chris's profile, or infer identity from a name,
exercise, or previous session.

## Authenticated Workout Tracker identity

The Coach Cadence connector authenticates the athlete with the same account used in
the gym app. Its tools derive identity from the OAuth bearer token and do not accept
a `user_id` argument. Supabase Row Level Security enforces ownership.

`display_name` names the athlete. `user_id` pins this workspace to the authenticated
account UUID. During initial setup only, call `get_athlete_context`; show the returned
identity and routines to the user, obtain confirmation, then record its `athlete_id`
and agreed routine mappings in athlete-config.json. Until that binding is complete,
do not call any other Workout Tracker tool or recommend training.

For every later tool result, require `athlete_id` to equal the pinned `user_id`. Stop
on a mismatch and ask the athlete to reconnect the correct account. Never pass the
pinned ID as authorization data, and never store passwords, access tokens, refresh
tokens, service keys, or connector credentials in the workspace.

`routine_type_ids` maps that athlete's session labels to routine UUIDs returned by
`get_athlete_context`. Verify the selected routine remains active before programming.
Never invent IDs or copy another athlete's routine mapping.

## Allowed Workout Tracker tools

Use only these narrow named tools:

- `get_athlete_context` — authenticated identity and active assigned routines
- `get_workout_history` — recent owned workout sets for one assigned routine
- `publish_workout` — atomically publish one complete plan with an idempotent request ID
- `list_programmed_workouts` — list owned plans by status, routine, or date
- `get_programmed_workout` — read one owned plan and optionally its linked actuals
- `reschedule_programmed_workout` — move one owned pending plan

Do not use `execute_sql`, a generic database tool, REST table access, or broad
exploratory queries. The connector returns `not_found` for inaccessible IDs so one
athlete cannot learn whether another athlete's record exists. Treat
`unauthenticated`, `routine_not_assigned`, `not_found`, `not_pending`,
`validation_error`, and `conflict` as failures; do not bypass them with another data
path. Never expose raw connector or database error details to the athlete.

Read `source-of-truth.md`, `user-profile.md`, and `strength-template.md` only from
this workspace. Create fresh files through onboarding. Bundled personal references
are available only if `legacy_chris_profile` is explicitly true AND the user confirms
this is Chris's workspace. They never override newer workspace files. Do not copy
his history, health context, loads, goals, or behavior patterns to another athlete.

Only pull integrations explicitly enabled in `integrations`, using that person's
connections. Missing Whoop/Strava/intervals data is normal: use reported readiness
and app workout history without inventing measurements. HUD updates are optional;
only update an artifact explicitly associated with this athlete's workspace.
