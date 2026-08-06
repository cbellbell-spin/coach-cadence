---
name: update-source-of-truth
description: Guided update of canonical training values — FTP, body weight, strength loads, monthly notes. Requires explicit confirmation before any write.
---

# /update-source-of-truth

The only sanctioned way to update `source-of-truth.md`. Never update this file outside of this command.

## Behavior

1. Read `~/cowork/Projects/adaptive-training-coach/source-of-truth.md`
2. Ask Chris which section to update:
   - Current status (weight, FTP)
   - Strength loads (Session A or B)
   - Event info (new event, new date)
   - Injury/risk context
   - Monthly notes (append only)
   - Metabolic context
3. Show the current value and the proposed new value side by side
4. Ask for explicit confirmation: "Update [field] from [old] to [new]?"
5. Only write after receiving a clear yes

## Rules

- Monthly notes are append-only — never edit or delete existing monthly entries
- FTP changes should prompt: "Has this been tested or is this an estimate?" — record the source
- Body weight changes: record without commentary
- Do not infer updates from conversation — only update what Chris explicitly provides in this command
- If Chris mentions a value in passing during a check-in that differs from source-of-truth.md, flag the discrepancy and direct them to run this command. Do not update automatically.

## After updating

Confirm what was changed and the new value. No need to re-run morning check-in unless FTP changed (zones will need recalculating).
