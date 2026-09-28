# Workspace Resolution

One athlete per session-connected folder. Each contains `athlete-config.json`,
`user-profile.md`, `source-of-truth.md`, `strength-template.md`, and coaching notes.
Never use a plugin-wide default path, Drive folder ID, or another athlete's folder.
If no folder is connected, ask the user to connect their training folder and stop.
For sessions without filesystem access, the user must explicitly identify that
athlete's Drive folder; read and update files scoped to that folder only.

If desktop/mobile continuity is needed, connect a Drive-mirrored folder and use
that same folder on every surface. Do not create a second copy when access fails.
Keep the existing session-log.md format for now; avoid concurrent coaching sessions
that write the same athlete's files. See ATHLETE.md for identity checks.
