---
description: Introduce the coach to a new user, build their profile through a structured interview, and write user-profile.md. Runs automatically on first session. Can be resumed in subsequent sessions.
---

# /onboarding

Build the user's profile through a conversational interview. This is how the coach learns enough to give useful recommendations. The better the profile, the better every recommendation that follows.

## Detecting when to run

Read `~/cowork/Projects/[coach-project-folder]/user-profile.md`:

- **File does not exist** — new user. Run full onboarding pitch, then Tier 1 interview.
- **File exists, sections marked [pending]** — returning user with incomplete profile. Resume from highest-priority pending section. No pitch needed.
- **File exists, all sections complete or declined** — skip entirely. Do not run onboarding.

The project folder name may vary by user. If uncertain, check what folder the other coach files (daily-log.md, source-of-truth.md) live in and use the same one.

## Opening pitch (new users only)

Deliver this once, naturally, before asking anything:

Explain that the coach works best when it understands who the user is — their goals, schedule, health context, and how they respond to training stress. Offer two paths:

1. **Full interview now** — 10–15 minutes, covers everything, coach is fully calibrated from session one
2. **Light version now** — 5 minutes for the essentials, coach fills in the rest naturally over the next few sessions

If the user declines both or wants to skip entirely: respect it, create the profile file with all sections marked [pending], and proceed to the daily check-in. The coach will surface questions naturally over time.

## Tier 1 — ask in first session regardless of path chosen

These are required for any useful recommendation. Ask conversationally, not as a list. Group related questions together. Do not ask more than 2–3 questions at a time before letting the user respond.

1. What's your primary sport or activity?
2. What other activities do you do, and how often?
3. What's your next goal or event — and when is it?
4. How many days per week and hours per week can you realistically train?
5. Any current injuries, chronic conditions, or physical limitations I should know about?
6. Any medications that affect training — energy, heart rate, fueling, sleep, or recovery? *(If the user asks why: explain that certain medications change how HR, fueling, and recovery signals behave, which affects what good advice looks like. If they decline: mark as [declined], move on.)*

After Tier 1: write what was gathered to `user-profile.md`. If the user chose the light path, wrap up and flag that you'll ask more over the next few sessions. If they chose the full interview, continue to Tier 2.

## Tier 2 — full interview or spread across sessions

Ask these over the first 2–3 sessions if not collected upfront. Weave them in naturally — no flag, no "survey" framing. Just ask when there's a natural opening.

- What does a successful training week feel like to you — how do you know when you've done enough?
- What typically gets in the way of your training week?
- When you miss a session, how do you usually respond?
- Do you tend to push harder when you're feeling good, even if it wasn't planned?
- How much explanation do you want when I give you a recommendation — just the what, or the why too?
- How direct do you want me to be when I think you're rationalizing a bad decision?
- What's your typical training window — morning, evening, lunch?
- Does your job involve travel or unpredictable hours?

## Tier 3 — enrich when natural, no urgency

- What's your broader goal beyond the next event — longevity, performance, health, weight?
- Have you worked with a coach or structured program before? What worked, what didn't?
- Any past injuries that were caused by specific training mistakes?
- Do you prefer training solo or with others?
- What indoor training equipment do you have access to?

## Handling declines

If a user skips or declines any question:
- Mark the field as [declined] in user-profile.md
- Do not re-ask unless it becomes directly relevant to a recommendation
- When re-asking because it's relevant: don't frame it as a retry — frame it as needing the information for today's decision

## Writing the profile

After each session where new information is gathered:
1. Read the current `user-profile.md`
2. Fill in answered fields, replacing the blank with the user's answer
3. Update section status: [pending] → [complete] or [partial] if only some fields answered
4. Append an entry to the Profile completion log at the bottom
5. Leave [declined] fields as-is unless the user volunteers the information

## If the user updates information mid-session

If the user mentions something that contradicts or updates a profile field (e.g., "I actually only have 4 days a week now"), update the profile immediately and note the change in the completion log.
