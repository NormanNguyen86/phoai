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
| strengths | list | 4 | Fourth field: what the student should keep doing. It comes before the weaknesses so that the learner feels encouraged first. |
| priority_problems | list | 5 | Fifth field: the one or two most important problems to work on, written after the diagnosis so that the advice follows from it. |
| overall_summary | text | 6 | Last field: one sentence summarizing the photo and the single most important thing to work on. |

## Field reference

`RunRecord` fields are described in "Run metadata". The `Evidence` object is described in "Evidence format".

### Critique

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| intent | `Intent` object | see "Intent" | yes | The intent the model assumes for the photo, and its confidence in that assumption. |
| analysis_limits | list of text | free text, one reason per item | no | Reasons why parts of the analysis may be unreliable (for example "the image is too small to judge sharpness"). An empty list when there are none. |
| dimensions | `Dimensions` object | exactly five keys, see "Dimensions" | yes | The diagnosis of the photo on five dimensions. |
| strengths | list of `Strength` | 1–2 items | yes | What the student should keep doing. |
| priority_problems | list of `PriorityProblem` | 0–2 items, see invariants 3 and 4 | yes | The most important problems to work on. |
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

### Strength

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| dimension | literal | one of the five dimension keys | yes | The dimension this strength belongs to. |
| observation | text | free text | yes | What is visible in the photo that works well. |
| evidence | list of `Evidence` | at least 1 item | yes | Where in the photo it shows. |

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

## Invariants

Rules that involve more than one field, or that go beyond the field types. "Code" means a validator in `schema.py` rejects the output. A rejected output is treated as invalid output and goes through the retry path.

| # | Rule | Enforced by |
|---|---|---|
| 1 | The `root_dimension` of a problem is rated `needs_work`, or `fine` when no dimension is `needs_work`. | Code, and stated in the prompt |
| 2 | `related_dimensions` does not contain the `root_dimension`. | Code, and stated in the prompt |
| 3 | `priority_problems` has at most 2 items. | Code, and stated in the prompt |
| 4 | `priority_problems` is empty if and only if no dimension is rated `needs_work` or `fine`. A photo whose dimensions are all `good` or `not_assessable` therefore has an empty list. | Code, and stated in the prompt |
| 5 | `rank` values are increasing and not duplicated. | Code, and stated in the prompt |
| 6 | `strengths` has 1–2 items. | Code, and stated in the prompt |
| 7 | Every `evidence` list has at least 1 item, and every `description` is not empty. | Code |
| 8 | `Critique` rejects unknown fields, so run metadata cannot appear in the model output. | Code (`extra="forbid"`) |
| 9 | `schema_version`, `prompt_version`, `model_id` and `git_sha` are set by the pipeline, never by the model. | Code (pipeline) |

Rules that exist only in the prompt are listed in "Known limitations / Backlog".

## Evidence format

Every `evidence` field in the schema (in `strengths` and in `priority_problems`) is a **list of `Evidence` objects**. Each object points to one place in the photo.

| field | type | allowed values | required | meaning |
|---|---|---|---|---|
| zone | literal | one of the 11 values in the vocabulary below | yes | Where in the photo the observation applies. |
| description | text | non-empty | yes | A short phrase naming what is visible in that zone (e.g. "the walker in a grey jacket"). |

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
| `global` | The observation applies to the whole image (flat light, a color cast). |
| `cannot_localize` | The observation is real but the model cannot tell where it is. The model must not guess a grid zone. |

### Rules

- An `evidence` list has at least one item.
- One observation can list several zones: add one `Evidence` object per zone.
- `zone` is validated against the vocabulary above. Any other value (`upper-left`, `middle-center`, `Center`) is rejected.
- Zones refer to the image **as it was sent to the model**. The same photo rotated gives different zones. In v0.1.0 the input is a PNG already rotated upright by an offline script (see Known limitations); the pipeline does not rotate or check orientation.
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

A street photo: a person in a grey jacket walks past a grey wall, with a patch of sunlight in the upper right. This is a `Critique`, not a `RunRecord`.

```json
{
  "intent": {
    "summary": "You may have wanted to capture a pedestrian moment in a city street, with the patch of sunlight adding atmosphere.",
    "confidence": "medium"
  },
  "analysis_limits": [],
  "dimensions": {
    "subject_story": {
      "label": "needs_work",
      "comment": "The moment has potential, but the walker does not stand out, so the viewer's eye has no clear place to land first.",
      "confidence": "high"
    },
    "composition": {
      "label": "needs_work",
      "comment": "The low camera angle gives a good sense of space, but the walker sits low in the frame, far from the bright area and against a wall of the same tone.",
      "confidence": "medium"
    },
    "light_exposure": {
      "label": "fine",
      "comment": "The shaft of sunlight in the upper right is attractive and clearly directional, but it does not fall on the walker.",
      "confidence": "high"
    },
    "color_tone": {
      "label": "good",
      "comment": "The warm greys of the wall and jacket are consistent and create a calm mood, with no color cast.",
      "confidence": "medium"
    },
    "technical": {
      "label": "good",
      "comment": "The walker is sharp, and at this resolution there is no visible motion blur or significant noise.",
      "confidence": "medium"
    }
  },
  "strengths": [
    {
      "dimension": "composition",
      "observation": "The low angle makes the wall taller and the street wider, which gives the frame a strong sense of space.",
      "evidence": [
        { "zone": "global", "description": "the sense of space created by the low angle across the whole frame" }
      ]
    }
  ],
  "priority_problems": [
    {
      "rank": 1,
      "root_dimension": "composition",
      "related_dimensions": ["light_exposure", "subject_story"],
      "title": "The subject blends into the background and is separated from the light",
      "observation": "The walker, in a grey jacket, stands against an equally grey wall, low in the frame and far from the shaft of sunlight in the upper right.",
      "evidence": [
        { "zone": "bottom-center", "description": "the walker in a grey jacket" },
        { "zone": "top-right", "description": "the brightest patch of sunlight in the image" }
      ],
      "why": "The brightest area pulls the viewer's eye to the upper right, where nothing important is happening, while the walker's jacket merges with the wall and cannot hold attention.",
      "what_to_try": "Move so the patch of sunlight is behind the walker, then wait until they step into it before pressing the shutter."
    }
  ],
  "overall_summary": "A good moment and atmosphere, but the viewer is not sure where to look; next time, prioritize getting your subject into the light."
}
```

### Invalid examples

Each case below breaks one rule. The fragment shows only the part that is wrong.

| # | Fragment | Why it is invalid | Caught by |
|---|---|---|---|
| 1 | `"label": "ok"` | Not one of `good`, `fine`, `needs_work`, `not_assessable`. | Literal type |
| 2 | `"zone": "upper-left"` | Not in the zone vocabulary. | Literal type |
| 3 | `"evidence": ["bottom-center: the walker"]` | `evidence` items must be objects with `zone` and `description`, not strings. | Type check |
| 4 | `"root_dimension": "color_tone"` while `color_tone` is rated `good` | The root dimension of a problem must be rated `needs_work` (or `fine` only when no dimension is `needs_work`). | Validator |
| 5 | `"root_dimension": "composition", "related_dimensions": ["composition"]` | `related_dimensions` must never contain the root dimension. | Validator |
| 6 | `priority_problems` with 3 items | At most 2 problems. | Validator |
| 7 | No dimension is `needs_work` or `fine` (for example all five `good`) and one item in `priority_problems` | The list must be empty when no dimension is `needs_work` or `fine`, because no valid root dimension exists. | Validator |
| 8 | A top-level `"model_id": "..."` in `Critique` | Unknown field (`extra="forbid"`). Metadata belongs to `RunRecord`. | `extra="forbid"` |
| 9 | One dimension is `needs_work` and `"priority_problems": []` | At least one problem is required when a dimension is `needs_work` or `fine`. | Validator |

## Known limitations / Backlog

Limits of schema v0.1.0. None of them is hidden; each one has a place where it will be handled or a reason it is accepted.

**Not covered by the prompt or the schema**

- Whether `global` or `cannot_localize` may appear together with grid zones in the same `evidence` list is not specified. The schema accepts any mix.
- Image orientation is outside the schema and the pipeline in v0.1.0. The model input is an upright PNG made offline by `data/processed_raw/preprocess.py` (EXIF Orientation applied, metadata stripped). An image sent with an unapplied orientation would get zones on a rotated image, and nothing detects it. Auto-orienting arbitrary uploads is in the Backlog of `STATUS.md`.

**Rules that exist only in the prompt**

These are not machine-checked. The schema accepts a violation, and only review or later evaluation will notice it.

- `comment` is 1–2 sentences.
- `what_to_try` is one concrete action (at most two numbered steps).
- A rule name appears at most once in `why`, and only in parentheses.
- Advice may name a camera setting to change but must not state its current value.
- All text is plain English addressed to the student.
- The order `intent` and `dimensions` before `priority_problems` is an instruction for generation. Pydantic does not check the order of keys in the input, so a different order is still valid.

**Accepted for v0.1.0, planned later**

- Evidence is a 3×3 zone, not a region with coordinates, and nothing verifies that the description matches the image. Grounding and verification are planned for v0.3. Adding an optional field to `Evidence` is a minor bump; removing or renaming `zone` is a major bump.
- `RunRecord` does not record token usage, cost, or the identity of the input image. Evaluation in v0.2 will show whether they are needed.
- Dimension keys (`subject_story`, `composition`, `light_exposure`, `color_tone`, `technical`) are stable identifiers. The names shown to the reader are a presentation concern and can change without changing the schema.
