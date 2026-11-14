# Architecture Decision Records

One short file per decision: tool choices (uv, pydantic, model provider), design choices
(JSON mode vs function calling, grounding model), and anything an interviewer might ask "why?" about.

- Name: `NNNN-short-title.md` (e.g. `0001-use-uv.md`), numbered in order, never renumbered.
- A decision that changes later gets a **new** ADR that supersedes the old one; the old one stays.
- Start from [0000-template.md](0000-template.md).

| # | Decision | Status |
|---|---|---|
| 0001 | [Use uv for package and environment management](0001-use-uv.md) | accepted |
