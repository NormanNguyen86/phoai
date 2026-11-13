---
name: start
description: Open a PhoAI coding session for one task. Use when the user runs /start, says "start session", or names the issue/task he is about to code.
---

# Start a coding session

1. Read `docs/STATUS.md` and the current spec it links to. If the user named an issue,
   read it (`gh issue view <n>` if available, otherwise ask him to paste it).
2. Check git state: current branch, uncommitted changes. If he is on `main`, suggest a
   branch name (`feat/…`, `fix/…`, `docs/…`) — he creates it himself.
3. Restate in 3 lines: the task, its done-criterion, which DoD item it moves.
   If the task is not in the current spec, say so and suggest the Backlog.
4. Ask: "How do you plan to do it?" Wait for his plan or pseudo-code.
5. Comment on the plan only: gaps, risks, edge cases, what to read first (official docs).
   Do not write core code.
6. Remind: one task = one session; `/check` before committing; `/clear` when done.
