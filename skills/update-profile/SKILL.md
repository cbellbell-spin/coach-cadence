---
name: update-profile
description: Update a specific section of the user profile. Use when the user volunteers new information or explicitly wants to correct something.
---

# /update-profile

Updates `user-profile.md` with new or corrected information.

## Behavior

1. Read the current `user-profile.md`
2. Ask which section to update — or if triggered by mid-session context, show the relevant field and proposed new value
3. Confirm the change before writing: "Update [field] from [old value] to [new value]?"
4. Write after explicit confirmation
5. Append an entry to the Profile completion log: `[date] — [section] — updated`

## Triggered automatically when

The coach notices mid-session that the user has mentioned something that conflicts with or updates a profile field. Surface it naturally: "You mentioned X — want me to update your profile to reflect that?"

## Never

- Auto-update without showing the user what's changing
- Infer profile values from vague conversational references without confirming
