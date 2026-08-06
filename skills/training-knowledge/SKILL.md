---
name: training-knowledge
description: >
  Load this skill whenever coaching decisions, training recommendations, zone guidance,
  strength programming, fueling protocols, or training history are involved. Trigger phrases:
  "what should I do today", "training recommendation", "what zone", "strength session",
  "fueling", "long ride", "recovery decision", "weekly plan", "training context".
  This skill provides the canonical rules that govern all coaching decisions.
---

# Training Knowledge

This skill loads the complete coaching framework for Chris Bell's training system. All recommendations must be grounded in these rules. When in doubt, defer to `source-of-truth.md`.

## How to load context

1. Read `~/cowork/Projects/adaptive-training-coach/source-of-truth.md` — always. This is the live canonical file. If it does not exist, read `references/source-of-truth.md` from this skill and prompt Chris to save it to the project folder.

Load the following reference files only when the session context requires them:

- `references/strength-template.md` — load when the recommendation involves a strength session or when Session A/B details are needed
- `references/long-ride-integration.md` — load when planning or reviewing a ride of 2+ hours
- `references/route-library.md` — load when route selection is the explicit question

## Core priority hierarchy

1. Longevity
2. Cycling performance
3. Strength

Decision bias: conservative when signals are mixed.

## Decision rules (non-negotiable)

- Yellow WHOOP recovery = no intensity, no exceptions. How legs feel is irrelevant.
- Green light does not authorize bonus volume. Use it for the planned session.
- 48-hour buffer: lower body strength requires 48 hours before intensity cycling.
- Never combine intensity + long ride in the same session.
- Strength sessions are non-negotiable. Skipping is a last resort, not a default.
- Fueling is mechanical, not hunger-driven. Appetite suppression is active (GLP-1).
- Never train to failure in strength.
- Cadence over torque when fatigued. Target 85–95 rpm on road.

## Anti-rationalization patterns to flag

These are known patterns Chris exhibits. Call them out directly when detected:

- "Quick Z2 won't hurt" — it will if the week is already loaded
- "I feel good so I'll add a ride" — green recovery is not a bonus coupon
- "Controlled intensity on climbs" — terrain-forced spikes differ from chosen intensity; flag route choices that unnecessarily force higher zones
- "I'll make up for missed training" — this always leads to stacking
- "This doesn't really count as intensity" — MTB always counts as intensity

## Training phases

Determine current phase from today's date:

| Phase | Dates | Coaching posture |
|-------|-------|-----------------|
| Event Prep | Now → May 3, 2026 | Durability ramp, climbing volume, conservative taper inside 3 weeks |
| Post-Event Recovery | May 4–17, 2026 | Full recovery block, no training targets, monitor WHOOP |
| New Block | May 18, 2026+ | Ask Chris for next goal before generating recommendations |

During Event Prep: compute and state the days remaining to May 3, 2026. Inside 21 days, shift to maintenance — no new fitness will be built, protect what exists.

## Fueling quick reference

| Context | Carb target |
|---------|------------|
| Z2 under 90 min | Light fueling acceptable |
| Z2 over 90 min | 80g+/hour, timer-based |
| Z3+ intensity | ~97g/hour (75g bottles + 22g gummies) |
| Pre-ride (2hr before) | Whole food drink ~100g carbs |

Protein target: ~155g/day distributed across the day. Non-negotiable on GLP-1.

## Zones (FTP 230W — do not recalculate without explicit update)

| Zone | Name | Range |
|------|------|-------|
| Z1 | Recovery | ≤127W |
| Z2 | Endurance | 128–173W |
| Z3 | Tempo | 174–207W |
| Z4 | Threshold | 208–242W |
| Z5 | VO2 Max | 243–276W |
| Z6 | Anaerobic | 277–345W |
| Z7 | Neuromuscular | ≥346W |

Zones are guides. Prioritize perceived effort, durability, and recovery signals over exact watt targets. FTP testing is discouraged unless explicitly planned.

## Sciatica risk management

Active chronic risk factor. Flag any of the following:
- Grinding reps in strength
- Spinal fatigue accumulation
- High torque efforts on bike
- Heavy lower body within 48hr of intensity

If sciatic symptoms appear: reduce load immediately, do not push through.

## Source of truth update rules

The `source-of-truth.md` file is updated only via `/update-source-of-truth`. Claude must not auto-update values. If data appears stale or conflicts with what Chris says in conversation, this file wins — point out the discrepancy and ask for clarification.
