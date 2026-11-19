# Prompt changelog

One entry per prompt version, newest first. Format: `vN (dd/mm): what changed — why`.
Old prompt files are kept (`critique_v1.md`, `critique_v2.md`, …). The version used by a run is stored as `prompt_version` in its run record.

## v1 (19/11)

Initial version of the critique prompt.

- Evaluates every photo on five fixed dimensions (`subject_story`, `composition`, `light_exposure`, `color_tone`, `technical`), each with a label (`good`, `fine`, `needs_work`, `not_assessable`), a comment and a confidence.
- Infers the photographer's intent first and states it as an assumption with a confidence.
- Gives each dimension its own include/exclude criteria and a tie-break rule, so that a problem has exactly one `root_dimension`. Brightness and lost tonal detail always belong to Light & Exposure.
- Selects at most two priority problems, each with `observation`, `evidence`, `why` and one concrete `what_to_try`. The list is empty when no dimension is `needs_work` or `fine`.
- Lists 0–2 strengths. The list is empty when nothing real can be praised or no dimension can be assessed.
- Evidence is a list of objects with `zone` (3×3 grid, `global` or `cannot_localize`) and `description`.
- Grounding rules: describe only what is visible, never state a camera setting's current value, and use `not_assessable` or a lower confidence when unsure.
- Output is one JSON object that follows the `Critique` schema in `docs/schema.md` (schema version 0.1.0). Field order puts the diagnosis before the advice.
