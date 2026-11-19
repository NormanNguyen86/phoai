# Critique schema

## Purpose and consumers

The schema.md is a reference document that describes the structure, fields, and rules of the schema used in PhoAI (`Critique` and `RunRecord`). It is intended for developers, reviewers, and anyone who needs to understand or work with the schema.

## Versioning

The schema has its own version, `schema_version`, independent of the project release tags. It starts at 0.1.0. A version below 1.0.0 means the schema is still in initial development and can change; 1.0.0 is reserved for the first version declared stable. The versioning follows semantic versioning principles, where major changes that break backward compatibility will increment the major version, minor changes that add functionality in a backward-compatible manner will increment the minor version, and patches that fix bugs will increment the patch version. While the version is below 1.0.0, a breaking change increments the minor version.

## Top-level structure

`Critique` has six fields. The order is the order in which the model writes them.

| field | type | order | reason |
|---|---|---|---|
| intent | object | 1 | First field: the intent the model assumes for the photo, and how confident it is in that assumption. Everything after it is judged against this intent. |
| analysis_limits | list of text | 2 | Second field: the reasons why parts of the analysis may be unreliable (for example low resolution). It comes before the analysis so that the labels and confidences that follow can take these limits into account. |
| dimensions | object | 3 | Third field: the diagnosis of the photo on five fixed dimensions, so that the model examines each one before giving advice. |
| priority_problems | list | 4 | Fourth field: the one or two most important problems to work on, written after the diagnosis so that the advice follows from it. |
| strengths | list | 5 | Fifth field: what the student should keep doing. It follows the problems, in the same order as the steps in the prompt (diagnose, advise, then list what to keep). |
| overall_summary | text | 6 | Last field: one sentence summarizing the photo and the single most important thing to work on. |

## Field reference

`RunRecord` fields are described in "Run metadata". The `Evidence` object is described in "Evidence format".

### Critique

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| intent | `Intent` object | see "Intent" | yes | The intent the model assumes for the photo, and its confidence in that assumption. |
| analysis_limits | list of text | free text, one reason per item | yes | Reasons why parts of the analysis may be unreliable (for example "the image is too small to judge sharpness"). Always present; an empty list `[]` when there are none. |
| dimensions | `Dimensions` object | exactly five keys, see "Dimensions" | yes | The diagnosis of the photo on five dimensions. |
| priority_problems | list of `PriorityProblem` | 0–2 items, see invariants 3 and 4 | yes | The most important problems to work on. |
| strengths | list of `Strength` | 0–2 items | yes | What the student should keep doing. May be empty. |
| overall_summary | text | one sentence | yes | A summary of the photo and the single most important thing to work on. |

### Intent

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| summary | text | free text | yes | The intent the model assumes, worded as an assumption, not as a fact. |
| confidence | literal | `high`, `medium`, `low` | yes | How sure the model is about the assumed intent. |

### Dimensions

`dimensions` is an object with exactly five keys. Each value is a `Dimension`. The keys are stable identifiers; the names shown to the reader can change without changing the schema.

| key | display name |
|---|---|
| subject_story | Subject & Story |
| composition | Composition |
| light_exposure | Light & Exposure |
| color_tone | Color & Tone |
| technical | Technical Execution |

`Dimension`:

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| label | literal | `good`, `fine`, `needs_work`, `not_assessable` | yes | The rating of this dimension. |
| comment | text | free text | yes | The specific reason for the label. When the label is `not_assessable`, it says why. |
| confidence | literal | `high`, `medium`, `low` | yes | How sure the model is about this rating. |

### PriorityProblem

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| rank | integer | increasing, no duplicates | yes | Importance of the problem; 1 is the most important. |
| root_dimension | literal | one of the five dimension keys | yes | The dimension whose fix solves the problem. A problem has only one. |
| related_dimensions | list of literal | dimension keys, not including `root_dimension` | yes | Other dimensions the problem also touches. May be empty. |
| title | text | free text | yes | A short name for the problem. |
| observation | text | free text | yes | What is actually visible in the photo. |
| evidence | list of `Evidence` | at least 1 item | yes | Where in the photo it shows. |
| why | text | free text | yes | The effect on the viewer, and why the alternative would work better. |
| what_to_try | text | free text | yes | One concrete action for the next shoot. |

### Strength

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| dimension | literal | one of the five dimension keys | yes | The dimension this strength belongs to. |
| observation | text | free text | yes | What is visible in the photo that works well. |
| evidence | list of `Evidence` | at least 1 item | yes | Where in the photo it shows. |

## Invariants

Rules that involve more than one field, or that go beyond the field types. "Code" means a validator in `schema.py` rejects the output. A rejected output is treated as invalid output and goes through the retry path.

| # | Rule | Enforced by |
|---|---|---|
| 1 | The `root_dimension` of a problem is rated `needs_work`, or `fine` when no dimension is `needs_work`. | Code, and stated in the prompt |
| 2 | `related_dimensions` does not contain the `root_dimension`. | Code, and stated in the prompt |
| 3 | `priority_problems` has at most 2 items. | Code, and stated in the prompt |
| 4 | `priority_problems` has at least 1 item when a dimension is rated `needs_work`, and is empty when no dimension is rated `needs_work` or `fine`. When the worst rating is `fine`, it has 0–2 items. | Code, and stated in the prompt |
| 5 | `rank` values are increasing and not duplicated. | Code, and stated in the prompt |
| 6 | `strengths` has at most 2 items. It may be empty. | Code, and stated in the prompt |
| 7 | Every `evidence` list has at least 1 item, and every `description` is not empty. | Code |
| 8 | `Critique` rejects unknown fields, so run metadata cannot appear in the model output. | Code (`extra="forbid"`) |
| 9 | `schema_version`, `prompt_version`, `model_id` and `git_sha` are set by the pipeline, never by the model. | Code (pipeline) |

Rules that exist only in the prompt are listed in "Known limitations / Backlog".

## Evidence format

Every `evidence` field in the schema (in `strengths` and in `priority_problems`) is a **list of `Evidence` objects**. Each object points to one place in the photo.

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| zone | literal | one of the 11 values in the vocabulary below | yes | Where in the photo the observation applies. |
| description | text | non-empty | yes | A short phrase naming what is visible in that zone (e.g. "the small boat on the water"). |

### Zone vocabulary

The photo is divided into a 3×3 grid. Rows are top / middle / bottom, columns are left / center / right. The middle cell is written `center`.

```
top-left       top-center      top-right
middle-left    center          middle-right
bottom-left    bottom-center   bottom-right
```

Two special values sit outside the grid:

| zone | use when |
|---|---|
| `global` | The observation applies to the whole image (for example flat light over the whole lake, or a color cast over the water and sky). |
| `cannot_localize` | The observation is real but the model cannot tell where it is. The model must not guess a grid zone. |

### Rules

- An `evidence` list has at least one item.
- One observation can list several zones: add one `Evidence` object per zone.
- `zone` is validated against the vocabulary above. Any other value (`upper-left`, `middle-center`, `Center`) is rejected.
- Zones refer to the image **as it was sent to the model**, after any preprocessing in the pipeline (for example an orientation fix). The same photo rotated gives different zones.
- A zone is a coarse hint for a beginner about where to look. It is not a coordinate, and in v0.1.0 nothing checks that the description matches what is really in that zone.

## Run metadata

Two objects are used, and they have different authors.

- `Critique`: the object the **model** generates and the schema validates. It has the six fields in "Top-level structure".
- `RunRecord`: the object the **pipeline** stores for one run. It holds the run metadata plus the validated `Critique`.

| field | type | set by | meaning |
|---|---|---|---|
| run_id | text | pipeline | Identifier of the run. Same as the folder name `runs/<run_id>/`. |
| schema_version | text (semver) | pipeline | Version of this schema, read from a single constant next to the schema code. |
| prompt_version | text | pipeline | The prompt file used for the run (for example `critique_v1`). |
| model_id | text | pipeline | The model ID from `config/default.yaml` that was actually called. |
| git_sha | text | pipeline | Commit of the code that produced the run. |
| critique | `Critique` | model | The validated model output. |

Why the metadata is kept out of the model's output:

- The model cannot know its own exact ID or the commit of the code calling it. If asked, it would produce plausible but unreliable values, and a record of "how this output was made" must be reliable.
- The prompt does not ask for these fields and `Critique` rejects unknown fields (`extra="forbid"`). If the model adds one anyway, validation fails and the run goes through the retry path.
- From v0.2, evaluation results are compared across runs. Runs can only be compared fairly if each one states `schema_version`, `prompt_version` and `model_id`.

`schema_version` covers both `Critique` and `RunRecord`. Adding or renaming a field in either object follows the bump rules in "Versioning".

## Valid and invalid examples

### Valid example

A lake photo: a small rowing boat on a calm lake in morning light, hills on the far shore, and a shore line that slopes down toward the left. This is a `Critique`, not a `RunRecord`. The same example is used in `prompts/critique_v1.md`; when one copy changes, change the other. It is shown as an indented block instead of a fenced one, to match the prompt, which tells the model not to use code fences.

    {
      "intent": {
        "summary": "You may have wanted to capture a calm, quiet morning on a lake, with a single boat as the focus.",
        "confidence": "medium"
      },
      "analysis_limits": [],
      "dimensions": {
        "subject_story": {
          "label": "good",
          "comment": "A single small boat on an empty lake gives the photo a clear subject, and the eye goes to it first because it is the only man-made shape.",
          "confidence": "high"
        },
        "composition": {
          "label": "good",
          "comment": "The boat sits in the lower left of the frame with open water stretching ahead of it, so it has room to move, and the far hills stay clear of it.",
          "confidence": "medium"
        },
        "light_exposure": {
          "label": "good",
          "comment": "The soft, even morning light keeps detail in both the bright sky and the dark water, with no clipped highlights or crushed shadows.",
          "confidence": "medium"
        },
        "color_tone": {
          "label": "good",
          "comment": "The cool blue-green palette is consistent across the water, hills and sky, which supports the calm mood.",
          "confidence": "high"
        },
        "technical": {
          "label": "needs_work",
          "comment": "The far shore line slopes down toward the left, which is easy to see against the straight edges of the frame, although the boat itself is sharp.",
          "confidence": "high"
        }
      },
      "priority_problems": [
        {
          "rank": 1,
          "root_dimension": "technical",
          "related_dimensions": [],
          "title": "The horizon is tilted",
          "observation": "The line where the far shore meets the water slopes down from the right side of the frame to the left side, while the calm water should sit flat.",
          "evidence": [
            { "zone": "middle-left", "description": "the far shore line, lower here" },
            { "zone": "middle-right", "description": "the far shore line, higher here" }
          ],
          "why": "The eye expects a horizon to be level, so the tilt looks like a mistake and makes the calm scene feel as if it is sliding to one side. A level horizon lets the quiet mood come through.",
          "what_to_try": "On your next lake shoot, turn on the camera's grid and line the far shore up with a horizontal grid line before pressing the shutter."
        }
      ],
      "strengths": [
        {
          "dimension": "composition",
          "observation": "The boat has open water ahead of it, which gives the scene a feeling of quiet space.",
          "evidence": [
            { "zone": "bottom-left", "description": "the small boat with open water in front of it" }
          ]
        },
        {
          "dimension": "color_tone",
          "observation": "The blue-green palette is consistent from the water to the sky, so nothing distracts from the calm mood.",
          "evidence": [
            { "zone": "global", "description": "the cool blue-green tones across the whole frame" }
          ]
        }
      ],
      "overall_summary": "A calm, well-balanced lake scene held back by a tilted horizon; next time, level the horizon before you shoot."
    }

### Invalid examples

Each case below breaks one rule. The fragment shows only the part that is wrong.

| # | Fragment | Why it is invalid | Caught by |
|---|---|---|---|
| 1 | `"label": "ok"` | Not one of `good`, `fine`, `needs_work`, `not_assessable`. | Literal type |
| 2 | `"zone": "upper-left"` | Not in the zone vocabulary. | Literal type |
| 3 | `"evidence": ["bottom-left: the small boat"]` | `evidence` items must be objects with `zone` and `description`, not strings. | Type check |
| 4 | `"root_dimension": "color_tone"` while `color_tone` is rated `good` | The root dimension of a problem must be rated `needs_work` (or `fine` only when no dimension is `needs_work`). | Validator |
| 5 | `"root_dimension": "composition", "related_dimensions": ["composition"]` | `related_dimensions` must never contain the root dimension. | Validator |
| 6 | `priority_problems` with 3 items | At most 2 problems. | Validator |
| 7 | No dimension is `needs_work` or `fine` (for example all five `good`) and one item in `priority_problems` | The list must be empty when no dimension is `needs_work` or `fine`, because no valid root dimension exists. | Validator |
| 8 | A top-level `"model_id": "..."` in `Critique` | Unknown field (`extra="forbid"`). Metadata belongs to `RunRecord`. | `extra="forbid"` |
| 9 | One dimension is `needs_work` and `"priority_problems": []` | At least one problem is required when a dimension is `needs_work`. | Validator |
| 10 | `analysis_limits` is missing from the object | The field is required. When there are no limits it must be written as `[]`. | Required field |

## Known limitations / Backlog

Limits of schema v0.1.0. None of them is hidden; each one has a place where it will be handled or a reason it is accepted.

**Not covered by the prompt or the schema**

- Whether `global` or `cannot_localize` may appear together with grid zones in the same `evidence` list is not specified. The schema accepts any mix.
- When the worst rating is `fine`, whether to list a problem is the model's judgement. The schema accepts both an empty list and 1–2 problems.

**Rules that exist only in the prompt**

These are not machine-checked. The schema accepts a violation, and only review or later evaluation will notice it.

- `comment` is 1–2 sentences.
- `strengths` is empty only when nothing real can be praised (for example when no dimension can be assessed). The schema does not check why the list is empty.
- `what_to_try` is one concrete action (at most two numbered steps).
- A rule name appears at most once in `why`, and only in parentheses.
- Advice may name a camera setting, but must not state its current value or say that it was wrong. Nothing checks this automatically; an eval check for phrases such as "your ISO is …" is planned for v0.2.
- All text is plain English addressed to the student.
- The order `intent` and `dimensions` before `priority_problems` is an instruction for generation. Pydantic does not check the order of keys in the input, so a different order is still valid.

**Accepted for v0.1.0, planned later**

- Evidence is a 3×3 zone, not a region with coordinates, and nothing verifies that the description matches the image. Grounding and verification are planned for v0.3. Adding an optional field to `Evidence` is a minor bump; removing or renaming `zone` is a major bump.
- `RunRecord` does not record token usage, cost, or the identity of the input image. Evaluation in v0.2 will show whether they are needed.
- Dimension keys (`subject_story`, `composition`, `light_exposure`, `color_tone`, `technical`) are stable identifiers. The names shown to the reader are a presentation concern and can change without changing the schema.
