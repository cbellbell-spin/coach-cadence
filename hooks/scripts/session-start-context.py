#!/usr/bin/env python3
"""
SessionStart command hook — opens the session with the morning check-in, but
only inside an actual training workspace.

Replaces a prompt-type SessionStart hook. SessionStart does not support
prompt-type hooks (per https://code.claude.com/docs/en/hooks: "SessionStart
and Setup support command and mcp_tool hooks. They don't support http,
prompt, or agent hooks."), so the original was an invalid combination and is
rejected by the Cowork install approval UI. Mirrors the equivalent script in
kate-career-coach.

The guard matters because this is installed as a personal (cross-project)
plugin: "the plugin is enabled" and "this is a training session" are not the
same thing. Without it, every unrelated Cowork session opens by trying to run
a morning check-in.

`source-of-truth.md` is the marker — the coach cannot do anything useful
without it, so its absence means this is not a training workspace.

Per the docs, plain stdout already reaches Claude for this event, so a hook
that only loads context can print directly and exit 0 — no JSON envelope.
"""
import json
import os
import sys

INSTRUCTIONS = """A new training session has started. Run the morning-check-in skill before responding to the user."""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # No parseable payload — can't determine cwd, so can't confirm this is
        # a training workspace. Stay silent rather than risk bleed-over.
        return 0

    cwd = payload.get("cwd") or os.getcwd()

    if not os.path.isfile(os.path.join(cwd, "source-of-truth.md")):
        return 0

    print(INSTRUCTIONS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
