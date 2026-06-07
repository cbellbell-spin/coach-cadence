---
name: update-source-of-truth
description: >
  Guided update of canonical training values - FTP, body weight, strength loads, monthly
  notes. Requires explicit confirmation before any write. Also logs FTP and event changes
  to the permanent record. Trigger phrases: "update source of truth", "update my FTP",
  "update my weight", "update my loads", "new FTP".
---

# Update Source of Truth

The only sanctioned way to update `source-of-truth.md`. Never update this file outside of
this command.

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

- Monthly notes are append-only - never edit or delete existing monthly entries
- FTP changes should prompt: "Has this been tested or is this an estimate?" - record the source
- Body weight changes: record without commentary
- Do not infer updates from conversation - only update what Chris explicitly provides here
- If Chris mentions a value in passing during a check-in that differs from source-of-truth.md,
  flag the discrepancy and direct them to run this command. Do not update automatically.

## Permanent record - log FTP and event changes

When updating FTP or recording an event result, also append to `permanent-record.md`:
- FTP change: add a row to the FTP History table with date, new value, old value, and method
  (tested / estimated / adjusted)
- New event added: add a row to the Event Results table once the event completes
- Body composition change: if DEXA results are being entered, add to DEXA Results table

Create `permanent-record.md` with full headers if it does not yet exist.

## After updating

Confirm what was changed and the new value. No need to re-run morning check-in unless FTP
changed (zones will need recalculating).
