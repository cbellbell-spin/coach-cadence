---
description: Manually log a strength session, indoor ride, or any activity not captured by Whoop or Strava. Appends context to today's daily log entry.
---

# /log-workout

Use this to record qualitative context that Whoop and Strava don't capture — how a session felt, load used, any flags.

## Prompt Chris for

- Session type: Strength A / Strength B / Indoor ride / Other
- Duration (minutes)
- For strength: any loads changed from source-of-truth.md?
- RPE (1–10)
- How did it feel: smooth / normal / heavy / grinding
- Any physical flags: back, sciatica, joints
- Fueling: adequate / skipped / partial
- Any notes worth carrying forward

## Write behavior

1. Read `~/cowork/Projects/adaptive-training-coach/daily-log.md`
2. Find today's entry (if morning check-in was run, it exists)
3. Append to the Notes field of today's entry
4. If no entry for today exists, create one with the logged data and mark it as manually created (no Whoop pull)

## If loads changed vs source-of-truth.md

Note the discrepancy in the log entry and prompt: "This looks different from your recorded working loads. Want to update source-of-truth.md?" — do not update automatically.

## Tone

No commentary on the quality of the session unless Chris asks. Log the facts. If grinding reps or sciatic flags are mentioned, note it clearly and remind Chris of the red flag protocol.
