---
name: training-knowledge
description: Load the current athlete's profile, program, and constraints before coaching or strength programming.
---

# Training Knowledge

Read the plugin's `references/ATHLETE.md` first and resolve the session athlete.
Stop and run setup/onboarding if identity or the workspace source of truth is missing.
Never load bundled personal values as a fallback.

Read this athlete's `source-of-truth.md` and `user-profile.md`. For strength work,
read their workspace `strength-template.md`, including current program, equipment,
loads, progression preferences, and accepted changes. Their goals determine priorities;
cycling, event dates, medication, nutrition targets, and injury assumptions are not defaults.

If `legacy_chris_profile` is explicitly true and this is confirmed as the athlete's workspace,
read `references/legacy-chris.md` for his established framework, but ignore its fallback
file instruction: missing workspace data requires setup. Live workspace data overrides
historical dates, values, and personal assumptions. Additional bundled references are
for the athlete only and require the same opt-in.

Use reported constraints and recent performance when choosing a manageable session.
Do not infer medical conditions or prescribe a copied load. If the needed training
information is absent, ask for it. Do not silently replace the athlete's current program.
Explain proposed changes and record those they accept. Source-of-truth values change
only through `/update-source-of-truth`; flag conflicting information for clarification.
