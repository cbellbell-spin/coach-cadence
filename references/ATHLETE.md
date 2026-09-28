# Athlete identity and workspace

Read this before any coaching skill, database operation, or external data pull.
Use only the session-connected athlete folder. Read its `athlete-config.json`.
If absent or invalid, stop coaching and database operations and run onboarding/setup.
Never search another athlete's folder, fall back to Chris's profile, or infer identity
from an email, name, exercise, or previous session.

`display_name` names the athlete. `user_id` must be the UUID of that person's
Supabase Auth account, verified against the account they sign into in the gym app.
A setup operator records it; the shared SQL connector's account is NOT the athlete.
`routine_type_ids` maps that athlete's session labels to existing routine UUIDs.
Verify selected routines belong to the athlete (or are explicitly shared by the app)
before programming. Never invent IDs or copy Chris's routine mapping by default.
UUID fields must parse as UUIDs before being substituted into SQL.

An unset identity permits a profile interview and setup only, never database access
or training recommendations. No identity, no query. Do not store passwords, access
tokens, service keys, or connector credentials in this file.

Every SQL read/update must scope the parent row to `<user_id>` from this config.
Child rows must join their owned parent. Inserts must use this same user ID.
All SQL examples use placeholders, not literal executable values. Bind values when
the connector supports parameters; otherwise use validated UUID/date/numeric values
and correctly escaped SQL string literals (double single quotes). Never concatenate
unescaped athlete text into SQL. Do not run broad exploratory queries over athletes.

This deliberately retains the existing shared Supabase `execute_sql` connector.
Config and WHERE clauses prevent routine mixups, but are NOT an authorization
boundary: privileged SQL can bypass app RLS. Both users must understand that the
connector operator can access both accounts. No custom authentication service is added.

Read `source-of-truth.md`, `user-profile.md`, and `strength-template.md` only from
this workspace. Create fresh files through onboarding. Bundled personal references
are available only if `legacy_chris_profile` is explicitly true AND the user confirms
this is Chris's workspace. They never override newer workspace files. Do not copy
his history, health context, loads, goals, or behavior patterns to another athlete.

Only pull integrations explicitly enabled in `integrations`, using that person's
connections. Missing Whoop/Strava/intervals data is normal: use reported readiness
and app workout history without inventing measurements. HUD updates are optional;
only update an artifact explicitly associated with this athlete's workspace.
