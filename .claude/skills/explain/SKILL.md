---
name: explain
description: Explain PhoAI code that exists in the repo — a file, function, config or a line the user points at. Use when he runs /explain or asks "what does this do / why is it written like this".
---

# Explain code in this repo

Read-only. Never edit files in this skill.

1. Read the target (file, function, selection). Read only the callers/callees needed.
2. Explain, in Vietnamese with English technical terms:
   - **Purpose**: what problem it solves in PhoAI, which DoD item it serves
   - **Data flow**: inputs → transformations → outputs (types included)
   - **Line by line** for the non-obvious parts only
   - **Why this way**: the design choice and one realistic alternative with its trade-off
   - **Failure modes**: what breaks it (bad input, API errors, edge cases) and whether it is handled
3. If the code is the user's own and something is wrong, point it out directly with the reason.
4. End with 3 questions he should answer without looking (interview style).
   If he answers, grade the answers briefly.
